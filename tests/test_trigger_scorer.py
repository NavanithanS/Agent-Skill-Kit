"""Tests for the offline trigger/collision audit (Layer 1 of `ask test`)."""

import pytest

from ask.utils.eval.trigger_scorer import (
    build_index,
    run_trigger_audit,
    DEFAULT_COLLISION_MARGIN,
)


@pytest.fixture
def skills():
    return [
        {
            "name": "laravel-architect",
            "description": "Scaffold new Laravel APIs with models and migrations.",
            "triggers": ["new laravel api", "scaffold laravel", "laravel migration"],
            "_path": None,
        },
        {
            "name": "laravel-mechanic",
            "description": "Debug and fix existing Laravel apps and broken queries.",
            "triggers": ["fix laravel", "debug eloquent", "laravel error"],
            "_path": None,
        },
        {
            "name": "docker-expert",
            "description": "Optimize Docker images and multi-stage container builds.",
            "triggers": ["dockerfile", "docker compose", "container build"],
            "_path": None,
        },
    ]


def test_index_ranks_relevant_skill_first(skills):
    index = build_index(skills)
    ranked = index.score("optimize my dockerfile multi-stage build")
    assert ranked[0][0] == "docker-expert"
    assert ranked[0][1] > 0


def test_unrelated_prompt_scores_low(skills):
    index = build_index(skills)
    ranked = dict(index.score("write a haiku about the ocean"))
    # No shared vocabulary -> every skill scores zero.
    assert all(score == 0.0 for score in ranked.values())


def test_score_is_deterministic(skills):
    index = build_index(skills)
    prompt = "scaffold a new laravel api"
    assert index.score(prompt) == index.score(prompt)


def test_ranking_is_stably_sorted(skills):
    """Equal scores must tie-break by name so output is reproducible."""
    index = build_index(skills)
    ranked = index.score("xyzzy nonsense")  # all zero
    names = [n for n, _ in ranked]
    assert names == sorted(names)


def _with_evals(skill, prompts):
    return {**skill, "should_fire": prompts}


def test_audit_detects_sibling_collision(monkeypatch, skills):
    """Architect and mechanic share 'laravel' vocabulary -> they should collide."""
    laravel_skills = [s for s in skills if "laravel" in s["name"]]

    def fake_load_evals(skill):
        if skill["name"] == "laravel-mechanic":
            return {"should_fire": ["fix my broken laravel eloquent query"]}
        return None

    monkeypatch.setattr(
        "ask.utils.eval.trigger_scorer.load_evals", fake_load_evals
    )
    report = run_trigger_audit(skills, margin=0.5)
    assert report.total_prompts == 1
    result = report.results[0]
    assert result.skill == "laravel-mechanic"
    # The architect sibling competes for the same prompt.
    competitors = [c for c, _ in result.collisions]
    assert "laravel-architect" in competitors


def test_buckets_partition_results(monkeypatch, skills):
    def fake_load_evals(skill):
        if skill["name"] == "docker-expert":
            return {"should_fire": ["optimize my dockerfile build", "irrelevant zzz"]}
        return None

    monkeypatch.setattr(
        "ask.utils.eval.trigger_scorer.load_evals", fake_load_evals
    )
    report = run_trigger_audit(skills)
    # clear + contested + misses must cover every result exactly once.
    total = len(report.clean) + len(report.contested) + len(report.misses)
    assert total == report.total_prompts


def test_default_margin_is_sane():
    assert 0 < DEFAULT_COLLISION_MARGIN < 1
