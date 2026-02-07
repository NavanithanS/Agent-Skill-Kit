---
name: ask-unit-test-generation
description: Generate comprehensive unit tests with edge cases, mocking, and AAA pattern.
triggers: ["generate unit tests", "write tests for", "create test suite", "improve coverage"]
---

<critical_constraints>
❌ NO tests without edge cases
❌ NO generic assertions (assertTrue) → use specific (assertEqual, toEqual)
❌ NO test dependencies → each test must be independent
✅ MUST follow Arrange-Act-Assert (AAA) pattern
✅ MUST mock external dependencies (APIs, DB, filesystem)
✅ MUST use descriptive test names (what + expected outcome)
</critical_constraints>

<detection>
Detect framework from existing tests:
- Python default: pytest
- JS/TS default: Jest
- Java: JUnit
- Ruby: RSpec
- Go: testing package
</detection>

<test_categories>
1. Normal cases: typical usage
2. Edge cases: empty, zero, max, boundary
3. Error cases: invalid input, exceptions
4. Type edges: None/null, wrong types
5. Performance: large inputs (if applicable)
</test_categories>

<templates>
## Python (pytest)
```python
class TestFunctionName:
    def test_normal_case(self):
        assert func(input) == expected
    
    def test_edge_empty(self):
        assert func([]) == []
    
    def test_error_raises(self):
        with pytest.raises(ValueError):
            func(invalid)
```

## JavaScript (Jest)
```javascript
describe('functionName', () => {
  it('should return X when Y', () => {
    expect(func(input)).toBe(expected);
  });
  
  it('should throw on invalid', () => {
    expect(() => func(null)).toThrow(TypeError);
  });
});
```
</templates>

<heuristics>
- Conditional logic → test both branches
- Loop → test 0, 1, many iterations
- Division → test divide by zero
- Strings → test empty, unicode, long
- Collections → test empty, single, many
</heuristics>
