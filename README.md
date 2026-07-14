# al-dente

**Precise. Data-first. GitHub-native.**

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-222?logo=github)](https://al-dente.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-C45C3B)](LICENSE)
[![Status: Active Development](https://img.shields.io/badge/Status-Active%20Development-4CAF50)]()

---

## What is al-dente?

**al-dente** is the living register of the agentic engineering ecosystem. It maps the two things that matter most right now — **MCP Servers** and **Skills** — as plain Markdown files with YAML frontmatter. We call this the [Open Knowledge Format (OKF)](spec.md), and it means the data *is* the product.

No walled gardens. No APIs to rate-limit you. No opaque databases. Just a GitHub repository full of structured, versioned, human-readable knowledge that happens to be trivially ingestible by agents. Every MCP server, every skill taxonomy, every relationship between what agents *can do* and the tools that make it possible — tracked as diffable files you can `cat`, `grep`, or feed straight into Claude.

This is the map the agentic community doesn't have yet. The ecosystem is growing explosively — MCP has become the de facto "USB-C for AI agents" — but the landscape is fragmented across registries, directories, and framework-specific taxonomies. al-dente solves this by doing one thing precisely: maintaining a **high-signal, curated, evolving map** that shows both the current state and the direction of travel.

The philosophy is simple: cook it firm to the bite. High signal, low noise. Curated over exhaustive. Extensible without being bloated. *Al dente.*

---

## Live Views

Three ways to explore the same canonical data — because one representation is never enough:

- **[Dashboard Overview](https://al-dente.dev)** — Stats, trends, and directional insights at a glance.
- **[Searchable Register](https://al-dente.dev/register.html)** — Filter, sort, and search every MCP server and skill in the register.
- **[Knowledge Graph](https://al-dente.dev/graph.html)** — Interactive graph of entities, relations, and emergent patterns.

*(Views are generated from the same OKF source. Add a new view by contributing a generator script in `pipeline/views/`.)*

---

## Current Status

**Phase 0: Foundation** (July – August 2026). We are building the OKF data model, populating initial MCP servers, and standing up the first proof-of-concept views. The core schema is stabilizing. Community contributions are open and welcome.

See the [Roadmap](roadmap.md) for the full phased timeline — from foundation to community-driven public good.

---

## Repository Structure

```
al-dente/
├── data/               # Canonical OKF data (Markdown + YAML)
│   ├── mcp-servers/    # MCP server entries
│   ├── skills/         # Skill taxonomy entries
│   ├── categories/     # Hierarchical categories
│   ├── patterns/       # Agentic design patterns
│   ├── publishers/     # Publishers and maintainers
│   ├── snapshots/      # Point-in-time captures
│   └── index.md        # Entry point for navigation
├── ontology/           # OKF schema definitions and validation rules
├── pipeline/           # Automation scripts (discover → enrich → build → deploy)
│   ├── discover/
│   ├── enrich/
│   ├── build/
│   ├── views/          # View generators (graph, register, dashboard, ...)
│   └── snapshot/
├── docs/               # GitHub Pages source (interactive views)
│   ├── assets/
│   └── _config.yml
├── prd.md              # Product Requirements Document
├── design-system.md    # Visual design & representation guidelines
├── spec.md             # Technical specification (data model, pipeline, architecture)
├── roadmap.md          # Phased delivery plan
├── project-description.md  # Full project description and philosophy
├── CONTRIBUTING.md     # How to contribute (start here!)
└── LICENSE             # MIT License
```

---

## Quick Start

### Browse the Data

The OKF data lives in `data/` as plain Markdown files. Every entity is a file. Open any `.md` file to see structured YAML frontmatter + human-readable description. That's it. No build step needed to explore.

```bash
# Clone and explore
git clone https://github.com/al-dente-dev/al-dente.git
cd al-dente
cat data/mcp-servers/official-github-mcp-server.md
```

### Run the Pipeline Locally

```bash
# Install dependencies
make install

# Build OKF bundle (validates schema + compiles to JSON)
make build

# Serve views locally for development
make serve
```

### Contribute

The fastest way to help: add a new `.md` file in the appropriate `data/` subdirectory following the schema in `ontology/schema.yaml`. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow — it's simpler than you think.

---

## Core Principles

- **Data-first (OKF)** — Knowledge as Markdown+YAML. Git-versioned, diffable, `cat`-able, agent-ingestible. Views are *projections* of the data, not the source of truth.
- **GitHub-native** — The repo IS the knowledge base. Actions, Pages, Projects, Discussions — all first-class. Low operational overhead, high community accessibility.
- **Dual & Integrated** — MCP Servers and Skills modeled symmetrically with rich cross-linking (`realizes`, `realized_by`, `commonly_composed_with`).
- **Temporal & Directional** — Snapshots and diffs make change visible: new servers, emerging patterns, shifting concentrations. You can see where the field is heading, not just where it is.
- **Multiple Representations** — One OKF source → many views (graph, table, timeline, taxonomy map, dashboard, agent bundle). Easy to extend. Add a view by adding a generator.
- **Precise ("al dente")** — High-signal, curated core. Not bloated, not overcooked. We prefer a smaller set of excellent entries over an exhaustive directory of everything.

---

## Project Documents

| Document | Purpose |
|----------|---------|
| [PRD](prd.md) | Product requirements, goals, success metrics, and scope |
| [Design System](design-system.md) | Visual language, representation styles, and component guidelines |
| [Specification](spec.md) | Technical architecture, data model, pipeline design, and extensibility |
| [Roadmap](roadmap.md) | Phased delivery plan from foundation to community-driven public good |

---

## License

MIT — see [LICENSE](LICENSE)

---

*To the tooth.*
