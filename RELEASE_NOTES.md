# 🚀 Agent Skill Kit Releases

## v0.7.0
**Date**: March 17, 2026
**Theme**: Smarter `ask copy` + Terminal UI Polish

### 🔍 Fuzzy Skill Name Matching

No more copy-pasting exact skill names. `--skill` now accepts partial names:

```bash
ask copy claude --skill fastapi-arch     # → ask-fastapi-architect (auto-resolved)
ask copy claude --skill laravel          # → shows 4 matches to pick from
```

Single matches resolve automatically with a hint. Multiple matches show a numbered list.

---

### 🧠 Project Stack Detection

Run `ask copy` in your project directory — ASK reads your dependency files and suggests skills before you even see the full list:

```
Detected: laravel, vue
Suggested: ask-laravel-architect, ask-laravel-mechanic, ask-vue-architect
```

Detects: **Laravel**, **Vue**, **Next.js**, **React**, **Flutter**, **FastAPI** from `composer.json`, `package.json`, `pubspec.yaml`, `requirements.txt`, and `pyproject.toml`.

---

### ⚡ Upfront Conflict Scan

Previously, conflicts surfaced one-by-one mid-copy. Now, all skills are pre-checked before anything is written. If conflicts exist, you choose a strategy once:

```
Warning: 2 skill(s) already installed: ask-laravel-architect, ask-vue-architect
1 skip all  2 overwrite all  3 ask per skill
Strategy [1/2/3] (1):
```

No more unexpected interruptions halfway through a bulk install.

---

### 🔎 Search/Filter in Interactive Skill List

The interactive skill picker now starts with a search prompt:

```
Search (Enter to list all): docker
1 match(es)
```

Type anything to filter by name or description. Press Enter to list all 38 skills.

---

### 🎨 Terminal UI Polish

All 12 command outputs have been refreshed with a consistent, minimal aesthetic inspired by pnpm/yarn:

- Emoji removed throughout
- `  ✓ skill-name → agent` for success
- `  ✗ skill-name reason` for failure
- `  – skill-name skipped` for skips
- `N copied · N skipped · N failed` dim summary lines
- No panel borders or heavy box styles
- `[bold]Header[/bold]  [dim]subtitle[/dim]` header pattern

---

## v0.6.0
**Date**: March 14, 2026
**Theme**: Interactive Wizard & GitHub Pages Docs Site

### 🧙 ask wizard — Guided CLI Workflow

A new top-level command that walks you through copy, purge, sync, or update in a friendly numbered-step UI:

```bash
ask wizard
```

You'll be guided through:
1. **Action** — copy, purge, sync, or update
2. **Skill selection** — multi-select with numbers or `all`
3. **Agent selection** — multi-select with compatibility hints
4. **Scope** — global or local

No more memorizing flags for common workflows.

---

### 🌐 GitHub Pages Docs Site

Agent Skill Kit now has a live docs site at **https://navanithans.github.io/Agent-Skill-Kit/**

**Command Builder** — point-and-click command generation:
- Select one or more skills (with search + category filter)
- Pick an action: **copy** or **purge**
- Choose your agent (compatibility-filtered for copy; all agents + `all` for purge)
- Set scope (global / local)
- Get a ready-to-paste command — with a one-click copy button

**Skill Browser** — explore all 38 skills:
- Search by name, description, or trigger phrase
- Filter by category
- See agent compatibility badges per skill
- Click `+ Select` to instantly load a skill into the Command Builder

**Dark mode** — full shadcn/ui zinc palette (🌙/☀️ toggle, respects `prefers-color-scheme`).

The site is auto-generated from `skills/manifest.json` on every push via GitHub Actions.

---

### 🐛 Fixes
- Docs site: action switching now correctly resets the skill list's visual state
- Docs site: purge → copy transition no longer generates invalid `ask copy all` commands

## v0.5.2
**Date**: March 13, 2026
**Theme**: Frictionless Copy — Scope Flags & USoT Clarity

### 🚀 What's New

**No more destination prompts when you know where you're copying:**

`ask copy` now accepts `--global` and `--local` flags to skip the destination prompt entirely.

```bash
ask copy claude --skill ask-code-reviewer --global      # straight to ~/.claude/skills/
ask copy universal --skill ask-laravel-mechanic --local  # straight to .agents/skills/
ask copy claude --skill ask-code-reviewer --overwrite   # overwrite without conflict prompt
```

**`--overwrite` / `-f`:** Skip the "already exists in USoT" conflict menu and overwrite directly. Ideal for update workflows.

**Smarter preview table:** When `--local` or `--global` is passed, the preview table now only shows the relevant path column — no more noise from the other scope.

**`universal` skips compatibility check:** Copying to `universal` no longer asks "this agent isn't listed, copy anyway?" — USoT accepts all skills by definition.

**`ask purge all` now tells you about USoT leftovers:**

```
✨ No ask-* skills found to purge in the selected agent(s).
💡 Found in USoT: ask-laravel-mechanic
   Run: ask purge universal to remove them.
```

### 🐛 What's Fixed
- `--global`/`--local` conflict error now fires before the preview table renders (not after a blank table)
- Scope prompt default could reference an invalid choice when only one scope was supported
- Copy failures (OSError) were silently ignored in the final summary — now shown as `X failed`
- `ask purge all` USoT hint was filtering by `ask-` prefix — now always scans all skills so nothing is missed
- Duplicate skill names suppressed in purge hint when the same skill exists in both local and global USoT

## v0.5.1
**Date**: March 12, 2026
**Theme**: Bug Fix Release — CLI Correctness & USoT Integrity

### 🐛 What's Fixed

**`ask create skill` was broken end-to-end:**
- Created `README.md` instead of `SKILL.md` — every new skill immediately failed `ask validate`
- Didn't scaffold `scripts/` or `tests/` directories — two more instant validation failures
- Offered `"reasoning"` and `"other"` as categories — both point to directories the skill registry never scans, making skills permanently undiscoverable. Fixed to `["coding", "planning", "tooling"]`.

**`ask sync` bypassed the Universal Source of Truth:**
- Previously wrote skills directly to each agent's folder, bypassing `.agents/skills/`. Synced skills were invisible to `ask update` and broke the symlink architecture introduced in v0.5.0. Now uses the same USoT-first, then-symlink pattern as `ask copy`.
- `ask sync` (without `all`) now works — the `all` argument is optional.

**`ask validate` showed an incorrect final count:**
- The "Result: X passed, Y failed" summary printed before the dependency check ran, so circular-dependency failures were never reflected in it.

**`ask copy` UX fixes:**
- `[yellow](exists)` markup in the preview table was accidentally stripped during a cleanup pass, removing the visual conflict warning.
- Single interactively-selected skill incorrectly displayed as `"Dependency"` in the preview table.
- `universal` agent was excluded from the compatibility list for single-skill selections.
- Conflict resolution replaced a confusing free-text prompt with a clear 4-option menu: **use existing / overwrite / rename / skip**.

**Other fixes:**
- `ask add-agent` tip referenced `bug-finder` (invalid) — fixed to `ask-bug-finder`.
- `ask purge` agent argument now validated at runtime instead of import time.

## v0.5.0
**Date**: March 11, 2026
**Theme**: Universal Source of Truth & Rule Generation

### 🌐 Universal Source of Truth (USoT)
Agent Skill Kit now pioneers the **Universal Source of Truth** for AI agent skills. As AI coding tools multiply (Cursor, Claude Code, Gemini, Antigravity), managing skills across all of them was becoming tedious.
- **`ask copy`**: Now intelligently copies the skill definition to a universal directory (`.agents/skills/`) and automatically deploys a symlink to the specific agent's folder (e.g. `.cursor/rules/`). Updates to the USoT instantly reflect across all your agents!
- **`ask purge`**: A brand new interactive command that allows you safely and rapidly delete `ask-*` tracking capabilities from selected legacy agent folders.

### 📜 Universal Rule Generation
Agents often use "Rules" (like `.cursorrules` or `CLAUDE.md`) to define passive repo constraints ("always use TypeScript", "no Tailwind"). ASK now manages these globally!
- **`ask rules compile`**: Simply place your rule snippets in `.agents/rules/` (`~/.agents/rules/` for global) and run this new command to instantly compile them into `.cursorrules`, `CLAUDE.md`, and `.agent/rules/rules.md`. Write your rules once, apply them everywhere.

## v0.4.2
**Date**: March 9, 2026
**Theme**: Claude Adapter Update & New Skills

### 🚀 Claude Adapter Update
- **`ask.adapters.claude`**: Updated the skill copying logic for Claude. It now expects and correctly handles the `skills/<skill-name>/SKILL.md` structure with YAML frontmatter, aligning Claude with the new "Gold Standard" skill architecture.

### 🛠️ New Skills & Manifest
- Added the **`ask-impact-sentinel`** skill.
- Updated the central `manifest.json` for skill routing.

## v0.4.1
**Date**: March 8, 2026
**Theme**: Safety First & Version Unification

### 🛡️ Safety Update: "Zero Auto-Commit"
We've overhauled the **`ask-commit-assistance`** skill (bumped to v1.1.0). This update introduces strict constraints that prevent any AI agent from executing `git commit` autonomously. 
- Agents will now review, scan for secrets, and stage files, but the final commit remains a manual user action.
- Added explicit `❌ NEVER AUTO-COMMIT` critical constraints.

### 📦 Project Unification
- Unified the package version to **v0.4.1** across `pyproject.toml`, adapters, and Homebrew formulae to resolve inconsistencies.

## v0.4.0
**Date**: March 7, 2026
**Theme**: Hierarchical Multi-Agent Systems (HMAS) & Orchestration

### 🧠 New Paradigm: Subagent Orchestration
We've introduced the concept of **Orchestrators** and **Subagents** to the Agent Skill Kit. This allows AI agents to bypass the context window limits of single-agent workflows by chunking tasks and delegating them to highly constrained parallel workers.

### 🛠️ New Skills
- **`ask-parallel-auditor`**: The premier Orchestrator skill. Chunks massive repositories and spawns parallel background subtasks inside isolated Git worktrees.
- **`ask-ast-mapper`**: A highly constrained, read-only Subagent. Generates lightweight JSON dependency maps to prevent parent orchestrators from burning tokens reading codebase structure.
- **`ask-context-janitor`**: An aggressive token-optimizing subagent. Summarizes massive logs, pull requests, and multi-agent audit outputs into strict Markdown/JSON executive summaries.

### 🛡️ Technical & Governance Updates
- **Validation Gates Enforced**: The new tooling skills strictly enforce the presence of `scripts/` and `tests/` directories to pass rigorous CI validation checks.
- **Token Schemas**: Leveraged the v2.0 token-optimized `<critical_constraints>` format to keep subagent prompts under 200 tokens.
- **Versioning**: Bumped package version to `0.4.0`.

---

## v0.3.1
**Date**: March 7, 2026
**Theme**: Tooling Updates

### 🛠️ Enhancements
- **`ask-shadcn-architect`**: Updated the skill instructions to natively support new `shadcn/cli v4` features. Agents are now instructed on how to use styling `--preset` flags, handle monorepo configurations with `--cwd`, and explicitly defer to official `shadcn/skills` for complex component implementation instead of generating them from scratch.
- **Versioning**: Bumped package version to `0.3.1`.

---

## v0.3.0

### 1. Model Context Protocol (MCP) Support
ASK is now compatible with the Model Context Protocol, allowing skills to be used directly by AI clients like Claude Desktop.
- **New Server**: `ask.mcp.server` exposes all skills as executable tools.
- **Tool Search**: New fuzzy search capability (`search_skills`) to find relevant skills dynamically.
- **Reference**: See `walkthrough.md` for configuration instructions.

### 2. "Gold Standard" Skill Architecture
We have redefined what a "Skill" is. Every skill now follows a strict, validation-enforced anatomy:
- **`SKILL.md`**: The brain. Contains optimized Frontmatter, Triggers, and Algorithmic Instructions.
- **`scripts/`**: The hands. Contains executable code (e.g., `validate.py`) for the skill to perform actions or verify results.
- **`assets/`**: The knowledge. Contains examples, checklists, and reference docs (Progressive Disclosure).
- **`tests/`**: The proof. Contains inputs and expected outputs for testing.

### 3. Execution & Validation Gates
- **`ask validate` CLI**: Updated to strictly enforce the new directory structure. It checks for the existence of `scripts/` and `tests/`.
- **Runtime Validation**: Skills now include a `<validation_gate>` step in their process, requiring agents to run a `validate.py` script to self-correct before finishing.

## 🛠️ Enhancements

- **Global Refactor**: All **33 skills** in the repository have been migrated to the new structure.
- **Cognitive Optimization**: 
  - `ask-owasp-security-review` (Pilot) and `ask-code-reviewer` have been rewritten with **Chain of Thought (CoT)** prompts and **Algorithmic Instructions** to reduce hallucinations and improve output quality.
- **GitHub Compatibility**: All `README.md` files have been preserved/restored to the root of each skill directory to ensure the repository remains browsable and documented on GitHub.
- **Versioning**: Bumped package version to `0.3.0`.

## 🐛 Fixes
- Fixed `ask-skill-creator` to generate the new folder structure automatically.
- Fixed inconsistent naming conventions (enforced `kebab-case`).

## 📋 Upgrade Guide
No manual action is required for existing skills; the migration script has already run.
To use the new MCP server:
1. Ensure you have `mcp` installed (`pip install mcp`).
2. Add the server config to your `claude_desktop_config.json`.
