# Wiki Schema

This document governs how the LLM maintains this wiki. Follow it consistently across all sessions.

## Purpose

A persistent, compounding knowledge base for the Agent Skill Kit (ASK) project. It captures architecture decisions, entity definitions, concept pages, and a running log of changes — so context accumulates rather than being re-derived from the codebase each session.

## Directory Layout

```
wiki/
├── SCHEMA.md           # This file — LLM conventions
├── index.md            # Content catalog (update on every change)
├── log.md              # Append-only chronological record
├── overview.md         # High-level project orientation
├── concepts/           # How things work (patterns, mechanisms)
├── entities/           # What things are (skills, adapters, agents)
└── decisions/          # Architectural decisions and trade-offs
```

## Page Frontmatter

Every wiki page (except SCHEMA.md and log.md) must start with YAML frontmatter:

```markdown
---
title: Page Title
type: concept | entity | decision | overview
tags: [comma, separated]
updated: YYYY-MM-DD
sources: 1          # number of codebase areas this synthesizes
---
```

## Conventions

- **index.md** — one line per page: `- [Title](path.md) — one-line summary`. Update on every ingest or page creation.
- **log.md** — append only. Entry format: `## [YYYY-MM-DD] <action> | <subject>`. Actions: `ingest`, `query`, `update`, `lint`.
- **Cross-references** — always use relative markdown links. When adding a concept, link back from related pages.
- **Contradictions** — when new info conflicts with a page, mark the old claim with `> **Superseded:** ...` and add the updated claim below.
- **Orphans** — every page must be linked from index.md. Run a lint check if unsure.

## Workflows

### Adding a new page
1. Write the page with frontmatter.
2. Add it to `index.md` under the right category.
3. Append an `ingest` or `update` entry to `log.md`.
4. Add cross-links from related pages.

### Answering a query
1. Read `index.md` to find relevant pages.
2. Read those pages and synthesize.
3. If the answer is non-trivial, file it as a new page (type: `decision` or `concept`).
4. Append a `query` entry to `log.md`.

### Lint pass
Check for: orphan pages, stale claims, missing cross-references, concepts mentioned without their own page.
