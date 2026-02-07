---
name: ask-bug-finder
description: Systematic debugging with reproduction, isolation, and hypothesis testing.
triggers: ["help find this bug", "debug this error", "why is this failing", "systematic debugging"]
---

<critical_constraints>
❌ NO fixing without reproducing first
❌ NO changing random things hoping it works
❌ NO fixing symptoms instead of root cause
✅ MUST read full error message including stack trace
✅ MUST form hypothesis before making changes
✅ MUST write test after fixing to prevent recurrence
</critical_constraints>

<process>
1. **Reproduce**: consistent steps, expected vs actual, all environments?
2. **Gather**: error messages, logs, recent changes, environment
3. **Hypothesize**: which component, simplest explanation?
4. **Test**: strategic logging, assertions, comment out sections
5. **Fix**: minimal change, verify, check regressions, add test
</process>

<techniques>
- **Binary Search**: git bisect to find breaking commit
- **Rubber Duck**: explain problem aloud, bug reveals itself
- **Divide & Conquer**: midpoint check, narrow scope
- **Print Debug**: `[DEBUG] func_name: var={var}` (not just "here")
</techniques>

<common_patterns>
- Off-by-one: `range(len(x)-1)` → should be `range(len(x))`
- Null reference: `user.name` without checking `user is None`
- Race condition: check-then-act pattern
- State mutation: `items.sort()` modifies original
</common_patterns>

<tools>
| Tool | Use |
|------|-----|
| Debugger (pdb) | step through, inspect |
| Logger | track execution flow |
| Profiler | performance issues |
| git bisect | find breaking commit |
</tools>

<when_stuck>
1. Take a break
2. Explain to someone (rubber duck)
3. Check the obvious (is server running?)
4. Search for similar issues
5. Create minimal reproduction
</when_stuck>
