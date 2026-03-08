---
name: ask-impact-sentinel
description: Guidelines for impact analysis, breaking change detection, and strategic database design.
---

# Impact Sentinel

A skill focused on impact analysis, breaking change detection, and strategic database design.

<critical_constraints>
- ❌ NEVER introduce breaking changes to shared functions without verifying all dependents.
- ❌ NEVER optimize code at the expense of existing functionality or stability.
- ❌ DO NOT perform database operations without considering performance and indexing.
- ✅ ALWAYS identify dependencies before modifying core logic.
- ✅ ALWAYS ensure optimizations are intelligent and verified.
- ✅ ALWAYS use strategic database access and query design.
</critical_constraints>

<heuristics>
- If modifying a shared function → Run full dependency check first.
- If optimizing → Verify "Before vs After" performance and correctness.
- If accessing database → Check for missing indexes or potential N+1 issues.
- If breaking change is unavoidable → Propose a migration path or versioned API.
</heuristics>

## Purpose

The `ask-impact-sentinel` skill guides AI agents to think critically about the consequences of their changes. It ensures that optimizations don't break existing functionality and that database interactions are designed for performance and reliability.

## Usage

Apply this skill when:
- Modifying core functions or shared utilities.
- Refactoring existing logic that has many dependencies.
- Designing or optimizing database schemas and queries.
- Preparing for a release where stability is paramount.

### Core Protocol

1. **Impact Analysis**: Identify downstream effects of every code change.
2. **Regression Prevention**: Validate that existing features remain functional.
3. **Intelligent Optimization**: Focus on high-impact areas without introducing side effects.
4. **Strategic Data Access**: Prioritize efficient query design and database best practices.

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

- **Comprehensive Verification**: Use automated tests and manual verification for all affected paths.
- **Maintain Stability**: Treat the current stable state as sacred; change it only with full awareness.
- **Database Strategy**: Avoid expensive table scans; leverage existing architecture or propose minimal, high-impact improvements.
