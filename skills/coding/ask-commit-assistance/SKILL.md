---
name: ask-commit-assistance
description: Code review, staging, and Conventional Commit message generation. MUST NOT COMMIT.
triggers: ["review my changes", "help commit", "draft commit message", "check for secrets"]
---

# Ask Commit Assistance

This skill assists in the "pre-commit" phase: scanning for secrets, reviewing new code, and staging files.

<critical_constraints>
❌ **NEVER AUTO-COMMIT**: Execution of `git commit` is strictly forbidden for the agent. DO NOT execute it under any circumstance, even if requested.
❌ NO `git add .` → stage specific files only.
❌ NO committing secrets/debug code without explicit user confirmation.
✅ **BRANCH CHECK**: MUST verify the current branch. If on `release` (or a branch containing `release`), MUST stop and prompt user to confirm if they need to change branches.
✅ **ATOMIC COMMITS**: If changes span multiple unrelated domains, you MUST suggest splitting them into separate atomic commits.
✅ MUST scan for API keys, tokens, passwords before staging.
✅ MUST use Conventional Commits format for suggested messages.
✅ MUST offer detailed and short message options.
✅ **USER FINALIZATION**: Always provide the final `git commit` command for the user to execute manually.
</critical_constraints>

<workflow>
1. **Check Current Branch**: Run `git branch --show-current`. If the current branch is `release` (or contains `release`), **STOP immediately** and ask the user if they need to change branches before proceeding.
2. **Review Unstaged Changes**: Run `git status`, `git diff`, and `git ls-files --others --exclude-standard` to inspect the full contents of all modified and untracked files before staging them. 
3. **Safety scan**: Scan content for API keys, debug code (print/console.log/dd), and TODO/FIXME markers.
4. **Code Review**: Check for bugs, naming conventions, and refactoring opportunities. Suggest atomic splits if the scope is too broad.
5. **Stage**: Run `git add <file>` specifically for reviewed and approved files.
6. **Ticket Linking**: Ask the user if this commit relates to an active Issue or Jira Ticket (e.g., `#123`).
7. **Draft message**: Propose two Conventional Commits options (Detailed and Short). Ensure the body text wraps at 72 characters.
8. **Handover**: Provide the final `git commit -m "..."` command to the user. **DO NOT run it yourself.**
</workflow>

<safety_scan>
Check for:
- Secrets: API keys, tokens, passwords
- Debug: print(), console.log(), dd()
- Markers: TODO, FIXME, HACK
→ Warn user before staging if found. No automated cleanup unless requested.
</safety_scan>

<commit_format>
Types: feat, fix, docs, style, refactor, test, chore
Format: `type(scope): description`

Rule: The commit message body MUST wrap at 72 characters to conform with Git log standards.

Option 1 (detailed): subject + body explaining why/what + optional footer (e.g., Fixes #123)
Option 2 (short): just subject line
</commit_format>

<commands>
```bash
git branch --show-current
git status
git diff
git diff --cached
git ls-files --others --exclude-standard
git add <file>
# FOR USER ONLY:
# git commit -m "feat(scope): description"
```
</commands>
