# 🚀 Agent Skill Kit Releases

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
