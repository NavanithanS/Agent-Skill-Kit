# 🚀 Agent Skill Kit Releases

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
