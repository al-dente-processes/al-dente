# al-dente Roadmap

**Version**: 0.1 (July 2026)  
**Principle**: Precise, phased delivery. We ship high-signal increments that demonstrate the power of OKF data + multiple representations. “Al dente” means we resist scope creep and over-engineering.

## Guiding Themes

- **Data is the product** — OKF is canonical.
- **Multiple representations** — Views are projections, easy to add.
- **Temporal visibility** — Change and direction are first-class.
- **Community & GitHub-native** — Low friction contribution and maintenance.
- **Dual focus** — MCP Servers and Skills developed in parallel and richly linked.

## Phase 0: Foundation (July – August 2026)

**Goal**: Establish the OKF data model, basic automation, and proof-of-concept views.

**Key Deliverables**
- Repository structure and initial OKF schema (`ontology/`)
- Core entities modeled: `MCP-Server`, `Skill`, `Category`, `Publisher`, `Agentic-Pattern`
- Sample OKF files for 10–20 high-signal MCP servers + core skill taxonomy entries
- Basic OKF builder script (Python)
- One interactive view (simple force-directed graph or searchable table) served via GitHub Pages
- Initial GitHub Action skeleton (manual trigger)
- README, Project Description, PRD, Design System, and this Roadmap published
- GitHub Projects board created with columns for each phase

**Success Criteria**
- Anyone can clone the repo and see meaningful OKF data + at least one rendered view.
- Contribution guide exists and is clear.

## Phase 1: MCP Servers Core (August – September 2026)

**Goal**: Robust, automated MCP server discovery, enrichment, and multiple high-quality views.

**Key Deliverables**
- Full discovery pipeline (Official MCP Registry + PulseMCP + FindMCP + GitHub + npm)
- Enrichment layer (categorization, capability extraction, quality signals)
- OKF generation for hundreds of servers with rich metadata and relations
- Three core live views on GitHub Pages:
  - Interactive Knowledge Graph
  - Searchable Register + Detail
  - Dashboard (stats + top entities)
- Basic snapshot system (monthly OKF bundle snapshots committed)
- Weekly automated GitHub Action with quality gates
- Quality tier framework (Official/Reference, Verified, Community, Experimental) implemented

**Success Criteria**
- Top 100+ high-signal MCP servers represented with good coverage.
- Views are useful and performant.
- First community PRs merged.

## Phase 2: Skills Integration & Linking (September – October 2026)

**Goal**: Symmetric Skills side + rich connections between servers and skills.

**Key Deliverables**
- Skills discovery sources integrated (taxonomies such as os-taxonomy, Open Ontologies, skill search servers, MCP tool → skill mappings)
- OKF modeling and population for Skills entities and taxonomies
- Cross-linking: `realizes` / `realized_by` relations between Skills and MCP tools/servers
- Skills Taxonomy Map view (hierarchical + links to realizing servers)
- Enhanced Graph view showing both sides together
- Updated Dashboard with skills coverage and emerging skill patterns
- Refined snapshot + basic diff viewer between snapshots

**Success Criteria**
- Core skill taxonomy + key mappings to MCP servers exist.
- Users can explore “which skills are enabled by which tools” fluidly.
- Clear value in the integrated view.

## Phase 3: Temporal Intelligence & Advanced Views (October – December 2026)

**Goal**: Make change and direction visible and actionable.

**Key Deliverables**
- Robust snapshot & diff engine (rich changelogs on release)
- Timeline / Change View showing evolution between snapshots
- “What’s New”, “Rising Patterns”, and “Directional Insights” components in Dashboard
- Additional specialized views (at least one community-proposed)
- Agent consumption examples (how to load filtered al-dente OKF bundles into Claude, Cursor, or custom agents)
- Improved contribution workflow (preview of how a new entity will appear in multiple views)

**Success Criteria**
- Temporal views clearly communicate the evolution of the ecosystem.
- Community starts using snapshots for analysis or agent context.

## Phase 4: Community, Polish & Extensibility (Q1 2027 onward)

**Goal**: Make al-dente a self-sustaining, community-driven public good that is trivially extensible.

**Key Deliverables**
- Mature governance model and curation processes
- al-dente MCP server (so agents can query the register itself via MCP)
- Expanded set of high-quality views (security/governance lens, multi-agent composition explorer, etc.)
- Strong documentation, examples, and onboarding
- Potential integration or federation with other agentic knowledge efforts
- Regular release cadence with rich narrative changelogs

**Success Criteria**
- Healthy flow of community contributions and discussions.
- External projects and agents reference or consume al-dente data.
- New views can be added by contributors with low friction.

## Long-term Vision (2027+)

- al-dente becomes a foundational reference layer for agentic engineering.
- Rich ecosystem of derived tools, analyses, and agent behaviors built on the OKF data.
- Clear signals about the maturation of MCP, skill standardization, governance patterns, and multi-agent architectures.
- Sustainable maintenance through a combination of automation, community curation, and light institutional support if needed.

## How We Prioritize

1. **Signal over volume** — High-quality core first.
2. **Data before views** — New views only after the OKF modeling supports them cleanly.
3. **Automation & maintainability** — Everything that can be automated should be.
4. **Community feedback loops** — Early and continuous input shapes direction.
5. **“Al dente” discipline** — We ship when it’s precise and valuable, not when it’s complete.

---

**This roadmap is a living document.** It will be updated in GitHub as we learn. Major shifts will be discussed in GitHub Discussions before implementation.

*To the tooth.*