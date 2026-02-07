---
name: ask-project-memory
description: Maintains a 'Project Brain' by recording architectural decisions and tech stack choices in a memory file.
---

## Goal
Stop the "Groundhog Day" effect where we re-discuss the same decisions.

## Instructions
**Trigger:** We make a decision (e.g., "Use UUIDs for all models", "Use dark mode by default").

### Action
1.  **Read:** Check if `.docs/decisions.md` (or `ADR.md`) exists.
2.  **Update:** Append the new decision in a structured format:
    ```markdown
    ## [Date] Decision: Use UUIDs
    * **Context:** Needed for security/scaling.
    * **Decision:** All new migrations must use `$table->uuid('id')`.
    * **Status:** Accepted.
    ```
3.  **Reference:** Before starting any *new* task, read this file to ensure you aren't violating past decisions.

## Trigger Phrases

Activate this skill when the user says things like:
- "Record this decision"
- "We decided to use..."
- "Update project memory"
- "Check past decisions about..."

