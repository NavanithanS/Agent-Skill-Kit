# Wiki Index

Content catalog for the Agent Skill Kit wiki. Updated on every page addition or change.

## Overview

- [overview.md](overview.md) — High-level project orientation: what ASK is, supported agents, key data flow, skill count

## Concepts

- [concepts/adapter-pattern.md](concepts/adapter-pattern.md) — How adapters transform and deploy skills to agents; safe copy protocol; dynamic loading
- [concepts/release-protocol.md](concepts/release-protocol.md) — Checklist for version bumping and release management across files (pyproject, Python modules, Homebrew formula)
- [concepts/eval-harness.md](concepts/eval-harness.md) — `ask test`: two-layer skill evaluation; Layer 1 offline TF-IDF collision audit, Layer 2 live-model behavioral eval
- [concepts/mcp-server.md](concepts/mcp-server.md) — `ask mcp serve`: read-only MCP server exposing list/search/get_skill so agents discover skills at runtime

## Entities

- [entities/skill.md](entities/skill.md) — What a skill is: directory structure, skill.yaml fields, naming conventions, lifecycle

## Reference

- [skills-catalog.md](skills-catalog.md) — All ~40 skills organized by category (coding, planning, tooling)

## Meta

- [SCHEMA.md](SCHEMA.md) — Wiki conventions and LLM maintenance workflows
- [log.md](log.md) — Chronological record of ingests, queries, and updates
