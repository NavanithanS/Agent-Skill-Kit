# Impact Sentinel

A skill focused on impact analysis, breaking change detection, and strategic database design.

## Purpose

The `ask-impact-sentinel` skill guides AI agents to think critically about the consequences of their changes. It ensures that optimizations don't break existing functionality and that database interactions are designed for performance and reliability.

## Usage

Apply this skill when:
- Modifying core functions or shared utilities.
- Refactoring existing logic that has many dependencies.
- Designing or optimizing database schemas and queries.
- Preparing for a release where stability is paramount.

### Step-by-Step Instructions

1. **Identify Dependencies**: Before modifying a function, identify all other functions or components that depend on it.
2. **Check for Breaking Changes**: Assess if the proposed changes will alter the expected behavior, return types, or parameter signatures in a way that breaks dependents.
3. **Strategic Optimization**: Ensure that any "optimizations" are actually improvements and do not introduce regressions or hidden complexities.
4. **Database Guardrails**: Analyze database access patterns. Use indexes, avoid N+1 queries, and ensure transactions are used where appropriate.

## Examples

### Before Impact Analysis
```python
# Modifying a shared utility without checking dependents
def get_user_data(user_id):
    return db.query("SELECT * FROM users WHERE id = ?", user_id)
```

### After Impact Analysis
```python
# Checking dependents and ensuring no breaking changes
def get_user_data(user_id):
    # Verified that 5 other modules use this. 
    # Adding a cache layer instead of changing the return structure.
    data = redis.get(f"user:{user_id}")
    if not data:
        data = db.query("SELECT * FROM users WHERE id = ?", user_id)
        redis.set(f"user:{user_id}", data)
    return data
```

## Best Practices

- **Regression Testing**: Always run existing tests for dependent modules after making changes.
- **Backward Compatibility**: Aim for backward compatibility unless a breaking change is explicitly required.
- **Query Profiling**: Profile new or modified database queries to ensure they perform well under load.
- **Mindful Refactoring**: Don't refactor just for the sake of "cleaner" code if it risks systemic stability.

## Notes

This skill is a "Senior Engineer" mindset tool. It prioritizes stability and long-term maintainability over quick, isolated fixes.
