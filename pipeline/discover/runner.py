#!/usr/bin/env python3
"""
al-dente Discovery Pipeline Runner.

Orchestrates the full discovery → enrichment → gating → OKF generation flow:

1. DISCOVER: Crawl Official MCP Registry, PulseMCP, GitHub Topics
2. MERGE: Deduplicate candidates by GitHub URL, merge signals
3. ENRICH: Fetch GitHub metadata, README, config files
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

logger = logging.getLogger("al-dente.discovery")

# Paths
REPO_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = REPO_ROOT / "data" / "mcp-servers"
CACHE_DIR = REPO_ROOT / "pipeline" / ".cache"


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

    # 2. ENRICH
    logger.info("\n" + "=" * 60)
    logger.info("STEP 2: ENRICH — Fetching GitHub metadata")
    logger.info("=" * 60)
    candidates = batch_enrich(candidates)

    # 3. GATE
    logger.info("\n" + "=" * 60)
    logger.info(f"STEP 3: GATE — Applying '{gate_preset}' quality thresholds")
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
    logger.info("STEP 4: GENERATE — Writing OKF files")
    logger.info("=" * 60)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    stats = {"added": 0, "updated": 0, "unchanged": 0, "errors": 0}
    existing_ids = set()

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
                    existing_ids.add(server.id)
                    continue
                else:
                    action = "updated"
                    stats["updated"] += 1
            else:
                action = "added"
                stats["added"] += 1

            existing_ids.add(server.id)

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


def run(
    gate_preset: str = "balanced",
    dry_run: bool = False,
) -> dict:
    """
    Run the full discovery pipeline.

    Returns dict with pipeline statistics.
    """
    logger.info("\n" + "=" * 70)
    logger.info(f"al-dente Discovery Pipeline — {datetime.utcnow().isoformat()}Z")
    logger.info(f"Gate preset: {gate_preset} | Dry run: {dry_run}")
    logger.info("=" * 70)

    # Discover + gate
    passed_servers = discover(gate_preset=gate_preset)

    # Generate OKF
    stats = generate_okf(passed_servers, dry_run=dry_run)

    # Final report — machine-readable lines for GitHub Actions parsing
    logger.info("\n" + "=" * 70)
    logger.info("PIPELINE COMPLETE")
    logger.info("=" * 70)
    logger.info(f"DISCOVERY_STATS: passed={len(passed_servers)}, added={stats['added']}, updated={stats['updated']}, unchanged={stats['unchanged']}, errors={stats['errors']}, preset={gate_preset}")

    return {
        "passed": len(passed_servers),
        **stats,
        "preset": gate_preset,
        "dry_run": dry_run,
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

    result = run(gate_preset=args.preset, dry_run=args.dry_run)

    # Exit with error if nothing passed (pipeline misconfiguration?)
    if result["passed"] == 0:
        logger.error("No servers passed quality gate. Check API keys and thresholds.")
        sys.exit(1)

    return 0


if __name__ == "__main__":
    sys.exit(main())
