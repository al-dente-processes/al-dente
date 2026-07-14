# al-dente

**Precise. Data-first. GitHub-native.**

al-dente is the living, open register of the agentic engineering ecosystem — stored as **Open Knowledge Format (OKF)** bundles.

[OKF](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) is an open specification published by Google Cloud (June 2026) for representing knowledge as Markdown files with YAML frontmatter. al-dente is a producer and consumer of OKF — we did not create the format; we use it and extend it for the agentic engineering domain.

It provides a canonical, versionable, human- and agent-readable source of truth for:

- **MCP Servers** — the standardized connective tissue that lets AI agents discover and use tools, data, and capabilities.
- **Skills** — agent capabilities, taxonomies, patterns, and the relationships between what agents *can do* and the MCP servers/tools that realize them.

### Why al-dente exists

Agentic engineering is maturing rapidly. MCP has become the de facto “USB-C for AI agents.” Skills and capabilities are proliferating across frameworks, taxonomies, and community efforts. Yet there is no single, precise, evolving map of this landscape that shows both the current state and its direction of travel.

al-dente solves this by treating **data as the product**:
- The OKF bundle is the single source of truth.
- All views, dashboards, graphs, and agent contexts are *representations* derived from that data.
- This makes it trivial to add new ways of seeing the ecosystem at any time.

### Core Principles

- **Data-first (OKF)**: Knowledge lives as plain Markdown files with YAML frontmatter. Git-versioned, diffable, `cat`-able, and directly consumable by agents.
- **GitHub-native**: The repository *is* the knowledge base. Automation, releases, Pages, Projects, and community features are first-class.
- **Dual & Integrated**: MCP Servers and Skills are modeled symmetrically and richly linked.
- **Temporal & Directional**: Snapshots and diffs make change visible — new servers, emerging patterns, shifting concentrations, maturing governance.
- **Multiple Representations**: One OKF source → many views (graph, table, timeline, taxonomy map, dashboard, agent bundle). Easy to extend.
- **Precise (“al dente”)**: High-signal, curated core with clear quality tiers. Not bloated, not overcooked.

### What you can do with al-dente today (and tomorrow)

- Browse or search the current state of MCP servers and skills.
- Explore relationships (which skills are realized by which tools, common compositions, design patterns).
- See evolution over time through snapshots and trend views.
- Feed filtered OKF bundles directly into agents or MCP clients as high-quality context.
- Contribute new servers, skills, or patterns via simple PRs.
- Build new views or analyses on top of the canonical data with minimal effort.

al-dente is both a public good for the agentic community and a practical tool for engineers, researchers, and platform builders who want to understand — and shape — where agentic systems are heading.

**Status**: Early foundation phase. Core OKF modeling and initial MCP server population in progress. Community contributions welcome.

---

*To the tooth.*