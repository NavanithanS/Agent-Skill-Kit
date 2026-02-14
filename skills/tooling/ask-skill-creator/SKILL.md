---
name: ask-skill-creator
description: >
  Use this skill when the user asks to create a new skill or add a new capability to the Agent Skill Kit.
  Triggers: "create a skill", "new skill", "add skill for", "teach the agent".
  
  Do NOT use this skill for:
  - Creating normal software features (use a coding architect).
  - Modifying the core ASK runtime.

  Capabilities:
  - Scaffolds the "Gold Standard" directory structure (SKILL.md, scripts/, assets/, tests/).
  - Generates optimized Frontmatter and Algorithmic Instructions.
  - Updates the root README.md.
---

# Skill Creation Protocol

## <critical_constraints>
1. ❌ **NO** generic descriptions. Be highly specific and semantic.
2. ❌ **NO** missing directories. MUST create `scripts/`, `assets/`, `tests/`.
3. ✅ **MUST** prefix skill name with `ask-` and use kebab-case.
4. ✅ **MUST** include `<critical_constraints>`, `<process>`, and `<thinking>` sections in the new `SKILL.md`.
</critical_constraints>

## <file_structure>
skills/<category>/<skill-name>/
├── SKILL.md          # 🧠 The Brain (Frontmatter + Protocol)
├── scripts/          # 🛡️ Guardrails (Empty .py/.js placeholders)
├── assets/           # 📚 Knowledge (examples.md)
└── tests/            # 🧪 Verification (case1.md)
</file_structure>

## <process>
1. **Analyze Request**:
   - Determine `category` (coding, planning, tooling).
   - Determine `skill-name` (must start with `ask-`).

2. **<thinking> Template Design**:
   - Draft the `SKILL.md` frontmatter with clear `Triggers` and `Negative Constraints`.
   - Design 3-5 algorithmic steps for the `<process>` section.
   - Plan at least one "Critical Constraint" specific to this skill.
   </thinking>

3. **Scaffold Directory**:
   - Create `skills/<category>/<skill-name>/`.
   - Create subfolders: `scripts/`, `assets/`, `tests/`.

4. **Generate Content**:
   - **`SKILL.md`**: Write the full protocol.
   - **`assets/examples.md`**: Create a placeholder or basic example.
   - **`tests/case1.md`**: Create a sample input/output test case.

5. **Register**:
   - Update the root `README.md` skill table with the new skill.
</process>

## <templates>

### SKILL.md Frontmatter
```yaml
---
name: ask-example-skill
description: >
  Use when [user intent].
  Triggers: "phrase 1", "phrase 2".
  
  Do NOT use for:
  - [Constraint 1]
---
```

### SKILL.md Body
```markdown
# [Skill Name] Protocol

## <critical_constraints>
1. ...
</critical_constraints>

## <process>
1. **Step 1**: ...
2. **<thinking> Plan**: ...
   </thinking>
3. **Step 3**: ...
</process>
```
</templates>
