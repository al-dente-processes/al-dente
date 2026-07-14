---
type: MCP-Server
id: sentry
name: Sentry
publisher: modelcontextprotocol
transport: stdio
install:
  type: npm
  command: "npx -y @modelcontextprotocol/server-sentry"
capabilities:
  tools:
    - sentry_get_issue
    - sentry_list_issues
    - sentry_get_project
    - sentry_list_projects
    - sentry_get_event
    - sentry_create_comment
  resources:
    - sentry://projects
    - sentry://issues
  prompts:
    - analyze_error
    - triage_issues
stars: 1900
last_updated: 2025-04-02
verified: true
tier: Official
categories:
    - infrastructure
    - development
skills_realized:
relations:
  exposes:
    - sentry://projects
    - sentry://issues
  belongs_to:
    - infrastructure
    - development
  commonly_composed_with:
    - slack
    - github
  realizes_skills:
license: MIT
source_url: https://github.com/modelcontextprotocol/server-sentry
homepage: https://github.com/modelcontextprotocol/server-sentry
description: Official Sentry MCP server enabling agents to monitor application errors, inspect stack traces, retrieve issues, and assist with bug triage.
---

The official Sentry MCP server enables AI agents to monitor and analyze application errors through the Model Context Protocol. Agents can retrieve issues, inspect stack traces, and help triage bugs.

## Key Features

- **Issue Retrieval**: Get detailed issue information with full stack traces
- **Issue Management**: List and filter issues by project, status, and priority
- **Project Browsing**: Explore projects and organizations
- **Event Inspection**: Deep-dive into individual error events with context
- **Team Collaboration**: Add comments to issues for workflow coordination
- **Analysis Prompts**: Built-in error analysis and triage assistance

## Authentication

Requires a `SENTRY_AUTH_TOKEN` environment variable with `org:read`, `project:read`, and `event:read` scopes.

## Use Cases

- Automated error triage and prioritization
- Root cause analysis from stack traces
- Bug report generation and ticket creation
- Error trend monitoring and alerting
