#!/usr/bin/env python3
"""
Skill inference — maps MCP server capabilities to skills and auto-generates
skill taxonomy entries from discovered data.

This is the bridge between the tool layer (what servers DO) and the skill layer
(what agents CAN DO). Every tool exposed by an MCP server maps to one or more
skills. Every skill is realized by one or more MCP servers.

The mapping is heuristic-based, extensible, and learns from the data.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from .models import CandidateServer

logger = logging.getLogger(__name__)

# ─── Capability → Skill Mapping ───────────────────────────────────────────────
# Maps tool name patterns, resource patterns, and description keywords to skills.
# This is the core of skill inference. Extend as the ecosystem grows.

CAPABILITY_TO_SKILLS: list[dict[str, Any]] = [
    # Code Generation & Manipulation
    {
        "skills": ["code-generation", "code-editing"],
        "patterns": [
            r"\b(code|generate|create|write|refactor|edit|modify|lint|format|compile|build)\b.*\b(code|file|function|class|method)\b",
            r"\b(template|scaffold|boilerplate|snippet)\b",
            r"\b(generate_code|write_code|create_file|edit_file|apply_edit|replace|insert)\b",
        ],
    },
    # Code Review & Analysis
    {
        "skills": ["code-review", "static-analysis"],
        "patterns": [
            r"\b(review|audit|analyze|inspect|check|scan|detect|find)\b.*\b(code|bug|vuln|security|issue|smell|pattern)\b",
            r"\b(lint|type.?check|format\.check|test\.coverage)\b",
        ],
    },
    # Database Query & Management
    {
        "skills": ["database-query", "data-management"],
        "patterns": [
            r"\b(query|select|insert|update|delete|create|drop|alter|schema|table|database|db|sql|nosql)\b",
            r"\b(postgres|mysql|sqlite|redis|mongodb|dynamodb|cassandra|elasticsearch)\b",
            r"\b(read|write|migrate|seed|backup|sync)\b.*\b(database|db|data)\b",
        ],
    },
    # Web Search & Information Retrieval
    {
        "skills": ["web-search", "information-retrieval"],
        "patterns": [
            r"\b(search|find|lookup|query|browse|crawl|scrape|index)\b.*\b(web|internet|site|page|url|google|bing|duckduckgo)\b",
            r"\b(serp|search_engine|web_search|internet_search)\b",
        ],
    },
    # Browser Automation
    {
        "skills": ["browser-automation", "web-interaction"],
        "patterns": [
            r"\b(browser|puppeteer|playwright|selenium|chrome|headless|navigate|click|type|screenshot|viewport)\b",
            r"\b(visit|goto|open|load|scroll|fill|submit|intercept)\b.*\b(page|site|url|form)\b",
        ],
    },
    # File Operations
    {
        "skills": ["file-operations", "filesystem-management"],
        "patterns": [
            r"\b(read|write|create|delete|move|copy|list|search|find|glob|watch|monitor)\b.*\b(file|directory|folder|path)\b",
            r"\b(filesystem|fs|file_system|file_manager)\b",
        ],
    },
    # Communication & Collaboration
    {
        "skills": ["communication", "notification"],
        "patterns": [
            r"\b(slack|discord|email|telegram|matrix|teams|message|chat|notify|alert|send|post)\b",
            r"\b(channel|dm|thread|mention|notification|webhook|inbox)\b",
        ],
    },
    # Knowledge Retrieval & Documentation
    {
        "skills": ["knowledge-retrieval", "documentation-access"],
        "patterns": [
            r"\b(doc|documentation|readme|wiki|knowledge|faq|help|guide|reference|manual|api_doc)\b",
            r"\b(notion|confluence|obsidian|wiki|kb|knowledge_base)\b",
            r"\b(read|search|query)\b.*\b(doc|documentation|knowledge)\b",
        ],
    },
    # Reasoning & Planning
    {
        "skills": ["reasoning", "planning", "sequential-thinking"],
        "patterns": [
            r"\b(thinking|reason|plan|strategy|step|chain|sequence|workflow|orchestrate|decompose)\b",
            r"\b(sequential_thinking|think|reflect|plan_ahead|multi_step)\b",
        ],
    },
    # AI Operations
    {
        "skills": ["ai-operations", "model-interaction"],
        "patterns": [
            r"\b(llm|model|embedding|vector|rag|prompt|completion|token|inference|fine.?tune|train)\b",
            r"\b(generate|summarize|translate|classify|extract|embed|tokenize)\b.*\b(text|image|audio|content)\b",
        ],
    },
    # Infrastructure & DevOps
    {
        "skills": ["infrastructure-management", "deployment"],
        "patterns": [
            r"\b(docker|kubernetes|k8s|terraform|ansible|pulumi|helm|deploy|provision|infra|serverless)\b",
            r"\b(container|pod|service|deployment|cluster|node|vpc|lambda|ec2|gcp|azure)\b",
        ],
    },
    # Security & Access Control
    {
        "skills": ["security", "access-control"],
        "patterns": [
            r"\b(auth|oauth|jwt|sso|mfa|permission|role|acl|secret|vault|encrypt|decrypt|sign|verify)\b",
            r"\b(security|vulnerability|pentest|audit|compliance|gdpr|hipaa)\b",
        ],
    },
    # Monitoring & Observability
    {
        "skills": ["monitoring", "observability"],
        "patterns": [
            r"\b(monitor|observe|metric|log|trace|alert|dashboard|sentry|datadog|grafana|prometheus)\b",
            r"\b(error|exception|crash|performance|latency|throughput|uptime)\b.*\b(track|monitor|alert)\b",
        ],
    },
    # Version Control & Git
    {
        "skills": ["version-control", "git-operations"],
        "patterns": [
            r"\b(git|github|gitlab|bitbucket|repo|repository|commit|branch|merge|pr|pull_request|clone|checkout|diff|blame)\b",
            r"\b(issue|milestone|release|tag|changelog|contrib)\b",
        ],
    },
    # Time & Scheduling
    {
        "skills": ["time-management", "scheduling"],
        "patterns": [
            r"\b(time|timezone|clock|timer|schedule|cron|calendar|date|deadline|reminder|alarm)\b",
        ],
    },
    # Maps & Location
    {
        "skills": ["geolocation", "mapping"],
        "patterns": [
            r"\b(map|location|geo|gps|coordinate|latitude|longitude|address|place|direction|routing|geocode)\b",
            r"\b(google_maps|openstreetmap|mapbox|nominatim)\b",
        ],
    },
    # Image & Media Processing
    {
        "skills": ["image-processing", "media-generation"],
        "patterns": [
            r"\b(image|photo|picture|video|audio|media|draw|generate_image|generate_video|transcribe|tts|stt)\b",
            r"\b(dall[eé]|midjourney|stable.?diffusion|ffmpeg|opencv|pillow)\b",
        ],
    },
    # API Integration
    {
        "skills": ["api-integration", "service-orchestration"],
        "patterns": [
            r"\b(api|rest|graphql|grpc|webhook|sdk|client|integration|connector|adapter|proxy|gateway)\b",
            r"\b(fetch|request|call|invoke|post|get|put|delete|patch)\b.*\b(api|endpoint|service)\b",
        ],
    },
]

# ─── Tool name → Skill direct mapping ────────────────────────────────────────
# Common tool names that directly indicate a skill.

TOOL_TO_SKILL: dict[str, list[str]] = {
    # Git tools
    "search_repos": ["version-control", "code-review"],
    "get_file_contents": ["version-control", "file-operations"],
    "create_issue": ["version-control", "communication"],
    "create_pull_request": ["version-control"],
    "get_commit": ["version-control"],
    "list_branches": ["version-control"],
    "fork_repository": ["version-control"],
    # Filesystem tools
    "read_file": ["file-operations"],
    "write_file": ["file-operations", "code-generation"],
    "list_directory": ["file-operations"],
    "search_files": ["file-operations"],
    # Database tools
    "query": ["database-query"],
    "execute": ["database-query"],
    "list_tables": ["database-query"],
    "describe_table": ["database-query"],
    # Search tools
    "brave_web_search": ["web-search"],
    "brave_local_search": ["web-search"],
    "search": ["web-search", "information-retrieval"],
    # Browser tools
    "puppeteer_navigate": ["browser-automation"],
    "puppeteer_screenshot": ["browser-automation", "image-processing"],
    "puppeteer_click": ["browser-automation"],
    "puppeteer_evaluate": ["browser-automation"],
    # Communication tools
    "slack_post_message": ["communication"],
    "slack_list_channels": ["communication"],
    # Maps tools
    "maps_geocode": ["geolocation"],
    "maps_directions": ["geolocation", "mapping"],
    "maps_search_places": ["geolocation", "web-search"],
    # AI tools
    "generate_image": ["ai-operations", "media-generation"],
    "generate_text": ["ai-operations", "code-generation"],
    "embed_text": ["ai-operations"],
    # Reasoning
    "sequentialthinking": ["reasoning", "planning"],
    # Time
    "get_current_time": ["time-management"],
    "convert_timezone": ["time-management"],
}


def infer_skills(server: CandidateServer) -> list[str]:
    """
    Infer skills realized by an MCP server from its capabilities and metadata.

    Combines three strategies:
    1. Direct tool name → skill mapping
    2. Regex pattern matching on tool/resource names and descriptions
    3. Keyword matching on server description

    Returns deduplicated list of skill IDs.
    """
    skills: set[str] = set()
    text_to_match = _extract_matchable_text(server)

    # Strategy 1: Direct tool name mapping
    capabilities = server._github_api_data.get("capabilities", {}) if hasattr(server, "_github_api_data") else {}
    if isinstance(capabilities, dict):
        tools = capabilities.get("tools", [])
        for tool in tools:
            tool_lower = tool.lower().replace("-", "_").replace(".", "_")
            for pattern_tool, pattern_skills in TOOL_TO_SKILL.items():
                if pattern_tool.lower() in tool_lower or tool_lower in pattern_tool.lower():
                    skills.update(pattern_skills)

    # Strategy 2: Regex pattern matching
    for mapping in CAPABILITY_TO_SKILLS:
        for pattern in mapping["patterns"]:
            if re.search(pattern, text_to_match, re.IGNORECASE):
                skills.update(mapping["skills"])
                break  # One match per mapping is enough

    # Strategy 3: Name-based inference
    name_lower = server.name.lower()
    if "git" in name_lower:
        skills.update(["version-control"])
    if any(db in name_lower for db in ["postgres", "sqlite", "mysql", "redis", "mongo", "db"]):
        skills.update(["database-query", "data-management"])
    if any(s in name_lower for s in ["search", "brave", "google", "bing"]):
        skills.update(["web-search", "information-retrieval"])
    if any(b in name_lower for b in ["browser", "puppeteer", "playwright"]):
        skills.update(["browser-automation"])
    if any(f in name_lower for f in ["file", "fs", "filesystem"]):
        skills.update(["file-operations"])
    if any(c in name_lower for c in ["slack", "discord", "email", "telegram"]):
        skills.update(["communication"])
    if "time" in name_lower:
        skills.update(["time-management"])
    if any(m in name_lower for m in ["map", "google-maps", "location"]):
        skills.update(["geolocation", "mapping"])
    if any(a in name_lower for a in ["ai", "llm", "openai", "anthropic", "claude"]):
        skills.update(["ai-operations"])
    if "sequential" in name_lower or "thinking" in name_lower:
        skills.update(["reasoning", "planning"])
    if any(s in name_lower for s in ["sentry", "monitor", "observ"]):
        skills.update(["monitoring", "observability"])
    if "security" in name_lower or "auth" in name_lower:
        skills.update(["security", "access-control"])

    return sorted(skills)


def _extract_matchable_text(server: CandidateServer) -> str:
    """Extract all matchable text from a server for pattern matching."""
    parts = []

    # Description
    if server.description:
        parts.append(server.description)

    # Server name
    parts.append(server.name)
    if server.display_name:
        parts.append(server.display_name)

    # GitHub topics
    parts.extend(server.github_topics)

    # Capabilities from raw data
    for source in server.sources:
        raw = source.raw_data
        if isinstance(raw, dict):
            # Tools from registry data
            srv = raw.get("server", raw)
            caps = srv.get("capabilities", {})
            if isinstance(caps, dict):
                parts.extend(caps.get("tools", []))
                parts.extend(caps.get("resources", []))
                parts.extend(caps.get("prompts", []))

    return " ".join(str(p) for p in parts if p)


def generate_skill_taxonomy(servers: list[CandidateServer]) -> dict[str, dict]:
    """
    Generate skill taxonomy entries from a collection of servers.

    For each skill realized by at least one server, creates a skill entry
    with metadata and realized_by relations.

    Returns: {skill_id: skill_dict}
    """
    skill_servers: dict[str, list[str]] = {}

    for server in servers:
        skills = infer_skills(server)
        for skill_id in skills:
            if skill_id not in skill_servers:
                skill_servers[skill_id] = []
            skill_servers[skill_id].append(server.id)

    # Build skill entries
    skill_entries = {}
    for skill_id, server_ids in sorted(skill_servers.items(), key=lambda x: -len(x[1])):
        # Filter skills with at least 2 realizers (avoid noise)
        if len(server_ids) < 2 and skill_id not in _CORE_SKILLS:
            continue

        skill_entries[skill_id] = {
            "id": skill_id,
            "name": _skill_name(skill_id),
            "taxonomy": "al-dente-auto",
            "level": _skill_level(skill_id),
            "realized_by": sorted(set(server_ids)),
            "realized_by_count": len(set(server_ids)),
            "description": _skill_description(skill_id),
        }

    return skill_entries


# Core skills that always exist even with few realizers
_CORE_SKILLS = {
    "code-generation", "code-review", "database-query", "web-search",
    "browser-automation", "file-operations", "communication",
    "knowledge-retrieval", "reasoning", "ai-operations",
}


def _skill_name(skill_id: str) -> str:
    """Human-readable name from skill ID."""
    return skill_id.replace("-", " ").title()


def _skill_level(skill_id: str) -> int:
    """Taxonomy level: 1=broad, 5=specific."""
    broad = {"code-generation", "database-query", "web-search", "communication",
             "file-operations", "ai-operations", "reasoning"}
    if skill_id in broad:
        return 2
    specific = {"sequential-thinking", "git-operations", "timezone-conversion"}
    if skill_id in specific:
        return 4
    return 3


def _skill_description(skill_id: str) -> str:
    """Description for a skill."""
    descriptions = {
        "code-generation": "Generate, write, and modify source code across programming languages.",
        "code-editing": "Apply precise edits to existing code files and structures.",
        "code-review": "Analyze code for bugs, style issues, security vulnerabilities, and improvement opportunities.",
        "static-analysis": "Examine code without executing it to find patterns, smells, and issues.",
        "database-query": "Execute queries against databases to read, write, and manage structured data.",
        "data-management": "Create, modify, and maintain database schemas, migrations, and data pipelines.",
        "web-search": "Search the internet for current information, documentation, and references.",
        "information-retrieval": "Find and extract relevant information from large document collections and knowledge bases.",
        "browser-automation": "Control web browsers programmatically for testing, scraping, and interaction.",
        "web-interaction": "Navigate and interact with web pages as a human user would.",
        "file-operations": "Read, write, search, and manage files and directories in the local filesystem.",
        "filesystem-management": "Organize, monitor, and maintain directory structures and file systems.",
        "communication": "Send and receive messages through team communication platforms.",
        "notification": "Send alerts, notifications, and reminders through various channels.",
        "knowledge-retrieval": "Access and query structured knowledge bases, wikis, and documentation systems.",
        "documentation-access": "Read and navigate project documentation, READMEs, and API docs.",
        "reasoning": "Apply structured thinking, step-by-step analysis, and logical problem solving.",
        "planning": "Decompose complex tasks into ordered sequences of actions.",
        "ai-operations": "Interact with AI models for generation, embedding, classification, and other ML tasks.",
        "model-interaction": "Manage prompts, context windows, and model parameters for optimal outputs.",
        "infrastructure-management": "Provision, configure, and manage cloud infrastructure and containers.",
        "deployment": "Deploy applications and services to production environments.",
        "security": "Perform security audits, manage secrets, and enforce access controls.",
        "access-control": "Manage authentication, authorization, permissions, and identity.",
        "monitoring": "Track application health, performance metrics, and error rates in real time.",
        "observability": "Collect and analyze logs, traces, and metrics for system understanding.",
        "version-control": "Interact with Git repositories: commit, branch, merge, review code changes.",
        "git-operations": "Execute git commands and manage repository state programmatically.",
        "time-management": "Get current time, convert timezones, schedule events and reminders.",
        "scheduling": "Create and manage recurring jobs, cron schedules, and timed events.",
        "geolocation": "Convert addresses to coordinates, calculate distances, and resolve locations.",
        "mapping": "Generate maps, find routes, and visualize geographic data.",
        "image-processing": "Analyze, transform, and generate images programmatically.",
        "media-generation": "Create images, videos, audio, and other media content using AI models.",
        "api-integration": "Connect to external APIs, manage authentication, and handle rate limits.",
        "service-orchestration": "Coordinate multiple services and APIs to accomplish complex workflows.",
    }
    return descriptions.get(skill_id, f"Skill: {_skill_name(skill_id)}")


def update_server_relations(servers: list[CandidateServer]) -> None:
    """
    In-place update of server relations with inferred skills and cross-links.

    After running this, each server has:
    - skills_realized: [skill_id, ...]
    - relations.realizes_skills: [skill_id, ...]
    - relations.belongs_to: [category_id, ...] (already set)
    """
    for server in servers:
        skills = infer_skills(server)
        server.skills_realized = skills
        if "realizes_skills" in server.relations:
            server.relations["realizes_skills"] = skills
        else:
            server.relations.setdefault("realizes_skills", skills)

    # Cross-link: infer commonly_composed_with from shared skills
    _infer_composition_relations(servers)


def _infer_composition_relations(servers: list[CandidateServer]) -> None:
    """
    Infer commonly_composed_with relations based on shared skills.
    Two servers that realize the same skill are likely used together.
    """
    # Build skill → servers index
    skill_servers: dict[str, list[CandidateServer]] = {}
    for server in servers:
        for skill in server.skills_realized:
            skill_servers.setdefault(skill, []).append(server)

    # For each server, find peers that share skills (but limit results)
    for server in servers:
        peers: set[str] = set()
        for skill in server.skills_realized:
            for peer in skill_servers.get(skill, []):
                if peer.id != server.id:
                    peers.add(peer.id)
        # Keep top 5 most relevant peers
        server.relations["commonly_composed_with"] = sorted(peers)[:5]
