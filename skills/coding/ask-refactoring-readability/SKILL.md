---
name: ask-refactoring-readability
description: Refactor code for readability using DRY, meaningful names, and modularization.
triggers: ["make this readable", "simplify this logic", "refactor for clarity", "clean up this code"]
---

<critical_constraints>
❌ NO behavior changes → refactoring only
❌ NO applying without approval
❌ NO generic names (data, temp, obj, x)
✅ MUST show before/after diffs
✅ MUST explain why each change improves code
✅ MUST verify tests pass after each change
</critical_constraints>

<techniques>
1. **Rename**: Use descriptive names conveying intent
2. **Extract**: Break large functions into single-responsibility units
3. **Flatten**: Replace nesting with guard clauses/early returns
4. **DRY**: Consolidate repeated code into reusable functions
5. **Simplify**: Replace complex conditionals with lookup tables
</techniques>

<templates>
## Flatten Nesting (Guard Clauses)
```python
# Before: deep nesting
if user:
    if user.is_active:
        if user.has_permission('edit'):
            # logic

# After: guard clauses
if not user: return False
if not user.is_active: return False
if not user.has_permission('edit'): return False
# logic
```

## Extract Function
```javascript
// Before: all-in-one
function handleOrder(order) { /* validate, calc, discount */ }

// After: composed
function handleOrder(order) {
    validateOrder(order);
    const subtotal = calculateSubtotal(order.items);
    return applyDiscount(subtotal, order.discountCode);
}
```
</templates>

<heuristics>
- Function >20 lines → extract smaller functions
- Nesting >3 levels → use guard clauses
- Same code in 2+ places → extract to shared function
- Single-letter variables → rename to descriptive
</heuristics>
