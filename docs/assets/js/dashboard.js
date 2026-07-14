/**
 * al-dente Dashboard View
 * Handles stat cards, featured servers, skills, and categories.
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
  const metadata = DATA.metadata || {};

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

  function formatDate(dateStr) {
    if (!dateStr) return "—";
    try {
      const d = new Date(dateStr);
      return d.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
    } catch {
      return dateStr;
    }
  }

  function countServersRealizingSkill(skillId) {
    const servers = byType["MCP-Server"] || [];
    return servers.filter(sid => {
      const s = entities[sid];
      return s && s.skills_realized && s.skills_realized.includes(skillId);
    }).length;
  }

  // ------------------------------------------------------------------
  // Empty State
  // ------------------------------------------------------------------

  function emptyStateHTML(message) {
    return `
      <div class="empty-state" style="grid-column: 1 / -1;">
        <div class="empty-state__icon">📋</div>
        <p class="empty-state__title">No data available</p>
        <p class="empty-state__text">${esc(message)}</p>
      </div>
    `;
  }

  // ------------------------------------------------------------------
  // Stats
  // ------------------------------------------------------------------

  function renderStats() {
    const container = document.getElementById("statsGrid");
    if (!container) return;

    const serverCount = (byType["MCP-Server"] || []).length;
    const skillCount = (byType["Skill"] || []).length;
    const publisherCount = (byType["Publisher"] || []).length;
    const generated = metadata.generated ? formatDate(metadata.generated) : "—";

    const stats = [
      { number: serverCount, label: "MCP Servers", delay: "stagger-1" },
      { number: skillCount, label: "Skills", delay: "stagger-2" },
      { number: publisherCount, label: "Publishers", delay: "stagger-3" },
      { number: generated, label: "Last Updated", delay: "stagger-4" }
    ];

    container.innerHTML = stats.map(s => `
      <div class="card stat-card animate-count ${s.delay}" tabindex="0">
        <div class="stat-card__number">${esc(String(s.number))}</div>
        <div class="stat-card__label">${esc(s.label)}</div>
      </div>
    `).join("");
  }

  // ------------------------------------------------------------------
  // Featured Servers
  // ------------------------------------------------------------------

  function renderFeaturedServers() {
    const container = document.getElementById("serversGrid");
    if (!container) return;

    const servers = (byType["MCP-Server"] || [])
      .map(id => entities[id])
      .filter(Boolean)
      .sort((a, b) => (b.stars || 0) - (a.stars || 0))
      .slice(0, 6);

    if (servers.length === 0) {
      container.innerHTML = emptyStateHTML("No servers in the register yet. Data will be populated by the pipeline.");
      return;
    }

    container.innerHTML = servers.map((s, i) => {
      const tierClass = getTierBadgeClass(s.tier);
      const capCount = s.capabilities
        ? ((s.capabilities.tools || []).length + (s.capabilities.resources || []).length + (s.capabilities.prompts || []).length)
        : 0;

      return `
        <a href="register.html?server=${esc(s.id)}"
           class="card entity-card card--clickable animate-fade-in stagger-${Math.min(i + 1, 6)}"
           role="listitem"
           aria-label="${esc(s.name)} - ${esc(s.tier || "unknown tier")} server">
          <div class="entity-card__header">
            <span class="entity-card__title">${esc(s.name)}</span>
            ${s.tier ? `<span class="badge ${tierClass}">${esc(s.tier)}</span>` : ""}
          </div>
          <div class="entity-card__meta">
            ${s.transport ? `<span class="transport-icon">${esc(s.transport)}</span>` : ""}
            ${s.stars ? `<span class="star-count">${s.stars.toLocaleString()}</span>` : ""}
            <span style="font-size:12px;color:var(--color-text-muted);">${capCount} caps</span>
          </div>
          <p class="entity-card__description">${esc(s.description || "No description available.")}</p>
          <div class="entity-card__footer">
            <span style="font-size:12px;color:var(--color-text-muted);">${formatDate(s.last_updated)}</span>
            <span style="font-size:12px;color:var(--color-accent);">View →</span>
          </div>
        </a>
      `;
    }).join("");
  }

  // ------------------------------------------------------------------
  // Featured Skills
  // ------------------------------------------------------------------

  function renderFeaturedSkills() {
    const container = document.getElementById("skillsGrid");
    if (!container) return;

    const skills = (byType["Skill"] || [])
      .map(id => entities[id])
      .filter(Boolean)
      .map(s => ({ ...s, _realizedCount: countServersRealizingSkill(s.id) }))
      .sort((a, b) => b._realizedCount - a._realizedCount)
      .slice(0, 4);

    if (skills.length === 0) {
      container.innerHTML = emptyStateHTML("No skills in the register yet. Data will be populated by the pipeline.");
      return;
    }

    container.innerHTML = skills.map((s, i) => `
      <a href="register.html?skill=${esc(s.id)}"
         class="card entity-card card--clickable animate-fade-in stagger-${Math.min(i + 1, 6)}"
         role="listitem"
         aria-label="${esc(s.name)} - realized by ${s._realizedCount} servers">
        <div class="entity-card__header">
          <span class="entity-card__title">${esc(s.name)}</span>
          <span class="badge badge--type-skill">Skill</span>
        </div>
        <p class="entity-card__description">${esc(s.description || "No description available.")}</p>
        <div class="entity-card__footer">
          <span style="font-size:12px;color:var(--color-text-muted);">
            Realized by <strong style="color:var(--color-text);">${s._realizedCount}</strong> server${s._realizedCount !== 1 ? "s" : ""}
          </span>
          <span style="font-size:12px;color:var(--color-accent);">View →</span>
        </div>
      </a>
    `).join("");
  }

  // ------------------------------------------------------------------
  // Categories
  // ------------------------------------------------------------------

  function renderCategories() {
    const container = document.getElementById("categoriesGrid");
    if (!container) return;

    const cats = (byType["Category"] || [])
      .map(id => entities[id])
      .filter(Boolean);

    if (cats.length === 0) {
      container.innerHTML = `<span class="text-muted" style="font-size:14px;">No categories yet.</span>`;
      return;
    }

    // Count entities per category
    const catCounts = {};
    cats.forEach(c => { catCounts[c.id] = 0; });
    Object.values(entities).forEach(e => {
      (e.categories || []).forEach(cid => {
        if (catCounts[cid] !== undefined) catCounts[cid]++;
      });
    });

    container.innerHTML = cats.map(c => {
      const count = catCounts[c.id] || 0;
      return `
        <a href="register.html?category=${esc(c.id)}"
           class="pill"
           role="listitem"
           aria-label="${esc(c.name)} - ${count} entities">
          ${esc(c.name)}
          <span style="background:rgba(0,0,0,0.08);padding:2px 8px;border-radius:9999px;font-size:11px;font-weight:600;">${count}</span>
        </a>
      `;
    }).join("");
  }

  // ------------------------------------------------------------------
  // Init
  // ------------------------------------------------------------------

  function init() {
    renderStats();
    renderFeaturedServers();
    renderFeaturedSkills();
    renderCategories();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
