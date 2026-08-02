---
title: Agent Skill Kit — Overview
type: overview
tags: [architecture, cli, skills, adapters]
updated: 2026-08-02
sources: 5
---

# Agent Skill Kit (ASK)

**ASK** is a CLI tool (`ask`) that acts as a package manager for AI agent skills. It manages a central library of reusable skill definitions and deploys them to multiple AI agents in their native formats. Current version: **v0.9.1**.

## Core Metaphor

Think of ASK like `npm` or `pip`, but for AI agent instructions:
- The **skill library** (`skills/`) is the registry.
- Each **adapter** knows how to install a skill into a specific agent.
- The **Universal Source of Truth** (`.agents/skills/`) holds one copy; agents get symlinks.
- The **`ask copy`** command is the install step; **`ask install`** fetches from remote registries.

## Supported Agents

| Agent | Local target | Global target | Format |
|---|---|---|---|
| `claude` | `.claude/skills/` | — | SKILL.md files |
| `gemini` | `.gemini/skills/` | — | Gemini-native format |
| `cursor` | `.cursorrules` area | — | Cursor rules format |
| `codex` | `.codex/skills/` | — | Codex format |
| `antigravity` | `.agents/skills/<name>/SKILL.md` | `~/.gemini/config/skills/<name>/SKILL.md` | YAML frontmatter + Markdown |
| `universal` | `.agents/skills/` | — | Generic fallback (USoT) |

## Skill Library Structure

Skills live in `skills/<category>/<skill-name>/`. Categories: `coding/`, `planning/`, `tooling/`, `workflows/`.

Each skill directory (Gold Standard format):
```
skills/coding/ask-code-reviewer/
├── skill.yaml     # Metadata: name, version, agents, depends_on
├── SKILL.md       # Instructions with YAML frontmatter
├── scripts/       # Optional helper scripts
├── tests/         # Optional tests; tests/evals.yaml drives `ask test` (trigger audit)
└── config/        # Optional sidecar config (copied alongside SKILL.md)
```

## Key Data Flow

```
ask copy <skill> [--agent <name>]
   └─ Command (ask/commands/copy.py)
       └─ SkillRegistry.get_skill()
           └─ AgentRegistry
               └─ FileSystem.get_adapter()   ← dynamic importlib load
                   └─ Adapter.copy_skill()   ← safe copy protocol
                       └─ deploy_skill_link()  ← symlink USoT → agent
```

## CLI Commands (15 registered)

| Command | Purpose |
|---|---|
| `ask copy` | Deploy skills to agent directories (with fuzzy matching, stack detection) |
| `ask install <url>` | Clone and install skills from remote Git registries |
| `ask sync` | Sync all skills across agents via USoT |
| `ask update` | Update installed skills to newer versions |
| `ask remove` | Remove a skill from an agent |
| `ask purge` | Interactively bulk-remove skills |
| `ask create` | Scaffold a new skill directory |
| `ask list` | List available skills (with `--search` and category/agent filtering) |
| `ask validate` | Check skill structure, dependencies, and integrity |
| `ask wizard` | Interactive guided workflow for all operations |
| `ask add-agent` | Scaffold a new agent adapter directory |
| `ask skill lint\|profile\|compile` | Token analysis, profiling, manifest generation |
| `ask rules compile` | Compile rules from `.agents/rules/` to agent formats |
| `ask test` | Trigger/collision audit (TF-IDF Layer 1) + behavior eval (Layer 2, stubbed) |
| `ask mcp serve\|tools\|probe` | Run MCP server for runtime skill discovery |

## Safe Copy Protocol

`BaseAdapter.copy_skill()` enforces:
1. Never overwrite existing files unless `--force`.
2. Detect conflicts before writing anything.
3. Support `--dry-run` to preview without writing.
4. `new_name` parameter for conflict resolution.

See [adapter-pattern.md](concepts/adapter-pattern.md) for details.

## Skill Count (as of 2026-08-02)

| Category | Count |
|---|---|
| coding | 26 |
| planning | 6 |
| tooling | 10 |
| workflows | 1 |
| **Total** | **42** |

See [skills-catalog.md](skills-catalog.md) for the full list.
