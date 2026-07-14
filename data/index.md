# al-dente — Agentic Engineering Ecosystem

A living register of MCP Servers, Skills, Categories, Agentic Patterns, and Publishers — stored as Open Knowledge Format (OKF) bundles.

## Quick Navigation

### Entities by Type

| Type | Count | Directory |
|------|-------|-----------|
| [MCP Servers](./mcp-servers/) | 15 | `data/mcp-servers/` |
| [Skills](./skills/) | 8 | `data/skills/` |
| [Categories](./categories/) | 6 | `data/categories/` |
| [Agentic Patterns](./patterns/) | 3 | `data/patterns/` |
| [Publishers](./publishers/) | 8 | `data/publishers/` |

### MCP Servers by Category

- **[Development](./categories/development.md)**: [github](./mcp-servers/github.md), [filesystem](./mcp-servers/filesystem.md), [sentry](./mcp-servers/sentry.md)
- **[Data](./categories/data.md)**: [postgres](./mcp-servers/postgres.md), [sqlite](./mcp-servers/sqlite.md), [redis](./mcp-servers/redis.md)
- **[Web](./categories/web.md)**: [brave-search](./mcp-servers/brave-search.md), [puppeteer](./mcp-servers/puppeteer.md), [fetch](./mcp-servers/fetch.md), [google-maps](./mcp-servers/google-maps.md)
- **[Communication](./categories/communication.md)**: [slack](./mcp-servers/slack.md)
- **[AI Operations](./categories/ai-operations.md)**: [sequential-thinking](./mcp-servers/sequential-thinking.md), [aws-kb-retrieval](./mcp-servers/aws-kb-retrieval.md), [everart](./mcp-servers/everart.md)
- **[Infrastructure](./categories/infrastructure.md)**: [filesystem](./mcp-servers/filesystem.md), [time](./mcp-servers/time.md), [sentry](./mcp-servers/sentry.md), [redis](./mcp-servers/redis.md)

### Skills Realized

| Skill | Realized By |
|-------|-------------|
| [code-review](./skills/code-review.md) | [github](./mcp-servers/github.md) |
| [database-query](./skills/database-query.md) | [postgres](./mcp-servers/postgres.md), [sqlite](./mcp-servers/sqlite.md), [redis](./mcp-servers/redis.md) |
| [web-search](./skills/web-search.md) | [brave-search](./mcp-servers/brave-search.md) |
| [browser-automation](./skills/browser-automation.md) | [puppeteer](./mcp-servers/puppeteer.md) |
| [file-operations](./skills/file-operations.md) | [filesystem](./mcp-servers/filesystem.md) |
| [knowledge-retrieval](./skills/knowledge-retrieval.md) | [aws-kb-retrieval](./mcp-servers/aws-kb-retrieval.md) |
| [reasoning](./skills/reasoning.md) | [sequential-thinking](./mcp-servers/sequential-thinking.md) |
| [code-generation](./skills/code-generation.md) | *Available for implementation* |

### Agentic Patterns

- **[tool-composition](./patterns/tool-composition.md)** — Multiple MCP servers composed for complex tasks
- **[skill-realization](./patterns/skill-realization.md)** — Abstract skills mapped to concrete implementations
- **[context-amplification](./patterns/context-amplification.md)** — Retrieval tools augment agent context

### Publishers

| Publisher | Type | Servers |
|-----------|------|---------|
| [modelcontextprotocol](./publishers/modelcontextprotocol.md) | Official | 13 servers |
| [anthropic](./publishers/anthropic.md) | Official | — |
| [community](./publishers/community.md) | Community | sqlite, redis |
| [pulsarity-labs](./publishers/pulsarity-labs.md) | Community | — |
| [smithery](./publishers/smithery.md) | Community | — |
| [jetbrains](./publishers/jetbrains.md) | Official | — |
| [docker](./publishers/docker.md) | Official | — |
| [individual](./publishers/individual.md) | Individual | — |

## About OKF

The **Open Knowledge Format (OKF)** is a convention for storing structured knowledge as Markdown files with YAML frontmatter. Each entity is one `.md` file. The format is human-readable, version-control friendly, and machine-parseable.

### Schema

See [`ontology/schema.yaml`](../ontology/schema.yaml) for the complete OKF schema definition including all entity types, required fields, and relation types.

### Building

```bash
# Validate and compile the OKF bundle
python pipeline/build_okf.py --input data/ --output output/

# This produces:
#   output/okf_bundle.json   — Complete JSON bundle
#   output/okf_data.js       — JavaScript bundle (window.OKF_DATA)
```
