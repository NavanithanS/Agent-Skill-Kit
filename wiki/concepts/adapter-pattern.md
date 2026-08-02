---
title: Adapter Pattern
type: concept
tags: [adapter, architecture, agents, copy]
updated: 2026-08-02
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

Optional overrides:

```python
def install_resources(self, skill, target_dir, dry_run, force) -> Dict:
    """Copy scripts, reference files, etc. alongside the main skill file."""

def install(self, skill) -> Dict:
    """Thin wrapper that delegates to copy_skill(). Override for custom install flows."""

def remove_skill(self, skill, name=None) -> Dict:
    """Remove a skill directory or file. Returns {status, target}."""
```

## Dynamic Loading

Adapters are discovered at runtime via `importlib` in `ask/utils/filesystem.py`. The `get_adapter()` function:
1. Imports `agents.<name>.adapter` dynamically.
2. Constructs the class name from the agent name (e.g., `gemini` → `GeminiAdapter`).
3. Uses `inspect.signature` to check whether the adapter accepts `project_root`.
4. Instantiates and returns the adapter.

This means **adding a new agent requires no changes to core code** — just drop in a new directory with `adapter.py`.

## Safe Copy Protocol (from BaseAdapter)

`copy_skill()` enforces a two-phase check-then-write:

1. **Conflict check on main file** — if `target.exists()` and not `force`, return `{status: "conflict"}`.
2. **Conflict check on resources** — call `install_resources(..., dry_run=True)` and check for conflicts.
3. **Write phase** — only if both checks pass (or `force=True`):
   - Create parent dirs.
   - `transform()` the skill and write.
   - `install_resources(..., dry_run=False)`.

The `dry_run=True` path returns `would_conflict: bool` without touching disk.

## Sidecar Resources

`install_resources()` copies auxiliary files and directories alongside `SKILL.md`. The Antigravity adapter (the most feature-complete implementation) copies these sidecar resources:

```python
["scripts", "reference", "images", "assets", "examples.md",
 "reference.md", "config", "resources", "references", "examples"]
```

> **v0.9.1 fix:** Previously, sidecar resources were always copied with `force=True`, violating the Safe Copy protocol. This was corrected so that `install_resources` now respects the caller's `force` parameter.

## Legacy Path Migration

The `AntigravityAdapter` performs automatic one-time migration on initialization:

| Scope | Legacy path | New path |
|---|---|---|
| Local | `.agent/skills/` | `.agents/skills/` |
| Global | `~/.gemini/antigravity/skills/` | `~/.gemini/config/skills/` |

Migration uses `shutil.move()` and only triggers if the legacy path exists and the new path does not, preventing data loss.

## Version Parsing

`BaseAdapter._parse_skill_version(skill_file)` reads the `version:` field from SKILL.md frontmatter. Returns `"0.0.0"` if missing or unparseable. Used by `list_installed_skills()`.

## Adding a New Adapter

Run `ask add-agent` — this scaffolds the directory and adapter stub. Then implement `get_target_path()` and `transform()`.

See the [ask-add-agent skill](../../skills/tooling/ask-add-agent/) for the guided workflow.
