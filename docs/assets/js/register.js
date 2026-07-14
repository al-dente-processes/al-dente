/**
 * al-dente Register View
 * Searchable, filterable, sortable data table with detail panel.
 * Works with window.OKF_DATA (loaded from data.js).
 */

(function() {
  "use strict";

  // ------------------------------------------------------------------
  // Config
  // ------------------------------------------------------------------
  const DATA = window.OKF_DATA || { entities: {}, byType: {}, metadata: {} };
  const entities = DATA.entities || {};
  const byType = DATA.byType || {};

  const PAGE_SIZE = 20;

  // ------------------------------------------------------------------
  // State
  // ------------------------------------------------------------------
  let state = {
    searchQuery: "",
    activeTier: "all",
    activeType: "all",
    sortColumn: null,
    sortDirection: "asc",
    currentPage: 1,
    selectedEntityId: null
  };

  // Debounce timer for search
  let searchDebounce = null;

  // ------------------------------------------------------------------
  // Utilities
  // ------------------------------------------------------------------

  function esc(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function getTierBadgeClass(tier) {
    switch (tier) {
      case "Official": return "badge--official";
      case "Verified": return "badge--verified";
      case "Community": return "badge--community";
      case "Experimental": return "badge--experimental";
      default: return "";
    }
  }

  function getTypeBadgeClass(type) {
    switch (type) {
      case "MCP-Server": return "badge--type-server";
      case "Skill": return "badge--type-skill";
      case "Category": return "badge--type-category";
      case "Agentic-Pattern": return "badge--type-pattern";
      case "Publisher": return "badge--type-publisher";
      default: return "";
    }
  }

  function formatDate(dateStr) {
    if (!dateStr) return "—";
    try {
      const d = new Date(dateStr);
      return d.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
    } catch {
      return dateStr;
    }
  }

  function countCapabilities(entity) {
    if (!entity.capabilities) return 0;
    return (entity.capabilities.tools || []).length +
           (entity.capabilities.resources || []).length +
           (entity.capabilities.prompts || []).length;
  }

  // ------------------------------------------------------------------
  // Get all entities as array
  // ------------------------------------------------------------------

  function getAllEntities() {
    return Object.values(entities);
  }

  // ------------------------------------------------------------------
  // Filtering
  // ------------------------------------------------------------------

  function matchesSearch(entity, query) {
    if (!query) return true;
    const q = query.toLowerCase();
    const name = (entity.name || "").toLowerCase();
    const desc = (entity.description || "").toLowerCase();
    const pub = (entity.publisher || "").toLowerCase();
    return name.includes(q) || desc.includes(q) || pub.includes(q);
  }

  function matchesTier(entity, tier) {
    if (tier === "all") return true;
    return entity.tier === tier;
  }

  function matchesType(entity, type) {
    if (type === "all") return true;
    return entity.type === type;
  }

  function getFilteredEntities() {
    return getAllEntities()
      .filter(e => matchesSearch(e, state.searchQuery))
      .filter(e => matchesTier(e, state.activeTier))
      .filter(e => matchesType(e, state.activeType));
  }

  // ------------------------------------------------------------------
  // Sorting
  // ------------------------------------------------------------------

  function sortEntities(list) {
    if (!state.sortColumn) return list;

    const dir = state.sortDirection === "asc" ? 1 : -1;

    return [...list].sort((a, b) => {
      let av, bv;

      switch (state.sortColumn) {
        case "name":
          av = (a.name || "").toLowerCase();
          bv = (b.name || "").toLowerCase();
          break;
        case "type":
          av = a.type || "";
          bv = b.type || "";
          break;
        case "publisher":
          av = a.publisher || "";
          bv = b.publisher || "";
          break;
        case "tier":
          av = a.tier || "";
          bv = b.tier || "";
          break;
        case "stars":
          av = a.stars || 0;
          bv = b.stars || 0;
          break;
        case "capabilities":
          av = countCapabilities(a);
          bv = countCapabilities(b);
          break;
        case "last_updated":
          av = a.last_updated || "";
          bv = b.last_updated || "";
          break;
        default:
          return 0;
      }

      if (av < bv) return -1 * dir;
      if (av > bv) return 1 * dir;
      return 0;
    });
  }

  // ------------------------------------------------------------------
  // Table Rendering
  // ------------------------------------------------------------------

  function renderTable() {
    const tbody = document.getElementById("tableBody");
    if (!tbody) return;

    let filtered = getFilteredEntities();
    filtered = sortEntities(filtered);

    const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
    if (state.currentPage > totalPages) state.currentPage = totalPages;
    if (state.currentPage < 1) state.currentPage = 1;

    const start = (state.currentPage - 1) * PAGE_SIZE;
    const pageItems = filtered.slice(start, start + PAGE_SIZE);

    if (pageItems.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="7" style="text-align:center;padding:var(--space-5);">
            <div class="empty-state">
              <div class="empty-state__icon">🔍</div>
              <p class="empty-state__title">No results found</p>
              <p class="empty-state__text">Try adjusting your search or filters.</p>
            </div>
          </td>
        </tr>
      `;
    } else {
      tbody.innerHTML = pageItems.map(entity => {
        const tierClass = getTierBadgeClass(entity.tier);
        const typeClass = getTypeBadgeClass(entity.type);
        const capCount = entity.type === "MCP-Server" ? countCapabilities(entity) : "—";
        const stars = entity.stars ? entity.stars.toLocaleString() : "—";

        // Resolve publisher name
        let pubName = entity.publisher || "—";
        if (entity.publisher && entities[entity.publisher]) {
          pubName = entities[entity.publisher].name || entity.publisher;
        }

        return `
          <tr data-id="${esc(entity.id)}" tabindex="0" role="button" aria-label="View details for ${esc(entity.name)}">
            <td class="table-cell__name">
              <a href="javascript:void(0)" onclick="event.stopPropagation();">${esc(entity.name)}</a>
            </td>
            <td><span class="badge ${typeClass}">${esc(entity.type)}</span></td>
            <td>${esc(pubName)}</td>
            <td>${entity.tier ? `<span class="badge ${tierClass}">${esc(entity.tier)}</span>` : "—"}</td>
            <td>${stars}</td>
            <td>${capCount}</td>
            <td>${formatDate(entity.last_updated)}</td>
          </tr>
        `;
      }).join("");
    }

    // Update sort indicators
    document.querySelectorAll(".data-table th").forEach(th => {
      th.classList.remove("sort-asc", "sort-desc");
      const col = th.getAttribute("data-sort");
      if (col === state.sortColumn) {
        th.classList.add(state.sortDirection === "asc" ? "sort-asc" : "sort-desc");
      }
    });

    renderPagination(filtered.length, totalPages);
  }

  // ------------------------------------------------------------------
  // Pagination
  // ------------------------------------------------------------------

  function renderPagination(totalItems, totalPages) {
    const container = document.getElementById("pagination");
    if (!container) return;

    if (totalPages <= 1) {
      container.innerHTML = `<span class="pagination__info">${totalItems} result${totalItems !== 1 ? "s" : ""}</span>`;
      return;
    }

    let buttons = "";

    // Prev
    buttons += `<button class="pagination__btn" ${state.currentPage === 1 ? "disabled" : ""} data-page="${state.currentPage - 1}">←</button>`;

    // Page numbers (simplified)
    for (let i = 1; i <= totalPages; i++) {
      if (
        i === 1 ||
        i === totalPages ||
        (i >= state.currentPage - 1 && i <= state.currentPage + 1)
      ) {
        buttons += `<button class="pagination__btn ${i === state.currentPage ? "pagination__btn--active" : ""}" data-page="${i}">${i}</button>`;
      } else if (
        i === state.currentPage - 2 ||
        i === state.currentPage + 2
      ) {
        buttons += `<span class="pagination__info">…</span>`;
      }
    }

    // Next
    buttons += `<button class="pagination__btn" ${state.currentPage === totalPages ? "disabled" : ""} data-page="${state.currentPage + 1}">→</button>`;

    container.innerHTML = `
      ${buttons}
      <span class="pagination__info">${state.currentPage} / ${totalPages} · ${totalItems} total</span>
    `;
  }

  // ------------------------------------------------------------------
  // Detail Panel
  // ------------------------------------------------------------------

  function openDetailPanel(entityId) {
    const entity = entities[entityId];
    if (!entity) return;

    state.selectedEntityId = entityId;

    const title = document.getElementById("detailTitle");
    const meta = document.getElementById("detailMeta");
    const content = document.getElementById("detailContent");

    if (title) title.textContent = entity.name || entity.id;

    // Meta badges
    const typeClass = getTypeBadgeClass(entity.type);
    const tierClass = getTierBadgeClass(entity.tier);
    let metaHTML = `<span class="badge ${typeClass}">${esc(entity.type)}</span>`;
    if (entity.tier) metaHTML += ` <span class="badge ${tierClass}">${esc(entity.tier)}</span>`;
    if (meta) meta.innerHTML = metaHTML;

    // Build content sections
    let html = "";

    // Description
    if (entity.description) {
      html += `
        <div class="detail-panel__section">
          <h3 class="detail-panel__section-title">Description</h3>
          <div class="detail-panel__content"><p>${esc(entity.description)}</p></div>
        </div>
      `;
    }

    // Properties
    html += `<div class="detail-panel__section"><h3 class="detail-panel__section-title">Properties</h3><div class="detail-panel__content">`;
    html += `<table style="width:100%;font-size:13px;">`;

    const props = [
      ["ID", entity.id],
      ["Name", entity.name],
      ["Type", entity.type],
      ["Publisher", entity.publisher ? (entities[entity.publisher]?.name || entity.publisher) : "—"],
      ["Transport", entity.transport || "—"],
      ["License", entity.license || "—"],
      ["Tier", entity.tier || "—"],
      ["Stars", entity.stars ? entity.stars.toLocaleString() : "—"],
      ["Verified", entity.verified ? "Yes" : "No"],
      ["Last Updated", formatDate(entity.last_updated)],
      ["Source URL", entity.source_url ? `<a href="${esc(entity.source_url)}" target="_blank" rel="noopener">${esc(entity.source_url)}</a>` : "—"],
      ["Homepage", entity.homepage ? `<a href="${esc(entity.homepage)}" target="_blank" rel="noopener">${esc(entity.homepage)}</a>` : "—"]
    ];

    props.forEach(([label, value]) => {
      html += `<tr><td style="color:var(--color-text-muted);padding:3px 12px 3px 0;white-space:nowrap;vertical-align:top;">${esc(label)}</td><td style="vertical-align:top;">${value}</td></tr>`;
    });

    html += `</table></div></div>`;

    // Capabilities (for servers)
    if (entity.capabilities) {
      const tools = entity.capabilities.tools || [];
      const resources = entity.capabilities.resources || [];
      const prompts = entity.capabilities.prompts || [];

      html += `<div class="detail-panel__section"><h3 class="detail-panel__section-title">Capabilities</h3><div class="detail-panel__content">`;

      if (tools.length > 0) {
        html += `<p><strong>Tools (${tools.length}):</strong></p>`;
        html += `<ul style="margin:4px 0 12px 16px;padding:0;">`;
        tools.forEach(t => { html += `<li><code>${esc(t)}</code></li>`; });
        html += `</ul>`;
      }
      if (resources.length > 0) {
        html += `<p><strong>Resources (${resources.length}):</strong></p>`;
        html += `<ul style="margin:4px 0 12px 16px;padding:0;">`;
        resources.forEach(r => { html += `<li><code>${esc(r)}</code></li>`; });
        html += `</ul>`;
      }
      if (prompts.length > 0) {
        html += `<p><strong>Prompts (${prompts.length}):</strong></p>`;
        html += `<ul style="margin:4px 0 12px 16px;padding:0;">`;
        prompts.forEach(p => { html += `<li><code>${esc(p)}</code></li>`; });
        html += `</ul>`;
      }

      if (tools.length === 0 && resources.length === 0 && prompts.length === 0) {
        html += `<p>No capabilities listed.</p>`;
      }

      html += `</div></div>`;
    }

    // Relations
    if (entity.relations) {
      const relEntries = Object.entries(entity.relations).filter(([, v]) => v && v.length > 0);
      if (relEntries.length > 0) {
        html += `<div class="detail-panel__section"><h3 class="detail-panel__section-title">Relations</h3><div class="detail-panel__content">`;
        relEntries.forEach(([relType, targets]) => {
          html += `<p style="margin-bottom:4px;"><strong>${esc(relType)}:</strong></p>`;
          html += `<ul style="margin:0 0 12px 16px;padding:0;">`;
          targets.forEach(tid => {
            const t = entities[tid];
            const tName = t ? (t.name || tid) : tid;
            html += `<li><a href="register.html?${t?.type?.toLowerCase().replace(/[^a-z]/g, "") || "id"}=${esc(tid)}">${esc(tName)}</a></li>`;
          });
          html += `</ul>`;
        });
        html += `</div></div>`;
      }
    }

    if (content) content.innerHTML = html;

    // Show panel
    const panel = document.getElementById("detailPanel");
    const backdrop = document.getElementById("detailBackdrop");
    if (panel) {
      panel.classList.add("detail-panel--open");
      panel.setAttribute("aria-hidden", "false");
    }
    if (backdrop) {
      backdrop.classList.add("detail-panel__backdrop--open");
      backdrop.setAttribute("aria-hidden", "false");
    }
  }

  function closeDetailPanel() {
    state.selectedEntityId = null;
    const panel = document.getElementById("detailPanel");
    const backdrop = document.getElementById("detailBackdrop");
    if (panel) {
      panel.classList.remove("detail-panel--open");
      panel.setAttribute("aria-hidden", "true");
    }
    if (backdrop) {
      backdrop.classList.remove("detail-panel__backdrop--open");
      backdrop.setAttribute("aria-hidden", "true");
    }
  }

  // ------------------------------------------------------------------
  // URL params (pre-select filters from URL)
  // ------------------------------------------------------------------

  function readURLParams() {
    const params = new URLSearchParams(window.location.search);
    const type = params.get("type");
    const server = params.get("server");
    const skill = params.get("skill");
    const category = params.get("category");

    if (type) {
      state.activeType = type;
      // Update UI
      document.querySelectorAll("[data-filter-type]").forEach(btn => {
        btn.classList.toggle("pill--active", btn.getAttribute("data-filter-type") === type);
        btn.setAttribute("aria-pressed", btn.getAttribute("data-filter-type") === type ? "true" : "false");
      });
    }

    // If a specific entity is requested, open its detail
    const targetId = server || skill || category;
    if (targetId && entities[targetId]) {
      // Need to render table first then open detail
      setTimeout(() => openDetailPanel(targetId), 100);
    }
  }

  // ------------------------------------------------------------------
  // Event Handlers
  // ------------------------------------------------------------------

  function setupEventListeners() {
    // Search
    const searchInput = document.getElementById("searchInput");
    if (searchInput) {
      searchInput.addEventListener("input", function() {
        clearTimeout(searchDebounce);
        searchDebounce = setTimeout(() => {
          state.searchQuery = this.value.trim();
          state.currentPage = 1;
          renderTable();
        }, 200);
      });
    }

    // Tier filters
    document.querySelectorAll("[data-filter-tier]").forEach(btn => {
      btn.addEventListener("click", function() {
        const tier = this.getAttribute("data-filter-tier");
        state.activeTier = tier;
        state.currentPage = 1;

        document.querySelectorAll("[data-filter-tier]").forEach(b => {
          b.classList.toggle("pill--active", b === this);
          b.setAttribute("aria-pressed", b === this ? "true" : "false");
        });

        renderTable();
      });
    });

    // Type filters
    document.querySelectorAll("[data-filter-type]").forEach(btn => {
      btn.addEventListener("click", function() {
        const type = this.getAttribute("data-filter-type");
        state.activeType = type;
        state.currentPage = 1;

        document.querySelectorAll("[data-filter-type]").forEach(b => {
          b.classList.toggle("pill--active", b === this);
          b.setAttribute("aria-pressed", b === this ? "true" : "false");
        });

        renderTable();
      });
    });

    // Sort headers
    document.querySelectorAll(".data-table th[data-sort]").forEach(th => {
      th.addEventListener("click", function() {
        const col = this.getAttribute("data-sort");
        if (state.sortColumn === col) {
          state.sortDirection = state.sortDirection === "asc" ? "desc" : "asc";
        } else {
          state.sortColumn = col;
          state.sortDirection = "asc";
        }
        renderTable();
      });
    });

    // Row click → detail panel
    const tbody = document.getElementById("tableBody");
    if (tbody) {
      tbody.addEventListener("click", function(e) {
        const row = e.target.closest("tr[data-id]");
        if (row) {
          openDetailPanel(row.getAttribute("data-id"));
        }
      });

      tbody.addEventListener("keydown", function(e) {
        if (e.key === "Enter" || e.key === " ") {
          const row = e.target.closest("tr[data-id]");
          if (row) {
            e.preventDefault();
            openDetailPanel(row.getAttribute("data-id"));
          }
        }
      });
    }

    // Pagination
    const pagination = document.getElementById("pagination");
    if (pagination) {
      pagination.addEventListener("click", function(e) {
        const btn = e.target.closest("[data-page]");
        if (btn) {
          const page = parseInt(btn.getAttribute("data-page"), 10);
          if (!isNaN(page)) {
            state.currentPage = page;
            renderTable();
          }
        }
      });
    }

    // Detail panel close
    const closeBtn = document.getElementById("detailClose");
    if (closeBtn) {
      closeBtn.addEventListener("click", closeDetailPanel);
    }

    const backdrop = document.getElementById("detailBackdrop");
    if (backdrop) {
      backdrop.addEventListener("click", closeDetailPanel);
    }

    document.addEventListener("keydown", function(e) {
      if (e.key === "Escape" && state.selectedEntityId) {
        closeDetailPanel();
      }
    });
  }

  // ------------------------------------------------------------------
  // Init
  // ------------------------------------------------------------------

  function init() {
    readURLParams();
    renderTable();
    setupEventListeners();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
