#!/usr/bin/env python3
"""
al-dente Discovery Pipeline Runner.

Orchestrates the full discovery → enrichment → gating → OKF generation flow:

1. DISCOVER: Crawl Official MCP Registry, PulseMCP, GitHub Topics
2. PRE-GATE: Fast heuristic filter (no API calls) — drops low-signal candidates
3. ENRICH: Fetch GitHub metadata, README, config files (only pre-passed)
4. GATE: Apply quality thresholds, only high-signal servers pass
5. GENERATE: Create/update OKF .md files in data/mcp-servers/
6. REPORT: Log what was added, updated, skipped

Designed for weekly execution via GitHub Actions.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import yaml
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from discover.models import CandidateServer
from discover.mcp_registry import crawl_servers as crawl_registry
from discover.pulsemcp import crawl_servers as crawl_pulsemcp
from discover.github_search import crawl_servers as crawl_github
from discover.enrich import batch_enrich
from discover.gate import gate_batch, report_gate_results
from discover.skills import (
    infer_skills,
    generate_skill_taxonomy,
    update_server_relations,
)

logger = logging.getLogger("al-dente.discovery")

# Paths
REPO_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = REPO_ROOT / "data" / "mcp-servers"
CACHE_DIR = REPO_ROOT / "pipeline" / ".cache"

# Default cap: max new servers per run (gradual population)
DEFAULT_MAX_SERVERS = 200


def _pre_gate(candidates: list[CandidateServer]) -> tuple[list[CandidateServer], list[CandidateServer]]:
    """
    Fast heuristic filter — no API calls.
    
    Keeps candidates that have ANY of:
    - Registry published (strong signal)
    - PulseMCP official/verified classification
    - GitHub stars >= 50
    - GitHub stars unknown (might be good, let gate decide)
    
    Drops candidates that have ALL of:
    - No registry presence
    - No PulseMCP signal
    - Known low stars (< 20)
    - No GitHub URL at all
    """
    passed = []
    dropped = []
    
    for c in candidates:
        # Strong signals — always keep
        if c.registry_published:
            passed.append(c)
            continue
        if c.pulsemcp_official or c.pulsemcp_classification in ("official", "reference", "verified"):
            passed.append(c)
            continue
        
        # Moderate signals — keep for enrichment
        if c.github_stars is not None and c.github_stars >= 50:
            passed.append(c)
            continue
        
        # Unknown stars — keep (might be good, gate will decide)
        if c.github_stars is None and c.github_url:
            passed.append(c)
            continue
            
        # Weak signals — drop without API calls
        if c.github_stars is not None and c.github_stars < 20:
            dropped.append(c)
            continue
        if not c.github_url and not c.registry_published:
            dropped.append(c)
            continue
            
        # Everything else — keep (borderline)
        passed.append(c)
    
    return passed, dropped


def discover(gate_preset: str = "balanced") -> list[CandidateServer]:
    """
    Run full discovery pipeline. Returns list of gated, enriched candidates.
    """
    logger.info("=" * 60)
    logger.info("STEP 1: DISCOVER — Crawling sources")
    logger.info("=" * 60)

    all_candidates: dict[str, CandidateServer] = {}  # github_url → candidate

    # 1a. Official MCP Registry (highest signal, no auth)
    logger.info("\n--- Source: Official MCP Registry ---")
    try:
        count = 0
        for candidate in crawl_registry(limit=100, max_pages=None):
            key = candidate.github_url or candidate.registry_namespace or candidate.name
            if key in all_candidates:
                all_candidates[key].merge(candidate)
            else:
                all_candidates[key] = candidate
            count += 1
        logger.info(f"Registry: {count} candidates")
    except Exception as e:
        logger.error(f"Registry crawl failed: {e}")

    # 1b. PulseMCP (enrichment + classification, needs API key)
    logger.info("\n--- Source: PulseMCP ---")
    if os.environ.get("PULSE_MCP_API_KEY"):
        try:
            count = 0
            for candidate in crawl_pulsemcp(max_pages=None):
                key = candidate.github_url or candidate.registry_namespace or candidate.name
                if key in all_candidates:
                    all_candidates[key].merge(candidate)
                else:
                    all_candidates[key] = candidate
                count += 1
            logger.info(f"PulseMCP: {count} candidates")
        except Exception as e:
            logger.error(f"PulseMCP crawl failed: {e}")
    else:
        logger.info("PulseMCP: skipped (no PULSE_MCP_API_KEY)")

    # 1c. GitHub Topic Search (discovery of community servers)
    logger.info("\n--- Source: GitHub Topics ---")
    if os.environ.get("GITHUB_TOKEN"):
        try:
            count = 0
            for candidate in crawl_github(max_pages_per_query=3, min_stars=50):
                key = candidate.github_url or candidate.name
                if key in all_candidates:
                    all_candidates[key].merge(candidate)
                else:
                    all_candidates[key] = candidate
                count += 1
            logger.info(f"GitHub Topics: {count} candidates")
        except Exception as e:
            logger.error(f"GitHub crawl failed: {e}")
    else:
        logger.info("GitHub Topics: skipped (no GITHUB_TOKEN)")

    candidates = list(all_candidates.values())
    logger.info(f"\nTotal unique candidates after merge: {len(candidates)}")

    # 2. PRE-GATE: Fast heuristic filter before expensive GitHub API calls
    logger.info("\n" + "=" * 60)
    logger.info("STEP 2: PRE-GATE — Fast heuristic filter")
    logger.info("=" * 60)
    pre_passed, pre_dropped = _pre_gate(candidates)
    logger.info(f"Pre-gate: {len(pre_passed)}/{len(candidates)} candidates kept "
                f"({len(pre_dropped)} dropped without API calls)")

    # 3. ENRICH (only pre-passed candidates — saves hours of API calls)
    logger.info("\n" + "=" * 60)
    logger.info("STEP 3: ENRICH — Fetching GitHub metadata")
    logger.info("=" * 60)
    enriched = batch_enrich(pre_passed)
    candidates = enriched + pre_dropped

    # 4. GATE (full quality gate on all candidates)
    logger.info("\n" + "=" * 60)
    logger.info(f"STEP 4: GATE — Applying '{gate_preset}' quality thresholds")
    logger.info("=" * 60)
    passed, failed = gate_batch(candidates, preset=gate_preset)

    report = report_gate_results(passed, failed)
    logger.info("\n" + report)

    return [r.candidate for r in passed]


def generate_okf(servers: list[CandidateServer], dry_run: bool = False) -> dict:
    """
    Generate OKF .md files for passed servers.

    Returns stats dict with counts of added/updated/unchanged.
    """
    logger.info("\n" + "=" * 60)
    logger.info("STEP 5: GENERATE — Writing OKF files")
    logger.info("=" * 60)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    stats = {"added": 0, "updated": 0, "unchanged": 0, "errors": 0}

    for server in servers:
        try:
            okf_data = server.to_okf_dict()
            file_path = DATA_DIR / f"{server.id}.md"

            # Build YAML frontmatter
            yaml_content = yaml.dump(
                okf_data,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
                width=120,
            )

            # Build Markdown body
            body_parts = []
            if server.description:
                body_parts.append(server.description)
                body_parts.append("")

            # Add source attribution
            source_names = [s.source for s in server.sources]
            body_parts.append(f"*Discovered via: {', '.join(set(source_names))}*")
            body_parts.append("")

            # Add GitHub stats if available
            if server.github_stars:
                body_parts.append(f"**GitHub Stars:** {server.github_stars:,}")
            if server.github_language:
                body_parts.append(f"**Language:** {server.github_language}")
            if server.pulsemcp_visitors_weekly:
                body_parts.append(f"**PulseMCP Weekly Visitors:** {server.pulsemcp_visitors_weekly:,}")
            body_parts.append("")

            body = "\n".join(body_parts)

            # Full file content
            content = f"---\n{yaml_content}---\n\n{body}\n"

            if file_path.exists():
                existing = file_path.read_text()
                if existing == content:
                    stats["unchanged"] += 1
                    continue
                else:
                    action = "updated"
                    stats["updated"] += 1
            else:
                action = "added"
                stats["added"] += 1

            if not dry_run:
                file_path.write_text(content)
                logger.info(f"  {action.upper():8s} {server.id:40s} — {server.display_name or server.name}")
            else:
                logger.info(f"  {action.upper():8s} {server.id:40s} — {server.display_name or server.name} (DRY RUN)")

        except Exception as e:
            logger.error(f"  ERROR    {server.id:40s} — {e}")
            stats["errors"] += 1

    # Log summary
    logger.info(f"\nOKF Generation: {stats['added']} added, {stats['updated']} updated, "
                f"{stats['unchanged']} unchanged, {stats['errors']} errors")

    return stats


def _write_skills(skills: dict[str, dict], dry_run: bool = False) -> int:
    """Write skill taxonomy entries as OKF .md files."""
    skills_dir = REPO_ROOT / "data" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    for skill_id, skill_data in skills.items():
        file_path = skills_dir / f"{skill_id}.md"

        frontmatter = {
            "type": "Skill",
            "id": skill_id,
            "name": skill_data["name"],
            "taxonomy": skill_data["taxonomy"],
            "level": skill_data["level"],
            "categories": [],
            "relations": {
                "realized_by": skill_data["realized_by"],
                "belongs_to": [],
                "related_to": [],
            },
            "description": skill_data["description"],
        }

        yaml_content = yaml.dump(
            frontmatter,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=120,
        )

        content = f"---\n{yaml_content}---\n\n{skill_data['description']}\n\n"
        content += f"*Realized by {skill_data['realized_by_count']} MCP server(s).*\n"

        if not dry_run:
            file_path.write_text(content)
            written += 1

    return written


def run(
    gate_preset: str = "balanced",
    dry_run: bool = False,
    max_servers: int = DEFAULT_MAX_SERVERS,
    bootstrap: bool = False,
) -> dict:
    """
    Run the full discovery pipeline.

    Args:
        gate_preset: Quality gate preset (strict/balanced/lenient)
        dry_run: Don't write files, just report
        max_servers: Max servers to write per run (gradual population, 0=unlimited)
        bootstrap: If True, no server cap + generates full skill taxonomy

    Returns dict with pipeline statistics.
    """
    if bootstrap:
        max_servers = 0  # Unlimited
        logger.info("BOOTSTRAP MODE: Unlimited servers, full skill generation")

    effective_max = "unlimited" if max_servers == 0 else max_servers

    logger.info("\n" + "=" * 70)
    logger.info(f"al-dente Discovery Pipeline — {datetime.utcnow().isoformat()}Z")
    logger.info(f"Preset: {gate_preset} | Dry run: {dry_run} | Max servers: {effective_max} | Bootstrap: {bootstrap}")
    logger.info("=" * 70)

    # 1-4. Discover + pre-gate + enrich + gate
    passed_servers = discover(gate_preset=gate_preset)

    # 5. Infer skills and cross-link relations
    logger.info("\n" + "=" * 60)
    logger.info("STEP 5: INFER SKILLS — Mapping capabilities to skills")
    logger.info("=" * 60)
    update_server_relations(passed_servers)
    total_skills = sum(len(s.skills_realized) for s in passed_servers)
    unique_skills = len(set(skill for s in passed_servers for skill in s.skills_realized))
    logger.info(f"Inferred {total_skills} skill mappings across {unique_skills} unique skills")

    # 6. Cap servers (unless bootstrapping)
    total_passed = len(passed_servers)
    if not bootstrap and max_servers > 0 and total_passed > max_servers:
        logger.info(f"\nCapping from {total_passed} to {max_servers} servers for gradual population")
        passed_servers = passed_servers[:max_servers]

    # 7. Generate server OKF files
    logger.info("\n" + "=" * 60)
    logger.info("STEP 6: GENERATE SERVER OKF FILES")
    logger.info("=" * 60)
    stats = generate_okf(passed_servers, dry_run=dry_run)

    # 8. Generate skill taxonomy
    logger.info("\n" + "=" * 60)
    logger.info("STEP 7: GENERATE SKILL TAXONOMY")
    logger.info("=" * 60)
    skill_taxonomy = generate_skill_taxonomy(passed_servers)
    skills_written = _write_skills(skill_taxonomy, dry_run=dry_run)
    logger.info(f"Generated {skills_written} skill entries")

    # Final report
    logger.info("\n" + "=" * 70)
    logger.info("PIPELINE COMPLETE")
    logger.info("=" * 70)
    capped = (not bootstrap) and (max_servers > 0) and (total_passed > max_servers)
    logger.info(
        f"DISCOVERY_STATS: "
        f"passed={total_passed}, "
        f"added={stats['added']}, "
        f"updated={stats['updated']}, "
        f"unchanged={stats['unchanged']}, "
        f"errors={stats['errors']}, "
        f"skills={skills_written}, "
        f"preset={gate_preset}, "
        f"capped={capped}"
    )

    return {
        "passed": total_passed,
        **stats,
        "skills": skills_written,
        "preset": gate_preset,
        "dry_run": dry_run,
        "bootstrap": bootstrap,
        "max_servers": max_servers if not bootstrap else 0,
        "timestamp": datetime.utcnow().isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(
        description="al-dente Discovery Pipeline — Automated MCP server discovery with quality gating",
    )
    parser.add_argument(
        "--preset",
        choices=["strict", "balanced", "lenient"],
        default="balanced",
        help="Quality gate preset (default: balanced)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't write files, just report what would be done",
    )
    parser.add_argument(
        "--max-servers",
        type=int,
        default=DEFAULT_MAX_SERVERS,
        help=f"Max servers per run, 0=unlimited (default: {DEFAULT_MAX_SERVERS})",
    )
    parser.add_argument(
        "--bootstrap",
        action="store_true",
        help="Bootstrap mode: unlimited servers + full skill taxonomy generation",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    result = run(
        gate_preset=args.preset,
        dry_run=args.dry_run,
        max_servers=args.max_servers,
        bootstrap=args.bootstrap,
    )

    # Exit with error if nothing passed (pipeline misconfiguration?)
    if result["passed"] == 0:
        logger.error("No servers passed quality gate. Check API keys and thresholds.")
        sys.exit(1)

    return 0


if __name__ == "__main__":
    sys.exit(main())
