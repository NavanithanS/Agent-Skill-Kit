---
title: Skill
type: entity
tags: [skill, library, yaml, SKILL.md, frontmatter]
updated: 2026-04-06
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
└── tests/         # Tests (required for validation gate)
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
| `workflows/` | Multi-step process skills |

## Lifecycle

1. **Author** — create skill dir, write `skill.yaml` + `SKILL.md`.
2. **Validate** — `ask validate` checks structure; `ask skill lint` checks token limits.
3. **Deploy** — `ask copy <skill>` deploys to an agent via the appropriate adapter.
4. **Update** — bump `version` in `skill.yaml`; `ask copy` detects version delta.

## Dependency Resolution

`SkillRegistry` resolves `depends_on` chains with cycle detection. A skill won't install unless its dependencies are satisfied.

## Token Limits

`ask/utils/token_analyzer.py` enforces per-skill-type token limits via `tiktoken`. `ask skill lint` surfaces violations.

See [skills-catalog.md](../skills-catalog.md) for all available skills.
