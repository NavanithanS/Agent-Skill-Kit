# Ask Commit Assistance

This skill helps you review your code, stage changes, and prepare commit messages safely. It is strictly configured to **never** automatically commit files.

## Purpose

To provide a structured workflow for reviewing new code for bugs, secrets, and debug statements before staging. It ensures that the final commit is always a manual action by the user.

## Features

-   **Code Review**: Reviews recently created files for bugs and refactoring opportunities.
-   **Safety Checks**: Scans for secrets, debug code, and TODOs before committing.
-   **Staging**: Stages files after review (specific files only).
-   **Commit Messages**: Generates **Conventional Commits** (e.g., `feat: ...`, `fix: ...`) options.
-   **Zero Auto-Commit**: Guaranteed manual finalization.

## Usage

This skill is designed to be used by the agent when you ask for help with committing your changes.

1.  The agent identifies untracked or newly added files.
2.  The agent reviews and may suggest/apply fixes.
3.  The agent stages the reviewed files.
4.  The agent proposes commit messages.
5.  **You copy the final command and run it yourself.**

## Best Practices

> [!IMPORTANT]
> **Manual Commit Only**: AI agents using this skill are instructed to never run the `git commit` command. This ensures you have full control over the final repository state.
