---
name: refactoring-readability
description: Refactor code to enhance readability, following principles like DRY, meaningful names, and modularization.
---

# Refactoring for Readability

A skill that improves code structure without altering behavior, prioritizing clarity and maintainability.

## Purpose

To refactor code for enhanced readability, reduced complexity, and better maintainability—all while preserving the original functionality. This skill helps developers clean up legacy or verbose code by applying industry-standard best practices.

## When to Use

- The user requests refactoring or cleanup of legacy/verbose code
- Code needs simplification without changing behavior
- The codebase has grown unwieldy with nested logic or repetitive patterns
- Variable/function names are unclear or non-descriptive
- Code doesn't follow project conventions (e.g., PEP 8 for Python, ESLint for JavaScript)

## How to Proceed

1. **Verify Functionality Remains Unchanged**:
   - Understand what the code is *supposed* to do before making changes.
   - Identify existing tests or write quick tests to validate behavior post-refactor.
   - If no tests exist, document the expected inputs and outputs.

2. **Apply Improvements**:
   - **Rename Variables/Functions**: Use meaningful, descriptive names that convey intent.
   - **Extract Functions**: Break large functions into smaller, single-responsibility units.
   - **Reduce Nesting**: Flatten deeply nested conditionals using early returns or guard clauses.
   - **Remove Duplication (DRY)**: Consolidate repeated code into reusable functions or constants.
   - **Add Comments Sparingly**: Only where the *why* isn't obvious; prefer self-documenting code.
   - **Simplify Logic**: Replace complex conditionals with clear boolean expressions or lookup tables.

3. **Follow Project Conventions**:
   - Identify and adhere to the project's style guide (PEP 8, Airbnb, Google Style, etc.).
   - Match existing patterns in the codebase for consistency.
   - Use appropriate formatting tools (Black, Prettier, gofmt) if available.

4. **Present Diffs with Explanations**:
   - Show a clear before/after comparison for each change.
   - Explain *why* each change improves readability or maintainability.
   - Highlight any potential risks or edge cases that were considered.

5. **Seek Approval Before Applying**:
   - Never apply changes without user confirmation.
   - Offer to make changes incrementally if the refactoring is extensive.
   - Allow the user to prioritize which changes to apply first.

## Examples

### Example 1: Renaming & Simplifying

**Before**:
```python
def f(d):
    r = []
    for i in range(len(d)):
        if d[i] > 0:
            r.append(d[i] * 2)
    return r
```

**After**:
```python
def double_positive_values(data):
    """Return a list of doubled positive values from the input data."""
    return [value * 2 for value in data if value > 0]
```

**Explanation**: Renamed `f` to `double_positive_values` to describe intent. Used list comprehension to reduce verbosity and improve readability.

---

### Example 2: Reducing Nesting with Guard Clauses

**Before**:
```python
def process_user(user):
    if user is not None:
        if user.is_active:
            if user.has_permission('edit'):
                # ... actual logic
                return True
    return False
```

**After**:
```python
def process_user(user):
    """Process user if they exist, are active, and have edit permission."""
    if user is None:
        return False
    if not user.is_active:
        return False
    if not user.has_permission('edit'):
        return False
    
    # ... actual logic
    return True
```

**Explanation**: Used early returns (guard clauses) to flatten nested conditionals, making the main logic more prominent.

---

### Example 3: Extracting Functions

**Before**:
```javascript
function handleOrder(order) {
    // Validate order
    if (!order.items || order.items.length === 0) throw new Error('No items');
    if (!order.customer) throw new Error('No customer');
    
    // Calculate total
    let total = 0;
    for (const item of order.items) {
        total += item.price * item.quantity;
    }
    
    // Apply discount
    if (order.discountCode === 'SAVE10') total *= 0.9;
    
    return total;
}
```

**After**:
```javascript
function validateOrder(order) {
    if (!order.items || order.items.length === 0) {
        throw new Error('No items');
    }
    if (!order.customer) {
        throw new Error('No customer');
    }
}

function calculateSubtotal(items) {
    return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function applyDiscount(total, discountCode) {
    const discounts = { 'SAVE10': 0.9 };
    return discounts[discountCode] ? total * discounts[discountCode] : total;
}

function handleOrder(order) {
    validateOrder(order);
    const subtotal = calculateSubtotal(order.items);
    return applyDiscount(subtotal, order.discountCode);
}
```

**Explanation**: Extracted validation, calculation, and discount logic into separate functions, making `handleOrder` a clear orchestrator of smaller, testable units.

## Best Practices

- **Preserve Behavior**: Refactoring should never change what the code does—only how it does it.
- **Small, Incremental Changes**: Make one type of change at a time to reduce risk.
- **Test After Each Change**: Run tests (or manually verify) after each refactoring step.
- **Commit Frequently**: If using version control, commit after each successful refactor.
- **Document Trade-offs**: If a refactor sacrifices performance for readability, note it.

## Notes

- This skill focuses on *readability*, not performance optimization (though they often overlap).
- For performance-focused refactoring, consider profiling tools and algorithmic analysis.
- Refactoring is iterative—not every codebase needs to be perfect in one pass.
