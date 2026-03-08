---
name: ask-commit-assistance
description: Code review, staging, and Conventional Commit message generation. MUST NOT COMMIT.
triggers: ["review my changes", "help commit", "draft commit message", "check for secrets"]
---

# Ask Commit Assistance

This skill assists in the "pre-commit" phase: scanning for secrets, reviewing new code, and staging files.

<critical_constraints>
❌ **NEVER AUTO-COMMIT**: Execution of `git commit` is strictly forbidden for the agent.
❌ NO `git add .` → stage specific files only.
❌ NO committing secrets/debug code without explicit user confirmation.
✅ MUST scan for API keys, tokens, passwords before staging.
✅ MUST use Conventional Commits format for suggested messages.
✅ MUST offer detailed and short message options.
✅ **USER FINALIZATION**: Always provide the final `git commit` command for the user to execute manually.
</critical_constraints>

<workflow>
1. **Identify new files**: Run `git status`, `git diff --cached --name-only --diff-filter=A`
2. **Code Review**: Check for bugs, naming conventions, and refactoring opportunities.
3. **Safety scan**: Scan content for API keys, debug code (print/console.log/dd), and TODO/FIXME markers.
4. **Stage**: Run `git add <file>` specifically for reviewed and approved files.
5. **Draft message**: Propose two Conventional Commits options (Detailed and Short).
6. **Handover**: Provide the final `git commit -m "..."` command and wait for the user.
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

Option 1 (detailed): subject + body explaining why/what
Option 2 (short): just subject line
</commit_format>

<commands>
```bash
git status
git diff --cached --name-only --diff-filter=A
git ls-files --others --exclude-standard
git add <file>
# FOR USER ONLY:
# git commit -m "feat(scope): description"
```
</commands>
