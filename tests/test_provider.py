"""Tests for the read-only skill provider behind `ask mcp serve`."""

import pytest

from ask.utils import provider


@pytest.fixture
def fake_skills(monkeypatch):
    skills = [
        {
            "name": "ask-fastapi-architect",
            "description": "Scaffold FastAPI services with Pydantic v2.",
            "triggers": ["new fastapi service", "pydantic model", "async endpoint"],
            "agents": ["claude", "gemini"],
            "version": "1.0.0",
            "_path": "skills/coding/ask-fastapi-architect",
            "_instruction_file": "skills/coding/ask-fastapi-architect/SKILL.md",
        },
        {
            "name": "ask-docker-expert",
            "description": "Optimize Docker images and multi-stage builds.",
            "triggers": ["dockerfile", "docker compose", "container"],
            "agents": ["claude"],
            "version": "1.0.0",
            "_path": "skills/tooling/ask-docker-expert",
            "_instruction_file": "skills/tooling/ask-docker-expert/SKILL.md",
        },
    ]
    by_name = {s["name"]: s for s in skills}
    monkeypatch.setattr(provider, "get_all_skills", lambda *a, **k: skills)
    monkeypatch.setattr(provider, "get_skill", lambda n: by_name.get(n))
    monkeypatch.setattr(
        provider, "get_skill_readme", lambda s: f"# {s['name']}\nbody"
    )
    return skills


def test_list_payload_is_metadata_only(fake_skills):
    items = provider.list_skills_payload()
    assert len(items) == 2
    first = items[0]
    assert set(first) == {"name", "description", "category", "agents", "triggers", "version"}
    assert "content" not in first  # listing must not ship bodies


def test_category_derived_from_path(fake_skills):
    cats = {i["name"]: i["category"] for i in provider.list_skills_payload()}
    assert cats["ask-fastapi-architect"] == "coding"
    assert cats["ask-docker-expert"] == "tooling"


def test_search_ranks_relevant_skill_first(fake_skills):
    results = provider.search_skills_payload("optimize my dockerfile build", limit=5)
    assert results
    assert results[0]["name"] == "ask-docker-expert"
    assert results[0]["score"] > 0


def test_search_respects_limit(fake_skills):
    results = provider.search_skills_payload("fastapi pydantic async", limit=1)
    assert len(results) <= 1


def test_search_drops_zero_score_matches(fake_skills):
    results = provider.search_skills_payload("completely unrelated zzz", limit=5)
    assert results == []


def test_get_skill_includes_body(fake_skills):
    payload = provider.get_skill_payload("ask-fastapi-architect")
    assert payload is not None
    assert payload["name"] == "ask-fastapi-architect"
    assert payload["content"].startswith("# ask-fastapi-architect")


def test_get_skill_unknown_returns_none(fake_skills):
    assert provider.get_skill_payload("does-not-exist") is None


def test_serve_without_mcp_dep_prints_friendly_hint(monkeypatch):
    """Missing optional `mcp` dep must yield the install hint, not a traceback.

    The dep is imported lazily inside run_server(), so the guard has to wrap the
    call — this regression-tests that scope. Also checks the `[mcp]` extra isn't
    swallowed as Rich markup.
    """
    import builtins

    from click.testing import CliRunner
    from ask.commands.mcp_cmd import serve

    real_import = builtins.__import__

    def blocked_import(name, *args, **kwargs):
        if name == "mcp" or name.startswith("mcp."):
            raise ImportError("No module named 'mcp'")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked_import)
    result = CliRunner().invoke(serve, [])

    assert result.exit_code == 1
    assert "agent-skill-kit[mcp]" in result.output  # extra not eaten by markup
    # SystemExit is expected; any other exception means an escaped traceback.
    assert result.exception is None or isinstance(result.exception, SystemExit)
