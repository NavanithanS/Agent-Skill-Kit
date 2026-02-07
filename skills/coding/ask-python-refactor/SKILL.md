---
name: ask-python-refactor
description: Python refactoring for readability, maintainability, and performance.
triggers: ["refactor python", "improve python code", "make pythonic", "remove code smells"]
---

<critical_constraints>
❌ NO refactoring without tests first
❌ NO single-letter variables (n, x) → use descriptive names
❌ NO functions >20 lines → extract smaller functions
✅ MUST run tests after every change
✅ MUST commit frequently for easy rollback
</critical_constraints>

<naming>
Variables: descriptive nouns (user_count not n)
Functions: verb + object (calculate_total not calc)
Classes: entity nouns (OrderProcessor not OP)
</naming>

<code_smells>
- Duplicated code → extract to shared function
- Long parameter lists → group into dataclass
- Deep nesting → use early returns/guard clauses
- Magic numbers → replace with named constants
</code_smells>

<patterns>
## Dispatch Tables
```python
# Before: long if/elif chains
# After:
handlers = {'a': process_a, 'b': process_b}
handler = handlers.get(data.type, process_default)
return handler(data)
```

## Type Hints
```python
def get_user(user_id: int) -> Optional[User]:
    return db.find(user_id)
```
</patterns>

<workflow>
1. Ensure tests exist
2. Make small changes, verify each step
3. Run tests after every change
4. Commit frequently
5. Review diff before finalizing
</workflow>
