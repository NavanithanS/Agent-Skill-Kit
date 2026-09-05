---
title: Skills Catalog
type: overview
tags: [skills, catalog, library]
updated: 2026-09-05
sources: 1
---

# Skills Catalog

All skills in `skills/` as of 2026-09-05. Total: **42** registered skills across **3** populated categories (`coding/` 26, `planning/` 6, `tooling/` 10).

> **Superseded:** an earlier lint pass recorded `workflows/` as holding 1 skill.
> It holds none — see below.

## coding/ (26 skills)

| Skill | Description |
|---|---|
| ask-bug-finder | Systematic bug hunting and debugging best practices |
| ask-code-reviewer | AI code reviewer with constructive feedback |
| ask-commit-assistance | Code review and staging helper (never auto-commits) |
| ask-component-scaffolder | Standardizes UI component creation with consistent folder structure |
| ask-conceptual-integrity-sentinel | Audits repos for architectural drift and bloated abstractions |
| ask-db-migration-assistant | Safe database schema updates requiring migration + rollback scripts |
| ask-docker-expert | Docker, Docker Compose, and container optimization |
| ask-effective-llm-coder | Guides effective LLM-assisted coding with declarative workflows |
| ask-explaining-code | Explains code with analogies, ASCII diagrams, step-by-step walkthroughs |
| ask-fastapi-architect | FastAPI scaffolding with Pydantic V2 and async patterns |
| ask-flutter-architect | Flutter scaffolding using FVM, Provider, Layer-First Architecture |
| ask-flutter-mechanic | Flutter maintenance — clean builds, iOS/Android fixes, asset gen |
| ask-impact-sentinel | Impact analysis, breaking change detection, strategic DB design |
| ask-laravel-architect | Laravel scaffolding with SQL/Mongo, SoftDeletes, strict API standards |
| ask-laravel-mechanic | Laravel maintenance with Zero Data Loss policy |
| ask-nextjs-architect | Next.js 14+ App Router — Server Components, Server Actions, SEO |
| ask-owasp-security-review | Static security review against OWASP Top 10 |
| ask-python-refactor | Python code refactoring best practices |
| ask-readme-gardener | Keeps README in sync with code changes |
| ask-refactoring-readability | Refactoring for readability: DRY, meaningful names, modularization |
| ask-security-sentinel | Pre-flight secret scanning and vulnerable pattern detection |
| ask-shadcn-architect | shadcn/ui patterns, imports, and CLI usage enforcement |
| ask-shadcn-mechanic | shadcn/ui maintenance and fixes |
| ask-unit-test-generation | Comprehensive unit test generation with edge case coverage |
| ask-vue-architect | Vue 3 scaffolding for Laravel Inertia and Nuxt/Vite stacks |
| ask-vue-mechanic | Vue 3 maintenance — navigation reloads, prop mismatches |

## planning/ (6 skills)

| Skill | Description |
|---|---|
| ask-adr-logger | Records Architectural Decision Records automatically |
| ask-brainstorm | Explores intent, requirements, and design before implementation |
| ask-buildmaster | Epic orchestration — PM + Tech Lead + Delivery Manager |
| ask-hold-code | Planning-mode lock preventing code generation until approved |
| ask-project-memory | Maintains a Project Brain with architecture decisions |
| ask-solution-architect | Senior solution architecture guidance |

## tooling/ (10 skills)

| Skill | Description |
|---|---|
| ask-add-agent | Guide for adding new AI code editor support to ASK |
| ask-ast-mapper | Read-only subagent for generating AST dependency maps |
| ask-context-janitor | Aggressive token optimizer and context summarizer |
| ask-parallel-auditor | Splits repos into chunks and runs parallel audit subagents |
| ask-pdf-processing | PDF text extraction, form filling, and merging |
| ask-skill-capture | Meta-skill: saves current session's lessons as a reusable skill |
| ask-skill-creator | Teaches agents how to create new ASK skills |
| ask-smart-booking-test | Autonomous end-to-end booking flow testing |
| ask-system-architect-prime | Repo audits, complexity analysis, refactoring recommendations |
| ask-wiki-init | Scaffolds the LLM Wiki pattern into any project |

## workflows/ (0 registered skills)

`skills/workflows/skill-creator/` contains only `workflow.md` — **no `skill.yaml`
and no `SKILL.md`** — so `SkillRegistry` does not register it and it is absent
from `skills/manifest.json` (which holds 42, not 43). It duplicates the real
`tooling/ask-skill-creator`.

It is excluded from the Jekyll build so it does not publish as an orphan page,
but the directory itself is unresolved: it should either be deleted or promoted
into a proper skill. See [concepts/site-and-seo.md](concepts/site-and-seo.md).
