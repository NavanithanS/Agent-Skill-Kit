---
name: ask-skill-creator
description: Meta-skill for creating new skills in Agent Skill Kit.
triggers: ["create a skill", "new skill", "add skill for"]
---

<critical_constraints>
❌ NO skill names without `ask-` prefix
❌ NO generic descriptions → be specific
❌ NO skipping SKILL.md frontmatter
✅ MUST create: skill.yaml, README.md, SKILL.md
✅ MUST update root README.md skill table
✅ MUST follow kebab-case naming
</critical_constraints>

<naming_rules>
- Prefix: `ask-` (required)
- Format: lowercase-with-hyphens
- Length: 2-50 chars
- Chars: letters, numbers, hyphens only
✓ ask-python-refactor, ask-git-workflow
✗ python-refactor, MySkill, skill_1
</naming_rules>

<categories>
coding: programming, languages, refactoring
planning: analysis, decision-making, reasoning
tooling: tools, workflows, automation, meta-skills
</categories>

<file_structure>
skills/<category>/<skill-name>/
├── skill.yaml    # Metadata
├── README.md     # Documentation
└── SKILL.md      # Protocol (frontmatter + content)
</file_structure>

<templates>
## skill.yaml
```yaml
name: ask-example
version: 1.0.0
category: coding
description: Brief description (max 100 chars)
tags: [relevant, tags]
agents: [codex, gemini, claude, antigravity]
```

## SKILL.md
```markdown
---
name: skill-name
description: Brief description
triggers: ["phrase1", "phrase2"]
---

<critical_constraints>
❌ NO [forbidden]
✅ MUST [required]
</critical_constraints>

<heuristics>
- condition → action
</heuristics>
```
</templates>

<workflow>
1. Clarify: purpose, category, scope
2. Generate: skill.yaml, README.md, SKILL.md
3. Write to skills/<category>/<name>/
4. Update root README.md skill table
5. Verify: YAML valid, all fields present
</workflow>
