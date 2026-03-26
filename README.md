# Agent Skill Kit (ASK)

![Agent Skill Kit Banner](https://raw.githubusercontent.com/NavanithanS/Agent-Skill-Kit/master/assets/banner.png)

**Centralized skills repository and CLI toolkit for AI agents (Gemini, Claude, Codex, Cursor, Antigravity).**

> **📖 Docs & Command Builder → [navanithans.github.io/Agent-Skill-Kit](https://navanithans.github.io/Agent-Skill-Kit/)**
> Browse all 38 skills, generate `ask copy` / `ask purge` commands visually, with dark mode support.

---

## 🚀 What's New in v0.7.0

### 🔍 Fuzzy Skill Name Matching
Partial names now resolve automatically via `--skill`:
```bash
ask copy claude --skill fastapi-arch    # auto-resolves → ask-fastapi-architect
ask copy claude --skill laravel         # shows disambiguation list for 4 matches
```

### 🧠 Project Stack Detection
`ask copy` (interactive) sniffs your project files and surfaces relevant skills upfront:
```
Detected: laravel, vue
Suggested: ask-laravel-architect, ask-laravel-mechanic, ask-vue-architect
```

### ⚡ Upfront Conflict Scan
All conflicts are detected before copying begins — one batch prompt replaces per-skill interruptions:
```
Warning: 2 skill(s) already installed: ask-laravel-architect, ask-vue-architect
1 skip all  2 overwrite all  3 ask per skill
```

### 🔎 Search/Filter in Interactive Skill List
Type to filter the skill table before selecting — no more scrolling through all 38 skills:
```
Search (Enter to list all): laravel
4 match(es)
```

### 🎨 Terminal UI Polish
All 12 command outputs refreshed — emoji removed, pnpm-style `✓`/`✗`/`–` prefixes, dim summaries, no panel borders.

---

It serves as a unified "package manager" for your AI's capabilities, allowing you to define a skill once and deploy it to **Gemini, Claude, Codex, Antigravity, Cursor**, and more.

## 🧠 Why Agent Skill Kit?

Managing instructions for multiple AI agents is tedious. You often have to:
*   Copy `.cursorrules` to `.codex.md`.
*   Manually sync `~/instructions.md` with project-specific prompts.
*   Format skills differently for Gemini (`SKILL.md`) vs Claude (Slash Commands).

**ASK** solves this by treating skills as **reusable packages**.
1. **Define Once**: Write a skill in a standard format.
2. **Deploy Anywhere**: ASK transforms and copies the skill to the correct location and format for each agent.
3. **Sync**: Keep all your agents updated with a single command.

## 🚀 Features

- **Multi-Agent Support**: Native support for Gemini, Claude Code, OpenAI Codex, Antigravity, and Cursor.
- **Interactive Wizard**: `ask wizard` guides you through copy, purge, sync, and update with a step-by-step UI.
- **Docs Site**: Command Builder + Skill Browser at [navanithans.github.io/Agent-Skill-Kit](https://navanithans.github.io/Agent-Skill-Kit/).
- **Skill Dependencies**: Automatically resolves and installs dependent skills.
- **Universal Source of Truth**: Skills stored in `.agents/skills/` and symlinked to each agent — update once, propagate everywhere.
- **Dynamic Discovery**: Automatically discovers available agents in the `agents/` directory.
- **Safe Copy**: Never overwrites silently. Prompts to use existing, overwrite, rename, or skip on conflict.
- **Local & Global**: Choose between Project-Local (per-repo) or Global (user-wide) deployment.
- **Skill Linting**: Token analysis and schema validation with `ask skill lint`.
- **Manifest Generation**: Auto-generate `manifest.json` for skill routing.
- **Extensible**: Add support for any new AI agent in seconds via `ask add-agent`.

## 📦 Installation

### Homebrew (Recommended for Mac/Linux)
```bash
brew tap NavanithanS/Agent-Skill-Kit
brew install agent-skill-kit
```

### From PyPI
```bash
pip install agent-skill-kit
```

### From Source (Development)
```bash
# Clone the repository
git clone https://github.com/NavanithanS/Agent-Skill-Kit.git
cd Agent-Skill-Kit

# Install in editable mode
pip install -e .
```

### Upgrading an Existing Installation
When a new version (like `v0.4.0`) is released, you must upgrade the CLI and then sync the new skills down to your local AI agents.

```bash
# 1. Upgrade the CLI
pip install --upgrade agent-skill-kit  # If using PyPI
brew upgrade agent-skill-kit           # If using Homebrew

# 2. Sync the new skills to your agents
ask update
```

## 🛠 Usage

### 0. Interactive Wizard ⭐
The easiest way to use ASK — let the wizard guide you.

```bash
ask wizard
```

Guides you through four actions:
| # | Action | What it does |
|---|--------|-------------|
| 1 | **copy** | Select skills + agent + scope → install |
| 2 | **purge** | Select an agent → remove all `ask-*` skills |
| 3 | **sync** | Sync every skill to every agent |
| 4 | **update** | Update all installed skills to latest |

---

### 1. Copy Skills to an Agent
**The primary way to use ASK** — Deploy skills to your AI agents.

**Interactive Mode** (Recommended):
```bash
ask copy
```
The wizard guides you through:
1. **Stack detection** — auto-suggests skills for your project (Laravel, Vue, Next.js, Flutter, FastAPI)
2. **Search/filter** — type to narrow the skill list before selecting
3. **Skill selection** — numbered table with descriptions and categories
4. **Agent selection** — compatible agents highlighted for your chosen skill
5. **Destination** — local (project) or global (user-wide)
6. **Conflict scan** — all conflicts resolved upfront in one batch prompt

**Quick Mode** (with flags):
```bash
# Copy specific skill (fuzzy name matching — partial names work)
ask copy gemini --skill bug-finder
ask copy claude --skill fastapi-arch    # resolves → ask-fastapi-architect

# Copy all compatible skills to an agent
ask copy claude --all
```

### 2. List Available Skills
View your library of skills, including descriptions and supported agents.
```bash
# List all skills
ask list

# Search for skills
ask list --search "docker"

# Filter by category or agent
ask list --category coding --agent claude
```

### 3. Manage Rules (ask rules compile)
Easily manage rule files (`.cursorrules`, `CLAUDE.md`, `.agent/rules/`) by compiling them from a single central Universal Truth directory!
```bash
# Place your `.md` snippets in .agents/rules/ or ~/.agents/rules/
ask rules compile
```

### 4. Interactive Purge (ask purge)
Safely delete `ask-*` skills from selected target agents (or the entire Universal directory) with interactive selection prompts.
```bash
ask purge
```

### 5. Validate Library
Check your skill library for errors, missing metadata, or circular dependencies.
```bash
ask validate
```

### 6. Create a New Skill
**AI-Assisted** (Recommended):
Simply ask your AI agent to create a skill for you:
```
Create a new skill for Docker best practices

Make a skill that teaches REST API design

create new skill: explaining-code
Purpose: Explains code using analogies, ASCII diagrams, and step-by-step walkthroughs. Triggered by queries like "How does this work?"
Instructions emphasize conversational tone, multiple analogies, and highlighting common misconceptions.
```
*Prerequisites: Deploy `ask-skill-creator` to your agent first (see [Tooling Skills](#tooling-skills-meta-skills)).*

**Manual CLI** (Alternative):
Launch the interactive wizard to generate a standardized skill template.
```bash
ask create skill
```

### 7. Sync All Skills
Synchronize your entire skill library to all supported agents at once.
```bash
ask sync all
```

### 8. Update Skills
Keep your installed skills up-to-date with the latest versions from the repository.
```bash
ask update
```
Features:
- **Version Checks**: Compares installed version vs source.
- **Interactive**: Select which skills to update (or use `--yes` to update all).
- **Safe**: Automatic backup (`SKILL.md.bak`) created before overwriting.

### 9. Add Support for New Agents
Want to use **Windsurf** or **Aider**? Use the scaffold wizard:
```bash
ask add-agent
```
This creates the necessary adapter code, making the new agent available instantly.

### 10. Skill Development Tools (New in v0.2.0)

```bash
# Lint skills for token limits and schema compliance
ask skill lint

# View token usage report
ask skill profile

# Generate manifest.json for routing
ask skill compile
```

## 🎯 Supported Agents

| Agent | Local Path (Project) | Global Path (User) | Format |
|-------|----------------------|--------------------|--------|
| **Antigravity** | `.agent/skills/` | `~/.gemini/antigravity/skills/` | SKILL.md (YAML) |
| **Gemini CLI** | `.gemini/skills/` | `~/.gemini/skills/` | SKILL.md (YAML) |
| **Claude Code** | `.claude/commands/` | `~/.claude/commands/` | Markdown Command |
| **Codex** | `codex.md` | `~/.codex/instructions/` | Markdown |
| **Cursor** | `.cursor/rules/` | `~/.cursor/rules/` | Markdown Rules |

## � Available Skills

ASK comes with a curated collection of skills to boost your AI agent's capabilities. Each skill provides specialized instructions and best practices.

### Planning Skills

| Skill | Description | Use Cases |
|-------|-------------|-----------|
| **[adr-logger](skills/planning/ask-adr-logger/README.md)** | Automates creation of Architectural Decision Records | • Recording tech decisions<br>• Documenting context & consequences<br>• Maintaining decision history |
| **[brainstorm](skills/planning/ask-brainstorm/README.md)** | Guidelines for exploring user intent and requirements | • Defining user intent<br>• Gathering requirements<br>• Exploring design options |
| **[project-memory](skills/planning/ask-project-memory/README.md)** | Maintains a 'Project Brain' of decisions | • Avoiding re-discussions<br>• Checking past decisions<br>• Recording new choices |
| **[buildmaster](skills/planning/ask-buildmaster/README.md)** | Smart Epic Orchestration Agent | • Epic discovery & scoping<br>• Ticket decomposition<br>• Execution tracking & handoff |
| **[solution-architect](skills/planning/ask-solution-architect/README.md)** | Master Ideation and Strategic Architecture | • Multi-perspective ideation<br>• Designing robust systems<br>• Structured output via frameworks |

### Coding Skills

| Skill | Description | Use Cases |
|-------|-------------|-----------|
| **[bug-finder](skills/coding/ask-bug-finder/README.md)** | Best practices for systematic bug hunting and debugging | • Debugging complex issues<br>• Isolating bugs<br>• Using debugging tools |
| **[code-reviewer](skills/coding/ask-code-reviewer/README.md)** | AI code reviewer providing constructive feedback | • Code quality checks<br>• Security & performance review<br>• Learning best practices |
| **[effective-llm-coder](skills/coding/ask-effective-llm-coder/README.md)** | Guides agent in declarative, simple, tenacious coding | • Declarative workflows<br>• Simplicity & tenacity<br>• Iterative refinement |
| **[commit-assistance](skills/coding/ask-commit-assistance/README.md)** | Assist with code review, staging, and committing | • Pre-commit review<br>• Meaningful commit messages<br>• Staging files |
| **[explaining-code](skills/coding/ask-explaining-code/README.md)** | Explains code using analogies and diagrams | • Understanding complex code<br>• Visualizing flow<br>• Learning new codebases |
| **[flutter-architect](skills/coding/ask-flutter-architect/README.md)** | Senior Flutter skill using FVM | • Layer-First Architecture<br>• Stream-based Services<br>• Strict coding conventions |
| **[flutter-mechanic](skills/coding/ask-flutter-mechanic/README.md)** | Maintenance skill for Flutter projects using FVM | • Clean Build Protocol<br>• iOS/Android fixes<br>• Release protocols |
| **[laravel-architect](skills/coding/ask-laravel-architect/README.md)** | Senior scaffolding skill for Laravel (SQL/Mongo) | • Logic Layer separation<br>• Hybrid SQL/Mongo Relations<br>• Test-Driven Scaffolding |
| **[laravel-mechanic](skills/coding/ask-laravel-mechanic/README.md)** | Senior maintenance skill for database safety | • Zero Data Loss protocol<br>• N+1 Query prevention<br>• Queue debugging & forensics |
| **[owasp-security-review](skills/coding/ask-owasp-security-review/README.md)** | Static code analysis aligned with OWASP Top 10 | • Security scanning<br>• Identifying vulnerabilities<br>• Compliance checks |
| **[python-refactor](skills/coding/ask-python-refactor/README.md)** | Guidelines for Python code refactoring | • Improving code quality<br>• Refactoring legacy code<br>• Python best practices |
| **[refactoring-readability](skills/coding/ask-refactoring-readability/README.md)** | Improves code structure for clarity | • Renaming vars/functions<br>• Reducing complexity<br>• Improving readability |
| **[impact-sentinel](skills/coding/ask-impact-sentinel/README.md)** | Guidelines for impact analysis and database design | • Breaking change detection<br>• Strategic DB design<br>• Safe optimization |
| **[unit-test-generation](skills/coding/ask-unit-test-generation/README.md)** | Automates creation of comprehensive unit tests | • Generating new tests<br>• Covering edge cases<br>• Improving coverage |
| **[vue-architect](skills/coding/ask-vue-architect/README.md)** | Expert scaffolding for Vue 3 (Inertia/Nuxt) | • Component blueprints<br>• Stack detection<br>• Best practices enforcement |
| **[vue-mechanic](skills/coding/ask-vue-mechanic/README.md)** | Expert maintenance skill for Vue 3 (Inertia) | • Fixing navigation reloads<br>• Debugging prop mismatches<br>• Solving reactivity issues |
| **[component-scaffolder](skills/coding/ask-component-scaffolder/README.md)** | Standardizes UI component creation | • Consistent folder structure<br>• Typed props<br>• Auto-generating tests |
| **[db-migration-assistant](skills/coding/ask-db-migration-assistant/README.md)** | Ensures safe database schema updates | • Drafting migrations<br>• Creating rollback scripts<br>• Preventing data loss |
| **[readme-gardener](skills/coding/ask-readme-gardener/README.md)** | Keeps documentation in sync with code | • Updating API docs<br>• Documenting new features<br>• Maintaining README accuracy |
| **[shadcn-architect](skills/coding/ask-shadcn-architect/README.md)** | Enforces shadcn/ui patterns and consistency | • Preventing style bloat<br>• Enforcing import rules<br>• Promoting accessibility |
| **[shadcn-mechanic](skills/coding/ask-shadcn-mechanic/README.md)** | Expert maintenance for shadcn/ui components | • Customizing variants (CVA)<br>• Debugging form validation<br>• Fixing Tailwind layout limits |
| **[security-sentinel](skills/coding/ask-security-sentinel/README.md)** | Pre-flight security checker for secrets/vulns | • Blocking commits with secrets<br>• Detecting SQL injection<br>• Flagging unsafe Blade usage |
| **[nextjs-architect](skills/coding/ask-nextjs-architect/README.md)** | Expert scaffolding for Next.js 14+ (App Router) | • Server Components<br>• Server Actions<br>• Metadata API |
| **[fastapi-architect](skills/coding/ask-fastapi-architect/README.md)** | Expert scaffolding for FastAPI projects | • Pydantic V2<br>• Async SQLAlchemy<br>• Dep Injection |
| **[docker-expert](skills/coding/ask-docker-expert/README.md)** | Expert guidance on Docker & Containers | • Multi-stage builds<br>• Security best practices<br>• Image optimization |
| **[conceptual-integrity-sentinel](skills/coding/ask-conceptual-integrity-sentinel/README.md)** | Audits repositories for architectural drift and bloat | • Detecting complexity bloat<br>• Identifying dead code<br>• Enforcing simplicity |

---

### Tooling Skills (Meta-Skills)

#### 🧹 ask-context-janitor
**Description**: Aggressive token optimizer and context summarizer for reducing large text files, logs, or agent outputs.

**How to Use**:
```bash
ask copy antigravity --skill ask-context-janitor
```

**Use Cases**:
- Summarizing massive `.log` files from build errors.
- Digesting large `ARCHITECTURAL_AUDIT.md` files or `git diff` outputs.
- Acting as a data-reducer for multi-agent workflows.

---

#### �️ ask-ast-mapper
**Description**: Read-only subagent for generating lightweight AST dependency maps and structural overviews of directories.

**How to Use**:
```bash
ask copy antigravity --skill ask-ast-mapper
```

**Use Cases**:
- Quickly mapping dependencies of a directory without reading every file.
- Generating a lightweight JSON structure of imports and class methods.
- Acting as a reconnaissance subagent for heavier architectural agents.

---

#### ⚡ ask-parallel-auditor
**Description**: Orchestrator skill that splits a target repository into chunks and runs multiple audit subagents in parallel to bypass context limits.

**How to Use**:
```bash
ask copy antigravity --skill ask-parallel-auditor
```

**Use Cases**:
- Running repository-wide security scans or complexity audits.
- Delegating task subsets to identical subagents (e.g., `ask-owasp-security-review`).
- Bypassing the token limit of single-agent workflows.

---

#### �🛠️ ask-skill-creator
**Description**: Teaches AI agents how to create skills for Agent Skill Kit

**How to Use**:
```bash
# Deploy to all agents so they can create skills
ask sync all
```

**Use Cases**:
- **AI-Assisted Skill Creation**: Let your AI agent create new skills by simply asking
  ```
  "Create a skill for API design best practices"
  ```
- Standardizing skill structure and format
- Automating skill scaffolding
- Building your custom skill library
- Teaching AI agents the skill creation workflow

**Example Workflow**:
1. Deploy this skill to your agent: `ask copy gemini --skill ask-skill-creator`
2. Ask your agent: "Create a skill called 'ask-docker-best-practices' for containerization guidelines"
3. The agent generates the skill files automatically

---

#### 🎯 ask-add-agent
**Description**: How to add support for new AI code editors to Agent Skill Kit

**How to Use**:
```bash
# Deploy to help your agent add new editor support
ask copy antigravity --skill ask-add-agent
```

**Use Cases**:
- **Extending ASK**: Add support for new AI editors (Windsurf, Aider, etc.)
- Creating custom agent adapters
- Understanding the agent adapter architecture
- Contributing new agent support to the project

**Example Workflow**:
1. Deploy this skill to your agent
2. Run the wizard: `ask add-agent`
3. Or ask your agent to help: "Add support for Windsurf editor"
4. The agent follows the documented process to create the adapter

---

#### 📄 ask-pdf-processing
**Description**: Handle PDF text extraction, form filling, and merging

**How to Use**:
```bash
ask copy antigravity --skill ask-pdf-processing
```

**Use Cases**:
- Extracting text from PDF documents
- Processing PDF forms
- Merging multiple PDFs
- PDF automation workflows

---

#### 🧠 ask-skill-capture
**Description**: Meta-skill. Analyzes the current session's lessons and saves them as a permanent reusable skill.

**How to Use**:
```bash
# Deploy to your agent (e.g., Antigravity, Gemini)
ask copy antigravity --skill ask-skill-capture
```

**Use Cases**:
- **Chat-to-Code**: Turn "messy" chat context into a structured skill
- **Constraint Capture**: Permanently save rules like "Always use FVM" or "Don't use Tailwind"
- **Workflow Automation**: Save a successful debugging sequence as a reusable protocol
- **Team Scaling**: Share tacit knowledge with your team via git-committed skills

**Example Workflow**:
1. You struggle through a task and finally get it right
2. You say: "Capture this as a skill called 'ask-deployment-protocol'"
3. The agent analyzes the conversation and generates the `SKILL.md`
4. You verify and save it

---

#### 🏗️ ask-system-architect-prime
**Description**: Principal Software Architect for repository audits, complexity analysis, and actionable refactoring recommendations

**How to Use**:
```bash
ask copy antigravity --skill ask-system-architect-prime
```

**Use Cases**:
- **Full Repository Audit**: Analyze architecture, complexity, security, and test coverage
- **Performance Investigation**: Identify N+1 queries, blocking I/O, and bottlenecks
- **Security Review**: Scan for hardcoded secrets and vulnerabilities
- **Test Coverage Analysis**: Map source files to test suites and identify gaps

**Example Workflow**:
1. Deploy this skill to your agent
2. Ask: "Audit this repository for architectural flaws"
3. The agent generates an `ARCHITECTURAL_AUDIT.md` with health score, burn list, and recommendations

---

### 🚀 Quick Start with Skills

```bash
# Guided wizard (new in v0.6.0)
ask wizard

# Or use the docs site Command Builder — no terminal needed
# → https://navanithans.github.io/Agent-Skill-Kit/

# View all available skills
ask list

# Deploy a specific skill to an agent
ask copy gemini --skill ask-bug-finder --global

# Deploy all compatible skills to an agent
ask copy claude --all

# Sync all skills to all agents
ask sync all

# Create your own skill (interactive)
ask create skill
```

## �📐 Skill Format

Each skill is a directory containing:
*   **`skill.yaml`**: Metadata (name, description, tags, supported agents).
*   **`README.md`**: The actual prompt/instructions for the AI.

> [!IMPORTANT]
> **Naming Convention**: All skill names must start with the `ask-` prefix (e.g., `ask-bug-finder`, `ask-commit-assistance`).

```yaml
# skill.yaml
name: ask-bug-finder
version: 1.0.0
category: coding
agents:
  - gemini
  - claude
  - cursor
depends_on:
  - ask-code-reviewer  # Automatically installed when bug-finder is installed
```

### SKILL.md Format (v2.0)

As of v0.2.0, SKILL.md files use a token-optimized format:

```markdown
---
name: ask-example
description: Brief description
triggers: ["trigger phrase 1", "trigger phrase 2"]
---

<critical_constraints>
❌ NO forbidden actions
✅ MUST required actions
</critical_constraints>

<heuristics>
- condition → action
</heuristics>
```

## 🧩 Design Principles

1.  **Universal Definition**: Skills are defined in a neutral format that can be adapted to any agent.
2.  **Local-First, Global-Ready**: Prioritize project-specific skills (checked into git) while supporting user-wide global skills.
3.  **Safe by Default**: The CLI will **never** silently overwrite an existing skill. It always asks.
4.  **Agentic Workflow**: The toolkit includes skills (`skill-creator`) specifically designed to help AI agents help *you* build more skills.

## 🗂 Repository Structure

```
agent-skill-kit/
├── ask/                     # CLI Source Code
│   ├── commands/            # copy, sync, purge, wizard, create, …
│   └── utils/               # adapter loader, filesystem helpers
├── agents/                  # Adapters for each AI agent
│   ├── gemini/
│   ├── claude/
│   ├── codex/
│   ├── antigravity/
│   └── cursor/
├── skills/                  # The Skill Library (38 skills)
│   ├── coding/
│   ├── planning/
│   ├── tooling/
│   └── manifest.json        # Auto-generated by ask skill compile
├── docs/                    # GitHub Pages site
│   └── index.html           # Generated by scripts/generate_site.py
└── scripts/
    └── generate_site.py     # Static site generator
```

## 🤝 Contributing

Contributions are welcome!
1.  **Create a Skill**: Use `ask create skill` and submit a PR with your best prompts.
2.  **Add an Agent**: Use `ask add-agent`, test it, and submit the new adapter.

## License

MIT
