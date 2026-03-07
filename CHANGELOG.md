# Changelog

## [0.2.0] - 2026-02-07

### 🚀 New Features

#### Skill Schema v2.0
- **Token Optimization**: 61.6% token reduction across all 33 skills (32K → 12K tokens)
- **New CLI Commands**: `ask skill lint`, `ask skill profile`, `ask skill compile`
- **Manifest Generation**: `skills/manifest.json` for skill routing with triggers

#### CI Governance
- **Skill Linter**: Enforces token limits (≤500 OK, 501-700 warning, >700 error)
- **GitHub Workflow**: `.github/workflows/skill-lint.yml` for automated checks

#### Developer Experience
- Schema specification in `docs/skill-schema.md`
- YAML frontmatter support with `triggers` array
- `<critical_constraints>` blocks for clear AI guidance

### 📦 Technical Changes
- Added `token_analyzer.py` for token counting (tiktoken)
- Enhanced `skill_registry.py` with frontmatter parsing
- New `skill.py` CLI command group

### 🔄 Skill Format Changes
All 33 skills rewritten to v2.0 schema:
- YAML frontmatter with triggers
- `<critical_constraints>` blocks with ❌/✅ patterns
- Removed verbose prose, focused on actionable guidance

---

## [0.4.0] - 2026-03-07

### 🚀 New Features

#### Hierarchical Multi-Agent Systems (HMAS) & Orchestration
Introduced the concept of Orchestrators and Subagents to the Agent Skill Kit. This bypasses the context window limits of single-agent workflows.

-   **`ask-parallel-auditor`**: The premier Orchestrator skill. Chunks repositories and delegates audits to parallel background subagents inside isolated Git worktrees.
-   **`ask-ast-mapper`**: A highly constrained, read-only Subagent. Generates lightweight JSON dependency maps to prevent parent orchestrators from burning tokens reading codebase structure.
-   **`ask-context-janitor`**: An aggressive token-optimizing subagent. Summarizes massive logs, pull requests, and parallel audit outputs into strict Markdown/JSON summaries.

### 📦 Technical Changes
- All meta-tooling skills now strictly enforce the presence of `scripts/` and `tests/` directories to pass validation gates.

---

## [0.1.6] - 2026-02-01

### 🚀 New Features

#### Skill Dependencies
- **Recursive Resolution:** `ask copy` now automatically installs dependencies defined in `skill.yaml`'s `depends_on` field.
- **Cycle Detection:** Intelligent circular dependency detection prevents infinite loops.
- **O(N) Performance:** Optimized resolution algorithm using in-memory caching.
- **Preview:** `ask copy` preview now clearly distinguishes between "Direct" (requested) and "Dependency" (auto-included) skills.

#### Configuration & UX
- **Config File:** Support for `~/.askconfig.yaml` to set default agents and preferences.
- **Verbose Mode:** Added `--verbose` flag for detailed logging.
- **Search command:** `ask list` now supports `--search` and filtering by category/agent.
- **Validate command:** New `ask validate` command to check skill integrity and dependency correctness.

### 🛡 Security & Quality
- **Safe Copy:** Improved conflict resolution (prompt to rename/skip) prevents accidental overwrites.
- **Input Validation:** Hardened `add-agent` against path traversal.
- **Error Handling:** Graceful handling of file permissions and malformed configs.

### 🐛 Fixes
- Fixed potential path traversal in `add-agent` command.
- Removed duplicate logging in `copy.py`.
- Improved error messages for "no skills found".

### 📦 Internal
- Refactored `skill_registry` for better performance.
- Comprehensive unit tests added for dependency logic.
