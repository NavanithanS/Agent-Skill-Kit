# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

**Agent Skill Kit (ASK)** is a CLI tool (`ask`) that acts as a package manager for AI agent skills. It manages reusable skill definitions in a central library (`skills/`) and deploys them to multiple AI agents (Claude, Gemini, Cursor, Codex, Antigravity) in their native formats via an adapter pattern.

## Commands

```bash
# Development installation
pip install -e ".[dev]"

# Run all tests
pytest tests/

# Run a single test file
pytest tests/test_adapters.py

# Run with coverage
pytest tests/ --cov=ask --cov-report=xml

# Validate skill library
ask validate

# Install remote skills
ask install <url>

# Lint skills for token limits
ask skill lint

# Compile skill manifest
ask skill compile
```

## Architecture

**Layers (top to bottom):**

1. **CLI** (`ask/cli.py`) — Click entry point, registers all subcommands
2. **Commands** (`ask/commands/`) — One module per command; each orchestrates registries + adapters
3. **Registries** (`ask/utils/skill_registry.py`, `ask/utils/agent_registry.py`) — Discover and parse skills/agents from the filesystem
4. **Adapters** (`agents/*/adapter.py`) — Transform and deploy skills to agent-specific formats; all extend `agents/base.py`

**Key data flow for `ask copy`:**
`Command → SkillRegistry.get_skill() → AgentRegistry → FileSystem.get_adapter() → Adapter.copy_skill()`

**Adapter loading** is dynamic via `importlib` in `filesystem.py` — it scans `agents/` for `adapter.py` files at runtime.

**Skill library structure** (Gold Standard format):
```
skills/<category>/<skill-name>/
├── skill.yaml     # Metadata: name, version, agents, depends_on
├── SKILL.md       # Instruction file with YAML frontmatter + content
├── scripts/       # (Required for validation gate)
└── tests/         # (Required for validation gate)
```

**SKILL.md frontmatter format:**
```markdown
---
name: skill-name
description: Brief description
triggers: ["phrase 1", "phrase 2"]
---
```

**Adding a new agent adapter:** Run `ask add-agent` to scaffold the adapter, then implement `get_target_path()`, `transform()`, and `install_resources()` in the new `agents/<name>/adapter.py`.

## Key Files

- `ask/utils/skill_registry.py` — Skill discovery, YAML parsing, dependency resolution (with cycle detection)
- `ask/utils/filesystem.py` — Dynamic adapter loading, safe file I/O
- `agents/base.py` — `BaseAdapter` abstract class with safe copy protocol (conflict detection, backup)
- `ask/utils/token_analyzer.py` — Token counting via tiktoken; enforces per-skill-type limits
- `ask/utils/validators.py` — Validates skill names (kebab-case, 2–50 chars), categories, versions
- `~/.askconfig.yaml` — Optional user config for defaults (not in repo)

## Skill Name Convention

Skill names must be kebab-case, 2–50 characters. Category dirs are `coding/`, `planning/`, `tooling/`, `workflows/`.

## Knowledge Base (Wiki)

This repository maintains a persistent LLM-driven knowledge base in the `wiki/` directory.
- **Fetch & Reference:** Before making architectural decisions, researching project patterns, or answering complex codebase questions, ALWAYS read `wiki/index.md` first to discover relevant context.
- **Proactive Updates:** Whenever you learn new context, resolve a complex bug, establish a new convention, or ingest new requirements, you MUST proactively update the relevant `wiki/` pages (or create new ones) and append an entry to `wiki/log.md`.
