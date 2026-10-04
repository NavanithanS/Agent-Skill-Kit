---
title: Skill
type: entity
tags: [skill, library, yaml, SKILL.md, frontmatter]
updated: 2026-10-04
sources: 4
---

# Skill

A **skill** is the core unit of ASK — a reusable, versioned instruction set for an AI agent. Skills live in the central library and can be deployed to one or more agents.

## Directory Structure (Gold Standard)

```
skills/<category>/<skill-name>/
├── skill.yaml     # Machine-readable metadata
├── SKILL.md       # Human+LLM instruction file
├── scripts/       # Helper scripts (required for validation gate)
├── tests/         # Tests (required for validation gate)
│   └── evals.yaml # Trigger audit prompts for `ask test`
├── config/        # Optional sidecar configuration
└── resources/     # Optional reference materials
```

## skill.yaml Fields

```yaml
name: ask-code-reviewer
version: 1.2.0
agents: [claude, gemini]       # which agents this targets
depends_on: []                  # other skill names (resolved by SkillRegistry)
```

## SKILL.md Frontmatter

```markdown
---
name: ask-code-reviewer
description: Brief description of what the skill does
triggers: ["review my code", "check this PR"]
---

# Skill content here...
```

## Naming Convention

- **kebab-case**, 2–50 characters.
- All library skills are prefixed with `ask-` by convention.
- Validated by `ask/utils/validators.py`.

## Categories

| Category | Purpose |
|---|---|
| `coding/` | Language/framework-specific dev skills |
| `planning/` | Architecture, ADRs, project management |
| `tooling/` | Meta-skills (skill creation, context, auditing) |

These three are the only categories `validate_category()` (`ask/utils/validators.py`) accepts. `workflows/` was removed in `6b8fcf4`.

## Lifecycle

1. **Author** — create skill dir, write `skill.yaml` + `SKILL.md`.
2. **Validate** — `ask validate` checks structure; `ask skill lint` checks token limits.
3. **Eval** — `ask test` audits trigger collisions via `tests/evals.yaml`.
4. **Deploy** — `ask copy <skill>` deploys locally; `ask install <url>` fetches from remote registries.
5. **Update** — bump `version` in `skill.yaml`; `ask copy` detects version delta.

## Dependency Resolution

`SkillRegistry` resolves `depends_on` chains with cycle detection. `ask copy` installs the dependencies first, and `ask validate` fails on a missing or circular dependency.

> **Known gap (2026-10-04):** only `ask copy` resolves dependencies. `ask update` (`ask/commands/update.py`) overwrites each installed skill alone, and MCP `get_skill` returns one skill. So a skill that gains a `depends_on` in a new version reaches existing users without its dependency. Until that is fixed, a dependent `SKILL.md` must still work alone: put the key rules inline and use the dependency for the full detail. First real use: `ask-explaining-code` → `ask-ste-writing`.

## Token Limits

`ask/utils/token_analyzer.py` enforces per-skill-type token limits via `tiktoken`. `ask skill lint` surfaces violations.

See [skills-catalog.md](../skills-catalog.md) for all available skills.
