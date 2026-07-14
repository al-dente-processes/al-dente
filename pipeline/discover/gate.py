#!/usr/bin/env python3
"""
Quality gate — filters discovered servers by configurable criteria.

The gate enforces al-dente's "high signal, low noise" principle.
Not every discovered server gets an OKF entry. Only those that
meet configurable quality thresholds.

Scoring is multi-factor. A server can pass via multiple paths:
- Official registry presence (strong signal)
- High GitHub stars (community signal)
- High PulseMCP traffic (usage signal)
- Official/Verified classification (curator signal)

Gating modes:
- "strict"  : Only Official/Verified tier candidates (default for production)
- "balanced": Official + Verified + high-signal Community (default)
- "lenient" : Include Experimental with >=50 stars (for broad coverage)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Callable

from .models import CandidateServer

logger = logging.getLogger(__name__)

# Default quality thresholds
DEFAULT_THRESHOLDS = {
    "min_stars": 100,
    "min_pulsemcp_visitors_weekly": 5000,
    "require_registry_published": False,
    "require_pulsemcp_official": False,
    "max_age_days": 365,  # GitHub repo last updated
    "exclude_archived": True,
    "exclude_no_description": True,
    "exclude_no_github_url": True,
}

# Preset configurations
PRESETS = {
    "strict": {
        "min_stars": 500,
        "min_pulsemcp_visitors_weekly": 10000,
        "require_registry_published": False,
        "require_pulsemcp_official": False,
        "max_age_days": 365,
        "exclude_archived": True,
        "exclude_no_description": True,
        "exclude_no_github_url": True,
    },
    "balanced": {
        **DEFAULT_THRESHOLDS,
    },
    "lenient": {
        "min_stars": 50,
        "min_pulsemcp_visitors_weekly": 1000,
        "require_registry_published": False,
        "require_pulsemcp_official": False,
        "max_age_days": 730,
        "exclude_archived": False,
        "exclude_no_description": False,
        "exclude_no_github_url": True,
    },
}


@dataclass
class GateResult:
    """Result of quality gating for a single candidate."""
    candidate: CandidateServer
    passed: bool
    score: float  # 0-100 quality score
    reasons: list[str]  # Why it passed or failed
    tier: str  # Computed tier


def score_candidate(candidate: CandidateServer) -> float:
    """
    Compute a 0-100 quality score for a candidate.

    Factors:
    - Registry presence: +30 points
    - Official/Verified classification: +25 points
    - GitHub stars: up to +20 points (log scale)
    - PulseMCP visitors: up to +15 points
    - Has description: +5 points
    - Has install command: +5 points
    """
    score = 0.0

    # Registry presence (strong signal)
    if candidate.registry_published:
        score += 30

    # Official/Verified classification
    if candidate.pulsemcp_official:
        score += 25
    elif candidate.pulsemcp_classification == "reference":
        score += 20
    elif candidate.pulsemcp_classification == "verified":
        score += 15

    # GitHub stars (log scale, capped)
    if candidate.github_stars:
        import math
        score += min(20, 5 * math.log10(max(1, candidate.github_stars)))

    # PulseMCP traffic
    if candidate.pulsemcp_visitors_weekly:
        import math
        score += min(15, 3 * math.log10(max(1, candidate.pulsemcp_visitors_weekly)))

    # Content quality
    if candidate.description and len(candidate.description) > 20:
        score += 5
    if candidate.install_command:
        score += 5

    return min(100, score)


def apply_gate(
    candidate: CandidateServer,
    thresholds: dict | None = None,
) -> GateResult:
    """
    Apply quality gate to a single candidate.

    Returns GateResult with pass/fail, score, and detailed reasons.
    """
    t = thresholds or DEFAULT_THRESHOLDS
    reasons = []
    score = score_candidate(candidate)
    tier = candidate._compute_tier()

    # Automatic passes (strong signals that override thresholds)
    if candidate.pulsemcp_official or candidate.pulsemcp_classification in ("official", "reference"):
        reasons.append(f"PASS: Official/reference classification ({candidate.pulsemcp_classification})")
        return GateResult(candidate, True, score, reasons, tier)

    if candidate.registry_published and candidate.publisher_id in ("modelcontextprotocol", "anthropic"):
        reasons.append("PASS: Anthropic/MCP official publisher")
        return GateResult(candidate, True, score, reasons, tier)

    # Check thresholds
    passed = True

    # Stars check
    if candidate.github_stars is not None and candidate.github_stars < t["min_stars"]:
        reasons.append(f"FAIL: {candidate.github_stars} stars < {t['min_stars']} threshold")
        passed = False
    elif candidate.github_stars and candidate.github_stars >= t["min_stars"]:
        reasons.append(f"OK: {candidate.github_stars} stars >= {t['min_stars']} threshold")

    # No stars at all is a weak signal
    if candidate.github_stars is None or candidate.github_stars == 0:
        reasons.append("WARN: No GitHub star data")
        if t["min_stars"] > 0:
            passed = False

    # PulseMCP visitors
    if candidate.pulsemcp_visitors_weekly and candidate.pulsemcp_visitors_weekly < t["min_pulsemcp_visitors_weekly"]:
        reasons.append(f"WARN: {candidate.pulsemcp_visitors_weekly} weekly visitors < {t['min_pulsemcp_visitors_weekly']}")
        # This alone doesn't fail, just warns

    # Registry requirement
    if t["require_registry_published"] and not candidate.registry_published:
        reasons.append("FAIL: Not in official MCP registry")
        passed = False

    # Official requirement
    if t["require_pulsemcp_official"] and not candidate.pulsemcp_official:
        reasons.append("FAIL: Not PulseMCP official")
        passed = False

    # Must have GitHub URL
    if t["exclude_no_github_url"] and not candidate.github_url:
        reasons.append("FAIL: No GitHub URL")
        passed = False

    # Must have description
    if t["exclude_no_description"] and (not candidate.description or len(candidate.description) < 10):
        reasons.append("FAIL: No meaningful description")
        passed = False

    # Final score-based pass for borderline cases
    if not passed and score >= 60:
        reasons.append(f"OVERRIDE: Score {score:.1f} >= 60, passing despite threshold misses")
        passed = True

    if passed:
        reasons.insert(0, f"PASS: Score {score:.1f}/100, tier={tier}")
    else:
        reasons.insert(0, f"FAIL: Score {score:.1f}/100, tier={tier}")

    return GateResult(candidate, passed, score, reasons, tier)


def gate_batch(
    candidates: list[CandidateServer],
    thresholds: dict | None = None,
    preset: str | None = None,
) -> tuple[list[GateResult], list[GateResult]]:
    """
    Apply quality gate to a batch of candidates.

    Args:
        candidates: List of CandidateServer to evaluate.
        thresholds: Custom threshold dict. Overrides preset.
        preset: One of 'strict', 'balanced', 'lenient'.

    Returns:
        (passed, failed) — two lists of GateResult.
    """
    if thresholds:
        t = thresholds
    elif preset and preset in PRESETS:
        t = PRESETS[preset]
        logger.info(f"Using '{preset}' gate preset")
    else:
        t = DEFAULT_THRESHOLDS
        logger.info("Using default (balanced) gate thresholds")

    passed = []
    failed = []

    for candidate in candidates:
        result = apply_gate(candidate, t)
        if result.passed:
            passed.append(result)
        else:
            failed.append(result)

    logger.info(f"Gate results: {len(passed)} passed, {len(failed)} failed "
                f"(from {len(candidates)} candidates)")

    return passed, failed


def report_gate_results(passed: list[GateResult], failed: list[GateResult]) -> str:
    """Generate a human-readable report of gate results."""
    lines = []
    lines.append("=" * 60)
    lines.append("QUALITY GATE REPORT")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"PASSED: {len(passed)} servers")
    lines.append("-" * 40)

    # Sort by score descending
    for r in sorted(passed, key=lambda x: x.score, reverse=True):
        s = r.candidate
        lines.append(f"  [{r.tier:12s}] {s.name:40s} score={r.score:.1f} stars={s.github_stars or 0}")

    lines.append("")
    lines.append(f"FAILED: {len(failed)} servers")
    lines.append("-" * 40)

    for r in sorted(failed, key=lambda x: x.score, reverse=True)[:20]:  # Show top 20 failures
        s = r.candidate
        fail_reason = [x for x in r.reasons if x.startswith("FAIL")]
        reason = fail_reason[0] if fail_reason else r.reasons[0]
        lines.append(f"  {s.name:40s} score={r.score:.1f} — {reason}")

    if len(failed) > 20:
        lines.append(f"  ... and {len(failed) - 20} more")

    return "\n".join(lines)
