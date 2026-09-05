# Wiki Index

Content catalog for the Agent Skill Kit wiki. Updated on every page addition or change.

## Overview

- [overview.md](overview.md) — **High-level project orientation**. Provides a comprehensive introduction to ASK (v0.9.1), including its core "package manager" metaphor, the 6 supported AI agent targets (Claude, Gemini, Cursor, Codex, Antigravity, Universal), all 15 CLI commands and their purposes, the core data flow, the safe copy protocol, and a summary of the 42 currently available skills.

## Concepts

- [concepts/adapter-pattern.md](concepts/adapter-pattern.md) — **The Adapter Pattern**. Explains the `BaseAdapter` interface and how ASK transforms generic skills into agent-specific formats. Covers the dynamic loading mechanism, the Safe Copy protocol, how sidecar resources (scripts/configs) are handled, and legacy path migration.
- [concepts/usot-pattern.md](concepts/usot-pattern.md) — **Universal Source of Truth (USoT)**. Details the v0.5.0 architecture shift from duplicating skills across agent folders to a single-write + symlink pattern. Explains how `ask copy`, `ask sync`, and `ask purge` utilize this architecture.
- [concepts/release-protocol.md](concepts/release-protocol.md) — **Release Management Checklist**. A step-by-step guide for maintaining consistency during version bumps. Covers updating Python files, pyproject.toml, Homebrew formulas, CHANGELOG, manifest.json, and README.md.
- [concepts/eval-harness.md](concepts/eval-harness.md) — **Skill Evaluation (`ask test`)**. Explains the two-layer evaluation system: Layer 1 (offline TF-IDF lexical collision audit) and Layer 2 (live LLM-as-judge behavioral evaluation). Covers the `tests/evals.yaml` format and the underlying TF-IDF index.
- [concepts/site-and-seo.md](concepts/site-and-seo.md) — **Pages Site & Search Discoverability**. How the GitHub Pages site is actually built by *two* pipelines (Jekyll from the repo root, plus `scripts/generate_site.py`), which files are generated and must never be hand-edited (`docs/index.html`, `skills/README.md`, the README `SKILLS` block), why `_config.yml`'s `exclude:` list is large, the load-bearing `url`/`baseurl`/`google_site_verification` keys, the skill README front-matter contract and its instruction-file guard, how to verify a deploy, and the `robots.txt` limitation.
- [concepts/mcp-server.md](concepts/mcp-server.md) — **MCP Server (`ask mcp serve`)**. Documents the read-only Model Context Protocol server that allows agents to discover and pull ASK skills at runtime. Explains the `list_skills`, `search_skills`, and `get_skill` tools, and how it shares the TF-IDF routing index with the eval harness.

## Entities

- [entities/skill.md](entities/skill.md) — **The Skill Entity**. Defines exactly what constitutes a "skill" in ASK. Details the mandatory directory structure (SKILL.md, skill.yaml), naming conventions, the lifecycle of a skill (author, validate, eval, deploy, update), and dependency resolution.

## Reference

- [skills-catalog.md](skills-catalog.md) — **Full Skills Directory**. A complete list of all 42 skills currently shipped with ASK, organized by category: `coding/` (26), `planning/` (6), `tooling/` (10), and `workflows/` (1), along with descriptions for each.

## Meta

- [SCHEMA.md](SCHEMA.md) — **Wiki Maintenance Rules**. The rules that govern how AI agents maintain this wiki. Defines the directory layout, page frontmatter requirements, conventions, and operational workflows (ingest, query, lint).
- [log.md](log.md) — **Chronological History**. An append-only ledger of all modifications, ingests, and lint passes performed on this wiki by AI agents over time.
- [llm-wiki.md](llm-wiki.md) — **The LLM Wiki Pattern**. The foundational philosophy behind this wiki: an incrementally compounding knowledge base maintained automatically by LLMs, designed to eliminate the manual bookkeeping burden of traditional wikis.
