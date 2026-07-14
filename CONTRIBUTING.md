# Contributing to al-dente

Welcome. If you're here, you probably care about making the agentic engineering ecosystem more visible, more connected, and more useful. So do we.

al-dente is designed to be easy to contribute to. The entire knowledge base is plain Markdown + YAML. If you can write a README, you can contribute to this register. No complex build tools, no proprietary formats, no contribution agreements to sign.

---

## Ways to Contribute

There's more than one way to help, and all of them matter:

| Contribution | What it looks like | Skill level |
|-------------|-------------------|-------------|
| **Add an MCP server** | Create a new `.md` file in `data/mcp-servers/` | Beginner-friendly |
| **Add a skill** | Create a new `.md` file in `data/skills/` | Beginner-friendly |
| **Improve categories** | Add or refine entries in `data/categories/` | Beginner-friendly |
| **Add a pattern** | Document recurring agentic design patterns | Intermediate |
| **Improve views** | Enhance the graph, register, or dashboard | Web dev (JS/HTML) |
| **Pipeline work** | Discovery, enrichment, or automation scripts | Python/TS |
| **Fix bugs** | Open an issue or PR with a fix | Any level |
| **Suggest features** | Open a Discussion with your idea | Any level |
| **Review PRs** | Help review data contributions | Domain knowledge |

Not sure where to start? Check the [Issues](https://github.com/al-dente-dev/al-dente/issues) for `good first issue` labels, or open a [Discussion](https://github.com/al-dente-dev/al-dente/discussions) and say hello.

---

## OKF Data Contribution Workflow

The most common contribution: adding a new MCP server, skill, or category. Here's the exact process.

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR_USERNAME/al-dente.git
cd al-dente
```

### 2. Create Your Entry

Add a new `.md` file in the appropriate `data/` subdirectory. The filename should be a stable kebab-case ID (e.g., `filesystem-mcp-server.md`, `code-refactoring-skill.md`).

### 3. Write YAML Frontmatter + Markdown

Every OKF file starts with YAML frontmatter between `---` lines, followed by Markdown content. Here's the template for each entity type:

#### MCP Server

```markdown
---
type: MCP-Server
name: Filesystem MCP Server
publisher: modelcontextprotocol
transport: stdio
install: npx -y @modelcontextprotocol/server-filesystem /path/to/directory
capabilities:
  tools:
    - read_file
    - write_file
    - list_directory
    - search_files
categories:
  - filesystem
  - core-tooling
quality_tier: Official
stars: 1200
last_updated: 2026-07-10
verified: true
---

# Filesystem MCP Server

The official MCP server for filesystem operations. Provides safe, scoped
read/write access to a designated directory tree.

## Key Features

- Read, write, and list files within an allowed directory
- Full-text search across files
- Designed for integration with coding agents and IDEs

## Security Notes

The server respects OS-level permissions and requires explicit directory
scoping at startup.
```

**Required fields for MCP-Server**: `type`, `name`, `publisher`, `transport`, `capabilities`
**Recommended fields**: `install`, `categories`, `quality_tier`, `stars`, `last_updated`

#### Skill

```markdown
---
type: Skill
name: Code Refactoring
taxonomy: al-dente-core
level: 3
parent: software-engineering
realized_by:
  - github-mcp-server
  - codebase-analysis-tool
categories:
  - development
---

# Code Refactoring

The ability to restructure existing code without changing its external
behavior. Includes renaming, extracting functions, simplifying conditionals,
and reorganizing modules.

## Common Techniques

- Extract Method / Function
- Rename Variable
- Inline Temp
- Move Method
- Replace Conditional with Polymorphism
```

**Required fields for Skill**: `type`, `name`, `taxonomy`, `level`
**Recommended fields**: `parent`, `realized_by`, `categories`

#### Category

```markdown
---
type: Category
name: Data Access
parent: infrastructure
---

# Data Access

MCP servers and skills related to reading, writing, and querying data
stores including databases, APIs, file systems, and cloud storage.
```

**Required fields for Category**: `type`, `name`
**Recommended fields**: `parent`, `description`

### 4. Validate Your Changes

```bash
# Install dependencies (first time only)
make install

# Build and validate OKF bundle
make build
```

If `make build` succeeds, your YAML is valid and the entry compiles correctly. If it fails, the error message will tell you what's wrong (missing required field, schema violation, etc.). Fix and repeat.

### 5. Preview Locally

```bash
# Serve views locally to see how your entry renders
make serve
```

Open the local URL (typically `http://localhost:8000`) and check:
- Does your entry appear in the register?
- Does the graph show it correctly (if applicable)?
- Is the detail page rendering properly?

### 6. Submit a Pull Request

```bash
git checkout -b add-my-new-server
git add data/mcp-servers/my-new-server.md
git commit -m "data: add My New Server MCP server"
git push origin add-my-new-server
```

Then open a PR on GitHub. The PR template will guide you through the checklist. Include:
- What you added and why
- Source URL for verification
- Any notable capabilities or relationships

---

## Quality Guidelines

What makes a good contribution:

- **Accurate**: The information is correct and verifiable from the source.
- **Complete**: Required YAML fields are present. Markdown description is substantive (not just a one-liner).
- **Linked**: Cross-reference related entities where possible (skills realized, categories, related servers).
- **Sourced**: Include the GitHub/source URL so others can verify.
- **Fresh**: `last_updated` reflects when you checked. Don't copy stale data.
- **Signal over noise**: We prefer a smaller, high-quality register over an exhaustive dump. If a server is experimental, unmaintained, or has zero usage signals, it may not meet the bar yet.

### Quality Tiers

| Tier | Criteria |
|------|----------|
| **Official / Reference** | Published by the protocol owner (e.g., Model Context Protocol official servers) |
| **Verified** | Reviewed by al-dente maintainers, has clear usage signals |
| **Community** | Community-submitted, passes automated checks |
| **Experimental** | Early-stage, interesting but unproven — flagged as such |

Most new contributions start at **Community** tier and can be promoted based on signals and review.

---

## Code Contribution Guidelines

For contributions to the pipeline, views, or automation:

- **Python** for pipeline scripts (3.11+). Keep it simple, readable, well-typed.
- **Vanilla JS** for views. No frameworks unless there's a compelling reason.
- **Tests**: If you're adding pipeline logic, add a test. If you're modifying the schema, validate against existing data.
- **Documentation**: Update relevant docs if your change affects the contribution workflow or data model.
- **One concern per PR**: Don't mix a data addition with a pipeline refactor. Separate PRs move faster.

---

## Review Process

- Automated checks run on every PR (schema validation, build success, link checking).
- A maintainer will review within a few days.
- Data PRs are usually straightforward — if the build passes and the entry looks correct, we'll merge quickly.
- Code PRs may need a round or two of feedback. That's normal and healthy.

---

## Code of Conduct

Be precise. Be generous. Be respectful. This is a shared resource for the entire agentic engineering community. Assume good intent, give constructive feedback, and help newcomers learn.

We follow the [Contributor Covenant](https://www.contributor-covenant.org/) Code of Conduct. Report concerns to the maintainers privately.

---

## Questions?

- **Quick question or idea?** → [GitHub Discussions](https://github.com/al-dente-dev/al-dente/discussions)
- **Found a bug?** → [Open an Issue](https://github.com/al-dente-dev/al-dente/issues/new/choose)
- **Want to chat?** → Say hi in Discussions. We're friendly.

---

*To the tooth.*
