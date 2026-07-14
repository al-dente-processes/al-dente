# al-dente Design System

**Version**: 0.1  
**Philosophy**: Precise. Clean. “To the tooth.” Elegant minimalism inspired by Italian design — firm structure, excellent materials, nothing superfluous.

The design system governs both the visual language of al-dente and, more importantly, the **multiple representations of OKF data**.

## 1. Brand & Tone

- **Name meaning**: “Al dente” = cooked firm to the bite. Precise, not overdone. High-signal data and interfaces.
- **Voice**: Clear, confident, generous, slightly playful but never cute. Technical without being dry.
- **Values**: Precision • Openness • Extensibility • Community • Temporal awareness (change is visible and valuable).

## 2. Visual Language

### Typography
- Primary: Inter or system sans-serif (clean, highly legible).
- Headings: Slightly tighter tracking, medium weight.
- Code/Markdown: Monospace (Fira Code or system mono) with subtle syntax highlighting.

### Color
- **Primary**: Deep charcoal / near-black (#111111) for text and structure.
- **Accent**: Warm terracotta / muted orange-red (#C45C3B) — subtle Italian reference, used sparingly for highlights, links, and active states.
- **Secondary**: Soft warm gray (#F5F2ED) for backgrounds and cards.
- **Semantic**:
  - Verified / High quality: Subtle green accent.
  - Experimental: Muted purple.
  - Change / New: Terracotta highlight.

### Spacing & Layout
- Generous but disciplined whitespace (8px base grid).
- Cards with subtle elevation or clean borders.
- Maximum content width: ~1200px for readability.
- Responsive: Excellent on desktop; graceful on tablet; functional on mobile.

### Iconography
- Minimal line icons (Heroicons or custom).
- Graph nodes use simple geometric shapes with subtle color coding by entity type.

## 3. OKF Representation Styles

This is the heart of the design system. Because **data lives in OKF** and **UIs are projections**, we define canonical styles for rendering the same underlying OKF bundle.

### Style 1: Raw / Canonical OKF
- Direct rendering of the Markdown + YAML files (GitHub’s native view is already excellent).
- Used for: Deep inspection, agent ingestion, contribution editing.
- Characteristics: Full YAML frontmatter visible (collapsible), Markdown rendered cleanly, links between files are live.

### Style 2: Interactive Knowledge Graph
- Nodes = OKF entities (MCP-Server, Skill, Category, Pattern, Publisher).
- Edges = Relations (exposes, realizes, belongs_to, commonly_composed_with, etc.).
- Interactions: Zoom, pan, search/filter, click for detail panel, highlight neighborhoods.
- Layouts: Force-directed (default), hierarchical (for taxonomies), radial (for hub-and-spoke patterns).
- Color coding: By entity type + quality tier.
- Example use: “Show me the cluster around coding agents and which skills they commonly realize.”

### Style 3: Tabular Register + Detail
- Clean, searchable, filterable data table.
- Columns: Name, Type, Publisher, Quality Tier, Last Updated, Key Capabilities / Skills, Popularity signals.
- Clicking a row opens a rich detail view (all YAML properties + related entities + Markdown description).
- Powerful filters: Category, Transport (for servers), Quality Tier, Recently Updated, etc.
- Export options: CSV, filtered OKF sub-bundle.

### Style 4: Timeline & Change View
- Horizontal or vertical timeline of snapshots.
- Diff highlighting between selected snapshots (new entities, changed relations, popularity shifts, emerging patterns).
- “What’s new this month” and “Rising patterns” callouts.
- Git history integration for fine-grained changes.

### Style 5: Skills Taxonomy Map
- Hierarchical or radial tree/map view focused on the Skills side.
- Nodes sized by adoption signals or centrality.
- Edges or overlays show which MCP servers/tools realize each skill.
- Drill-down from broad categories → specific skills → concrete implementations.

### Style 6: Dashboard / Overview
- At-a-glance cards: Total Servers, Total Skills, Growth this period, Top Categories, Emerging Patterns.
- Small multiples / sparklines for trends.
- Featured “Spotlight” entities (new high-quality additions, interesting compositions).
- Directional insight callouts (curated or semi-automated).

### Style 7: Agent-Ready Bundle
- Clean, filtered OKF output (subset of files or condensed context).
- Optimized for direct ingestion into Claude, Cursor, custom agents, etc.
- Includes progressive disclosure via `index.md` files.
- Can be served as a static bundle or dynamically generated.

### Style 8: Specialized / Future Views (examples)
- Security & Governance lens (auth patterns, verified status, risk signals).
- Multi-agent Composition Explorer.
- Geographic or organizational adoption map (if data available).
- Comparison view (side-by-side two snapshots or two categories).

**Rule for new views**: Any new representation must be generated from the canonical OKF source with minimal or no duplication of data. The generator script lives in `pipeline/views/`.

## 4. Component Guidelines (for view builders)

- **Entity Card**: Consistent card used across graph tooltips, register rows, and dashboards. Shows: Name + Type badge + Quality tier + Key signals + Short description.
- **Relation Chip**: Small pill showing relation type (e.g., “realizes 12 skills”, “commonly composed with Filesystem”).
- **Quality Badge**: Clear visual indicator (Verified, Community, Experimental) with tooltip explaining criteria.
- **Snapshot Badge**: “As of July 2026” or “Snapshot v0.3”.
- **Progressive Disclosure**: Use `index.md` files and collapsible sections so agents/humans can load context at the right granularity.

## 5. Contribution & Curation UI Notes

When community members propose new entities via PR:
- Preview should show how the new Markdown will render in the main Register and Graph views.
- Automated checks for required YAML fields and basic quality signals.

## 6. Accessibility & Performance

- All views must meet WCAG 2.1 AA.
- Graph views should offer keyboard navigation and text alternatives.
- Heavy visualization computation happens at build time or in Web Workers; pages remain fast.

---

**Living Document**: This design system will evolve as we learn what representations are most valuable to the community. New styles are welcomed via proposal in Discussions.