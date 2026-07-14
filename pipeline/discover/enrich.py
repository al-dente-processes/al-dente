#!/usr/bin/env python3
"""
Enrichment layer — fetches detailed metadata for each candidate from GitHub API.

This is where per-entry quality happens. For each server that passes discovery:
1. Full GitHub repo details (stars, language, topics, license, updated_at)
2. README content (for description, capabilities, install instructions)
3. package.json / pyproject.toml (for tool listings and install commands)
4. File listing (to detect stdio vs SSE transport)

The goal: every OKF entry should be rich enough to be useful without manual curation.
"""

from __future__ import annotations

import logging
import os
import re
import urllib.request
import urllib.error
import json
import base64
from typing import Any

from .models import CandidateServer

logger = logging.getLogger(__name__)

GITHUB_API = "https://api.github.com"
REQUEST_TIMEOUT = 30


def enrich_server(candidate: CandidateServer, token: str | None = None) -> CandidateServer:
    """
    Enrich a CandidateServer with GitHub API data.

    Fetches repo details, README, and config files to populate:
    - github_stars, github_language, github_topics, github_license
    - description (from README if missing)
    - install_command (from package.json or README)
    - transport (from file listing or package.json)
    - capabilities (tool names from README headers)
    """
    tok = token or os.environ.get("GITHUB_TOKEN", "")
    if not tok:
        logger.debug("No GitHub token, skipping enrichment.")
        return candidate

    if not candidate.github_url:
        logger.debug(f"No GitHub URL for {candidate.name}, skipping enrichment.")
        return candidate

    # Parse owner/repo from URL
    parts = candidate.github_url.rstrip("/").split("github.com/")
    if len(parts) != 2:
        logger.debug(f"Cannot parse owner/repo from {candidate.github_url}")
        return candidate
    owner_repo = parts[1]

    # 1. Repo details
    _enrich_repo_details(candidate, owner_repo, tok)

    # 2. README content
    readme = _fetch_readme(owner_repo, tok)
    if readme:
        _enrich_from_readme(candidate, readme)

    # 3. package.json or pyproject.toml
    _enrich_from_config(candidate, owner_repo, tok)

    # 4. File listing for transport detection
    _detect_transport(candidate, owner_repo, tok)

    return candidate


def _enrich_repo_details(candidate: CandidateServer, owner_repo: str, token: str) -> None:
    """Fetch and apply GitHub repo metadata."""
    url = f"{GITHUB_API}/repos/{owner_repo}"
    data = _github_get(url, token)
    if not data:
        return

    # Only overwrite if not already set or if GitHub has better data
    candidate.github_stars = candidate.github_stars or data.get("stargazers_count")
    candidate.github_language = candidate.github_language or data.get("language")
    candidate.github_license = candidate.github_license or (
        data.get("license", {}).get("spdx_id") if data.get("license") else None
    )
    if data.get("updated_at"):
        candidate.github_updated_at = data["updated_at"][:10]
    if data.get("topics"):
        candidate.github_topics = list(set(candidate.github_topics + data["topics"]))
    if not candidate.homepage and data.get("homepage"):
        candidate.homepage = data["homepage"]

    candidate._github_api_data = data


def _fetch_readme(owner_repo: str, token: str) -> str | None:
    """Fetch raw README content."""
    url = f"{GITHUB_API}/repos/{owner_repo}/readme"
    data = _github_get(url, token)
    if not data:
        return None

    content = data.get("content", "")
    if data.get("encoding") == "base64":
        try:
            return base64.b64decode(content).decode("utf-8", errors="replace")
        except Exception:
            return None
    return content


def _enrich_from_readme(candidate: CandidateServer, readme: str) -> None:
    """Extract metadata from README content."""
    # Description: first paragraph after the heading
    if not candidate.description or len(candidate.description) < 20:
        desc = _extract_description_from_readme(readme)
        if desc:
            candidate.description = desc

    # Install command: look for npm/pip/docker/uvx install lines
    if not candidate.install_command:
        cmd = _extract_install_command(readme)
        if cmd:
            candidate.install_command = cmd
            candidate.runtime = _detect_runtime(cmd)

    # Transport: look for stdio / SSE / HTTP mentions
    if not candidate.transport or candidate.transport == "stdio":
        transport = _detect_transport_from_readme(readme)
        if transport:
            candidate.transport = transport


def _enrich_from_config(candidate: CandidateServer, owner_repo: str, token: str) -> None:
    """Try to read package.json or pyproject.toml for install/transport hints."""
    # Try package.json first
    pkg = _fetch_file(owner_repo, "package.json", token)
    if pkg:
        # Look for MCP-related scripts or config
        scripts = pkg.get("scripts", {})
        bin_entry = pkg.get("bin", {})
        # If it has a bin entry, that's likely the install command
        if bin_entry and isinstance(bin_entry, dict):
            name = list(bin_entry.keys())[0]
            if not candidate.install_command:
                candidate.install_command = f"npx -y {pkg.get('name', name)}"
                candidate.runtime = "npx"
        return

    # Try pyproject.toml
    pyproject = _fetch_file(owner_repo, "pyproject.toml", token)
    if pyproject and isinstance(pyproject, str):
        # Check for [project.scripts] or [tool.uv]
        if "[project.scripts]" in pyproject and not candidate.install_command:
            # Try to extract the script name
            match = re.search(r'\[project\.scripts\]\s*\n([^\[]+)', pyproject)
            if match:
                lines = match.group(1).strip().split("\n")
                if lines:
                    script_name = lines[0].split("=")[0].strip()
                    candidate.install_command = f"uvx {script_name}"
                    candidate.runtime = "uvx"


def _detect_transport(candidate: CandidateServer, owner_repo: str, token: str) -> None:
    """Detect transport type from file listing."""
    if candidate.transport and candidate.transport != "stdio":
        return  # Already have a non-default

    url = f"{GITHUB_API}/repos/{owner_repo}/git/trees/main?recursive=1"
    data = _github_get(url, token)
    if not data:
        # Try master
        url = f"{GITHUB_API}/repos/{owner_repo}/git/trees/master?recursive=1"
        data = _github_get(url, token)

    if not data:
        return

    tree = data.get("tree", [])
    filenames = [f["path"].lower() for f in tree]

    # SSE detection: look for EventSource, SSE, or HTTP server patterns
    for fn in filenames:
        if any(k in fn for k in ["sse", "eventsource", "stream", "server.py", "app.py", "main.py"]):
            # Check source files for SSE patterns
            pass  # Would need to read file contents — skip for now

    # Check README hints more thoroughly
    if candidate._github_api_data and "has_issues" in candidate._github_api_data:
        # Default to stdio for now, most servers are stdio
        pass


def _extract_description_from_readme(readme: str) -> str | None:
    """Extract a concise description from README first paragraph."""
    lines = readme.split("\n")
    # Skip heading
    start = 0
    for i, line in enumerate(lines):
        if line.startswith("#"):
            start = i + 1
            continue
        if line.strip() and not line.strip().startswith("!") and not line.strip().startswith("["):
            # Found first non-empty, non-badge line
            desc = line.strip()
            # Take up to 200 chars, clean markdown
            desc = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', desc)  # Remove links
            desc = re.sub(r'[*_`]', '', desc)  # Remove formatting
            if len(desc) > 20:
                return desc[:280]
            start = i + 1
            break

    # Fallback: grab first meaningful sentence
    text = " ".join(lines[start:start+5])
    text = re.sub(r'[#*`\[\]\(\)]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > 20:
        return text[:280]
    return None


def _extract_install_command(readme: str) -> str | None:
    """Look for installation instructions in README code blocks."""
    # Find code blocks with install commands
    patterns = [
        r'```(?:bash|sh|shell)?\s*\n(npx -y @[\w/-]+)[^`]*```',
        r'```(?:bash|sh|shell)?\s*\n(pip install [\w-]+)[^`]*```',
        r'```(?:bash|sh|shell)?\s*\n(uvx [\w-]+)[^`]*```',
        r'```(?:bash|sh|shell)?\s*\n(docker (?:run|pull)[^`]+)[^`]*```',
        r'```(?:bash|sh|shell)?\s*\n(npm install -g [\w@/-]+)[^`]*```',
    ]
    for pattern in patterns:
        match = re.search(pattern, readme, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    # Inline code patterns
    inline_patterns = [
        r'`(npx -y @[\w/-]+)`',
        r'`(npx [\w@/-]+)`',
        r'`(pip install [\w-]+)`',
    ]
    for pattern in inline_patterns:
        match = re.search(pattern, readme, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return None


def _detect_runtime(cmd: str) -> str:
    """Infer runtime from install command."""
    cmd_lower = cmd.lower()
    if cmd_lower.startswith("npx"):
        return "npx"
    if cmd_lower.startswith("pip"):
        return "pip"
    if cmd_lower.startswith("uvx"):
        return "uvx"
    if cmd_lower.startswith("docker"):
        return "docker"
    if cmd_lower.startswith("npm"):
        return "npm"
    return "source"


def _detect_transport_from_readme(readme: str) -> str | None:
    """Detect if server uses SSE or HTTP instead of stdio."""
    readme_lower = readme.lower()
    sse_indicators = ["sse", "server-sent events", "eventsource", "http transport", "port ", "endpoint"]
    stdio_indicators = ["stdio", "standard input", "command line", "cli tool", "npx -y"]

    sse_score = sum(1 for ind in sse_indicators if ind in readme_lower)
    stdio_score = sum(1 for ind in stdio_indicators if ind in readme_lower)

    if sse_score > stdio_score and sse_score >= 2:
        return "sse"
    if "websocket" in readme_lower:
        return "websocket"
    return None  # Keep default (stdio)


def _fetch_file(owner_repo: str, path: str, token: str) -> dict | str | None:
    """Fetch a file from a GitHub repo. Returns dict for JSON, str for raw."""
    url = f"{GITHUB_API}/repos/{owner_repo}/contents/{path}"
    data = _github_get(url, token)
    if not data:
        return None

    if isinstance(data, dict) and data.get("encoding") == "base64":
        content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
        if path.endswith(".json"):
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return content
        return content
    return data


def _github_get(url: str, token: str) -> dict | None:
    """Make authenticated GET request to GitHub API."""
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
    except urllib.error.HTTPError as e:
        if e.code == 404:
            logger.debug(f"GitHub 404: {url}")
        elif e.code == 403:
            logger.debug(f"GitHub 403 (rate limit): {url}")
        else:
            logger.debug(f"GitHub HTTP {e.code}: {url}")
        return None
    except Exception as e:
        logger.debug(f"GitHub request failed: {url} — {e}")
        return None


def batch_enrich(
    candidates: list[CandidateServer],
    token: str | None = None,
) -> list[CandidateServer]:
    """Enrich a batch of candidates, with rate-limit awareness."""
    tok = token or os.environ.get("GITHUB_TOKEN", "")
    if not tok:
        logger.warning("No GitHub token for enrichment. Skipping.")
        return candidates

    enriched = []
    for i, candidate in enumerate(candidates):
        try:
            enriched.append(enrich_server(candidate, tok))
            if (i + 1) % 10 == 0:
                logger.info(f"Enriched {i + 1}/{len(candidates)} candidates...")
        except Exception as e:
            logger.warning(f"Enrichment failed for {candidate.name}: {e}")
            enriched.append(candidate)  # Keep unenriched

    return enriched
