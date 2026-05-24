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
