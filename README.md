# al-dente

**Precise. Data-first. GitHub-native.**

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-222?logo=github)](https://al-dente.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-C45C3B)](LICENSE)
[![Status: Active Development](https://img.shields.io/badge/Status-Active%20Development-4CAF50)]()

---

## What is al-dente?

**al-dente** is the living register of the agentic engineering ecosystem. It maps the two things that matter most right now — **MCP Servers** and **Skills** — as a curated OKF bundle: plain Markdown files with YAML frontmatter, stored in a GitHub repository.

No walled gardens. No APIs to rate-limit you. No opaque databases. Just structured, versioned, human-readable knowledge that happens to be trivially ingestible by agents. Every MCP server, every skill taxonomy, every relationship between what agents *can do* and the tools that make it possible — tracked as diffable files you can `cat`, `grep`, or feed straight into Claude.

This is the map the agentic community doesn't have yet. The ecosystem is growing explosively — MCP has become the de facto "USB-C for AI agents" — but the landscape is fragmented across registries, directories, and framework-specific taxonomies. al-dente solves this by doing one thing precisely: maintaining a **high-signal, curated, evolving map** that shows both the current state and the direction of travel.

The philosophy is simple: cook it firm to the bite. High signal, low noise. Curated over exhaustive. Extensible without being bloated. *Al dente.*

### About OKF

al-dente stores its data in the **Open Knowledge Format (OKF)** — an open, vendor-neutral specification published by [Google Cloud](https://github.com/GoogleCloudPlatform/knowledge-catalog) in June 2026. OKF formalizes the "LLM wiki" pattern into a portable standard: a directory of Markdown files with YAML frontmatter, where each file represents one concept. The spec requires exactly one field (`type`) and leaves everything else to the producer.

We did not create OKF. We use it. Our data follows OKF v0.1 ([spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)) and layers domain-specific conventions on top — entity types like `MCP-Server` and `Skill`, relations like `realizes` and `commonly_composed_with`, and quality tiers. The minimal base is Google's. The agentic-engineering shape on top is ours.

> **OKF spec**: [`GoogleCloudPlatform/knowledge-catalog/okf/SPEC.md`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)  
> **OKF authors**: Sam McVeety & Amir Hormati (Google Cloud Data Cloud team)  
> **OKF license**: Apache 2.0

---

## Live Views

Three ways to explore the same canonical data — because one representation is never enough:

- **[Dashboard Overview](https://al-dente-processes.github.io/al-dente/index.html)** — Stats, trends, and directional insights at a glance.
- **[Searchable Register](https://al-dente-processes.github.io/al-dente/register.html)** — Filter, sort, and search every MCP server and skill in the register.
- **[Knowledge Graph](https://al-dente-processes.github.io/al-dente/graph.html)** — Interactive graph of entities, relations, and emergent patterns.

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
│   └── index.md        # Bundle entry point (OKF convention)
├── ontology/           # al-dente schema: entity types & validation rules on top of OKF
├── pipeline/           # Automation scripts (discover → enrich → build → deploy)
│   ├── build_okf.py    # Validates + compiles OKF data to JSON/JS bundles
│   └── views/          # View generators (graph, register, dashboard, ...)
├── docs/               # GitHub Pages source (interactive views)
│   ├── index.html      # Dashboard
│   ├── register.html   # Searchable table
│   ├── graph.html      # D3.js knowledge graph
│   └── assets/
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

The OKF bundle lives in `data/` as plain Markdown files. Every entity is a file. Open any `.md` file to see structured YAML frontmatter + human-readable description. That's it. No build step needed to explore.

```bash
# Clone and explore
git clone https://github.com/al-dente-dev/al-dente.git
cd al-dente
cat data/mcp-servers/github.md
```

Every file follows the OKF format: YAML frontmatter (with at minimum a `type` field) + Markdown body. See Google's [OKF spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) for the base format, and `ontology/schema.yaml` for al-dente's domain-specific extensions.

### Run the Pipeline Locally

```bash
# Install dependencies
make install

# Build OKF bundle (validates schema + compiles to JSON)
make build

# Serve views locally for development
make serve

# Run discovery pipeline (dry-run — shows what would be added)
make discover

# Run discovery pipeline (live — writes new servers to data/mcp-servers/)
make discover-live
```

### GitHub-Native Automation

al-dente runs entirely on GitHub — no external infrastructure needed. Three workflows handle everything:

| Workflow | File | Trigger | What It Does |
|----------|------|---------|-------------|
| **Discover** | `.github/workflows/discover.yml` | Weekly (Sundays 02:00 UTC) + manual | Crawls Official MCP Registry, PulseMCP, GitHub Topics → quality gates → commits new servers → opens PR for review |
| **Build & Deploy** | `.github/workflows/pages.yml` | Push to `main` (data/ontology/pipeline/docs changes) + manual | Validates OKF → builds JSON/JS bundles → generates views → deploys to GitHub Pages |
| **Validate** | `.github/workflows/ci.yml` | Pull request (data/ontology/pipeline changes) | Validates OKF schema integrity → reports status on PR |

**Automation flow:**
```
Every Sunday 02:00 UTC
        │
        ▼
┌──────────────────┐
│  discover.yml    │  ← Crawls sources, applies quality gates
│  (scheduled)     │  ← Creates PR with new/updated servers
└────────┬─────────┘
         │ (human reviews & merges PR)
         ▼
┌──────────────────┐
│  ci.yml          │  ← Validates OKF on PR
│  (PR trigger)    │  ← Must pass before merge
└────────┬─────────┘
         │ (PR merged to main)
         ▼
┌──────────────────┐
│  pages.yml       │  ← Builds OKF + views
│  (push trigger)  │  ← Deploys to GitHub Pages
└──────────────────┘
```

**Required secrets** (set in Settings → Secrets):
- `PULSE_MCP_API_KEY` — Get free key at [pulsemcp.com](https://www.pulsemcp.com)
- `GITHUB_TOKEN` — Auto-provided by GitHub Actions

### Contribute

The fastest way to help: add a new `.md` file in the appropriate `data/` subdirectory following the schema in `ontology/schema.yaml`. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow — it's simpler than you think.

---

## Core Principles

- **Data-first (OKF)** — Knowledge as Markdown+YAML, stored in Google's Open Knowledge Format. Git-versioned, diffable, `cat`-able, agent-ingestible. Views are *projections* of the data, not the source of truth.
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

## Acknowledgments

- **Open Knowledge Format (OKF)** — [Google Cloud](https://github.com/GoogleCloudPlatform/knowledge-catalog). The foundation this project builds on. Sam McVeety and Amir Hormati for the spec.
- **Model Context Protocol (MCP)** — [Anthropic](https://github.com/modelcontextprotocol). The protocol that makes agentic tool interoperability possible.
- **Andrej Karpathy** — For the [LLM Wiki](https://gist.github.com/karpathy/442ab79d716ee8ca7a9dcdd3f8ea5ac0) pattern that OKF formalized.

---

## License

MIT — see [LICENSE](LICENSE)

---

*To the tooth.*
