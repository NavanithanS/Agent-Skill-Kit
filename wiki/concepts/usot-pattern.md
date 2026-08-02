---
title: Universal Source of Truth (USoT)
type: concept
tags: [usot, architecture, symlink, copy, sync]
updated: 2026-08-02
sources: 3
---

# Universal Source of Truth (USoT)

Since v0.5.0, ASK uses a **single canonical location** for all installed skills and **symlinks** from each agent's target directory. This architecture guarantees that a skill installed once stays in sync across all agents without duplication.

## The Pattern

```
.agents/skills/<skill-name>/     ← USoT (one real copy)
    ├── SKILL.md
    ├── scripts/
    └── config/

.claude/skills/<skill-name>/     ← symlink → ../../.agents/skills/<skill-name>/
.gemini/skills/<skill-name>/     ← symlink → ../../.agents/skills/<skill-name>/
.cursor/skills/<skill-name>/     ← symlink → ../../.agents/skills/<skill-name>/
```

## Why It Exists

Before v0.5.0, `ask copy` wrote independent copies to each agent's directory. Problems:
1. **Drift** — updating one agent's copy left others stale.
2. **Disk waste** — the same skill content duplicated N times.
3. **Invisible to `ask update`** — skills synced via `ask sync` bypassed the copy registry entirely.

The USoT eliminates all three: one write, N symlinks, one place to update.

## How It Works

### `ask copy` Flow

1. **Write to USoT** — `UniversalAdapter.copy_skill()` writes the skill to `.agents/skills/<name>/SKILL.md`.
2. **Symlink to agent** — `deploy_skill_link()` creates a relative symlink from the agent's target path back to the USoT directory.
3. **Sidecar resources** — `adapter.install_resources()` copies scripts, config, etc. to the agent's target directory.

```python
# From ask/commands/copy.py
result = universal_adapter.copy_skill(skill, force=overwrite)
u_path = Path(result["target"])

if agent != "universal" and adapter:
    agent_target = adapter.get_target_path(skill, name_to_use)
    deploy_mode = deploy_skill_link(u_path, agent_target)
```

### `deploy_skill_link()` (from `ask/utils/filesystem.py`)

Creates a **relative** symlink (not absolute) for portability:

```python
rel_path = os.path.relpath(usot_path, agent_target.parent)
agent_target.symlink_to(rel_path)
```

**Windows fallback:** On Windows without Developer Mode, `symlink_to()` raises `WinError 1314`. The function catches this specific error and falls back to `shutil.copytree()` / `shutil.copy2()`, returning `"copy"` instead of `"symlink"`.

**Stale link cleanup:** Before creating a new symlink, existing entries (including broken symlinks from deleted skills) are removed automatically.

### `ask sync`

Rewritten in v0.5.1 to route through the USoT. `ask sync all` copies every skill to USoT first, then symlinks to each agent — matching the `ask copy` architecture.

### `ask purge`

Removes skills from both the agent symlink **and** the USoT directory (if requested).

### `ask update`

Detects version deltas by comparing the USoT-installed version against the library version, then overwrites in-place.

## Universal Adapter

The `UniversalAdapter` (`agents/universal/adapter.py`) is the adapter that targets the USoT. Its `target_dir` is always `.agents/skills/`. It is used as the first-stage writer in all multi-agent copy flows.

## Relationship to Other Concepts

- **[Adapter Pattern](adapter-pattern.md)** — Each adapter's `get_target_path()` returns where the symlink should point. The USoT is where the real file lives.
- **[Safe Copy Protocol](adapter-pattern.md#safe-copy-protocol-from-baseadapter)** — Conflict checks happen at the USoT level first, then at the agent level.
