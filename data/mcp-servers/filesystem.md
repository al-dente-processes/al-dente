---
type: MCP-Server
id: filesystem
name: Filesystem
publisher: modelcontextprotocol
transport: stdio
install:
  type: npm
  command: "npx -y @modelcontextprotocol/server-filesystem /path/to/allowed/dir"
capabilities:
  tools:
    - read_file
    - write_file
    - list_directory
    - create_directory
    - move_file
    - search_files
    - get_file_info
    - list_allowed_directories
  resources:
  prompts:
stars: 11000
last_updated: 2025-04-12
verified: true
tier: Official
categories:
    - development
    - infrastructure
skills_realized:
    - file-operations
relations:
  exposes:
  belongs_to:
    - development
    - infrastructure
  commonly_composed_with:
    - github
    - postgres
    - sqlite
  realizes_skills:
    - file-operations
license: MIT
source_url: https://github.com/modelcontextprotocol/server-filesystem
homepage: https://github.com/modelcontextprotocol/server-filesystem
description: Official Filesystem MCP server providing safe, sandboxed file system access with support for read, write, directory management, and file search operations.
---

The official Filesystem MCP server provides safe, sandboxed file system access for AI agents. All operations are restricted to explicitly allowed directories, preventing unauthorized access to sensitive system paths.

## Key Features

- **File Operations**: Read and write files with full text and binary support
- **Directory Management**: List, create, and traverse directories
- **File Search**: Pattern-based file search within allowed directories
- **Metadata Inspection**: Get file info including size, permissions, and timestamps
- **Sandboxed Access**: Multiple allowed directories with strict path validation

## Security Model

The server requires explicit directory paths as command-line arguments. It will refuse to access any path outside these allowed directories, making it safe to use with untrusted agents.

## Use Cases

- Local file management and organization
- Reading configuration files and logs
- Writing generated code, reports, and documentation
- Batch file processing and transformation
