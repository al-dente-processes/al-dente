---
type: MCP-Server
id: fetch
name: Fetch
publisher: modelcontextprotocol
transport: stdio
install:
  type: npm
  command: "npx -y @modelcontextprotocol/server-fetch"
capabilities:
  tools:
    - fetch_url
    - fetch_html
    - fetch_json
    - fetch_text
  resources:
  prompts:
stars: 4800
last_updated: 2025-04-09
verified: true
tier: Official
categories:
    - web
skills_realized:
relations:
  exposes:
  belongs_to:
    - web
  commonly_composed_with:
    - brave-search
    - puppeteer
    - sequential-thinking
  realizes_skills:
license: MIT
source_url: https://github.com/modelcontextprotocol/server-fetch
homepage: https://github.com/modelcontextprotocol/server-fetch
description: Official Fetch MCP server providing simple, reliable HTTP fetching with automatic HTML-to-Markdown conversion and JSON parsing.
---

The official Fetch MCP server provides simple, reliable HTTP fetching capabilities for AI agents. It handles HTML, JSON, and plain text content with automatic content-type detection and parsing.

## Key Features

- **HTTP Fetching**: GET, POST, and other HTTP methods with configurable headers
- **HTML-to-Markdown**: Automatic conversion of HTML pages to clean Markdown
- **JSON Parsing**: Automatic parsing and validation of JSON responses
- **Text Extraction**: Plain text extraction from web pages
- **Safety**: URL validation to prevent SSRF attacks

## Use Cases

- Quick data retrieval from REST APIs
- Content fetching for analysis and summarization
- Lightweight web scraping without browser overhead
- Webhook integration and callback handling
