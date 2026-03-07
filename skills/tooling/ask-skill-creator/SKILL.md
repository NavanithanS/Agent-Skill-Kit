---
name: ask-skill-creator
description: >
  Master Architect for creating new Agent Skills.
  Enforces the "Gold Standard" architecture: Config-driven, Resilient, and Lint-Compliant.
version: 2.0.0
permissions:
  - filesystem:write
  - agent:install
inputs:
  topic:
    description: The domain or capability to teach (e.g., "Postgres Migration", "HubSpot API").
    required: true
---

# Agent Skill Creation Protocol

## <critical_constraints>
1. **The Configuration Rule**: NEVER hardcode magic strings (URLs, creds, IDs). ALWAYS extract to `config/*.json` or `config/*.yaml`.
2. **The Anti-Flake Rule**: NEVER use `sleep()`. ALWAYS use Semantic State Polling (wait for element/condition).
3. **The Linting Rule**: Design for the 1000-Token Limit. Use telegraphic style (bullet points, no fluff). Run `ask skill lint` immediately.
4. **The Persona Rule**: ALWAYS define the agent's identity in `config/identity.json` (even if simple).
5. **The Structure Rule**: MUST generate the full tree:
   - `SKILL.md`: The Brain.
   - `scripts/`: The Hands (Logic).
   - `config/`: The Memory (Data).
   - `tests/`: The Proof (Verification).
</critical_constraints>

## <process>
### 1. Taxonomy & Scaffolding
- **Analyze Request**:
  - **Category**: `coding` (Dev), `planning` (Arch), `tooling` (Infra).
  - **Name**: `ask-<topic>` (kebab-case).
- **Create Tree**:
  ```text
  skills/<category>/ask-<topic>/
  ├── SKILL.md                 # Protocol
  ├── skill.yaml               # Metadata
  ├── config/                  # Data Separation
  │   ├── identity.json        # Persona
  │   └── settings.yaml        # Toggles/Selectors
  ├── scripts/                 # Logic Encapsulation
  │   └── helper.js            # Complex math/parsing
  ├── assets/                  # Knowledge
  │   └── examples.md
  └── tests/                   # QA
      └── case1.md
  ```

### 2. Protocol Design (SKILL.md)
- **Frontmatter**: Define `inputs` and `permissions` explicitly.
- **Critical Constraints**: Define 3-5 "NEVER/ALWAYS" rules specific to the domain.
- **Process**:
  - **Initialization**: Load config. Calculate derived state.
  - **Detection**: How to identify the environment context.
  - **Execution**: Step-by-step logic.
  - **Heuristics**: "If X happens, do Y" (Self-Healing).

### 3. Content Generation
- **`skill.yaml`**:
  - Name, Version, Description.
  - Tags: `[domain, capability, tool]`.
  - Agents: `[antigravity, codex]`.
- **`config/identity.json`**:
  - Define the "Expert Persona" (e.g., "Senior DBA", "Security Auditor").
- **`scripts/*.js`**:
  - Offload complex logic (Regex, Math, API transforms) here. Keep `SKILL.md` for high-level flow.

### 4. Verify
- **Lint**: `ask skill lint ask-<topic>`. Fix lengths.
- **Register**: `skills/manifest.json`.
</process>

## <templates>

### SKILL.md Skeleton
```markdown
---
name: ask-example
description: [Task] specialist.
version: 1.0.0
inputs:
  target: {required: true}
---

# Protocol

## <critical_constraints>
1. **Safety**: NEVER [dangerous action].
2. **Config**: Load `config/settings.yaml`.
</critical_constraints>

## <process>
### 1. Detect
- Scan env. Load Identity.

### 2. Execute
- Action -> Verify.
</process>

## <heuristics>
- **Error**: If [Error], try [Fix].
```

### Config Skeleton (identity.json)
```json
{
  "role": "Expert",
  "capabilities": ["audit"],
  "strict_mode": true
}
```
</templates>

## <reasoning_engine>
1. **Logic?** -> `scripts/`.
2. **Data?** -> `config/`.
3. **Rule?** -> `<critical_constraints>`.
4. **Flow?** -> `SKILL.md`.

**Optimization**:
- "Telegraphic": "Locate widget. Click Next."
- No Politeness: "MUST", "DO".
</reasoning_engine>
