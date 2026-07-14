---
type: MCP-Server
id: github
name: GitHub
publisher: modelcontextprotocol
transport: stdio
install:
  type: npm
  command: "npx -y @modelcontextprotocol/server-github"
capabilities:
  tools:
    - search_repositories
    - get_file_contents
    - create_issue
    - create_pull_request
    - list_commits
    - get_issue
    - update_issue
    - list_pull_requests
    - merge_pull_request
    - fork_repository
    - create_branch
    - search_code
    - list_issues
    - add_issue_comment
  resources:
    - repository://{owner}/{repo}
    - issue://{owner}/{repo}/{number}
    - pull-request://{owner}/{repo}/{number}
  prompts:
    - review_pull_request
    - analyze_repository
    - summarize_issues
stars: 13000
last_updated: 2025-04-15
verified: true
tier: Official
categories:
    - development
skills_realized:
    - code-review
relations:
  exposes:
    - repository://{owner}/{repo}
    - issue://{owner}/{repo}/{number}
    - pull-request://{owner}/{repo}/{number}
  belongs_to:
    - development
  commonly_composed_with:
    - filesystem
    - fetch
  realizes_skills:
    - code-review
license: MIT
source_url: https://github.com/modelcontextprotocol/server-github
homepage: https://github.com/modelcontextprotocol/server-github
description: Official GitHub MCP server providing comprehensive access to GitHub's API for repository management, issues, pull requests, and code review.
---

The official GitHub MCP server provides comprehensive access to GitHub's API through the Model Context Protocol. It enables agents to search repositories, read file contents, manage issues and pull requests, analyze commit history, and perform code review tasks.

## Key Features

- **Repository Operations**: Search, fork, and browse repositories across GitHub
- **Issue Management**: Create, read, update, and comment on issues
- **Pull Request Workflow**: Create, review, merge, and manage PRs
- **Code Search**: Search code across all of GitHub with advanced queries
- **Branch Management**: Create branches and manage repository structure

## Authentication

Requires a `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable with appropriate scopes. Recommended scopes: `repo`, `read:user`, and `read:org` for full functionality.

## Use Cases

- Automated code review and PR summarization
- Repository analysis and documentation generation
- Issue triage and bug tracking workflows
- Contributor analytics and project insights
