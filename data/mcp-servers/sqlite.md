---
type: MCP-Server
id: sqlite
name: SQLite
publisher: community
transport: stdio
install:
  type: npm
  command: "npx -y @modelcontextprotocol/server-sqlite /path/to/database.db"
capabilities:
  tools:
    - query
    - execute
    - list_tables
    - describe_table
    - create_table
    - insert_data
  resources:
    - sqlite://tables
    - sqlite://schema
  prompts:
    - schema_analysis
    - query_optimization
stars: 4200
last_updated: 2025-04-07
verified: false
tier: Community
categories:
    - data
skills_realized:
    - database-query
relations:
  exposes:
    - sqlite://tables
    - sqlite://schema
  belongs_to:
    - data
  commonly_composed_with:
    - filesystem
    - postgres
  realizes_skills:
    - database-query
license: MIT
source_url: https://github.com/modelcontextprotocol/server-sqlite
homepage: https://github.com/modelcontextprotocol/server-sqlite
description: SQLite MCP server providing local file-based database operations with full SQL support, schema introspection, and zero external dependencies.
---

The SQLite MCP server provides local, file-based database operations for AI agents. Unlike the PostgreSQL server, it requires no separate database process — just a path to a `.db` file.

## Key Features

- **SQL Operations**: Execute queries with full DDL and DML support
- **Schema Management**: Create, alter, and inspect tables and indexes
- **Data Manipulation**: Insert, update, delete with parameterized queries
- **Schema Introspection**: Automatic analysis of database structure
- **Zero Configuration**: No server setup — works directly with `.db` files

## Use Cases

- Local application data storage
- Prototyping and development databases
- Embedded analytics and reporting
- Data transformation pipelines
- Cache and session management
