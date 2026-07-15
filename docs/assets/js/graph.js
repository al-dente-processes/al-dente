/**
 * al-dente Knowledge Graph View
 * D3.js force-directed graph of MCP entities and their relationships.
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

  // Color palette (matches CSS custom properties)
  const COLORS = {
    "MCP-Server": "#3B6EA5",
    "Skill": "#2D8A4E",
    "Category": "#777777",
    "Agentic-Pattern": "#C45C3B",
    "Publisher": "#7B5EA7"
  };

  const TIER_COLORS = {
    "Official": "#1A5276",
    "Verified": "#2D8A4E",
    "Community": "#B9770E",
    "Experimental": "#7B5EA7"
  };

  const NODE_BASE_SIZE = 8;

  // ------------------------------------------------------------------
  // State
  // ------------------------------------------------------------------
  let simulation = null;
  let svg = null;
  let g = null;        // main group (zoomable)
  let nodeSel = null;  // d3 selection of nodes
  let linkSel = null;  // d3 selection of links
  let graphData = { nodes: [], links: [] };
  let activeFilters = {
    types: new Set(["MCP-Server", "Skill", "Category", "Agentic-Pattern", "Publisher"]),
    tiers: new Set(["Official", "Verified", "Community", "Experimental", null])
  };
  let fixedNodes = new Set();
  let hoveredNodeId = null;

  // ------------------------------------------------------------------
  // Data Preparation
  // ------------------------------------------------------------------

  function buildGraphData() {
    const nodes = [];
    const nodeMap = new Map();
    const links = [];

    // Create nodes for all entities
    Object.values(entities).forEach(entity => {
      if (!entity || !entity.id) return;

      const node = {
        id: entity.id,
        name: entity.name || entity.id,
        type: entity.type || "Unknown",
        tier: entity.tier || null,
        stars: entity.stars || 0,
        description: entity.description || "",
        publisher: entity.publisher || null,
        // D3 force properties
        x: 0,
        y: 0,
        vx: 0,
        vy: 0,
        fx: null,
        fy: null
      };

      nodes.push(node);
      nodeMap.set(entity.id, node);
    });

    // Create links from flat edges array (if available from build_okf.py)
    // Falls back to parsing entity.relations for backward compatibility
    const bundleEdges = DATA.edges || [];

    if (bundleEdges.length > 0) {
      bundleEdges.forEach(edge => {
        const source = nodeMap.get(edge.source);
        const target = nodeMap.get(edge.target);
        if (source && target) {
          const exists = links.some(l =>
            (l.source === source.id && l.target === target.id) ||
            (l.source === target.id && l.target === source.id)
          );
          if (!exists) {
            links.push({
              source: source.id,
              target: target.id,
              relationType: edge.type
            });
          }
        }
      });
    } else {
      // Fallback: parse relations from individual entities
      Object.values(entities).forEach(entity => {
        if (!entity.relations) return;
        Object.entries(entity.relations).forEach(([relType, targets]) => {
          if (!Array.isArray(targets)) return;
          targets.forEach(targetId => {
            const source = nodeMap.get(entity.id);
            const target = nodeMap.get(targetId);
            if (source && target) {
              const exists = links.some(l =>
                (l.source === source.id && l.target === target.id) ||
                (l.source === target.id && l.target === source.id)
              );
              if (!exists) {
                links.push({
                  source: source.id,
                  target: target.id,
                  relationType: relType
                });
              }
            }
          });
        });
      });
    }

    return { nodes, links };
  }

  // ------------------------------------------------------------------
  // Node size by type/stars
  // ------------------------------------------------------------------

  function getNodeRadius(node) {
    if (node.type === "MCP-Server") {
      // Size by star count, clamped
      const s = node.stars || 0;
      return NODE_BASE_SIZE + Math.min(s / 200, 20);
    }
    if (node.type === "Publisher") return NODE_BASE_SIZE + 2;
    if (node.type === "Category") return NODE_BASE_SIZE - 1;
    return NODE_BASE_SIZE;
  }

  // ------------------------------------------------------------------
  // Node shape rendering (SVG paths)
  // ------------------------------------------------------------------

  function getNodePath(node, r) {
    switch (node.type) {
      case "MCP-Server":
        // Circle
        return null; // Use circle element instead

      case "Skill":
        // Rounded rectangle
        const w = r * 2.4;
        const h = r * 1.8;
        const rx = 4;
        return `M${-w/2 + rx},${-h/2} h${w - 2*rx} a${rx},${rx} 0 0 1 ${rx},${rx} v${h - 2*rx} a${rx},${rx} 0 0 1 ${-rx},${rx} h${-(w - 2*rx)} a${rx},${rx} 0 0 1 ${-rx},${-rx} v${-(h - 2*rx)} a${rx},${rx} 0 0 1 ${rx},${-rx} z`;

      case "Category":
        // Hexagon
        const hr = r * 1.3;
        const points = [];
        for (let i = 0; i < 6; i++) {
          const angle = (Math.PI / 3) * i - Math.PI / 6;
          points.push(`${Math.cos(angle) * hr},${Math.sin(angle) * hr}`);
        }
        return `M${points.join(" L")} z`;

      case "Agentic-Pattern":
        // Diamond
        const dr = r * 1.4;
        return `M0,${-dr} L${dr},0 L0,${dr} L${-dr},0 z`;

      case "Publisher":
        // Square
        const sr = r * 1.2;
        return `M${-sr},${-sr} h${sr*2} v${sr*2} h${-sr*2} z`;

      default:
        return null;
    }
  }

  // ------------------------------------------------------------------
  // Filtering
  // ------------------------------------------------------------------

  function isNodeVisible(node) {
    if (!activeFilters.types.has(node.type)) return false;
    if (node.tier !== null && !activeFilters.tiers.has(node.tier)) return false;
    // Nodes with no tier: show if "null" is in tiers set
    if (node.tier === null && !activeFilters.tiers.has(null)) return false;
    return true;
  }

  function applyFilters() {
    if (!nodeSel || !linkSel) return;

    nodeSel.style("opacity", d => isNodeVisible(d) ? 1 : 0.08)
           .style("pointer-events", d => isNodeVisible(d) ? "all" : "none");

    linkSel.style("opacity", d => {
      const s = typeof d.source === "object" ? d.source : graphData.nodes.find(n => n.id === d.source);
      const t = typeof d.target === "object" ? d.target : graphData.nodes.find(n => n.id === d.target);
      return (s && t && isNodeVisible(s) && isNodeVisible(t)) ? 0.5 : 0.03;
    });

    // Highlight logic
    if (hoveredNodeId) {
      highlightNeighbors(hoveredNodeId);
    }
  }

  // ------------------------------------------------------------------
  // Highlight neighbors on hover
  // ------------------------------------------------------------------

  function highlightNeighbors(nodeId) {
    if (!nodeSel || !linkSel) return;

    const neighborIds = new Set();
    neighborIds.add(nodeId);

    graphData.links.forEach(l => {
      const sid = typeof l.source === "object" ? l.source.id : l.source;
      const tid = typeof l.target === "object" ? l.target.id : l.target;
      if (sid === nodeId) neighborIds.add(tid);
      if (tid === nodeId) neighborIds.add(sid);
    });

    nodeSel.style("opacity", d => {
      if (!isNodeVisible(d)) return 0.08;
      return neighborIds.has(d.id) ? 1 : 0.2;
    });

    linkSel.style("opacity", d => {
      const sid = typeof d.source === "object" ? d.source.id : d.source;
      const tid = typeof d.target === "object" ? d.target.id : d.target;
      const s = typeof d.source === "object" ? d.source : graphData.nodes.find(n => n.id === d.source);
      const t = typeof d.target === "object" ? d.target : graphData.nodes.find(n => n.id === d.target);
      if (!s || !t || !isNodeVisible(s) || !isNodeVisible(t)) return 0.03;
      return (sid === nodeId || tid === nodeId) ? 0.9 : 0.05;
    });
  }

  function clearHighlight() {
    hoveredNodeId = null;
    if (!nodeSel || !linkSel) return;

    nodeSel.style("opacity", d => isNodeVisible(d) ? 1 : 0.08);
    linkSel.style("opacity", d => {
      const s = typeof d.source === "object" ? d.source : graphData.nodes.find(n => n.id === d.source);
      const t = typeof d.target === "object" ? d.target : graphData.nodes.find(n => n.id === d.target);
      return (s && t && isNodeVisible(s) && isNodeVisible(t)) ? 0.5 : 0.03;
    });
  }

  // ------------------------------------------------------------------
  // Tooltip
  // ------------------------------------------------------------------

  function showTooltip(event, node) {
    const tooltip = document.getElementById("graphTooltip");
    if (!tooltip) return;

    const tierText = node.tier ? ` · ${node.tier}` : "";
    const starsText = node.stars ? ` · ★${node.stars.toLocaleString()}` : "";
    tooltip.innerHTML = `<strong>${esc(node.name)}</strong><br><span style="opacity:0.8">${esc(node.type)}${tierText}${starsText}</span>`;
    tooltip.classList.add("graph-tooltip--visible");

    // Position
    const container = document.getElementById("graphContainer");
    const rect = container.getBoundingClientRect();
    let x = event.clientX - rect.left + 12;
    let y = event.clientY - rect.top - 12;

    // Keep within bounds
    if (x + 200 > rect.width) x -= 220;
    if (y < 0) y = 12;

    tooltip.style.left = x + "px";
    tooltip.style.top = y + "px";
  }

  function hideTooltip() {
    const tooltip = document.getElementById("graphTooltip");
    if (tooltip) tooltip.classList.remove("graph-tooltip--visible");
  }

  function esc(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  // ------------------------------------------------------------------
  // Detail Card
  // ------------------------------------------------------------------

  function showDetailCard(node) {
    const card = document.getElementById("graphDetailCard");
    const title = document.getElementById("graphDetailTitle");
    const content = document.getElementById("graphDetailContent");
    if (!card || !title || !content) return;

    title.textContent = node.name;

    const color = COLORS[node.type] || "#777";
    let html = "";

    html += `<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">`;
    html += `<span style="width:10px;height:10px;border-radius:50%;background:${color};display:inline-block;"></span>`;
    html += `<span style="font-size:13px;color:var(--color-text-secondary);">${esc(node.type)}</span>`;
    if (node.tier) html += ` · <span style="font-size:13px;font-weight:600;color:${TIER_COLORS[node.tier] || '#777'};">${esc(node.tier)}</span>`;
    html += `</div>`;

    if (node.description) {
      html += `<p style="font-size:13px;color:var(--color-text-secondary);margin-bottom:8px;">${esc(node.description)}</p>`;
    }

    if (node.stars) {
      html += `<p style="font-size:13px;color:var(--color-text-muted);">★ ${node.stars.toLocaleString()} stars</p>`;
    }

    // Count relationships
    const relCount = graphData.links.filter(l => {
      const sid = typeof l.source === "object" ? l.source.id : l.source;
      const tid = typeof l.target === "object" ? l.target.id : l.target;
      return sid === node.id || tid === node.id;
    }).length;
    html += `<p style="font-size:13px;color:var(--color-text-muted);">${relCount} connection${relCount !== 1 ? "s" : ""}</p>`;

    if (node.publisher && entities[node.publisher]) {
      html += `<p style="font-size:13px;color:var(--color-text-muted);">Publisher: ${esc(entities[node.publisher].name || node.publisher)}</p>`;
    }

    // Link to register
    html += `<a href="register.html?${esc(node.type.toLowerCase().replace(/[^a-z]/g, ""))}=${esc(node.id)}" style="font-size:13px;margin-top:8px;display:inline-block;">View in Register →</a>`;

    content.innerHTML = html;
    card.style.display = "block";
  }

  function hideDetailCard() {
    const card = document.getElementById("graphDetailCard");
    if (card) card.style.display = "none";
  }

  // ------------------------------------------------------------------
  // Search Node
  // ------------------------------------------------------------------

  function searchNode(query) {
    if (!query || !nodeSel) return;

    const q = query.toLowerCase();
    const match = graphData.nodes.find(n =>
      isNodeVisible(n) && (n.name || "").toLowerCase().includes(q)
    );

    if (match && simulation) {
      // Center on matched node
      const container = document.getElementById("graphContainer");
      const width = container.clientWidth;
      const height = container.clientHeight;

      const transform = d3.zoomIdentity
        .translate(width / 2, height / 2)
        .scale(1.5)
        .translate(-match.x, -match.y);

      svg.transition().duration(500).call(
        d3.zoom().transform,
        transform
      );

      // Highlight the node
      nodeSel.style("opacity", d => {
        if (!isNodeVisible(d)) return 0.08;
        return d.id === match.id ? 1 : 0.15;
      });

      linkSel.style("opacity", d => {
        const s = typeof d.source === "object" ? d.source : graphData.nodes.find(n => n.id === d.source);
        const t = typeof d.target === "object" ? d.target : graphData.nodes.find(n => n.id === d.target);
        if (!s || !t || !isNodeVisible(s) || !isNodeVisible(t)) return 0.03;
        const sid = typeof d.source === "object" ? d.source.id : d.source;
        const tid = typeof d.target === "object" ? d.target.id : d.target;
        return (sid === match.id || tid === match.id) ? 0.9 : 0.05;
      });

      // Show detail
      showDetailCard(match);
    }
  }

  // ------------------------------------------------------------------
  // Force Simulation Setup
  // ------------------------------------------------------------------

  function initGraph() {
    const container = document.getElementById("graphContainer");
    if (!container) return;

    const width = container.clientWidth;
    const height = container.clientHeight;

    // Prepare data
    graphData = buildGraphData();

    if (graphData.nodes.length === 0) {
      container.innerHTML += `
        <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;">
          <div class="empty-state">
            <div class="empty-state__icon">🕸️</div>
            <p class="empty-state__title">No graph data available</p>
            <p class="empty-state__text">Data will be populated by the pipeline.</p>
          </div>
        </div>
      `;
      return;
    }

    // Create SVG
    svg = d3.select(container)
      .append("svg")
      .attr("class", "graph-svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("role", "img")
      .attr("aria-label", "Force-directed knowledge graph of MCP entities");

    // Zoom behavior
    const zoom = d3.zoom()
      .scaleExtent([0.1, 4])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });

    svg.call(zoom);

    // Main group (zoomable)
    g = svg.append("g");

    // Arrow marker for directed edges
    svg.append("defs").selectAll("marker")
      .data(["end"])
      .enter().append("marker")
      .attr("id", "arrow-end")
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 25)
      .attr("refY", 0)
      .attr("markerWidth", 6)
      .attr("markerHeight", 6)
      .attr("orient", "auto")
      .append("path")
      .attr("d", "M0,-5L10,0L0,5")
      .attr("fill", "#bbb");

    // Links
    linkSel = g.append("g")
      .attr("class", "links")
      .selectAll("line")
      .data(graphData.links)
      .enter().append("line")
      .attr("stroke", "#bbb")
      .attr("stroke-width", 1.5)
      .attr("stroke-opacity", 0.5);

    // Nodes group
    const nodeGroup = g.append("g")
      .attr("class", "nodes")
      .selectAll("g")
      .data(graphData.nodes)
      .enter().append("g")
      .attr("class", "node")
      .style("cursor", "pointer")
      .style("opacity", 0); // Start hidden for fade-in

    // Node shapes
    nodeGroup.each(function(d) {
      const el = d3.select(this);
      const r = getNodeRadius(d);
      const pathData = getNodePath(d, r);
      const color = COLORS[d.type] || "#777";
      const tierColor = TIER_COLORS[d.tier] || "#ccc";

      if (pathData === null) {
        // Circle (for servers)
        el.append("circle")
          .attr("r", r)
          .attr("fill", color)
          .attr("stroke", tierColor)
          .attr("stroke-width", d.tier ? 2.5 : 1)
          .attr("fill-opacity", 0.85);
      } else {
        // Custom path shape
        el.append("path")
          .attr("d", pathData)
          .attr("fill", color)
          .attr("stroke", tierColor)
          .attr("stroke-width", d.tier ? 2.5 : 1)
          .attr("fill-opacity", 0.85);
      }
    });

    nodeSel = nodeGroup;

    // Labels on nodes (only for larger nodes or specific types)
    const labeledNodes = graphData.nodes.filter(d =>
      d.type === "MCP-Server" || d.type === "Publisher" || d.type === "Category"
    );

    const labelSel = g.append("g")
      .attr("class", "labels")
      .selectAll("text")
      .data(labeledNodes)
      .enter().append("text")
      .text(d => d.name)
      .attr("font-size", 10)
      .attr("font-family", "Inter, sans-serif")
      .attr("fill", "#333")
      .attr("text-anchor", "middle")
      .attr("dy", d => getNodeRadius(d) + 13)
      .style("pointer-events", "none")
      .style("opacity", 0); // Start hidden

    // Fade-in animation
    nodeGroup.transition()
      .duration(800)
      .delay((d, i) => i * 15)
      .style("opacity", 1);

    labelSel.transition()
      .duration(800)
      .delay((d, i) => 300 + i * 15)
      .style("opacity", 0.8);

    // ----------------------------------------------------------------
    // Drag behavior
    // ----------------------------------------------------------------

    const drag = d3.drag()
      .on("start", (event, d) => {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      })
      .on("drag", (event, d) => {
        d.fx = event.x;
        d.fy = event.y;
      })
      .on("end", (event, d) => {
        if (!event.active) simulation.alphaTarget(0);
        if (!fixedNodes.has(d.id)) {
          d.fx = null;
          d.fy = null;
        }
      });

    nodeGroup.call(drag);

    // ----------------------------------------------------------------
    // Hover
    // ----------------------------------------------------------------

    nodeGroup
      .on("mouseenter", function(event, d) {
        hoveredNodeId = d.id;
        highlightNeighbors(d.id);
        showTooltip(event, d);
      })
      .on("mousemove", function(event, d) {
        showTooltip(event, d);
      })
      .on("mouseleave", function() {
        clearHighlight();
        hideTooltip();
      });

    // ----------------------------------------------------------------
    // Click (fix + detail)
    // ----------------------------------------------------------------

    nodeGroup.on("click", function(event, d) {
      event.stopPropagation();

      if (fixedNodes.has(d.id)) {
        // Already fixed, just show detail
        showDetailCard(d);
        return;
      }

      fixedNodes.add(d.id);
      d.fx = d.x;
      d.fy = d.y;
      showDetailCard(d);
    });

    // Double-click to release
    nodeGroup.on("dblclick", function(event, d) {
      event.stopPropagation();
      fixedNodes.delete(d.id);
      d.fx = null;
      d.fy = null;
      if (!event.active && simulation) simulation.alphaTarget(0);
      hideDetailCard();
    });

    // Background click to clear
    svg.on("click", function() {
      hideDetailCard();
    });

    // ----------------------------------------------------------------
    // Force simulation
    // ----------------------------------------------------------------

    simulation = d3.forceSimulation(graphData.nodes)
      .force("link", d3.forceLink(graphData.links)
        .id(d => d.id)
        .distance(d => {
          const s = typeof d.source === "object" ? d.source : graphData.nodes.find(n => n.id === d.source);
          const t = typeof d.target === "object" ? d.target : graphData.nodes.find(n => n.id === d.target);
          if (s && t) {
            if (s.type === "MCP-Server" && t.type === "Skill") return 80;
            if (s.type === "MCP-Server" && t.type === "Category") return 100;
          }
          return 120;
        })
        .strength(0.5)
      )
      .force("charge", d3.forceManyBody().strength(-250))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(d => getNodeRadius(d) + 8))
      .force("x", d3.forceX(width / 2).strength(0.05))
      .force("y", d3.forceY(height / 2).strength(0.05));

    simulation.on("tick", () => {
      linkSel
        .attr("x1", d => (typeof d.source === "object" ? d.source.x : 0))
        .attr("y1", d => (typeof d.source === "object" ? d.source.y : 0))
        .attr("x2", d => (typeof d.target === "object" ? d.target.x : 0))
        .attr("y2", d => (typeof d.target === "object" ? d.target.y : 0));

      nodeGroup
        .attr("transform", d => `translate(${d.x},${d.y})`);

      labelSel
        .attr("x", d => d.x)
        .attr("y", d => d.y);
    });

    // ----------------------------------------------------------------
    // Resize handler
    // ----------------------------------------------------------------

    const resizeObserver = new ResizeObserver(entries => {
      for (const entry of entries) {
        const w = entry.contentRect.width;
        const h = entry.contentRect.height;
        svg.attr("width", w).attr("height", h).attr("viewBox", [0, 0, w, h]);
        simulation.force("center", d3.forceCenter(w / 2, h / 2));
        simulation.alpha(0.3).restart();
      }
    });
    resizeObserver.observe(container);

    // Store for later use
    window._graphSimulation = simulation;
  }

  // ------------------------------------------------------------------
  // Control Panel Event Listeners
  // ------------------------------------------------------------------

  function setupControls() {
    // Type filters
    const typeMap = {
      "filterServer": "MCP-Server",
      "filterSkill": "Skill",
      "filterCategory": "Category",
      "filterPattern": "Agentic-Pattern",
      "filterPublisher": "Publisher"
    };

    Object.entries(typeMap).forEach(([checkboxId, typeName]) => {
      const cb = document.getElementById(checkboxId);
      if (cb) {
        cb.addEventListener("change", function() {
          if (this.checked) {
            activeFilters.types.add(typeName);
          } else {
            activeFilters.types.delete(typeName);
          }
          applyFilters();
        });
      }
    });

    // Tier filters
    const tierMap = {
      "tierOfficial": "Official",
      "tierVerified": "Verified",
      "tierCommunity": "Community",
      "tierExperimental": "Experimental"
    };

    Object.entries(tierMap).forEach(([checkboxId, tierName]) => {
      const cb = document.getElementById(checkboxId);
      if (cb) {
        cb.addEventListener("change", function() {
          if (this.checked) {
            activeFilters.tiers.add(tierName);
          } else {
            activeFilters.tiers.delete(tierName);
          }
          applyFilters();
        });
      }
    });

    // Reset view
    const resetBtn = document.getElementById("resetView");
    if (resetBtn && svg) {
      resetBtn.addEventListener("click", function() {
        // Reset zoom
        const container = document.getElementById("graphContainer");
        const width = container.clientWidth;
        const height = container.clientHeight;

        svg.transition().duration(500).call(
          d3.zoom().transform,
          d3.zoomIdentity
        );

        // Unfix all nodes
        fixedNodes.clear();
        graphData.nodes.forEach(d => {
          d.fx = null;
          d.fy = null;
        });

        // Reset filters
        activeFilters.types = new Set(["MCP-Server", "Skill", "Category", "Agentic-Pattern", "Publisher"]);
        activeFilters.tiers = new Set(["Official", "Verified", "Community", "Experimental", null]);

        // Reset checkboxes
        Object.keys(typeMap).forEach(id => {
          const cb = document.getElementById(id);
          if (cb) cb.checked = true;
        });
        Object.keys(tierMap).forEach(id => {
          const cb = document.getElementById(id);
          if (cb) cb.checked = true;
        });

        clearHighlight();
        hideDetailCard();
        applyFilters();

        // Restart simulation
        if (simulation) simulation.alpha(0.5).restart();
      });
    }

    // Search
    const searchInput = document.getElementById("graphSearch");
    if (searchInput) {
      let debounce;
      searchInput.addEventListener("input", function() {
        clearTimeout(debounce);
        debounce = setTimeout(() => searchNode(this.value.trim()), 300);
      });

      searchInput.addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
          clearTimeout(debounce);
          searchNode(this.value.trim());
        }
      });
    }

    // Close detail card
    const closeBtn = document.getElementById("graphDetailClose");
    if (closeBtn) {
      closeBtn.addEventListener("click", hideDetailCard);
    }
  }

  // ------------------------------------------------------------------
  // Init
  // ------------------------------------------------------------------

  function init() {
    // Check D3 is loaded
    if (typeof d3 === "undefined") {
      const container = document.getElementById("graphContainer");
      if (container) {
        container.innerHTML += `
          <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;">
            <div class="empty-state">
              <div class="empty-state__icon">📊</div>
              <p class="empty-state__title">D3.js not loaded</p>
              <p class="empty-state__text">The graph visualization requires D3.js.</p>
            </div>
          </div>
        `;
      }
      return;
    }

    initGraph();
    setupControls();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
