#!/usr/bin/env python3
"""
Official MCP Registry crawler.

The community-run canonical registry at registry.modelcontextprotocol.io.
Every server has a reverse-DNS namespace and verified ownership.
This is the highest-signal source and should be crawled first.

API: REST, no authentication required. Cursor-based pagination.
Endpoint: /v0/servers
Response format: {"servers": [{"server": {...}, "_meta": {...}}], "metadata": {"nextCursor": "...", "count": N}}
"""

from __future__ import annotations

import logging
import urllib.request
import urllib.error
import json
from typing import Iterator

from .models import CandidateServer, SourceRef

logger = logging.getLogger(__name__)

REGISTRY_BASE = "https://registry.modelcontextprotocol.io/v0"
DEFAULT_LIMIT = 100
REQUEST_TIMEOUT = 30


def crawl_servers(
    limit: int = DEFAULT_LIMIT,
    max_pages: int | None = None,
) -> Iterator[CandidateServer]:
    """
    Crawl the Official MCP Registry, yielding CandidateServer objects.
    De-duplicates by name, keeping only the latest version (isLatest=true).

    Args:
        limit: Page size (max 500).
        max_pages: Stop after this many pages. None = all pages.

    Yields:
        CandidateServer for each unique registry entry (latest version only).
    """
    page = 0
    cursor = None
    seen_names = set()

    while True:
        if max_pages is not None and page >= max_pages:
            logger.info(f"Reached max_pages={max_pages}, stopping.")
            break

        # Build URL with cursor-based pagination
        params = f"limit={limit}"
        if cursor:
            params += f"&cursor={urllib.parse.quote(cursor)}"
        url = f"{REGISTRY_BASE}/servers?{params}"
        logger.debug(f"Fetching page {page}: {url[:120]}...")

        try:
            req = urllib.request.Request(
                url,
                headers={"Accept": "application/json", "User-Agent": "al-dente-discovery/0.1"},
            )
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            logger.error(f"HTTP {e.code} from registry: {e.reason}")
            break
        except Exception as e:
            logger.error(f"Registry fetch failed: {e}")
            break

        entries = data.get("servers", [])
        if not entries:
            logger.info("No more servers from registry.")
            break

        logger.info(f"Page {page}: got {len(entries)} entries")

        for entry in entries:
            try:
                candidate = _parse_registry_entry(entry)
                if not candidate:
                    continue

                # De-duplicate by name — keep only latest version
                if candidate.name in seen_names:
                    continue
                seen_names.add(candidate.name)

                yield candidate

            except Exception as e:
                logger.warning(f"Failed to parse registry entry: {e}")
                continue

        # Cursor pagination
        cursor = data.get("metadata", {}).get("nextCursor")
        if not cursor:
            logger.info("No more pages (no cursor).")
            break

        page += 1


def _parse_registry_entry(entry: dict) -> CandidateServer | None:
    """Parse a single registry envelope into a CandidateServer."""
    # The server data is nested under "server"
    server = entry.get("server", {})
    if not server:
        return None

    name = server.get("name", "")
    if not name:
        return None

    # Meta info
    meta = entry.get("_meta", {})
    official_meta = meta.get("io.modelcontextprotocol.registry/official", {})
    is_latest = official_meta.get("isLatest", False)
    status = official_meta.get("status", "unknown")
    published_at = official_meta.get("publishedAt", "")[:10] if official_meta.get("publishedAt") else None
    updated_at = official_meta.get("updatedAt", "")[:10] if official_meta.get("updatedAt") else None

    # Only process latest versions
    if not is_latest:
        return None  # Will be skipped by de-dup logic anyway, but explicit

    # Extract remotes for transport detection
    remotes = server.get("remotes", [])
    transport = "stdio"  # Default
    for remote in remotes:
        rtype = remote.get("type", "").lower()
        if rtype in ("streamable-http", "http"):
            transport = "http"
        elif rtype == "sse":
            transport = "sse"
        elif rtype == "websocket":
            transport = "websocket"

    # Repository URL
    repo_url = None
    repo = server.get("repository", {})
    if isinstance(repo, dict):
        repo_url = repo.get("url")
    elif isinstance(repo, str):
        repo_url = repo

    # Homepage
    homepage = server.get("websiteUrl") or server.get("homepageUrl") or repo_url

    # Install command — try to construct from name
    install_cmd = None
    runtime = None
    # Many registry entries don't have packages yet; enrichment will fill this in

    return CandidateServer(
        name=name,
        display_name=server.get("title") or server.get("description", "").split(".")[0] or name.split("/")[-1],
        description=server.get("description", ""),
        github_url=repo_url,
        homepage=homepage,
        install_command=install_cmd,
        transport=transport,
        runtime=runtime,
        registry_published=True,
        registry_namespace=name,
        github_updated_at=updated_at or published_at,
        sources=[SourceRef(
            source="mcp_registry",
            source_id=name,
            source_url=f"https://registry.modelcontextprotocol.io/v0/servers/{name}",
            raw_data=entry,
        )],
    )


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(__file__).replace("/pipeline/discover/mcp_registry.py", ""))
    logging.basicConfig(level=logging.INFO)
    count = 0
    for server in crawl_servers(limit=100, max_pages=5):
        print(f"  {server.name:50s} | transport={server.transport:6s} | latest | {server.github_url or 'N/A'}")
        count += 1
    print(f"\nTotal unique servers: {count}")
