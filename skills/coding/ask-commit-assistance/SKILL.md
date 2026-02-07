---
name: ask-commit-assistance
description: A skill to assist with code review, staging, and committing changes.
---

# Ask Commit Assistance

This skill helps you review your code, stage changes, and prepare commit messages.

## 1. Code Review and Refactor

**Goal**: Review and fix bugs or refactor code in **recently created files only**.

### Instructions:
1.  **Identify New Files**:
    -   Run `git status` to find untracked files or files added as "new file".
    -   Run `git diff --cached --name-only --diff-filter=A` to find added files currently staged.
    -   Run `git ls-files --others --exclude-standard` to find untracked files.
2.  **Review**:
    -   For each identified new file, read the content.
    -   Check for bugs, potential errors, and refactoring opportunities (clean code, naming conventions, etc.).
3.  **Fix/Refactor**:
    -   If valid issues are found, apply the fixes directly to the files.

## 2. Safety Check

**Goal**: Ensure no sensitive data or temporary code is committed.

### Instructions:
1.  **Scan Content**: Check the files you are about to stage/review for:
    -   **Secrets**: API keys, exact tokens, passwords.
    -   **Debug Code**: `print()`, `console.log()`, `dd()`, etc. (unless necessary for the script).
    -   **Markers**: `TODO`, `FIXME`, `HACK`.
2.  **Warn User**: If any are found, explicitly ask the user if they intend to commit them.

## 3. Stage Changes

**Goal**: Stage the files after review and fixes.

### Instructions:
1.  Run `git add <file>` for the specific files you reviewed and fixed.
2.  **Avoid** `git add .` unless you are certain it won't include unwanted files (like `.DS_Store` or logs).

## 4. Prompt Commit Note

**Goal**: Generate commit messages following **Conventional Commits**.

### Instructions:
1.  Analyze the staged changes (`git diff --cached`).
2.  Draft two versions using the [Conventional Commits](https://www.conventionalcommits.org/) format (`type(scope): description`):
    -   **Option 1 (Detailed)**: `type(scope): subject` followed by a body explaining *why* and *what*.
    -   **Option 2 (Short)**: Just the `type(scope): subject` line.
    -   *Types include: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.*
3.  Present these options to the user.

## 5. Manual Commit

**Goal**: Let the user finalize the commit.

### Instructions:
1.  Do **not** run `git commit` yourself.
2.  Provide the `git commit -m "..."` command for the chosen message.
3.  Example output:
    > Here is the command to commit:
    > `git commit -m "feat(auth): implement login flow"`

## Trigger Phrases

Activate this skill when the user says things like:
- "Review my changes"
- "Help me commit code"
- "Draft a conventional commit message"
- "Check for secrets before committing"

