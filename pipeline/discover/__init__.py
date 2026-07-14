#!/usr/bin/env python3
"""
al-dente Discovery Pipeline — Automated MCP server discovery with quality gating.

Crawls canonical sources (Official MCP Registry, PulseMCP, GitHub Topics),
enriches candidates via GitHub API, applies quality gates, and generates
rich OKF entries for servers that pass.

Designed for weekly automated execution via GitHub Actions.
"""

__version__ = "0.1.0"
