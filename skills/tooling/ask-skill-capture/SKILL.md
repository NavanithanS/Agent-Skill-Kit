---
name: ask-skill-capture
description: Capture conversation lessons as permanent reusable skill files.
triggers: ["capture as skill", "save this workflow", "create skill from this", "remember how we did this"]
---

<critical_constraints>
❌ NO saving without user verification
✅ MUST analyze last 10-20 turns for lessons
✅ MUST use standard SKILL.md format with frontmatter
✅ MUST present draft for user approval before saving
</critical_constraints>

<workflow>
1. **Extract**: Review recent conversation for:
   - Constraints: "Don't do X", "Always do Y"
   - Patterns: file structures, naming conventions
   - Tools: specific libraries used
2. **Draft**: Generate SKILL.md with constraints/workflow
3. **Verify**: Ask user to confirm versions/commands
4. **Save**: Write to `.agent/skills/<name>/SKILL.md`
</workflow>

<template>
```markdown
---
name: <skill-name>
description: <One sentence summary>
triggers: ["phrase1", "phrase2"]
---

<critical_constraints>
❌ NO [forbidden pattern]
✅ MUST [required action]
</critical_constraints>

<workflow>
1. Step one
2. Step two
</workflow>
```
</template>

<example>
User: "Capture this as deploy-protocol"
Agent extracts: use force:true, check dist/ folder
Creates: deploy-protocol skill with those as rules
</example>
