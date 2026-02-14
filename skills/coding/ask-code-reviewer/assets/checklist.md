# Code Review Checklist

When reviewing code, systematically check these categories:

## 1. Correctness
- Does the code implement the intended logic?
- Are edge cases handled? (Null inputs, empty lists, boundaries)
- Are there logical errors or race conditions?

## 2. Security
- [ ] Injection risks (SQL, Command, etc.)
- [ ] XSS vulnerabilities
- [ ] Hardcoded secrets/credentials
- [ ] Unvalidated inputs
- [ ] Proper authentication/authorization

## 3. Performance
- [ ] Time complexity: Are there O(n²) or worse loops?
- [ ] Memory leaks: Is data managed efficiently?
- [ ] N+1 queries in databases
- [ ] Redundant calculations

## 4. Maintainability
- [ ] DRY (Don't Repeat Yourself) principle
- [ ] SOLID principles adherence
- [ ] Modular and decoupled components
- [ ] Clear variable and function naming

## 5. Style
- Follows language conventions (PEP 8, ESLint, Prettier)
- Consistent formatting
- Readable comments (explaining *why*, not *what*)
