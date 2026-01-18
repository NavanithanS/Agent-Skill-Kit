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

## 2. Stage Changes

**Goal**: Stage the files after review and fixes.

### Instructions:
1.  Run `git add <file>` for the files you reviewed and fixed.
2.  If you are confident, you may run `git add .` to stage all changes, but prefer adding specific files to be precise.

## 3. Prompt Commit Note

**Goal**: Generate commit messages for the user to choose from.

### Instructions:
1.  Analyze the staged changes (`git diff --cached`).
2.  Draft two versions of the commit message:
    -   **Option 1 (Long)**: A detailed message describing *why* and *what* changed.
    -   **Option 2 (Short)**: A concise, one-line summary (imperative mood, e.g., "Add feature X").
3.  Present these options to the user clearly.

## 4. Manual Commit

**Goal**: Let the user finalize the commit.

### Instructions:
1.  Do **not** run `git commit` yourself.
2.  Provide the `git commit -m "..."` command for the chosen message (or tell the user they can copy-paste their preferred message).
3.  Example output:
    > Here is the command to commit with the short message:
    > `git commit -m "Your short message here"`
