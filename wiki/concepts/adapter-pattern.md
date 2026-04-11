---
title: Adapter Pattern
type: concept
tags: [adapter, architecture, agents, copy]
updated: 2026-04-06
sources: 3
---

# Adapter Pattern

The adapter layer translates a skill from the canonical library format into whatever format a specific agent expects. Each agent has exactly one adapter.

## Class Hierarchy

```
agents/base.py :: BaseAdapter (ABC)
    ├── agents/claude/adapter.py
    ├── agents/gemini/adapter.py
    ├── agents/cursor/adapter.py
    ├── agents/codex/adapter.py
    ├── agents/antigravity/adapter.py
    └── agents/universal/adapter.py
```

## Required Interface

Every adapter must implement:

```python
def get_target_path(self, skill: Dict, name: str = None) -> Path:
    """Where to write the skill file for this agent."""

def transform(self, skill: Dict) -> str:
    """Convert skill dict → agent-native string content."""
```

Optional override:

```python
def install_resources(self, skill, target_dir, dry_run, force) -> Dict:
    """Copy scripts, reference files, etc. alongside the main skill file."""
```

## Dynamic Loading

Adapters are discovered at runtime via `importlib` in `ask/utils/filesystem.py`. The filesystem scanner looks for `agents/*/adapter.py` files and imports them. This means **adding a new agent requires no changes to core code** — just drop in a new directory with `adapter.py`.

## Safe Copy Protocol (from BaseAdapter)

`copy_skill()` enforces a two-phase check-then-write:

1. **Conflict check on main file** — if `target.exists()` and not `force`, return `{status: "conflict"}`.
2. **Conflict check on resources** — call `install_resources(..., dry_run=True)` and check for conflicts.
3. **Write phase** — only if both checks pass (or `force=True`):
   - Create parent dirs.
   - `transform()` the skill and write.
   - `install_resources(..., dry_run=False)`.

The `dry_run=True` path returns `would_conflict: bool` without touching disk.

## Version Parsing

`BaseAdapter._parse_skill_version(skill_file)` reads the `version:` field from SKILL.md frontmatter. Returns `"0.0.0"` if missing or unparseable. Used by `list_installed_skills()`.

## Adding a New Adapter

Run `ask add-agent` — this scaffolds the directory and adapter stub. Then implement the three methods above.

See [ask-add-agent skill](../entities/skill-add-agent.md) for the guided workflow.
