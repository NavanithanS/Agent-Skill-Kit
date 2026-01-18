---
name: ask-readme-gardener
description: Keeps documentation in sync with code by updating the README.md when features or APIs are added.
---

# Readme Gardener

Keeps documentation in sync with code.

## Purpose

To ensure the project documentation (specifically `README.md`) accurately reflects the current state of the codebase, preventing outdated or misleading information.

## When to Use

- **Trigger**: "I just added a new API endpoint."
- **Trigger**: "I changed the behavior of the `xyz` function."
- **When** the user explicitly asks to update the README.
- **When** you notice a discrepancy between code and documentation during a task.

## Instructions

1.  **Analyze the Change**
    *   Understand the new feature, API endpoint, or logic change.
    *   Identify the exact parameters, return values, and side effects.
    *   Look for a relevant "API Reference", "Usage", or "Features" section in `README.md`.

2.  **Draft the Update**
    *   **New Endpoint**: Add an entry with Method (GET/POST), URL, Parameters, and Example Response.
    *   **Modified Feature**: Update existing descriptions to match the new behavior.
    *   **New Feature**: Add a bullet point or section describing what it does and how to use it.

3.  **Update README.md**
    *   Edit the `README.md` file directly.
    *   Maintain the existing style and headers (e.g., table formats, code block styles).

## Example

**Trigger**: "I added a `/status` endpoint."

**Action**:
find `## API Reference` in `README.md` and append:

```markdown
### GET /status

Returns the current system status.

**Response**
```json
{
  "status": "ok",
  "uptime": 1234
}
```
```
