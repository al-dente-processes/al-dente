---
type: MCP-Server
id: postgres
name: PostgreSQL
publisher: modelcontextprotocol
transport: stdio
install:
  type: npm
  command: "npx -y @modelcontextprotocol/server-postgres postgresql://localhost/mydb"
capabilities:
  tools:
    - query
    - execute
    - list_tables
    - describe_table
    - get_connections
  resources:
    - database://schemas
    - database://tables
  prompts:
    - analyze_schema
    - optimize_query
stars: 8500
last_updated: 2025-04-10
verified: true
tier: Official
categories:
    - data
skills_realized:
    - database-query
relations:
  exposes:
    - database://schemas
    - database://tables
  belongs_to:
    - data
  commonly_composed_with:
    - filesystem
    - redis
  realizes_skills:
    - database-query
license: MIT
source_url: https://github.com/modelcontextprotocol/server-postgres
homepage: https://github.com/modelcontextprotocol/server-postgres
description: Official PostgreSQL MCP server enabling SQL query execution, schema introspection, and database management with read-only and read-write modes.
---

The official PostgreSQL MCP server enables AI agents to interact with PostgreSQL databases through the Model Context Protocol. It supports both read-only and read-write operations with configurable permissions.

## Key Features

- **SQL Execution**: Run queries with parameterized safety against injection
- **Schema Introspection**: List tables, describe columns, and analyze relationships
- **Read-Only Mode**: Safe exploration mode for production databases
- **Transaction Support**: Full ACID transaction support for write operations
- **Connection Management**: Efficient connection pooling and multi-database support

## Connection

Pass a PostgreSQL connection string as a command-line argument. Supports all standard PostgreSQL connection options including SSL and custom ports.

## Use Cases

- Database exploration and schema analysis
- SQL query generation and optimization
- Data migration and transformation scripts
- Reporting and analytics workflows
