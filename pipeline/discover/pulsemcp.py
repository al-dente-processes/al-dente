#!/usr/bin/env python3
"""
PulseMCP Sub-Registry API client.

PulseMCP aggregates the official registry + community submissions.
Their API returns official server.json PLUS PulseMCP enrichment:
- visitor estimates (weekly + total)
- official/reference/community classification
- popularity rankings

API: REST, requires X-API-Key header.
Free tier available at pulsemcp.com.
"""

from __future__ import annotations

import logging
import os
import urllib.request
import urllib.error
import json
from typing import Iterator

from .models import CandidateServer, SourceRef

logger = logging.getLogger(__name__)

PULSE_API_BASE = "https://api.pulsemcp.com/v0.1"
DEFAULT_LIMIT = 100
REQUEST_TIMEOUT = 30


def crawl_servers(
    api_key: str | None = None,
    limit: int = DEFAULT_LIMIT,
    max_pages: int | None = None,
) -> Iterator[CandidateServer]:
    """
    Crawl PulseMCP API, yielding CandidateServer objects.

    Args:
        api_key: PulseMCP API key. Falls back to PULSE_MCP_API_KEY env var.
        limit: Page size.
        max_pages: Stop after this many pages. None = all pages.

    Yields:
        CandidateServer for each entry.
    """
    key = api_key or os.environ.get("PULSE_MCP_API_KEY")
    if not key:
        logger.warning("No PulseMCP API key provided. Set PULSE_MCP_API_KEY env var. "
                       "Skipping PulseMCP crawl.")
        return

    page = 0
    offset = 0

    while True:
        if max_pages is not None and page >= max_pages:
            logger.info(f"Reached max_pages={max_pages}, stopping.")
            break

        url = f"{PULSE_API_BASE}/servers?limit={limit}&offset={offset}"

        try:
            req = urllib.request.Request(
                url,
                headers={
                    "Accept": "application/json",
                    "X-API-Key": key,
                    "User-Agent": "al-dente-discovery/0.1",
                },
            )
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 401:
                logger.error("PulseMCP API key invalid or expired.")
            elif e.code == 429:
                logger.error("PulseMCP rate limit hit.")
            else:
                logger.error(f"PulseMCP HTTP {e.code}: {e.reason}")
            break
        except Exception as e:
            logger.error(f"PulseMCP fetch failed: {e}")
            break

        servers = data.get("servers", [])
        if not servers:
            logger.info("No more servers from PulseMCP.")
            break

        logger.info(f"PulseMCP page {page}: got {len(servers)} servers")

        for raw in servers:
            try:
                candidate = _parse_pulsemcp_entry(raw)
                if candidate:
                    yield candidate
            except Exception as e:
                logger.warning(f"Failed to parse PulseMCP entry: {e}")
                continue

        offset += len(servers)
        page += 1


def _parse_pulsemcp_entry(raw: dict) -> CandidateServer | None:
    """Parse a PulseMCP API entry into a CandidateServer."""
    # PulseMCP wraps the official server.json in their own envelope
    server = raw.get("server", raw)  # Try both formats
    name = server.get("name", "")
    if not name:
        return None

    # Extract PulseMCP-specific meta
    meta = raw.get("_meta", {})
    pulsemcp_meta = meta.get("com.pulsemcp/server", {})

    is_official = pulsemcp_meta.get("isOfficial", False)
    classification = pulsemcp_meta.get("classification", "community")
    visitors_weekly = pulsemcp_meta.get("visitorsEstimateMostRecentWeek")
    visitors_total = pulsemcp_meta.get("visitorsEstimateTotal")

    # Repository
    repo_url = None
    repo = server.get("repository", {})
    if isinstance(repo, dict):
        repo_url = repo.get("url")
    elif isinstance(repo, str):
        repo_url = repo

    # Install
    packages = server.get("packages", [])
    install_cmd = None
    runtime = None
    transport = None

    for pkg in packages:
        cmd = pkg.get("command")
        if cmd:
            install_cmd = cmd
            if cmd.startswith("npx"):
                runtime = "npx"
            elif cmd.startswith("pip") or cmd.startswith("uvx"):
                runtime = "pip"
            elif cmd.startswith("docker"):
                runtime = "docker"
            else:
                runtime = "source"
        t = pkg.get("type", "").lower()
        if t in ("stdio", "sse", "http", "websocket"):
            transport = t

    return CandidateServer(
        name=name,
        display_name=server.get("description", "").split(".")[0] if server.get("description") else name.split("/")[-1],
        description=server.get("description", ""),
        github_url=repo_url,
        homepage=server.get("homepage") or repo_url,
        install_command=install_cmd,
        transport=transport or "stdio",
        runtime=runtime or "npx",
        pulsemcp_official=is_official,
        pulsemcp_classification=classification,
        pulsemcp_visitors_weekly=visitors_weekly,
        registry_published=True,  # PulseMCP only indexes published servers
        registry_namespace=name,
        sources=[SourceRef(
            source="pulsemcp",
            source_id=name,
            source_url=f"https://www.pulsemcp.com/servers/{name.replace('/', '-').replace('.', '-').lower()}",
            raw_data=raw,
        )],
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    count = 0
    for server in crawl_servers(max_pages=1):
        print(f"  {server.name:50s} | official={server.pulsemcp_official!s:5s} | "
              f"class={server.pulsemcp_classification or 'N/A':10s} | "
              f"visitors={server.pulsemcp_visitors_weekly or 'N/A'}")
        count += 1
    print(f"\nTotal: {count} servers")
