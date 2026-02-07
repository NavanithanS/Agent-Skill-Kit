---
name: ask-adr-logger
description: Automatically records Architectural Decision Records (ADRs) when a significant technical decision is made.
---

# ADR Logger

Automatically records Architectural Decision Records (ADRs) when a significant technical decision is made.

## Purpose

To capture the context, decision, and consequences of architectural changes in a consistent format (ADR). This helps document the "why" behind technical choices for future reference.

## When to Use

- **Immediately after** agreeing on a tech stack change (e.g., "Switch to Tailwind").
- **When** a significant design pattern is adopted.
- **When** a major dependency is added or removed.
- **When** a structural change to the codebase is decided.

## Usage

Use the provided script to generate a new ADR file.

```bash
python skills/planning/ask-adr-logger/scripts/create_adr.py --title "Use Tailwind CSS"
```

The script will:
1.  Find the next available ADR number (e.g., `001`, `002`).
2.  Create a file in `docs/ADR/` (e.g., `docs/ADR/001-use-tailwind-css.md`).
3.  Populate it with the standard ADR template.

## Template Content

The generated file will include:

-   **Title**: The decision name.
-   **Context**: What was the problem? What were the options?
-   **Decision**: What did we choose?
-   **Consequences**: What are the trade-offs (good and bad)?

## Trigger Phrases

Activate this skill when the user says things like:
- "Log an ADR"
- "Record this architectural decision"
- "Create a decision record"
- "We are choosing technology X"

