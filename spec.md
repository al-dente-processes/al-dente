# al-dente — Summarizing Specification

**Version**: 0.1 (July 2026)  
**Type**: High-level technical & data specification

## 1. Purpose

al-dente provides a canonical, versionable, Open Knowledge Format (OKF) representation of the agentic engineering ecosystem, with a focus on MCP Servers and Skills. It enables multiple derived representations (views) while keeping the underlying data as the single source of truth. The project is fully GitHub-native and community-oriented.

## 2. Core Concepts

### 2.1 Open Knowledge Format (OKF)
- al-dente uses Google’s Open Knowledge Format (v0.1+) as the foundational storage model.
- Knowledge is expressed as a directory of Markdown files with YAML frontmatter.
- One concept = one file.
- Directory hierarchy + Markdown links create a navigable graph.
- Required frontmatter field: `type`.
- Human-readable, agent-ingestible, Git-diffable, and portable.

### 2.2 Primary Entity Types

| Type              | Description                                      | Key Properties (YAML)                          | Example Relations                     |
|-------------------|--------------------------------------------------|------------------------------------------------|---------------------------------------|
| `MCP-Server`      | Implementation of the Model Context Protocol     | name, publisher, transport, install, capabilities (tools/resources/prompts), stars, last_updated, verified, categories | exposes, belongs_to, commonly_composed_with, realizes_skills |
| `Skill`           | Agent capability or taxonomy entry               | name, taxonomy, level, description, realized_by_mcp_tools | realized_by, belongs_to, related_to   |
| `Category`        | Hierarchical classification                      | name, parent, description                      | contains, parent_of                   |
| `Agentic-Pattern` | Recurring design or architectural pattern        | name, description, examples                    | exemplified_by, related_to            |
| `Publisher`       | Organization or maintainer                       | name, type (official/community), links         | publishes, maintains                  |
| `Snapshot`        | Point-in-time capture of the OKF bundle          | timestamp, version, summary_of_changes         | captures_state_of                     |

### 2.3 Relations (expressed in YAML + Markdown links)
- `exposes` / `realizes`
- `belongs_to` / `contains`
- `commonly_composed_with`
- `realized_by` / `realizes_skills`
- `maintained_by` / `publishes`
- `evolves_from` / `related_to`
- Temporal: links to `Snapshot` entities

## 3. Data Architecture

### 3.1 Canonical Storage
- Location: `/data/` in the repository (or root for simplicity in early phases).
- Structure:
  ```
  data/
  ├── mcp-servers/
  ├── skills/
  ├── categories/
  ├── patterns/
  ├── publishers/
  ├── snapshots/
  └── index.md
  ```
- Each entity is a `.md` file named by a stable ID (e.g., `github-mcp-server.md` or `io.github.modelcontextprotocol/server-github.md`).
- `index.md` files provide progressive disclosure and navigation.

### 3.2 Pipeline (Automation)
1. **Discover**: Crawl Official MCP Registry API, directories, GitHub, package ecosystems, skill taxonomies.
2. **Enrich**: Normalize, categorize, extract capabilities, infer relations, apply quality signals (rules + LLM-assisted).
3. **Build OKF**: Generate or update Markdown + YAML files according to the schema.
4. **Snapshot & Diff**: Create timestamped snapshots; compute meaningful diffs.
5. **Generate Views**: Run view generators that read the OKF source and produce HTML/JS visualizations.
6. **Commit & Release**: Automated commit (with conventional commits) → trigger Pages deploy and create Release with rich changelog.

All steps are implemented as modular scripts in `/pipeline/`.

### 3.3 Views as Projections
- Views **never** duplicate canonical data.
- Each view is a generator script (Python, TypeScript, etc.) that consumes the OKF directory.
- Current planned views (see Design System for details):
  - Interactive Knowledge Graph
  - Searchable Register + Detail
  - Dashboard
  - Skills Taxonomy Map
  - Timeline / Diff Viewer
  - Agent-Ready Bundles

New views can be added by contributing a new generator in `pipeline/views/`.

## 4. Quality & Governance

- **Tiers**:
  - Official / Reference
  - Verified (reviewed)
  - Community (community-submitted, auto-checked)
  - Experimental
- Curation happens via GitHub PRs with preview of impact on views.
- Automated quality gates in the pipeline (required fields, basic consistency checks).
- Human review layer for high-tier entities.

## 5. Temporal Model

- Monthly (or event-driven) snapshots of the full OKF bundle are committed to `/data/snapshots/`.
- Releases on GitHub tag these snapshots and include narrative changelogs highlighting:
  - New high-signal entities
  - Emerging patterns
  - Shifts in concentration or quality
  - Notable relations or compositions
- Diff views allow comparison between any two snapshots.

## 6. GitHub-Native Implementation

- Repository = living OKF knowledge base + automation code.
- `.github/workflows/`: Scheduled and event-driven Actions for pipeline execution.
- GitHub Pages: Hosts all generated views.
- Releases: Versioned OKF snapshots + changelogs.
- GitHub Projects: Roadmap and task tracking.
- Issues + Discussions: Community input and curation.
- Pull Requests: Primary contribution mechanism (with preview of OKF impact).

## 7. Extensibility Principles

- **Data model first**: Changes to entities or relations are made in the OKF schema before views are updated.
- **Generator pattern**: New representations are added as independent generators.
- **Minimal core**: Keep the OKF schema and pipeline lean; power comes from composition and derived views.
- **Agent-friendly**: OKF bundles (full or filtered) can be used directly as high-quality context for any MCP-compatible agent.

## 8. Non-Goals (for clarity)

- al-dente is **not** a new protocol or runtime.
- It is **not** a centralized database with an API (though projections can expose APIs).
- It does **not** aim for exhaustive coverage of every possible server or skill.
- It prioritizes signal, precision, and extensibility over volume.

## 9. Summary

al-dente delivers a precise, evolving, OKF-based map of MCP servers and skills. By keeping data canonical and views as lightweight projections, it provides lasting value as a reference, analysis tool, and high-quality context source for the agentic engineering community — all while being fully maintainable and extensible within GitHub.

---

**This specification is intentionally high-level.** Detailed schemas, pipeline implementation details, and view generator contracts live in the repository (`ontology/`, `pipeline/`, and individual view documentation) and will evolve with the project.

*To the tooth.*