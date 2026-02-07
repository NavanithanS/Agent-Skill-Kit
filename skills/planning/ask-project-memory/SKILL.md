---
name: ask-project-memory
description: Maintain project brain with architectural decisions in memory file.
triggers: ["record decision", "we decided to", "update project memory", "check past decisions"]
---

<critical_constraints>
✅ MUST read decisions file before starting new tasks
✅ MUST not violate past decisions
✅ MUST append new decisions in structured format
</critical_constraints>

<workflow>
1. **Read**: Check if `.docs/decisions.md` exists
2. **Update**: Append new decision in structured format
3. **Reference**: Read before any new task to ensure consistency
</workflow>

<format>
```markdown
## [Date] Decision: Use UUIDs
* **Context:** Needed for security/scaling.
* **Decision:** All new migrations must use `$table->uuid('id')`.
* **Status:** Accepted.
```
</format>
