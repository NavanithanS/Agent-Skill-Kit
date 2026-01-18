# Python Refactor

Best practices and guidelines for Python code refactoring.

## Purpose

This skill provides guidance for refactoring Python code to improve readability, maintainability, and performance while preserving functionality.

## Key Principles

### 1. Extract Functions
Break down large functions into smaller, focused units:
- Each function should do one thing well
- Aim for functions under 20 lines
- Use descriptive names that explain intent

### 2. Rename for Clarity
- Variables: Use descriptive nouns (`user_count` not `n`)
- Functions: Use verbs that describe actions (`calculate_total` not `calc`)
- Classes: Use nouns that describe entities (`OrderProcessor` not `OP`)

### 3. Remove Code Smells
- **Duplicated code**: Extract to shared functions
- **Long parameter lists**: Group into data classes
- **Deep nesting**: Use early returns and guard clauses
- **Magic numbers**: Replace with named constants

### 4. Improve Structure
```python
# Before
def process(d):
    if d['type'] == 'a':
        # 50 lines...
    elif d['type'] == 'b':
        # 50 lines...

# After
def process(data: ProcessData) -> Result:
    handlers = {
        'a': process_type_a,
        'b': process_type_b,
    }
    handler = handlers.get(data.type, process_default)
    return handler(data)
```

### 5. Add Type Hints
```python
# Before
def get_user(id):
    return db.find(id)

# After
def get_user(user_id: int) -> Optional[User]:
    return db.find(user_id)
```

## Refactoring Workflow

1. **Ensure tests exist** before refactoring
2. **Make small changes** and verify each step
3. **Run tests** after every change
4. **Commit frequently** to enable easy rollback
5. **Review the diff** before finalizing

## Common Patterns

### Extract Method
Move code blocks into separate functions.

### Introduce Parameter Object
Group related parameters into a class or dataclass.

### Replace Conditional with Polymorphism
Use inheritance or strategy pattern instead of if/else chains.

### Simplify Boolean Expressions
Use early returns and positive conditions.

## Notes

- Always prioritize readability over cleverness
- Refactor in small, testable increments
- Consider performance implications for hot paths
- Document any non-obvious design decisions
