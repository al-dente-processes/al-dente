---
type: MCP-Server
id: time
name: Time
publisher: modelcontextprotocol
transport: stdio
install:
  type: npm
  command: "npx -y @modelcontextprotocol/server-time"
capabilities:
  tools:
    - get_current_time
    - convert_timezone
    - list_timezones
    - parse_natural_time
  resources:
  prompts:
stars: 2100
last_updated: 2025-04-03
verified: true
tier: Official
categories:
    - infrastructure
skills_realized:
relations:
  exposes:
  belongs_to:
    - infrastructure
  commonly_composed_with:
    - slack
    - sentry
  realizes_skills:
license: MIT
source_url: https://github.com/modelcontextprotocol/server-time
homepage: https://github.com/modelcontextprotocol/server-time
description: Official Time MCP server providing time and timezone operations including current time, timezone conversion, and natural language time parsing.
---

The official Time MCP server provides time and timezone operations for AI agents. It enables getting current time, converting between timezones, and parsing natural language time expressions.

## Key Features

- **Current Time**: Get precise current time in any IANA timezone
- **Timezone Conversion**: Convert timestamps between timezones
- **Timezone Listing**: Browse all available IANA timezone identifiers
- **Natural Language Parsing**: Understand expressions like "3pm tomorrow in Tokyo"
- **ISO 8601 Output**: Machine-readable timestamp formatting

## Use Cases

- Multi-timezone scheduling and coordination
- Deadline tracking and countdown calculations
- Timestamp normalization across data sources
- Meeting time finding across time zones
