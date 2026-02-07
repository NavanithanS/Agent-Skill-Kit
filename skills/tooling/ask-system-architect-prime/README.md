# System Architect Prime

A comprehensive repository analysis tool that acts as a Principal Software Architect. It audits codebases for architectural integrity, cyclomatic complexity, security vulnerabilities, and test coverage gaps.

## Purpose

This skill enables AI agents to perform enterprise-grade code audits, generating detailed, actionable reports with code-level refactoring suggestions. It combines static analysis with architectural best practices to identify:

- **Architectural Flaws**: Circular dependencies, leaky abstractions, tight coupling
- **Code Complexity**: Cyclomatic complexity, Halstead metrics, maintainability issues
- **Security Vulnerabilities**: Hardcoded secrets, unsafe regex, injection risks
- **Test Coverage Gaps**: Missing unit tests, fragile happy-path-only coverage

## Usage

### Audit an Entire Repository
```
Audit this repository for architectural flaws.
```

### Investigate Performance Issues
```
Why is the backend module performance degrading?
```

### Check Test Coverage
```
Check the test coverage of the payment gateway.
```

### Generate a Full Report
```
Generate an ARCHITECTURAL_AUDIT.md for this codebase.
```

## Execution Workflow

### Phase 1: Reconnaissance (The Map)
1. Ingest the file structure and identify entry points
2. Identify the core technology stack (Node.js, Python, Rust, etc.)
3. Locate configuration sources (package.json, pyproject.toml, .env.example)
4. Determine the architectural pattern (Monolith, Microservices, Serverless, Clean Architecture)

### Phase 2: Deep Analysis (The Audit)
1. **Complexity Analysis**: Analyze top 10 largest files
   - Threshold: Cyclomatic Complexity > 15 = "Critical Risk"
2. **Security Scan**: Ensure no secrets are exposed in source
3. **Coverage Mapping**: Map source files to test suites
   - Heuristic: If `User.ts` exists but `User.test.ts` does not = "Untested"

### Phase 3: Synthesis (The Report)
Generate `ARCHITECTURAL_AUDIT.md` containing:
- **System Health Score**: Grade from F to A+ based on metrics
- **The Burn List**: Top 3 files requiring immediate refactoring
- **Architecture Diagram**: Mermaid graph showing module relationships
- **Detailed Findings**: Broken down by Architecture, Readability, Performance, Testing

## Analysis Guidelines

### Architecture & Design
- Look for **Circular Dependencies** (Module A imports B, B imports A)
- Identify **Leaky Abstractions** (Database logic in UI components)
- Flag **Tight Coupling** (Hardcoded instantiation instead of DI)

### Readability & Style
- Enforce **Self-Documenting Code** (If a function requires a comment to explain what it does, it's too complex)
- Critique **Naming Conventions** (Variables like `data`, `temp`, `obj` are forbidden)
- Check for **Consistency** (Don't mix async/await with raw Promises in the same module)

### Performance
- Highlight **N+1 Query Problems** in loop structures
- Flag **Blocking I/O** in the main thread (especially for Node.js)
- Identify **Redundant Computations** inside render loops or frequently called utilities

### Test Coverage
- Distinguish between **Unit Tests** (logic) and **Integration Tests** (flow)
- A repo with only **Happy Path tests** is considered "Fragile"

## Output Format

### System Health Score
| Grade | Meaning |
|-------|---------|
| A+ | Exemplary architecture, comprehensive tests, minimal complexity |
| A-B | Good overall, minor improvements needed |
| C | Acceptable but requires attention |
| D-F | Critical issues, immediate refactoring required |

### The Burn List
Top 3 files by priority:
1. File path with complexity score and specific issues
2. File path with identified vulnerabilities
3. File path with missing test coverage

## Safety Protocols

- **Read-Only**: Do not modify code unless explicitly asked to "Apply Fixes"
- **Privacy**: Do not output actual content of secrets found; only flag locations

## Best Practices

### Do
- Use data to back up assertions (e.g., "File X has a complexity score of 25")
- Provide code diffs for critical improvements
- Be concise and actionable
- Prioritize by severity

### Don't
- Make subjective judgments without metrics
- Output sensitive data (secrets, credentials)
- Suggest changes without understanding impact

## Example Report Structure

```markdown
# ARCHITECTURAL_AUDIT.md

## Executive Summary
**System Health Score**: B+
**Stack**: Node.js + TypeScript + PostgreSQL
**Pattern**: Layered Monolith

## The Burn List 🔥
1. `src/services/PaymentService.ts` (CC: 32, CRITICAL)
2. `src/utils/helpers.ts` (CC: 18, HIGH)
3. `src/controllers/UserController.ts` (Untested, MEDIUM)

## Architecture Diagram
(mermaid diagram here)

## Detailed Findings
### Architecture
- ⚠️ Circular dependency: auth ↔ user modules

### Readability
- ❌ Magic numbers in `pricing.ts` line 45

### Performance
- ⚠️ N+1 query pattern in `OrderRepository.ts`

### Testing
- ❌ 0% coverage: payment, notification modules
```

## Notes

This skill pairs well with:
- `ask-python-refactor` for implementing suggested changes
- `ask-unit-test-generation` for addressing test coverage gaps
- `ask-security-sentinel` for deeper security analysis
