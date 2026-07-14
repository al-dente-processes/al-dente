---
type: MCP-Server
id: brave-search
name: Brave Search
publisher: modelcontextprotocol
transport: stdio
install:
  type: npm
  command: "npx -y @modelcontextprotocol/server-brave-search"
capabilities:
  tools:
    - brave_web_search
    - brave_local_search
  resources:
  prompts:
    - search_and_summarize
stars: 5800
last_updated: 2025-04-14
verified: true
tier: Official
categories:
    - web
skills_realized:
    - web-search
relations:
  exposes:
  belongs_to:
    - web
  commonly_composed_with:
    - fetch
    - sequential-thinking
  realizes_skills:
    - web-search
license: MIT
source_url: https://github.com/modelcontextprotocol/server-brave-search
homepage: https://github.com/modelcontextprotocol/server-brave-search
description: Official Brave Search MCP server providing privacy-preserving web search and local business search capabilities.
---

The official Brave Search MCP server provides privacy-preserving web search capabilities for AI agents. It uses Brave's Search API to deliver high-quality search results without tracking user queries.

## Key Features

- **Web Search**: General search with pagination and configurable result counts
- **Local Search**: Find local businesses and points of interest
- **Privacy-First**: No user tracking or query profiling
- **Result Filtering**: Offset and count controls for result pagination
- **Search Prompts**: Built-in summarization and analysis prompts

## Authentication

Requires a `BRAVE_API_KEY` environment variable. Obtain a free or paid API key from the Brave Search API dashboard.

## Use Cases

- Research and information gathering
- Documentation lookup and technical reference
- Current event analysis and fact-checking
- Local business and service discovery
