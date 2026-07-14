---
type: Agentic-Pattern
id: skill-realization
name: Skill Realization
description: >-
  Abstract skills mapped to concrete tool implementations. This pattern describes how high-level capabilities (skills) are grounded in specific MCP server implementations. A single skill like 'database-query' can be realized by multiple servers (PostgreSQL, SQLite, Redis), each optimized for different scenarios.
examples:
    - postgres
    - sqlite
    - redis
    - brave-search
    - puppeteer
relations:
  exemplified_by:
    - postgres
    - sqlite
    - redis
    - brave-search
    - puppeteer
  related_to:
    - tool-composition
    - context-amplification
---
