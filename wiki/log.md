# Log

Append-only chronological record. Format: `## [YYYY-MM-DD] <action> | <subject>`

---

## [2026-04-06] ingest | Initial wiki creation

Bootstrap from codebase scan. Created: SCHEMA.md, overview.md, concepts/adapter-pattern.md, entities/skill.md, skills-catalog.md, index.md, log.md.

Sources: agents/base.py, ask/utils/skill_registry.py, CLAUDE.md, skills/** yaml inventory, agents/** adapter listing.

## [2026-04-11] ingest | Documented Release Protocol

Added `concepts/release-protocol.md` to ensure future agents update all hidden version references (Homebrew, init.py, etc.) during version bumps. Updated index.

## [2026-05-24] update | Added remote registries & diff viewer

Implemented `ask install <url>` to support remote Git-backed skill registries. Improved conflict resolution across CLI commands (`ask copy`, `ask update`, `ask install`) with an interactive `[v]iew diff` option. Hardened `skill_registry.py` to support scanning single-level directories for remote skills. Reduced token footprint of `ask-commit-assistance`, `ask-impact-sentinel`, and `ask-shadcn-mechanic` to satisfy linter constraints.

## [2026-05-30] update | Added `ask test` Layer 1 (trigger/collision audit)

Built the offline half of the skill eval harness. New `ask/utils/eval/` package with a pure-stdlib TF-IDF cosine ranker (`trigger_scorer.py`) and `ask/commands/test.py` exposing `ask test`. It audits each skill's `tests/evals.yaml` (`should_fire` prompts) against the whole library and flags **collisions** — similar skills competing for the same prompt — rather than claiming absolute routing accuracy, which is honestly framed as a lexical pre-screen (real accuracy is Layer 2's `--behavior`, still stubbed). Supports `--strict` (CI gate), `--json`, `--margin`, and per-skill scoping. Demo evals added to the laravel/vue architect+mechanic pairs; the audit correctly surfaces architect↔mechanic collisions. 7 new tests; suite 30→37. See `concepts/eval-harness.md`.

## [2026-05-30] update | Added `ask mcp serve` (MCP server, provider model)

Exposed the skill library to MCP-capable agents so they can discover/pull skills at runtime. Read-only *provider, not installer* design — no filesystem mutation. New `ask/utils/provider.py` (pure, testable: `list_skills_payload`/`search_skills_payload`/`get_skill_payload`), `ask/mcp_server.py` (thin FastMCP wrapper, `mcp` as optional `[mcp]` extra), and `ask/commands/mcp_cmd.py` (`ask mcp serve` / `tools` / `probe`). `search_skills` reuses the `ask test` TF-IDF index so search and trigger audit agree on skill topics. 8 new tests; suite 37→45. See `concepts/mcp-server.md`.

## [2026-07-15] update | Added `ask-wiki-init` and `ask-hold-code` skills

Created `ask-wiki-init` (tooling) to scaffold the LLM Wiki pattern and `ask-hold-code` (planning) to enforce a planning-mode lock. Refactored both to strictly follow the Gold Standard architecture from `ask-skill-creator` (extracted config, added identity/persona). Updated `README.md` to reflect 42 total skills.

## [2026-08-02] update | v0.9.1 Release: Database Indexing & Safe Copy Fix

Bumped version to 0.9.1. Enhanced `ask-impact-sentinel` with a mandatory Database Indexing Review protocol to systematically audit query paths and suggest migration scripts. Fixed a hardcoded `force=True` parameter in `ask copy` that violated the Safe Copy protocol when installing sidecar resources (`config/`, `scripts/`, etc.). Introduced a legacy path migration script for `AntigravityAdapter` to move old `.agent` installations to `.agents`.
