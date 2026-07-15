#!/usr/bin/env python3
"""
al-dente OKF Bundle Builder

Builds a complete OKF (Open Knowledge Format) bundle from Markdown source files
containing YAML frontmatter. Validates entities, resolves cross-references, and
outputs both JSON and JavaScript bundle files.

Usage:
    python -m pipeline.build_okf --input data/ --output docs/assets/js/
    python pipeline/build_okf.py --input data/ --output output/
    python -m pipeline.build_okf --input data --output /tmp/okf --validate-only
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Schema constants
# ---------------------------------------------------------------------------

VALID_ENTITY_TYPES: list[str] = [
    "MCP-Server",
    "Skill",
    "Category",
    "Agentic-Pattern",
    "Publisher",
]

VALID_TIERS: list[str] = ["Official", "Verified", "Community", "Experimental"]
VALID_TRANSPORTS: list[str] = ["stdio", "http", "sse", "websocket"]


class _DateTimeEncoder(json.JSONEncoder):
    """JSON encoder that handles datetime.date and datetime.datetime objects."""

    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return super().default(o)

# Required fields per entity type
REQUIRED_FIELDS: dict[str, list[str]] = {
    "MCP-Server": ["id", "name", "publisher", "transport", "capabilities", "tier"],
    "Skill": ["id", "name", "taxonomy", "level", "description"],
    "Category": ["id", "name", "description"],
    "Agentic-Pattern": ["id", "name", "description"],
    "Publisher": ["id", "name", "type_org"],
}

# Optional fields that are relation references — values should point to existing entity IDs
RELATION_FIELDS: dict[str, list[str]] = {
    "MCP-Server": ["publisher", "skills", "categories"],
    "Skill": ["categories", "patterns"],
    "Category": ["parent"],
    "Agentic-Pattern": [],
    "Publisher": [],
}

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("build_okf")


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

# Regex to extract YAML frontmatter between --- fences at the start of a file.
FRONTMATTER_RE = re.compile(
    r"^---\s*\n"          # Opening ---
    r"(.*?\n)"            # YAML content (captured)
    r"---\s*\n"           # Closing ---
    r"(.*)$",             # Remaining Markdown body (captured)
    re.DOTALL,
)


def parse_okf_file(file_path: Path) -> dict[str, Any] | None:
    """
    Parse a single OKF Markdown file.

    Extracts YAML frontmatter and Markdown body. Returns a dict with keys:
        - "file": str       — relative path of the source file
        - "frontmatter": dict — parsed YAML metadata
        - "body": str       — Markdown content after frontmatter
        - "id": str         — entity ID from frontmatter (convenience)
        - "type": str       — entity type from frontmatter (convenience)

    Args:
        file_path: Path to the .md file to parse.

    Returns:
        Parsed entity dict, or None if the file is invalid or missing frontmatter.
    """
    logger.debug("Parsing %s", file_path)

    try:
        raw = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        logger.error("Cannot read %s: %s", file_path, exc)
        return None

    match = FRONTMATTER_RE.match(raw)
    if not match:
        logger.error("No YAML frontmatter found in %s", file_path)
        return None

    yaml_raw, body_raw = match.group(1), match.group(2)

    try:
        frontmatter: dict[str, Any] = yaml.safe_load(yaml_raw) or {}
    except yaml.YAMLError as exc:
        logger.error("YAML parse error in %s: %s", file_path, exc)
        return None

    entity_id = frontmatter.get("id", "")
    entity_type = frontmatter.get("type", "")

    return {
        "file": str(file_path),
        "frontmatter": frontmatter,
        "body": body_raw.strip(),
        "id": entity_id,
        "type": entity_type,
    }


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_entity(entity: dict[str, Any], all_ids: set[str]) -> list[str]:
    """
    Validate a single parsed entity against the OKF schema.

    Checks:
        1. The ``type`` field exists and is a known entity type.
        2. All required fields for that type are present.
        3. Enumerated values (tier, transport) are valid.
        4. Relation fields reference existing entity IDs.

    Args:
        entity: Parsed entity dict from :func:`parse_okf_file`.
        all_ids: Set of all entity IDs discovered so far (for cross-ref checks).

    Returns:
        A list of human-readable error messages. An empty list means the entity
        is valid.
    """
    errors: list[str] = []
    fm = entity.get("frontmatter", {})
    entity_id = entity.get("id", "<unknown>")
    entity_type = fm.get("type", "")
    source = entity.get("file", "<unknown>")

    # 1. Validate type
    if not entity_type:
        errors.append(f"[{source}] Entity '{entity_id}': missing required field 'type'")
        return errors  # Cannot proceed without type

    if entity_type not in VALID_ENTITY_TYPES:
        errors.append(
            f"[{source}] Entity '{entity_id}': invalid type '{entity_type}'. "
            f"Must be one of: {', '.join(VALID_ENTITY_TYPES)}"
        )
        return errors  # Cannot proceed with unknown type

    # 2. Validate required fields
    required = REQUIRED_FIELDS.get(entity_type, [])
    for field in required:
        if field not in fm or fm[field] is None or fm[field] == "":
            errors.append(
                f"[{source}] Entity '{entity_id}' ({entity_type}): "
                f"missing required field '{field}'"
            )

    # 3. Validate enumerated values
    if entity_type == "MCP-Server":
        tier = fm.get("tier")
        if tier and tier not in VALID_TIERS:
            errors.append(
                f"[{source}] Entity '{entity_id}': invalid tier '{tier}'. "
                f"Must be one of: {', '.join(VALID_TIERS)}"
            )

        transport = fm.get("transport")
        if transport:
            transports = transport if isinstance(transport, list) else [transport]
            for t in transports:
                if t not in VALID_TRANSPORTS:
                    errors.append(
                        f"[{source}] Entity '{entity_id}': invalid transport '{t}'. "
                        f"Must be one of: {', '.join(VALID_TRANSPORTS)}"
                    )

    # 4. Validate relation references
    relation_fields = RELATION_FIELDS.get(entity_type, [])
    for field in relation_fields:
        value = fm.get(field)
        if value is None:
            continue  # Optional relation — skip if absent

        refs = value if isinstance(value, list) else [value]
        for ref in refs:
            if ref and ref not in all_ids:
                errors.append(
                    f"[{source}] Entity '{entity_id}' ({entity_type}): "
                    f"relation field '{field}' references unknown entity '{ref}'"
                )

    return errors


# ---------------------------------------------------------------------------
# Bundle construction
# ---------------------------------------------------------------------------


def build_bundle(
    input_dir: Path,
    validate_only: bool = False,
) -> tuple[dict[str, Any] | None, list[str]]:
    """
    Walk the input directory, parse all .md files, validate entities, and build
    the complete OKF bundle data structure.

    Args:
        input_dir: Root directory to scan for ``.md`` files.
        validate_only: If True, skip bundle assembly and only validate.

    Returns:
        A tuple of ``(bundle, errors)``. *bundle* is ``None`` if validation-only
        mode is requested or if fatal errors occur. *errors* is a list of all
        validation error messages collected across every file.
    """
    errors: list[str] = []
    parsed_entities: list[dict[str, Any]] = []

    # --- Pass 1: Parse all files and collect IDs ---
    logger.info("Scanning %s for .md files...", input_dir.resolve())
    md_files = sorted(input_dir.rglob("*.md"))
    if not md_files:
        logger.warning("No .md files found in %s", input_dir)
        return (None if validate_only else _empty_bundle()), errors

    # Skip index/navigation files that are not entities
    md_files = [f for f in md_files if f.name != "index.md"]

    logger.info("Found %d Markdown file(s)", len(md_files))

    for md_file in md_files:
        entity = parse_okf_file(md_file)
        if entity is None:
            errors.append(f"Failed to parse {md_file}")
            continue
        parsed_entities.append(entity)

    # Collect all IDs for cross-reference validation
    all_ids: set[str] = {
        e["id"] for e in parsed_entities if e.get("id")
    }

    # --- Pass 2: Validate each entity ---
    logger.info("Validating %d entity(ies)...", len(parsed_entities))
    for entity in parsed_entities:
        entity_errors = validate_entity(entity, all_ids)
        errors.extend(entity_errors)

    if errors:
        logger.warning("Validation completed with %d error(s)", len(errors))
    else:
        logger.info("Validation passed for all %d entity(ies)", len(parsed_entities))

    if validate_only:
        return None, errors

    # --- Pass 3: Build bundle ---
    bundle = _assemble_bundle(parsed_entities)
    return bundle, errors


def _assemble_bundle(entities: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Assemble the final OKF bundle structure from validated parsed entities.

    Builds entities index, type/category indexes, and a flat edges array
    for graph visualization.

    Args:
        entities: List of parsed entity dicts.

    Returns:
        The complete OKF bundle dict.
    """
    # Build the entities index
    entities_index: dict[str, dict[str, Any]] = {}
    for entity in entities:
        eid = entity.get("id")
        if not eid:
            continue
        # Merge frontmatter + body into the full entity dict
        full_entity = dict(entity["frontmatter"])
        full_entity["body"] = entity.get("body", "")
        full_entity["_source"] = entity.get("file", "")
        entities_index[eid] = full_entity

    # Build byType index
    by_type: dict[str, list[str]] = {t: [] for t in VALID_ENTITY_TYPES}
    for eid, ent in entities_index.items():
        etype = ent.get("type", "")
        if etype in by_type:
            by_type[etype].append(eid)

    # Build byCategory index (entities grouped by category)
    by_category: dict[str, list[str]] = {}
    for eid, ent in entities_index.items():
        cats = ent.get("categories", [])
        if isinstance(cats, str):
            cats = [cats]
        for cat in cats:
            if cat:
                by_category.setdefault(cat, []).append(eid)

    # Build flat edges array for graph visualization
    edges: list[dict[str, str]] = []
    _RELATION_TYPES = {
        "realizes_skills": "realizes",
        "realized_by": "realized_by",
        "commonly_composed_with": "composes_with",
        "belongs_to": "belongs_to",
        "exposes": "exposes",
        "exemplified_by": "exemplifies",
        "related_to": "related_to",
        "publishes": "publishes",
    }

    for eid, ent in entities_index.items():
        relations = ent.get("relations", {})
        if not isinstance(relations, dict):
            continue

        for rel_field, targets in relations.items():
            rel_type = _RELATION_TYPES.get(rel_field, rel_field)
            if not isinstance(targets, list):
                targets = [targets] if targets else []
            for target_id in targets:
                if target_id and target_id in entities_index:
                    edges.append({
                        "source": eid,
                        "target": target_id,
                        "type": rel_type,
                    })

        # Also extract skills_realized as edges
        skills_realized = ent.get("skills_realized", [])
        if isinstance(skills_realized, list):
            for skill_id in skills_realized:
                if skill_id and skill_id in entities_index:
                    edges.append({
                        "source": eid,
                        "target": skill_id,
                        "type": "realizes",
                    })

    # Deduplicate edges
    seen = set()
    unique_edges = []
    for edge in edges:
        key = (edge["source"], edge["target"], edge["type"])
        if key not in seen:
            seen.add(key)
            unique_edges.append(edge)

    # Sort all index lists for deterministic output
    for t in by_type:
        by_type[t].sort()
    for cat in by_category:
        by_category[cat] = sorted(set(by_category[cat]))

    # Counts by type
    counts_by_type = {t: len(ids) for t, ids in by_type.items()}

    # Metadata
    now = datetime.now(timezone.utc)
    metadata = {
        "generated": now.isoformat(),
        "version": "0.1.0",
        "entityCount": len(entities_index),
        "countsByType": counts_by_type,
        "edgeCount": len(unique_edges),
    }

    bundle: dict[str, Any] = {
        "entities": entities_index,
        "byType": by_type,
        "byCategory": by_category,
        "edges": unique_edges,
        "metadata": metadata,
    }

    return bundle


def _empty_bundle() -> dict[str, Any]:
    """Return an empty bundle structure (used when no .md files are found)."""
    now = datetime.now(timezone.utc)
    return {
        "entities": {},
        "byType": {t: [] for t in VALID_ENTITY_TYPES},
        "byCategory": {},
        "metadata": {
            "generated": now.isoformat(),
            "version": "0.1.0",
            "entityCount": 0,
            "countsByType": {t: 0 for t in VALID_ENTITY_TYPES},
        },
    }


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------


def write_outputs(bundle: dict[str, Any], output_dir: Path) -> None:
    """
    Write the OKF bundle to disk as both JSON and JavaScript files.

    Files produced:
        - ``{output_dir}/okf_bundle.json``  — Pretty-printed JSON
        - ``{output_dir}/okf_data.js``      — JavaScript: ``window.OKF_DATA = {...};``

    Args:
        bundle: The complete OKF bundle dict from :func:`build_bundle`.
        output_dir: Directory where output files will be written.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write JSON bundle
    json_path = output_dir / "okf_bundle.json"
    try:
        with json_path.open("w", encoding="utf-8") as fh:
            json.dump(bundle, fh, indent=2, ensure_ascii=False, cls=_DateTimeEncoder)
            fh.write("\n")
        logger.info("Wrote JSON bundle: %s", json_path)
    except OSError as exc:
        logger.error("Failed to write %s: %s", json_path, exc)
        raise

    # Write JavaScript bundle
    js_path = output_dir / "okf_data.js"
    try:
        js_content = "window.OKF_DATA = " + json.dumps(
            bundle, indent=2, ensure_ascii=False, cls=_DateTimeEncoder
        ) + ";\n"
        with js_path.open("w", encoding="utf-8") as fh:
            fh.write(js_content)
        logger.info("Wrote JS bundle: %s", js_path)
    except OSError as exc:
        logger.error("Failed to write %s: %s", js_path, exc)
        raise


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="build_okf",
        description="Build OKF bundles from Markdown+YAML source files.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data"),
        help="Input directory containing .md source files (default: data/)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output"),
        help="Output directory for generated bundles (default: output/)",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate data without writing output files",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose debug logging",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """
    Main entry point for the OKF bundle builder.

    Returns:
        Exit code: 0 on success, 1 on validation or I/O errors.
    """
    args = parse_args(argv)

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    input_dir: Path = args.input
    output_dir: Path = args.output

    if not input_dir.exists():
        logger.error("Input directory does not exist: %s", input_dir)
        return 1

    if not input_dir.is_dir():
        logger.error("Input path is not a directory: %s", input_dir)
        return 1

    bundle, errors = build_bundle(input_dir, validate_only=args.validate_only)

    # Report validation errors
    if errors:
        for err in errors:
            logger.error("VALIDATION: %s", err)

    if args.validate_only:
        if errors:
            logger.error("Validation failed with %d error(s)", len(errors))
            return 1
        logger.info("Validation passed — no errors found")
        return 0

    # Write outputs
    if bundle is not None:
        write_outputs(bundle, output_dir)
        logger.info(
            "Build complete: %d entities written to %s",
            bundle["metadata"]["entityCount"],
            output_dir,
        )

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
