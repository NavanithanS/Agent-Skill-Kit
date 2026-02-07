# Ask Skill Capture

Meta-skill. Analyzes the current session's lessons and saves them as a permanent reusable skill.

## Goal
Take the "lessons learned" from the current conversation and crystallize them into a new `SKILL.md` file so the agent doesn't make the same mistakes again.

## Usage Trigger
* User says: "Capture this as a skill called [name]"
* User says: "Save this workflow."
* User says: "Create a skill from this."

## Instructions

### Step 1: Analysis (The Extraction)
Look back at the last 10-20 turns of conversation. Identify:
1.  **Constraints:** Did the user say "Don't do X" or "Always do Y"?
2.  **Patterns:** Did we agree on a specific file structure or naming convention?
3.  **Tools:** Did we use specific libraries (e.g., FVM, Inertia)?

### Step 2: The Template
Generate a file at `.agent/skills/<skill-name>/SKILL.md` using this exact structure:

```markdown
---
name: <skill-name>
description: <One sentence summary of what this skill does>
---

## Goal
<What problem does this skill solve?>

## Critical Rules
<The strict constraints identified in the chat>

## Workflow
<The step-by-step process we followed to get the right result>
```

### Step 3: Verification
Before saving, ask the user to verify any specific library versions, commands, or critical rules identified. Present them clearly.

### Step 4: Review & Save
Present the generated Markdown to the user in a code block.

Ask: "Does this accurately capture what we just did?"

If confirmed, save the file to `.agent/skills/<skill-name>/SKILL.md` (or the appropriate skills directory for the user's project).

## Example
User: "Capture this as deploy-protocol."
Agent Action:
Thinking: User corrected me to use force: true and check the dist/ folder.
Drafting: Creates deploy-protocol with "Always check dist/ folder" as a rule.

## Trigger Phrases

Activate this skill when the user says things like:
- "Capture this as a skill"
- "Save this workflow"
- "Create a skill from our conversation"
- "Remember how we did this"
