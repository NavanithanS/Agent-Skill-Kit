---
name: ask-wiki-init
description: Scaffolds the LLM Wiki pattern into any project — a persistent, compounding knowledge base maintained by AI agents.
triggers: ["init wiki", "setup wiki", "create wiki", "install llm wiki", "setup knowledge base", "bootstrap wiki", "add wiki to project"]
version: 1.0.0
inputs: {}
permissions:
  - filesystem:write
---

<critical_constraints>
1. **Idempotent**: NEVER overwrite existing `wiki/`. If exists → STOP, inform user.
2. **Smart Inject**: Use `<!-- ASK:wiki-rules:start -->` / `<!-- ASK:wiki-rules:end -->` delimiters in agent config files. Replace if exists; append if not.
3. **Domain-Aware**: MUST detect project type → customize SCHEMA.md entity types.
4. **Read Pattern**: Read `references/llm-wiki.md` before scaffolding. Understand layers (sources, wiki, schema) and ops (ingest, query, lint).
5. **Config**: MUST load `config/identity.json` (Persona) and `config/settings.yaml` (Targets).
</critical_constraints>

<process>
### 1. Pre-Flight
- Load `config/identity.json` and assume the Persona.
- Load `config/settings.yaml`.
- `wiki/` exists? → STOP.
- `.docs/decisions.md` exists? → Note overlap with `ask-project-memory`.

### 2. Detect Project
Scan manifests: `package.json`, `composer.json`, `pyproject.toml`, `pubspec.yaml`, `Cargo.toml`, `go.mod`, `Gemfile`.
Extract: project name, language, framework. No manifest? → Ask user or use generic template.

### 3. Scaffold Base
Create from `resources/schema-template.md`:

```
wiki/
├── SCHEMA.md     # Replace {{PROJECT_NAME}}, adapt structure to project domain, AND generate a custom "Source of truth" table mapping 5-10 facts to specific codebase files.
├── index.md      # Section headers based on domain
├── log.md        # First entry: "[YYYY-MM-DD] ingest | Wiki initialized"
├── overview.md   # Will be populated in next step
```

### 4. Deep Auto-Ingestion (Stateful Orchestrator Pattern)
To bypass LLM output limits and force massive, deep documentation generation, you MUST act as a stateful orchestrator and follow this strict checklist sequence:
1. **Analyze Codebase**: Read `README.md` and *any* other `.md` files in the root. You MUST also actively read `composer.json`, `package.json`, `docker-compose.yml`, `.env.example`, or similar manifest files to explicitly identify the frameworks, dependencies, and tech stack (e.g., Laravel, Vue, React). Scan source directories (`app/`, `src/`, `resources/`) to map domain entities, services, and integrations.
2. **Create Plan**: Create a temporary file at `wiki/INGESTION_PLAN.md` explicitly listing **7 to 15 deep pages** you intend to generate. Plan pages **by category**:
   - **Architecture** (2-4 pages): `tech-stack.md` (MANDATORY), `request-flow.md`, `routing.md`, etc.
   - **Modules** (2-5 pages): one per major feature area or domain module.
   - **Entities** (1-3 pages): key data models, their relationships, and schemas.
   - **Integrations** (1-3 pages): external APIs, payment gateways, third-party services.
   Complex projects should target the upper range (12-15 pages). Simple projects may use 7-10.
3. **Sequential Execution**: You MUST IMMEDIATELY proceed to generate the pages listed in `INGESTION_PLAN.md` **one by one** using separate consecutive tool calls. Do NOT stop and wait for the user. After generating a page, update `INGESTION_PLAN.md` to check it off. You must autonomously loop through the entire plan until every page is checked off.
   - **Every page** MUST end with a `## See also` section containing wiki-links to related pages.
   - **Architecture pages** SHOULD include ASCII layered diagrams where the system has distinct layers (frontend → bridge → backend → database).
4. **Write `overview.md`**: This page MUST follow a strict structure:
   - `## What it is` — one-paragraph project description.
   - `## Who it's for` — target audiences (e.g., admins, end users, API consumers).
   - `## Core capabilities` — bullet list of major features.
   - `## Key numbers` — hard metrics extracted from the codebase (e.g., "85 models", "73 controllers", "18 services").
   - `## See also` — cross-links to related wiki pages.
5. **Core Files Recovery**: You MUST modify the existing `README.md` and `AGENTS.md` (or generate them if sparse/missing) to properly integrate the wiki. In `README.md`, do NOT just dump a link; instead, create a clean, professional section like `## AI Knowledge Base` with a bullet point `📖 [Explore the Wiki](wiki/index.md)`.
6. **Finalize**: Populate `index.md` using markdown tables (`| Page | Summary |`) grouped by category. Then delete `wiki/INGESTION_PLAN.md`.

### 5. Inject Rules
Read `resources/wiki-rules.md`. For each existing config from `config/settings.yaml` (`target_configs`):
- Delimiters present → replace block.
- No delimiters → append block.
- File missing → skip.

### 6. Gitignore
Append `wiki/.obsidian/` to `.gitignore` if not present.

### 7. Report
List all scaffolded files, generated content pages, and updated configs.
</process>

<heuristics>
- **No README**: Use directory name as project name.
- **Monorepo**: Ask user which package the wiki covers.
- **Existing `wiki/` with different structure**: DO NOT modify. Inform user.
</heuristics>
