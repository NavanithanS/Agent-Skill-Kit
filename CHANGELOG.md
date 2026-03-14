# Changelog

## [0.6.0] - 2026-03-14

### 🚀 New Features
- **`ask wizard`**: Interactive guided workflow — choose copy, purge, sync, or update from a numbered-step UI. Multi-selects skills and agents, prompts for scope, and executes the selected action.
- **GitHub Pages docs site**: New site at `https://navanithans.github.io/Agent-Skill-Kit/` featuring:
  - **Command Builder**: Interactive wizard for generating `ask copy` and `ask purge` commands with live output, multi-skill selection, agent compatibility filtering, dark mode, and one-click copy.
  - **Skill Browser**: Searchable, filterable table of all 38 skills with category badges, agent tags, and "+ Select" integration with the builder.
- **`scripts/generate_site.py`**: Static site generator — reads `skills/manifest.json` and outputs `docs/index.html` with full dark mode (shadcn/ui zinc palette).
- **`.github/workflows/docs.yml`**: GitHub Actions CI that auto-regenerates the docs site on every push to master.
- **`CLAUDE.md`**: Project guidance file for Claude Code with architecture overview and command reference.

### 🐛 Bug Fixes
- **Docs site**: `setAction()` now calls `renderSkillList()` on action switch — stale green checkboxes no longer persist after clearing selected skills.
- **Docs site**: `selectedAgent = 'all'` is now reset when switching purge → copy, preventing invalid `ask copy all --skill …` command generation.

### 🎨 Design
- Command Builder and Skill Browser badges follow shadcn/ui zinc palette: `rounded-md`, `font-semibold`, neutral zinc-100/zinc-900 backgrounds, zinc-200 borders.
- Agent pills updated from `rounded-full` to `rounded-md` throughout.
- Full dark mode using shadcn/ui zinc-950 (`#09090b`) page, zinc-900 cards, zinc-800 borders.

## [0.5.2] - 2026-03-13

### 🚀 New Features
- **`ask copy --global`**: New flag to copy directly to the global (user home) location without prompting for destination.
- **`ask copy --local`**: New flag to copy directly to the local (project) location without prompting for destination.
- **`ask copy --overwrite` / `-f`**: New flag to overwrite an existing skill in USoT without the conflict prompt.
- **`ask copy universal`**: Skips the compatibility warning — `universal` accepts all skills by definition.
- **Preview table**: Now shows only the relevant column (`Local` or `Global`) when a scope flag is passed.
- **`ask purge all` hint**: When no skills are found but the USoT contains skills, now shows their names and suggests `ask purge universal`.

### 🐛 Bug Fixes
- **`ask copy`**: `--global`/`--local` mutual exclusion guard now fires before the preview table renders (previously showed a malformed empty table first).
- **`ask copy`**: Scope prompt default was `"2"` even when only global scope was available — corrected to always match a valid choice.
- **`ask copy`**: Added guard for degenerate adapter configs where both local and global scopes are disabled.
- **`ask copy`**: `fail_count` now tracked and shown in the final summary (previously silent on OSError failures).
- **`ask purge all` hint**: USoT scan now always searches all skills regardless of `--all-skills` flag (previously missed non-`ask-` prefixed skills).
- **`ask purge all` hint**: Skill names deduplicated when same skill exists in both local and global USoT.

### 🧹 Cleanup
- Simplified skill type classification in preview table to a single expression.
- Fixed 5-space indentation inconsistency in copy loop print statements.
- Added `Optional[bool]` type annotations on `use_global`/`use_local` parameters.

## [0.5.1] - 2026-03-12

### 🐛 Bug Fixes
- **`ask create skill`**: Now scaffolds `SKILL.md` (not the deprecated `README.md`), and creates the required `scripts/` and `tests/` directories — new skills no longer fail `ask validate` immediately after creation.
- **`ask create skill` / `ask validate`**: Fixed category list — `"reasoning"` and `"other"` replaced with `"planning"` to match the actual `skills/` directory structure. Skills created under `"reasoning"` were silently undiscoverable.
- **`ask sync`**: Rewritten to route through the Universal Source of Truth (USoT) and symlink to each agent — matching the `ask copy` architecture. Previously bypassed USoT entirely, causing synced skills to be invisible to `ask update`.
- **`ask sync`**: `all` argument is now optional — `ask sync` works without arguments.
- **`ask validate`**: "Result" summary now prints after the dependency check so circular-dependency failures are included in the count.
- **`ask copy`**: Restored `[yellow](exists)` Rich markup in the preview table (was accidentally stripped during f-string cleanup).
- **`ask copy`**: Single skill selected interactively no longer displays as `"Dependency"` in the preview table.
- **`ask copy`**: `universal` agent now correctly shows as compatible with all skills in the agent selection table.
- **`ask copy`**: Conflict resolution replaced single free-text prompt with a 4-option menu: `use existing / overwrite / rename / skip`.
- **`ask purge`**: Agent argument validated at runtime (not import time); extracted `_collect_targets` helper to remove duplicate scan logic; added `--all-skills` flag.
- **`ask add-agent`**: Tip command now correctly references `ask-bug-finder` instead of the non-existent `bug-finder`.
- **Tests**: Updated stale `test_claude_transform` assertions to match the adapter's current frontmatter-only output format.

### 🧹 Cleanup
- Removed unused imports across 7 files (`pathlib.Path`, `yaml`, `os`, `typing.Optional`, `typing.Any`, `get_skill`, `get_skills_dir`, `get_agent_scopes`).

## [0.5.0] - 2026-03-11

### 🚀 New Features
- **Universal Source of Truth**: Added a new Universal Adapter allowing `.agents/skills/` to be the primary home for all skills.
- **Smart Symlinking**: `ask copy <agent>` now writes to the Universal Source of Truth and symlinks to the specific agent folder, keeping skills in sync across tools like Cursor and Claude Code.
- **Interactive Purge**: New `ask purge` command to cleanly interactive remove `ask-*` skills from selected agent directories.
- **Rule Generation**: New `ask rules compile` command to compile markdown files from `.agents/rules/` directly into `.cursorrules`, `CLAUDE.md`, and `.agent/rules/rules.md`.

## [0.4.2] - 2026-03-09

### New Features
- **Claude Adapter**: Updated the Claude skill adapter to use the new `skills/<skill-name>/SKILL.md` structure with YAML frontmatter.
- **Skills**: Added `ask-impact-sentinel` skill.
- **Skill Manifest**: Updated `manifest.json` with new skills.

## [0.4.1] - 2026-03-08

### 🛡️ Safety & Quality
- **ask-commit-assistance (v1.1.0)**: Strictly forbid autonomous commits. The agent must now hand over the final `git commit` command to the user.
- **Skill Standardization**: Restructured `ask-commit-assistance` to follow the v2.0 token-optimized format and `ask-skill-creator` guidelines.

### 🔄 Meta
- Unified project versioning across all core files to `0.4.1`.

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
