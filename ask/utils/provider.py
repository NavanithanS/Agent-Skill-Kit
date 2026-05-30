"""Skill provider — the read-only core behind the MCP server (`ask mcp serve`).

These are plain functions with NO MCP dependency so they stay unit-testable and
reusable. The MCP layer (`ask/mcp_server.py`) is a thin wrapper that exposes
them as tools. Philosophy: *provider, not installer* — agents pull skill content
on demand and use it inline; nothing is written to the filesystem.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from ask.utils.skill_registry import get_all_skills, get_skill, get_skill_readme
from ask.utils.eval.trigger_scorer import build_index


def _category(skill: Dict) -> str:
    path = skill.get("_path") or ""
    # skills/<category>/<skill-name>
    parts = [p for p in path.replace("\\", "/").split("/") if p]
    return parts[-2] if len(parts) >= 2 else ""


def _summary(skill: Dict) -> Dict:
    """Lightweight catalog entry — no body, safe to list in bulk."""
    return {
        "name": skill.get("name"),
        "description": skill.get("description", ""),
        "category": _category(skill),
        "agents": skill.get("agents", []),
        "triggers": skill.get("triggers", []),
        "version": skill.get("version", ""),
    }


def list_skills_payload() -> List[Dict]:
    """Return the catalog of every skill (metadata only, no body)."""
    skills = sorted(get_all_skills(), key=lambda s: s.get("name") or "")
    return [_summary(s) for s in skills]


def search_skills_payload(query: str, limit: int = 5) -> List[Dict]:
    """Rank skills against a free-text query using the TF-IDF routing index.

    Returns the top `limit` matches with a relevance score. The same lexical
    index that powers `ask test` ranks here, so search and the trigger audit
    agree on what a skill is "about".
    """
    # The index is rebuilt per call (re-reading skills from disk) on purpose:
    # this backs a long-running MCP server where skills can change underneath
    # it, and always-fresh results beat the staleness risk of a cached index.
    # Build cost is small (token counting over a few dozen short docs).
    skills = get_all_skills()
    if not skills:
        return []
    index = build_index(skills)
    by_name = {s.get("name"): s for s in skills}
    ranked = index.score(query)
    results: List[Dict] = []
    for name, score in ranked:
        if score <= 0:
            continue
        skill = by_name.get(name)
        if not skill:
            continue
        entry = _summary(skill)
        entry["score"] = round(score, 4)
        results.append(entry)
        if len(results) >= limit:
            break
    return results


def get_skill_payload(name: str) -> Optional[Dict]:
    """Return a skill's full instruction body so an agent can use it inline.

    Returns None if no skill matches `name`.
    """
    skill = get_skill(name)
    if not skill:
        return None
    payload = _summary(skill)
    payload["content"] = get_skill_readme(skill) or ""
    return payload
