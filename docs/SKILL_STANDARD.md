# Agent Skill Kit: The "Gold Standard" Architecture

## 1. Core Philosophy
Skills are not just prompt files; they are **semantic contracts** between the user's intent and the agent's capabilities.
We strictly adhere to Anthropic's "Building Skills for Claude" guide, prioritizing:
1.  **Progressive Disclosure**: Only load what is needed, when it is needed.
2.  **Cognitive Optimization**: Algorithmic instructions over prose.
3.  **Operational Excellence**: Proactive validation and testing.

## 2. Directory Structure (The Anatomy)
Every skill must reside in `skills/<category>/<skill-name>/` and follow this structure:

```text
skills/coding/ask-feature-name/
├── SKILL.md          # 🧠 The Brain: Frontmatter + Instructions
├── scripts/          # 🛡️ The Guardrails: Validation & Execution logic
│   └── validate.py
├── assets/           # 📚 The Knowledge: Templates & Docs (Loaded on demand)
│   └── examples.md
└── tests/            # 🧪 The Proof: Verification cases (Undertrigger/Overtrigger)
    └── case1_basic.md
```

### 2.1 Component Breakdown
- **`SKILL.md`**: The entry point. Contains metadata (Frontmatter) and the high-level logic (Protocol).
- **`scripts/`**: Executable code (Python/JS/Bash) that the skill *must* run to verify its work.
- **`assets/`**: Heavy contexts (long examples, API docs, large templates) that should *not* pollute the main context unless requested.
- **`tests/`**: Input prompts and expected outputs used to verify the skill triggers correctly and produces valid results.

## 3. Naming Conventions
- **Directories**: Strict **kebab-case** (e.g., `ask-react-architect`, not `AskReact` or `react_architect`).
- **Files**: `SKILL.md` is **case-sensitive** and mandatory.

## 4. `SKILL.md` Standard

### 4.1 Frontmatter (Level 1 Disclosure)
The header is the *only* thing the model sees initially. It must be highly optimized for retrieval.

```yaml
---
name: ask-specific-skill-name
description: >
  Use this skill when [user intent].
  Triggers: "phrase 1", "phrase 2".
  
  Do NOT use for:
  - [Negative Constraint 1]
  - [Negative Constraint 2]
  
  Capabilities:
  - [Capability 1]
  - [Capability 2]
---
```

### 4.2 The Protocol (Level 2 Disclosure)
Instructions must be **Algorithmic** and strictly structured.

#### Required Sections:
1.  **`<critical_constraints>`**: The "Thou Shalt Not" rules.
2.  **`<process>`**: A numbered list of steps.
3.  **`<thinking>` (CoT)**: Explicit instruction to plan before acting.

#### Example Protocol:
```markdown
# [Skill Name] Protocol

## <critical_constraints>
1. ❌ NO code execution without validation.
2. ✅ MUST output in Markdown.
</critical_constraints>

## <process>
1. **Analyze Request**: Identify the target file.
2. **<thinking> Plan**: 
   - Check if X exists.
   - Determine if Y is needed.
   </thinking>
3. **Execute**: Run the `scripts/validate.py`.
4. **Report**: Output results.
</process>
```

## 5. Validation Gates (Level 3 Execution)
Skills should not rely on "learning from mistakes". They must verify success *before* reporting to the user.
- **Pattern**: `Execution -> Validation Script -> User Notification`
- If the script fails, the agent must fix the issue and retry *without* bothering the user.
