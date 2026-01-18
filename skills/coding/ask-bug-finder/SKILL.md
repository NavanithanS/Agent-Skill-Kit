---
name: ask-bug-finder
description: Best practices for systematic bug hunting and debugging
---

# Bug Finder

Best practices for systematic bug hunting and debugging.

## Purpose

This skill provides a structured approach to finding and fixing bugs efficiently. It covers debugging strategies, tool usage, and systematic investigation techniques.

## The Bug Hunting Mindset

1. **Reproduce First** — Never fix what you can't reproduce
2. **Question Assumptions** — The bug is often where you least expect it
3. **Isolate the Problem** — Narrow down before diving deep
4. **Read the Error** — Error messages tell you more than you think

## Systematic Debugging Process

### Step 1: Reproduce the Bug

```
Before anything else:
- Can you reproduce it consistently?
- What are the exact steps?
- What's the expected vs actual behavior?
- Does it happen in all environments?
```

### Step 2: Gather Information

- **Error messages**: Read them completely, including stack traces
- **Logs**: Check application, server, and browser logs
- **Recent changes**: What changed since it last worked?
- **Environment**: OS, versions, dependencies, configuration

### Step 3: Form a Hypothesis

Based on the evidence, ask:
- What component is likely responsible?
- What could cause this specific behavior?
- What's the simplest explanation?

### Step 4: Test Your Hypothesis

```python
# Add strategic logging
print(f"DEBUG: value={value}, type={type(value)}")

# Use assertions to verify assumptions
assert user is not None, "User should exist at this point"

# Simplify the code path
# Comment out sections to isolate the issue
```

### Step 5: Fix and Verify

- Make the minimal fix
- Verify the bug is resolved
- Check for regressions
- Add a test to prevent recurrence

## Debugging Techniques

### Binary Search Debugging

When you have a large codebase or long history:

```bash
# Git bisect to find the breaking commit
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Git will help you find the exact commit
```

### Rubber Duck Debugging

Explain the problem out loud:
1. Describe what the code should do
2. Walk through what it actually does
3. Explain each assumption
4. The bug often reveals itself

### Print Debugging (Strategic)

```python
# Good: Informative, shows context
print(f"[DEBUG] process_order: order_id={order.id}, status={order.status}")

# Bad: Useless noise
print("here")
print(x)
```

### Divide and Conquer

1. Find the midpoint of the suspicious code
2. Add a check: Is the data correct here?
3. If yes, bug is after this point
4. If no, bug is before this point
5. Repeat until isolated

## Common Bug Patterns

### Off-by-One Errors
```python
# Bug: Missing last element
for i in range(len(items) - 1):  # Should be range(len(items))
```

### Null/None References
```python
# Bug: Assuming object exists
user.name  # Crashes if user is None

# Fix: Guard clause
if user is None:
    return default_value
```

### Race Conditions
```python
# Bug: Check-then-act pattern
if file_exists(path):
    # File might be deleted here by another process!
    read_file(path)
```

### State Mutation
```python
# Bug: Modifying shared state
def process(items):
    items.sort()  # Modifies original list!
    
# Fix: Work on a copy
def process(items):
    sorted_items = sorted(items)
```

## Debugging Tools

| Tool | Use Case |
|------|----------|
| Debugger (pdb, lldb) | Step through code, inspect state |
| Logger | Track execution flow in production |
| Profiler | Find performance issues |
| Network inspector | Debug API calls |
| Git bisect | Find breaking commit |

## When You're Stuck

1. **Take a break** — Fresh eyes find bugs faster
2. **Explain it to someone** — Rubber duck debugging
3. **Check the obvious** — Is it plugged in? Is the server running?
4. **Search for similar issues** — Someone likely hit this before
5. **Simplify** — Create a minimal reproduction

## Anti-Patterns to Avoid

- ❌ Changing random things hoping it works
- ❌ Fixing symptoms instead of root cause
- ❌ Not reading the full error message
- ❌ Assuming the bug is in someone else's code
- ❌ Not writing a test after fixing

## Notes

- Document your investigation for future reference
- Share findings with the team
- Update runbooks if this is a recurring issue
- Consider adding monitoring to catch similar bugs early
