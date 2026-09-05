# Wiki Schema

This document governs how the LLM maintains this wiki. Read it at the start of every session before touching any wiki file.

## Purpose

A persistent, compounding knowledge base for the {{PROJECT_NAME}} project. It captures architecture decisions, entity definitions, concept pages, and a running log of changes — so context accumulates rather than being re-derived from the codebase each session. It is **not** a substitute for the code — it explains the *why*, the *how things connect*, and the *things to watch out for*.

## Raw sources

If this project contains raw documentation (e.g. `docs/`, API references, issues), do **not** modify them. The wiki's job is to *synthesize* them, not duplicate them. Write wiki pages from the perspective of "what does the developer need to know."

## Directory Layout

```
wiki/
├── SCHEMA.md           # This file — LLM conventions
├── index.md            # Content catalog (update on every change)
├── log.md              # Append-only chronological record
├── overview.md         # High-level project orientation
├── architecture/       # System architecture and patterns
├── modules/            # Domain modules and feature areas
├── entities/           # Data models and domain entities
├── integrations/       # External services and APIs
└── decisions/          # Architectural decisions and trade-offs
```

New pages go into the most fitting subfolder. When adding a page, also add it to `index.md`.

## Page Format

Every wiki page (except SCHEMA.md and log.md) must start with YAML frontmatter:

```yaml
---
title: Page Title
type: concept | entity | decision | overview | architecture | module | integration
tags: [comma, separated]
updated: YYYY-MM-DD
sources:
  - path/to/source/file.php
---
```

Body conventions:
- Lead with a one-paragraph summary (used in index.md).
- Use `##` sections for subsections.
- Cross-references use standard relative markdown links `[folder/page](folder/page.md)`.
- Code blocks for schema snippets, field names, or config examples.
- Mark uncertainty: use "unclear", "TBD", or "investigate" rather than stating guesses as facts.
- Mark surprising or non-obvious information with **Note:** or **Gotcha:**.
- **Every page MUST end with a `## See also` section** containing standard markdown links to related pages. This creates an interconnected knowledge graph.

## Conventions

- **index.md** — must be formatted as markdown tables: `| Page | Summary |`, grouped by category. Update on every ingest or page creation.
- **log.md** — append only. Entry format: `## [YYYY-MM-DD] <action> | <subject>`. Actions: `ingest`, `query`, `update`, `lint`, `bootstrap`.
- **Cross-references** — always use standard relative markdown links. When adding a concept, link back from related pages.
- **Contradictions** — when new info conflicts with a page, mark the old claim with `> **Superseded:** ...` and add the updated claim below.
- **Orphans** — every page must be linked from index.md. Run a lint check if unsure.
- **See also** — every content page must end with `## See also` containing links to related pages.

## Naming Rules

- Page filenames: `kebab-case.md` (e.g., `request-flow.md`, `multi-tenancy.md`)
- Entity pages: named after the model (e.g., `Meter`, not `meters`)
- Concept pages: descriptive noun phrase (e.g., `Command State Machine`)
- Do not create pages for things fully described by a few sentences on another page — inline them instead.

## Workflows

### Adding a new page
1. Write the page with frontmatter.
2. Add it to `index.md` under the right category.
3. Append an `ingest` or `update` entry to `log.md`.
4. Add cross-links from related pages.
5. Add a `## See also` section at the bottom.

### Answering a query
1. Read `index.md` to find relevant pages.
2. Read those pages and synthesize.
3. If the answer is non-trivial, file it as a new page (type: `decision` or `concept`).
4. Append a `query` entry to `log.md`.

### Lint pass
Check for: orphan pages, stale claims, missing cross-references, broken markdown links, concepts mentioned but lacking their own page, pages missing `## See also`, missing or outdated frontmatter.

## Domain Conventions — {{PROJECT_NAME}}

*(Agent: Replace this section with project-specific domain knowledge. List primary entities, key concepts, and integrations as shown below. This acts as a roadmap for future agents.)*

**Primary entities** (each gets its own page):
- `{{Entity1}}` — description
- `{{Entity2}}` — description

**Key concepts** (each gets its own page):
- `{{Concept1}}` — description

**Integrations**:
- `{{Integration1}}` — description

## Source of truth (anti-drift)

When documenting stack facts, **prefer code over README/wiki memory**:

| Fact | Source of truth |
|------|-----------------|
| {{DYNAMIC_FACT_1}} | {{DYNAMIC_SOURCE_1}} |
| {{DYNAMIC_FACT_2}} | {{DYNAMIC_SOURCE_2}} |

*(Agent: Replace the table above with 5-10 project-specific facts and their definitive file locations in this codebase. E.g. "PHP version" → "`composer.json` → `require.php`")*

If wiki and code disagree, **update the wiki** (or fix the code if the wiki was intentional).
