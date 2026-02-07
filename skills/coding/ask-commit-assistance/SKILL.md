---
name: ask-commit-assistance
description: Code review, staging, and Conventional Commit message generation.
triggers: ["review my changes", "help commit", "draft commit message", "check for secrets"]
---

<critical_constraints>
❌ NO `git add .` → stage specific files only
❌ NO auto-running `git commit` → provide command for user
❌ NO committing secrets/debug code without warning
✅ MUST scan for API keys, tokens, passwords before staging
✅ MUST use Conventional Commits format
✅ MUST offer detailed and short message options
</critical_constraints>

<workflow>
1. **Identify new files**: `git status`, `git diff --cached --name-only --diff-filter=A`
2. **Review**: Check for bugs, refactoring opportunities
3. **Safety scan**: API keys, debug code (print/console.log/dd), TODO/FIXME
4. **Stage**: `git add <file>` for reviewed files only
5. **Draft message**: Conventional Commits format, two options
6. **Present command**: `git commit -m "..."` for user to run
</workflow>

<safety_scan>
Check for:
- Secrets: API keys, tokens, passwords
- Debug: print(), console.log(), dd()
- Markers: TODO, FIXME, HACK
→ Warn user before staging if found
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
git commit -m "feat(scope): description"
```
</commands>
