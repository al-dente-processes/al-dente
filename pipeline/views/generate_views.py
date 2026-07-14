#!/usr/bin/env python3
"""
al-dente View Generator

Generates documentation views from a built OKF bundle. Currently a stub that
logs a placeholder message. Individual view generators will be registered in
:func:`generate_all_views` as they are implemented.

Planned views:
    - Entity index pages (by type, by category)
    - Publisher directory
    - Relationship graphs (Mermaid or Cytoscape)
    - Search index for client-side full-text search

Usage:
    python -m pipeline.views.generate_views --input data/ --output docs/
    python pipeline/views/generate_views.py --input data/ --output docs/
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("generate_views")


# ---------------------------------------------------------------------------
# View generation
# ---------------------------------------------------------------------------


def generate_all_views(input_dir: Path, output_dir: Path) -> int:
    """
    Generate all documentation views from the OKF data.

    This is the main orchestration function. It discovers all view generators,
    validates the input data, and writes view artifacts to *output_dir*.

    Args:
        input_dir: Directory containing the OKF source Markdown files.
        output_dir: Directory where generated view files will be written.

    Returns:
        Exit code: 0 on success, 1 on errors.
    """
    logger.info("Input directory : %s", input_dir.resolve())
    logger.info("Output directory: %s", output_dir.resolve())

    if not input_dir.exists():
        logger.error("Input directory does not exist: %s", input_dir)
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)

    # TODO: Implement individual view generators here.
    #   - _generate_index_pages(input_dir, output_dir)
    #   - _generate_search_index(input_dir, output_dir)
    #   - _generate_mermaid_graphs(input_dir, output_dir)
    # Each generator should be registered and called from this function.

    logger.warning("View generation not yet implemented")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="generate_views",
        description="Generate documentation views from OKF data.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data"),
        help="Input directory containing OKF source files (default: data/)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs"),
        help="Output directory for generated views (default: docs/)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose debug logging",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """
    Main entry point for the view generator.

    Returns:
        Exit code from :func:`generate_all_views`.
    """
    args = parse_args(argv)

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    return generate_all_views(args.input, args.output)


if __name__ == "__main__":
    sys.exit(main())
