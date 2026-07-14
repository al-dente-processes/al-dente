---
type: MCP-Server
id: aws-kb-retrieval
name: AWS Knowledge Base Retrieval
publisher: modelcontextprotocol
transport: stdio
install:
  type: npm
  command: "npx -y @modelcontextprotocol/server-aws-kb-retrieval"
capabilities:
  tools:
    - retrieve_from_kb
    - query_kb
    - list_knowledge_bases
  resources:
    - aws://knowledge-bases
  prompts:
    - synthesize_knowledge
stars: 2400
last_updated: 2025-04-04
verified: true
tier: Official
categories:
    - ai-operations
    - data
skills_realized:
    - knowledge-retrieval
relations:
  exposes:
    - aws://knowledge-bases
  belongs_to:
    - ai-operations
    - data
  commonly_composed_with:
    - sequential-thinking
    - fetch
  realizes_skills:
    - knowledge-retrieval
license: MIT
source_url: https://github.com/modelcontextprotocol/server-aws-kb-retrieval
homepage: https://github.com/modelcontextprotocol/server-aws-kb-retrieval
description: Official AWS Knowledge Base Retrieval MCP server for querying Amazon Bedrock Knowledge Bases with semantic search and RAG support.
---

The official AWS Knowledge Base Retrieval MCP server enables AI agents to query Amazon Bedrock Knowledge Bases through the Model Context Protocol. It supports retrieval-augmented generation (RAG) workflows.

## Key Features

- **Knowledge Retrieval**: Fetch relevant documents from Bedrock Knowledge Bases
- **Semantic Search**: Natural language queries with vector similarity matching
- **KB Management**: List and explore available knowledge bases
- **Configurable Retrieval**: Control result count, relevance thresholds, and filters
- **RAG Integration**: Built-in prompts for knowledge synthesis

## Authentication

Requires standard AWS credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`) with permissions for `bedrock:Retrieve` and `bedrock-agent:ListKnowledgeBases`.

## Use Cases

- Enterprise knowledge base Q&A
- Document-grounded response generation
- Internal documentation search
- Compliance and policy lookup
