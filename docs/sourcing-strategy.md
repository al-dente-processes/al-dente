# al-dente Sourcing Strategy

**Version**: 0.1 (July 2026)  
**Status**: Research complete — ready for pipeline implementation

---

## The Landscape at a Glance

| Source | Servers | API Access | Curation | Signal for al-dente |
|--------|---------|------------|----------|---------------------|
| **Official MCP Registry** | ~500+ published | REST API, open | Namespace-verified only | **Primary source** — canonical |
| **PulseMCP** | 22,305 | Sub-Registry API (key auth) | official/reference/community tags | **High** — popularity + classification |
| **Glama** | 14,000+ | TBD | Security scorecards, vuln scans, license checks | **High** — quality signals |
| **MCP.so** | ~20,000 | Submit via GitHub issues | Community-driven | Medium |
| **Smithery** | 100,000+ tools | REST API (Bearer token) | Marketplace approach | Medium — volume, not curation |
| **GitHub Topics** | Thousands | GitHub Search API | None (raw) | Medium — discovery of unlisted |
| **Awesome Lists** | Hundreds | Static markdown | Community curated | Low-Medium — good for cross-check |
| **NPM Registry** | Thousands | NPM registry API | None | Low-Medium — install counts |

---

## Tier 1: Canonical Sources (Implement First)

### 1. Official MCP Registry

The community-run canonical registry. Every server published here has a reverse-DNS namespace and verified ownership. This is the source that feeds downstream directories.

- **Endpoint**: `https://registry.modelcontextprotocol.io/v0/servers`
- **Pagination**: cursor-based (`?limit=100&offset=N`)
- **Schema**: `server.json` with name, description, repository, packages (install), remotes, version
- **Fields we care about**:
  - `server.name` — reverse-DNS identifier (e.g. `io.github.modelcontextprotocol/filesystem`)
  - `server.description` — human description
  - `server.repository.url` — GitHub/source URL
  - `server.packages[]` — install method, transport (stdio/sse/http), runtime hint (npx/pip/docker)
  - `server.remotes[]` — remote endpoint URLs
  - `server.version` — version string
  - `_meta.{...}/official.status` — active/inactive
  - `_meta.{...}/official.publishedAt` — first seen
  - `_meta.{...}/official.updatedAt` — last update
- **Quality mapping**: Any server in the official registry → at least **Community** tier. Official/reference namespace → **Official** tier.
- **Pipeline action**: Primary crawl target. Full dump weekly.

**Sample call**:
```bash
curl "https://registry.modelcontextprotocol.io/v0/servers?limit=100"
```

### 2. PulseMCP Sub-Registry API

PulseMCP aggregates the official registry + community submissions. Their API returns the official server.json PLUS PulseMCP enrichment: visitor estimates, official/reference/community classification, and popularity rankings.

- **Endpoint**: `https://api.pulsemcp.com/v0.1/servers`
- **Auth**: `X-API-Key` header (free tier available)
- **Docs**: `https://www.pulsemcp.com/api/docs/v0.1`
- **PulseMCP-specific fields**:
  - `_meta.com.pulsemcp/server.visitorsEstimateMostRecentWeek` — weekly traffic
  - `_meta.com.pulsemcp/server.visitorsEstimateTotal` — cumulative traffic
  - `_meta.com.pulsemcp/server.isOfficial` — boolean
  - `_meta.com.pulsemcp/server.classification` — official / reference / community
- **Quality mapping**: `isOfficial=true` or classification=official/reference → **Official** tier. High visitor count → signals for **Verified** tier.
- **Pipeline action**: Cross-reference with official registry. Enrich OKF entries with popularity signals.

**Sample call**:
```bash
curl -H "X-API-Key: YOUR_KEY" "https://api.pulsemcp.com/v0.1/servers?limit=100"
```

### 3. Glama

Glama runs the strongest curation in the ecosystem: automated security scans, license verification, README quality checks, vulnerability detection. They publish a scorecard per server.

- **Endpoint**: Web interface at `https://glama.ai` — API access TBD
- **Fields they expose on web**:
  - Security score (vulnerability scan results)
  - License verification (is it valid?)
  - Quality score (README, docs, tests)
  - Maintainer verification (GitHub login verified)
  - Tier: Official / Claimed / Crawled
- **Quality mapping**: Glama-verified maintainer + security pass → **Verified** tier. Official tier → **Official**.
- **Pipeline action**: Manual or scraper-based enrichment for security/quality signals. Contact Glama for API access.

---

## Tier 2: Discovery Sources (Implement Second)

### 4. GitHub Topic Search

Finds MCP servers that exist on GitHub but haven't been published to the official registry yet.

- **Endpoint**: `https://api.github.com/search/repositories`
- **Query**: `topic:mcp-server` or `topic:model-context-protocol` or `mcp-server in:name,description`
- **Fields**: stars, updated_at, language, topics, description, full_name
- **Pipeline action**: Discovery pass. Cross-check against official registry. New repos not in registry → **Experimental** tier candidates.

**Sample call**:
```bash
curl -H "Authorization: token GITHUB_TOKEN" \
  "https://api.github.com/search/repositories?q=topic:mcp-server&sort=stars&order=desc&per_page=100"
```

### 5. Smithery Registry API

Smithery focuses on agent-tool connection. Large catalog, lighter curation.

- **Endpoint**: `https://api.smithery.ai/servers`
- **Auth**: `Authorization: Bearer <token>` (free API keys at smithery.ai/account/api-keys)
- **Fields**: qualifiedName, namespace, displayName, description, verified, useCount, score, remote, isDeployed
- **Pipeline action**: Cross-reference for popularity (`useCount`) and verification signals. Discover servers not in official registry.

**Sample call**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.smithery.ai/servers?page=1&pageSize=100"
```

### 6. NPM Registry Search

Many MCP servers are distributed as npm packages. Good for install-method data and version tracking.

- **Endpoint**: `https://registry.npmjs.org/-/v1/search`
- **Query**: `text=mcp-server&size=250`
- **Fields**: package.name, package.description, package.version, package.links, download count (from separate API)
- **Pipeline action**: Enrich OKF entries with npm package data. Correlate with `packages[]` from official registry.

**Sample call**:
```bash
curl "https://registry.npmjs.org/-/v1/search?text=mcp-server&size=250"
```

---

## Tier 3: Cross-Reference Sources (Implement Third)

### 7. Awesome MCP Servers Lists

Static curated lists. Good for discovering hidden gems not yet in registries.

- **wong2/awesome-mcp-servers** — `https://github.com/wong2/awesome-mcp-servers` (50k+ stars)
- **punkpeye/awesome-mcp-servers** — `https://github.com/punkpeye/awesome-mcp-servers`
- **apappascs/mcp-servers-hub** — `https://github.com/apappascs/mcp-servers-hub`
- **Pipeline action**: Parse markdown lists. Cross-reference with registry. Any server in multiple awesome lists → signal for higher tier.

### 8. Official Reference Implementations

The `modelcontextprotocol/servers` repo houses the canonical reference servers. Small but highest signal.

- **Repo**: `https://github.com/modelcontextprotocol/servers`
- **Current reference servers** (in `src/`): everything, fetch, filesystem, git, memory, sequentialthinking, time
- **Pipeline action**: Hardcode as **Official** tier. Source of truth for Anthropic-maintained servers.

---

## Proposed Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEEKLY DISCOVERY PIPELINE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ OFFICIAL REGISTRY │  │ PULSE MCP API    │  │ GLAMA        │  │
│  │ Full crawl        │  │ Enrichment pass  │  │ Scorecards   │  │
│  └────────┬─────────┘  └────────┬─────────┘  └──────┬───────┘  │
│           │                      │                     │          │
│           └──────────┬───────────┘─────────────────────┘          │
│                      ▼                                           │
│           ┌────────────────────┐                                │
│           │ MERGE & DEDUPE     │  by reverse-DNS name           │
│           └────────┬───────────┘                                │
│                    ▼                                             │
│           ┌────────────────────┐                                │
│           │ GITHUB TOPIC SEARCH │  discover new/unlisted         │
│           │ NPM SEARCH          │  enrich install data           │
│           │ SMITHERY API        │  cross-ref use counts          │
│           └────────┬───────────┘                                │
│                    ▼                                             │
│           ┌────────────────────┐                                │
│           │ QUALITY TIERING     │  Official → Verified →         │
│           │  - Registry presence │    Community → Experimental    │
│           │  - PulseMCP class    │                                │
│           │  - Glama scores      │                                │
│           │  - GitHub stars      │                                │
│           │  - Security signals  │                                │
│           └────────┬───────────┘                                │
│                    ▼                                             │
│           ┌────────────────────┐                                │
│           │ GENERATE OKF FILES │  Create/update .md files       │
│           │ in data/mcp-servers/ │                                │
│           └────────┬───────────┘                                │
│                    ▼                                             │
│           ┌────────────────────┐                                │
│           │ BUILD & VALIDATE   │  build_okf.py                  │
│           │ GENERATE VIEWS     │  generate_views.py             │
│           │ COMMIT & DEPLOY    │  GitHub Actions → Pages        │
│           └────────────────────┘                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tier Mapping Logic

| Tier | Criteria |
|------|----------|
| **Official** | Listed in official MCP Registry with verified namespace. OR maintained by Anthropic/modelcontextprotocol org. OR classification=official/reference on PulseMCP. |
| **Verified** | Registry-published + Glama security pass + README quality check. OR PulseMCP isOfficial=true with high traffic (>10k weekly visitors). OR GitHub-verified maintainer + 500+ stars. |
| **Community** | Listed in official registry (unverified namespace). OR found on PulseMCP with community classification. OR 100+ GitHub stars + active in last 6 months. |
| **Experimental** | Found via GitHub topic search or awesome lists. OR listed on Smithery/MCP.so but not in official registry. No quality verification. |

---

## Immediate Next Steps

1. **Implement Official Registry crawler** — `pipeline/discover/mcp_registry.py`
   - Paginated crawl of `registry.modelcontextprotocol.io/v0/servers`
   - Store raw JSON in `pipeline/.cache/mcp_registry/`
   - Generate OKF `.md` files for any server not yet in `data/mcp-servers/`

2. **Get PulseMCP API key** — Sign up at pulsemcp.com, get `X-API-Key`
   - Implement `pipeline/discover/pulsemcp.py`
   - Cross-reference with official registry data
   - Add visitor estimates and classification to OKF enrichment

3. **Implement GitHub topic search** — `pipeline/discover/github_topics.py`
   - Search `topic:mcp-server` sorted by stars
   - Filter out repos already in official registry
   - Flag as **Experimental** tier candidates

4. **Tier all existing 15 servers** using the mapping above
   - Currently all marked "Official" — verify against actual registry data
   - Some may be Community tier (redis, time, etc.)

---

*Sources verified July 2026. Endpoints and schemas subject to change — pipeline should handle schema drift gracefully.*
