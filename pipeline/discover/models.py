#!/usr/bin/env python3
"""
Shared data models for the discovery pipeline.

A CandidateServer represents a discovered MCP server before quality gating.
An EnrichedServer adds GitHub API metadata and README-derived capabilities.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class SourceRef:
    """Where a server was discovered."""
    source: str  # 'mcp_registry', 'pulsemcp', 'github_topics', etc.
    source_id: str | None = None  # ID in the source system
    source_url: str | None = None
    discovered_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    raw_data: dict = field(default_factory=dict, repr=False)


@dataclass
class CandidateServer:
    """A server discovered from a source, before enrichment or gating."""

    # Identification
    name: str  # Reverse-DNS or repo name (e.g. 'github', 'modelcontextprotocol/filesystem')
    display_name: str | None = None
    description: str | None = None
    github_url: str | None = None  # Primary source of truth
    homepage: str | None = None

    # Install / Transport
    install_command: str | None = None  # e.g. 'npx -y @modelcontextprotocol/server-filesystem'
    transport: str | None = None  # stdio | sse | http
    runtime: str | None = None  # npx | pip | docker | uvx

    # Signals
    github_stars: int | None = None
    github_topics: list[str] = field(default_factory=list)
    github_language: str | None = None
    github_updated_at: str | None = None
    github_license: str | None = None

    # Source-specific signals
    pulsemcp_official: bool = False
    pulsemcp_classification: str | None = None  # official / reference / community
    pulsemcp_visitors_weekly: int | None = None
    registry_published: bool = False  # In official MCP registry
    registry_namespace: str | None = None

    # Provenance
    sources: list[SourceRef] = field(default_factory=list)

    # Internal
    _github_api_data: dict = field(default_factory=dict, repr=False)

    @property
    def id(self) -> str:
        """Stable kebab-case ID for OKF.
        
        Uses full registry namespace (converted) for namespaced servers,
        or GitHub repo name for GitHub-derived entries.
        Ensures uniqueness — no two servers share an ID.
        """
        if self.registry_namespace:
            # ac.inference.sh/mcp → ac-inference-sh-mcp
            # io.github.modelcontextprotocol/filesystem → io-github-modelcontextprotocol-filesystem
            full = self.registry_namespace.replace(".", "-").replace("/", "-")
            slug = self._slugify(full)
            return slug if slug else self._slugify(self.name)
        if self.github_url:
            # github.com/owner/repo-name → repo-name
            parts = self.github_url.rstrip("/").split("/")
            return self._slugify(parts[-1])
        return self._slugify(self.name)

    @property
    def publisher_id(self) -> str | None:
        """Derive publisher ID from registry namespace or GitHub owner."""
        if self.registry_namespace:
            parts = self.registry_namespace.replace("io.github.", "").split("/")
            return self._slugify(parts[0]) if parts else None
        if self.github_url:
            parts = self.github_url.rstrip("/").split("/")
            return self._slugify(parts[-2]) if len(parts) >= 2 else None
        return None

    @staticmethod
    def _slugify(name: str) -> str:
        """Convert to kebab-case slug."""
        return name.lower().replace("_", "-").replace(" ", "-").replace(".", "-")

    def merge(self, other: CandidateServer) -> CandidateServer:
        """Merge another candidate for the same server, taking best data from each."""
        if self.github_url and other.github_url and self.github_url != other.github_url:
            raise ValueError(f"Cannot merge: different GitHub URLs {self.github_url} vs {other.github_url}")

        # Take non-null values from either
        for attr in ["display_name", "description", "github_url", "homepage",
                     "install_command", "transport", "runtime",
                     "github_stars", "github_language", "github_updated_at", "github_license",
                     "pulsemcp_official", "pulsemcp_classification", "pulsemcp_visitors_weekly",
                     "registry_published", "registry_namespace"]:
            self_val = getattr(self, attr)
            other_val = getattr(other, attr)
            if self_val is None and other_val is not None:
                setattr(self, attr, other_val)
            # Take max for numeric signals
            if attr in ("github_stars", "pulsemcp_visitors_weekly") and self_val and other_val:
                setattr(self, attr, max(self_val, other_val))

        # Merge lists
        self.github_topics = list(set(self.github_topics + other.github_topics))
        self.sources = self.sources + other.sources

        return self

    def to_okf_dict(self) -> dict[str, Any]:
        """Convert to OKF frontmatter dict for .md generation."""
        return {
            "type": "MCP-Server",
            "id": self.id,
            "name": self.display_name or self.name,
            "publisher": self.publisher_id,
            "transport": self.transport or "stdio",
            "install": {
                "type": self.runtime or "npx",
                "command": self.install_command or f"npx -y @modelcontextprotocol/server-{self.id}",
            },
            "capabilities": {
                "tools": [],
                "resources": [],
                "prompts": [],
            },
            "stars": self.github_stars or 0,
            "last_updated": self.github_updated_at or datetime.utcnow().strftime("%Y-%m-%d"),
            "verified": bool(self.pulsemcp_official or self.registry_published),
            "tier": self._compute_tier(),
            "categories": self._infer_categories(),
            "skills_realized": [],
            "relations": {
                "exposes": [],
                "belongs_to": self._infer_categories(),
                "commonly_composed_with": [],
                "realizes_skills": [],
            },
            "license": self.github_license or "",
            "source_url": self.github_url or "",
            "homepage": self.homepage or self.github_url or "",
            "description": self.description or "",
        }

    def _compute_tier(self) -> str:
        """Compute quality tier from signals."""
        # Official tier
        if self.pulsemcp_official or self.pulsemcp_classification in ("official", "reference"):
            return "Official"
        if self.registry_published and self.publisher_id in ("modelcontextprotocol", "anthropic"):
            return "Official"
        # Verified tier
        if self.github_stars and self.github_stars >= 500:
            return "Verified"
        if self.pulsemcp_visitors_weekly and self.pulsemcp_visitors_weekly >= 10000:
            return "Verified"
        if self.registry_published:
            return "Community"
        # Community tier
        if self.github_stars and self.github_stars >= 100:
            return "Community"
        return "Experimental"

    def _infer_categories(self) -> list[str]:
        """Infer categories from GitHub topics and description."""
        cats = set()
        text = " ".join(self.github_topics + [self.description or ""]).lower()

        mapping = {
            "development": ["code", "developer", "ide", "editor", "lint", "refactor", "terminal", "shell"],
            "data": ["database", "sql", "postgres", "sqlite", "redis", "cache", "storage", "db"],
            "web": ["browser", "scraping", "http", "api", "web", "fetch", "search", "google"],
            "communication": ["slack", "discord", "email", "message", "chat", "notification"],
            "ai-operations": ["ai", "llm", "model", "vector", "embedding", "rag", "reasoning", "thinking"],
            "infrastructure": ["docker", "kubernetes", "k8s", "aws", "cloud", "monitoring", "logging", "time"],
        }
        for cat, keywords in mapping.items():
            if any(kw in text for kw in keywords):
                cats.add(cat)
        if not cats:
            cats.add("development")  # default
        return sorted(cats)
