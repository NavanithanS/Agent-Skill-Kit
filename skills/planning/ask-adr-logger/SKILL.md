---
name: ask-adr-logger
description: Record Architectural Decision Records for significant technical decisions.
triggers: ["log adr", "record decision", "create decision record", "choosing technology"]
---

<critical_constraints>
✅ MUST use standard ADR format
✅ MUST include: Title, Context, Decision, Consequences
✅ MUST auto-number files (001, 002, etc.)
</critical_constraints>

<when_to_use>
- Tech stack change (e.g., "Switch to Tailwind")
- Design pattern adoption
- Major dependency added/removed
- Structural codebase change
</when_to_use>

<usage>
```bash
python skills/planning/ask-adr-logger/scripts/create_adr.py --title "Use Tailwind CSS"
```
Creates: `docs/ADR/001-use-tailwind-css.md`
</usage>

<template>
**Title**: The decision name
**Context**: Problem and options considered
**Decision**: What was chosen and why
**Consequences**: Trade-offs (good and bad)
</template>
