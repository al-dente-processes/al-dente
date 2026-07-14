---
type: MCP-Server
id: puppeteer
name: Puppeteer
publisher: modelcontextprotocol
transport: stdio
install:
  type: npm
  command: "npx -y @modelcontextprotocol/server-puppeteer"
capabilities:
  tools:
    - puppeteer_navigate
    - puppeteer_screenshot
    - puppeteer_click
    - puppeteer_type
    - puppeteer_evaluate
    - puppeteer_get_content
    - puppeteer_scroll
  resources:
    - browser://console
    - browser://network
  prompts:
    - debug_webpage
    - extract_data
stars: 7200
last_updated: 2025-04-11
verified: true
tier: Official
categories:
    - web
skills_realized:
    - browser-automation
relations:
  exposes:
    - browser://console
    - browser://network
  belongs_to:
    - web
  commonly_composed_with:
    - fetch
    - brave-search
  realizes_skills:
    - browser-automation
license: MIT
source_url: https://github.com/modelcontextprotocol/server-puppeteer
homepage: https://github.com/modelcontextprotocol/server-puppeteer
description: Official Puppeteer MCP server providing full browser automation via headless Chrome for navigation, interaction, screenshots, and JavaScript execution.
---

The official Puppeteer MCP server provides full browser automation capabilities for AI agents. Built on Google's Puppeteer, it enables navigation, interaction, screenshot capture, and JavaScript execution in headless Chrome.

## Key Features

- **Navigation**: Load URLs and wait for page stabilization
- **Screenshots**: Capture full-page or element-specific screenshots
- **Interaction**: Click elements, fill forms, and simulate user input
- **JavaScript Execution**: Run JS in browser context for dynamic content extraction
- **Content Extraction**: Retrieve structured data from rendered pages
- **Scrolling**: Handle infinite scroll and dynamic content loading

## Use Cases

- Web scraping and data extraction from JavaScript-heavy sites
- Visual regression testing and screenshot comparison
- Automated form submission and workflow testing
- PDF generation from web pages
- SPA (Single Page Application) interaction and testing
