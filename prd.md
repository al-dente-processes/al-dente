# PRD: al-dente — Agentic Engineering Register

**Version**: 0.1 (July 2026)  
**Status**: Draft for implementation  
**Owner**: al-dente maintainers

## 1. Problem Statement

The agentic engineering ecosystem is growing explosively but remains fragmented. MCP (Model Context Protocol) servers provide standardized tool access for agents, while skills, capabilities, and design patterns exist across frameworks, taxonomies, and community projects. There is no canonical, living, queryable map that shows:

- The current inventory and capabilities of MCP servers.
- The skills landscape and how skills relate to concrete MCP tools.
- Evolutionary trends, concentrations, gaps, and emerging patterns.

Without this, engineers duplicate effort, agents lack high-quality shared context, and the community lacks visibility into where the field is heading.

## 2. Goals & Success Metrics

**Primary Goal**  
Create a precise, data-first, GitHub-native register of MCP servers and skills as Open Knowledge Format (OKF) bundles, enabling multiple representations and making the status quo + direction of agentic engineering visible.

**Success Metrics (MVP → 6 months)**
- Core OKF bundle covers top 100+ high-signal MCP servers and core skill taxonomy.
- At least 3 distinct live views generated from the same OKF source.
- Automated weekly refresh via GitHub Actions with quality gates.
- Community contributions via PRs (target: 20+ merged in first 3 months).
- Measurable adoption signals (GitHub stars, forks, external references, agent usage of OKF bundles).
- Clear visibility of change (snapshot diffs, trend views) between monthly releases.

## 3. Target Users / Personas

| Persona                  | Needs                                      | How al-dente helps                              |
|--------------------------|--------------------------------------------|-------------------------------------------------|
| Agent Engineer           | Discover tools & skills, understand compositions | Searchable register + graph + composition links |
| Platform / Tool Builder  | See adoption, gaps, design patterns        | Trends, quality tiers, pattern views            |
| Researcher / Analyst     | Track evolution of the field               | Temporal snapshots, directional insights        |
| Community Curator        | Maintain quality & coverage                | Simple contribution workflow, quality framework |
| AI Agent (consumer)      | High-quality, structured context           | Direct OKF bundle ingestion                   |

## 4. Functional Requirements

### 4.1 Data Model (OKF)
- Canonical storage as OKF bundles (Markdown + YAML frontmatter).
- Core entities: `MCP-Server`, `Skill`, `Category`, `Agentic-Pattern`, `Publisher`, `Snapshot`.
- Rich relations (exposes, realizes, belongs_to, commonly_composed_with, evolves_from, etc.).
- Quality tiers and verification signals.
- Temporal snapshots for change tracking.

### 4.2 Discovery & Ingestion
- Automated crawling of Official MCP Registry, major directories (PulseMCP, FindMCP, etc.), GitHub, package registries.
- Support for both MCP servers and skills sources (taxonomies, skill registries, MCP tool → skill mappings).
- Deduplication and normalization.

### 4.3 Enrichment
- LLM-assisted + rule-based categorization, capability extraction, relation inference, and pattern detection.
- Quality scoring and verification flagging.

### 4.4 Views & Representations (all generated from OKF)
- Interactive knowledge graph (nodes = entities, edges = relations).
- Searchable/filterable register (table + detail pages).
- Timeline & diff viewer (changes between snapshots).
- Skills taxonomy map with links to realizing MCP tools.
- Dashboard with stats, trends, and directional insights.
- Agent-ready filtered bundles.
- Easy extensibility: new view = new generator script reading the OKF source.

### 4.5 Automation & GitHub Integration
- Scheduled GitHub Actions for crawl → enrich → OKF update → commit.
- Release process that versions OKF snapshots + publishes rich changelogs.
- GitHub Pages hosting of all views.
- Contribution workflow via Issues + PRs with clear guidelines.

### 4.6 Governance
- Quality tiers (Official/Reference, Verified, Community, Experimental).
- Curation guidelines and review process.
- Clear licensing and contribution license (MIT or similar).

## 5. Non-Functional Requirements

- **Precision & Signal**: High-signal core; avoid noise. Curated over exhaustive.
- **Extensibility**: Adding new views or entity types should require minimal changes to the data model.
- **Performance**: Views should load quickly; heavy computation happens in pipeline, not at render time.
- **Portability**: OKF bundles must be usable outside the project (standalone, in other tools, by agents).
- **Maintainability**: GitHub-native; low operational overhead.
- **Accessibility & Openness**: Fully public, community-driven.

## 6. Scope

**MVP (Phase 1–2)**
- OKF modeling for MCP-Server + Skill + supporting entities.
- Automated pipeline for MCP servers (top sources).
- Initial Skills integration (core taxonomy + key mappings).
- 3 core views: Graph, Register, Dashboard.
- Basic snapshot & diff capability.
- GitHub Actions automation + Pages deployment.

**Out of Scope (MVP)**
- Full enterprise governance features.
- Real-time streaming updates.
- Paid hosting or proprietary data.
- Exhaustive coverage of every obscure server/skill.

**Future Phases**
- Advanced temporal analytics and predictive signals.
- Rich agent consumption examples and MCP server for al-dente itself.
- Community-driven skill certification or verification layers.
- Additional specialized views (e.g., security/governance lens, multi-agent composition explorer).

## 7. Risks & Mitigations

| Risk                        | Mitigation                                      |
|-----------------------------|-------------------------------------------------|
| Data quality / noise        | Strong quality tiers + human curation layer     |
| Scope creep                 | Strict phased roadmap + “al dente” precision principle |
| Community adoption          | Excellent documentation, simple contribution flow, visible value |
| Technical debt in pipeline  | Clean modular design, preference for file-based OKF |

## 8. Success Definition

al-dente becomes the default reference point the community turns to when asking “What MCP servers and skills exist, how do they relate, and where is the field going?” — and it does so through clean, precise, extensible OKF data rather than any single UI.

---

*This PRD will be updated as the project evolves. Feedback welcome via GitHub Discussions or Issues.*