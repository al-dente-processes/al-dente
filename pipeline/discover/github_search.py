#!/usr/bin/env python3
"""
GitHub topic search for MCP servers.

Finds community MCP servers that exist on GitHub but haven't been
published to the official registry yet. Uses the GitHub Search API.

API: REST, requires GITHUB_TOKEN for authenticated requests (higher rate limits).
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

GITHUB_API = "https://api.github.com"
REQUEST_TIMEOUT = 30

# Search queries to find MCP servers
SEARCH_QUERIES = [
    "topic:mcp-server",                          # Tagged with mcp-server
    "topic:model-context-protocol",               # Tagged with model-context-protocol
    "mcp-server in:name,description",            # Named or described as mcp-server
    "model-context-protocol-server in:name",      # Named as model-context-protocol-server
]


def crawl_servers(
    token: str | None = None,
    per_page: int = 100,
    max_pages_per_query: int = 5,
    min_stars: int = 50,
) -> Iterator[CandidateServer]:
    """
    Search GitHub for MCP server repositories.

    Args:
        token: GitHub personal access token. Falls back to GITHUB_TOKEN env var.
        per_page: Results per page (max 100).
        max_pages_per_query: Pages to fetch per search query.
        min_stars: Minimum star count to include (quality pre-filter).

    Yields:
        CandidateServer for each matching repo.
    """
    tok = token or os.environ.get("GITHUB_TOKEN")
    if not tok:
        logger.warning("No GitHub token provided. Set GITHUB_TOKEN env var. "
                       "Unauthenticated requests have low rate limits (10/min). "
                       "Skipping GitHub search.")
        return

    seen_repos = set()  # Deduplicate across queries

    for query in SEARCH_QUERIES:
        logger.info(f"GitHub search: '{query}'")
        page = 1

        while page <= max_pages_per_query:
            url = f"{GITHUB_API}/search/repositories"
            params = f"q={urllib.parse.quote(query)}&sort=stars&order=desc&per_page={per_page}&page={page}"
            full_url = f"{url}?{params}"

            try:
                req = urllib.request.Request(
                    full_url,
                    headers={
                        "Accept": "application/vnd.github.v3+json",
                        "Authorization": f"token {tok}",
                        "User-Agent": "al-dente-discovery/0.1",
                    },
                )
                with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                if e.code == 403:
                    remaining = e.headers.get("X-RateLimit-Remaining", "0")
                    reset_at = e.headers.get("X-RateLimit-Reset", "?")
                    logger.error(f"GitHub rate limit exceeded. Remaining={remaining}, resets at {reset_at}")
                elif e.code == 422:
                    logger.error(f"GitHub search validation error for query '{query}': {e.reason}")
                else:
                    logger.error(f"GitHub HTTP {e.code}: {e.reason}")
                break
            except Exception as e:
                logger.error(f"GitHub search failed: {e}")
                break

            items = data.get("items", [])
            if not items:
                logger.debug(f"No more results for '{query}' at page {page}")
                break

            total_count = data.get("total_count", 0)
            logger.info(f"  Query '{query}' page {page}: {len(items)} repos (total_estimated={total_count})")

            for repo in items:
                repo_id = repo.get("full_name", "")
                if repo_id in seen_repos:
                    continue
                seen_repos.add(repo_id)

                stars = repo.get("stargazers_count", 0) or 0
                if stars < min_stars:
                    continue  # Pre-filter: skip low-star repos

                try:
                    candidate = _parse_github_repo(repo)
                    if candidate:
                        yield candidate
                except Exception as e:
                    logger.warning(f"Failed to parse GitHub repo {repo_id}: {e}")
                    continue

            page += 1


def _parse_github_repo(repo: dict) -> CandidateServer | None:
    """Parse a GitHub repository search result into a CandidateServer."""
    full_name = repo.get("full_name", "")
    if not full_name:
        return None

    # Try to extract install command from topics or description
    install_cmd = None
    runtime = None
    topics = repo.get("topics", [])
    description = repo.get("description", "") or ""

    # Heuristic: look for package name in description or topics
    # e.g. "npx @modelcontextprotocol/server-filesystem"
    name = full_name.split("/")[-1]

    return CandidateServer(
        name=name,
        display_name=name.replace("mcp-server-", "").replace("server-", "").replace("-", " ").title(),
        description=description,
        github_url=repo.get("html_url"),
        homepage=repo.get("homepage") or None,
        install_command=install_cmd,
        transport="stdio",  # Default; may be overridden by enrichment
        runtime=runtime,
        github_stars=repo.get("stargazers_count"),
        github_topics=topics,
        github_language=repo.get("language"),
        github_updated_at=repo.get("updated_at", "")[:10] if repo.get("updated_at") else None,
        github_license=repo.get("license", {}).get("spdx_id") if repo.get("license") else None,
        sources=[SourceRef(
            source="github_topics",
            source_id=str(repo.get("id", "")),
            source_url=repo.get("html_url"),
            raw_data={"full_name": full_name, "topics": topics},
        )],
    )


def enrich_with_readme(owner: str, repo: str, token: str) -> str | None:
    """Fetch the README content of a GitHub repository."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/readme"
    try:
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github.v3.raw",
                "Authorization": f"token {token}",
                "User-Agent": "al-dente-discovery/0.1",
            },
        )
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        logger.debug(f"Failed to fetch README for {owner}/{repo}: {e}")
        return None


def fetch_repo_details(full_name: str, token: str) -> dict:
    """Fetch full repository details from GitHub API."""
    url = f"{GITHUB_API}/repos/{full_name}"
    try:
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"token {token}",
                "User-Agent": "al-dente-discovery/0.1",
            },
        )
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        logger.debug(f"Failed to fetch repo details for {full_name}: {e}")
        return {}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    count = 0
    for server in crawl_github(max_pages_per_query=1, min_stars=100):
        print(f"  {server.name:30s} | {server.github_stars or 0:5d} stars | lang={server.github_language or 'N/A'}")
        count += 1
    print(f"\nTotal: {count} repos")
