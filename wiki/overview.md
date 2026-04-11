---
title: Agent Skill Kit — Overview
type: overview
tags: [architecture, cli, skills, adapters]
updated: 2026-04-06
sources: 5
---

# Agent Skill Kit (ASK)

**ASK** is a CLI tool (`ask`) that acts as a package manager for AI agent skills. It manages a central library of reusable skill definitions and deploys them to multiple AI agents in their native formats.

## Core Metaphor

Think of ASK like `npm` or `pip`, but for AI agent instructions:
- The **skill library** (`skills/`) is the registry.
- Each **adapter** knows how to install a skill into a specific agent.
- The **`ask copy`** command is the install step.

## Supported Agents

| Agent | Target path | Format |
|---|---|---|
| `claude` | `.claude/` | SKILL.md files |
| `gemini` | `.gemini/` | Gemini-native format |
| `cursor` | `.cursorrules` area | Cursor rules format |
| `codex` | `.codex/` | Codex format |
| `antigravity` | custom | custom |
| `universal` | `.agents/` | Generic fallback |

## Skill Library Structure

Skills live in `skills/<category>/<skill-name>/`. Categories: `coding/`, `planning/`, `tooling/`, `workflows/`.

Each skill directory (Gold Standard format):
```
skills/coding/ask-code-reviewer/
├── skill.yaml     # Metadata: name, version, agents, depends_on
├── SKILL.md       # Instructions with YAML frontmatter
├── scripts/       # Optional helper scripts
└── tests/         # Optional tests
```

## Key Data Flow

```
ask copy <skill> [--agent <name>]
   └─ Command (ask/commands/)
       └─ SkillRegistry.get_skill()
           └─ AgentRegistry
               └─ FileSystem.get_adapter()   ← dynamic importlib load
                   └─ Adapter.copy_skill()   ← safe copy protocol
```

## Safe Copy Protocol

`BaseAdapter.copy_skill()` enforces:
1. Never overwrite existing files unless `--force`.
2. Detect conflicts before writing anything.
3. Support `--dry-run` to preview without writing.
4. `new_name` parameter for conflict resolution.

See [adapter-pattern.md](concepts/adapter-pattern.md) for details.

## Skill Count (as of 2026-04-06)

| Category | Count |
|---|---|
| coding | ~25 |
| planning | ~5 |
| tooling | ~10 |
| **Total** | **~40** |

See [skills-catalog.md](skills-catalog.md) for the full list.
