# Unit Test Generation

A skill that automates the creation of comprehensive unit tests for functions or classes, emphasizing coverage of edge cases and assertions.

## Purpose

To generate thorough, production-ready unit tests that ensure code reliability and maintainability. This skill helps developers catch regressions early, document expected behavior, and follow testing best practices for their specific framework.

## When to Use

Trigger this skill when the user:
- Requests tests for new or existing code
- Says "Write tests for this function/class"
- Asks "Generate unit tests for..."
- Wants to improve test coverage

## Usage

When asked to generate unit tests, follow this process:

1.  **Analyze the Code**:
    *   Identify inputs, outputs, and return types.
    *   Understand the function's purpose and expected behavior.
    *   Look for edge cases: empty inputs, null/None values, boundary conditions, large inputs.
    *   Identify potential exceptions or error conditions.
    *   Note any dependencies (external APIs, databases, file systems) that may need mocking.

2.  **Detect the Testing Framework**:
    *   Check the project for existing test files to determine the framework in use.
    *   Default to **pytest** for Python projects.
    *   Default to **Jest** for JavaScript/TypeScript projects.
    *   Use **JUnit** for Java, **RSpec** for Ruby, **Go testing** for Go.
    *   Match the existing project style if tests already exist.

3.  **Generate Comprehensive Tests**:
    *   **Normal Cases**: Cover typical, expected usage scenarios.
    *   **Edge Cases**: Empty collections, zero values, maximum values, boundary conditions.
    *   **Error Cases**: Invalid inputs, exceptions, error handling paths.
    *   **Type Edge Cases**: None/null, wrong types (if dynamically typed).
    *   **Performance Considerations**: Large input tests where applicable.

4.  **Follow Best Practices**:
    *   **Descriptive Names**: Test names should clearly describe what is being tested and expected outcome.
    *   **Arrange-Act-Assert (AAA)**: Structure tests with clear setup, execution, and verification.
    *   **Independence**: Each test should be independent and not rely on other tests.
    *   **Mocking**: Mock external dependencies appropriately.
    *   **Assertions**: Use specific, clear assertions (not just `assertTrue`).

5.  **Output the Tests**:
    *   Place tests in the appropriate test directory (e.g., `tests/`, `__tests__/`, `spec/`).
    *   Follow the project's naming conventions (e.g., `test_*.py`, `*.test.js`).
    *   Include necessary imports and fixtures.

## Examples

### Python Example

**User Request**: "Write tests for this function"

```python
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate the discounted price."""
    if price < 0 or discount_percent < 0:
        raise ValueError("Price and discount must be non-negative")
    if discount_percent > 100:
        raise ValueError("Discount cannot exceed 100%")
    return price * (1 - discount_percent / 100)
```

**AI Response**:

```python
import pytest
from your_module import calculate_discount


class TestCalculateDiscount:
    """Tests for the calculate_discount function."""

    # Normal cases
    def test_calculate_discount_with_valid_values(self):
        """Test discount calculation with typical values."""
        assert calculate_discount(100.0, 20.0) == 80.0

    def test_calculate_discount_with_zero_discount(self):
        """Test that zero discount returns original price."""
        assert calculate_discount(50.0, 0.0) == 50.0

    def test_calculate_discount_with_full_discount(self):
        """Test that 100% discount returns zero."""
        assert calculate_discount(100.0, 100.0) == 0.0

    # Edge cases
    def test_calculate_discount_with_zero_price(self):
        """Test discount on zero price."""
        assert calculate_discount(0.0, 50.0) == 0.0

    def test_calculate_discount_with_small_values(self):
        """Test with very small decimal values."""
        result = calculate_discount(0.01, 10.0)
        assert result == pytest.approx(0.009, rel=1e-3)

    def test_calculate_discount_with_large_price(self):
        """Test with large price values."""
        assert calculate_discount(1_000_000.0, 25.0) == 750_000.0

    # Error cases
    def test_calculate_discount_negative_price_raises_error(self):
        """Test that negative price raises ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            calculate_discount(-10.0, 20.0)

    def test_calculate_discount_negative_discount_raises_error(self):
        """Test that negative discount raises ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            calculate_discount(100.0, -5.0)

    def test_calculate_discount_over_100_percent_raises_error(self):
        """Test that discount over 100% raises ValueError."""
        with pytest.raises(ValueError, match="exceed 100"):
            calculate_discount(100.0, 150.0)
```

### JavaScript Example

**User Request**: "Generate Jest tests for this function"

```javascript
function validateEmail(email) {
  if (typeof email !== 'string') {
    throw new TypeError('Email must be a string');
  }
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}
```

**AI Response**:

```javascript
const { validateEmail } = require('./validators');

describe('validateEmail', () => {
  // Normal cases
  it('should return true for valid email addresses', () => {
    expect(validateEmail('user@example.com')).toBe(true);
    expect(validateEmail('name.surname@domain.org')).toBe(true);
  });

  it('should return false for invalid email addresses', () => {
    expect(validateEmail('invalid-email')).toBe(false);
    expect(validateEmail('missing@domain')).toBe(false);
    expect(validateEmail('@nodomain.com')).toBe(false);
  });

  // Edge cases
  it('should return false for empty string', () => {
    expect(validateEmail('')).toBe(false);
  });

  it('should return false for email with spaces', () => {
    expect(validateEmail('user @example.com')).toBe(false);
  });

  // Error cases
  it('should throw TypeError for non-string input', () => {
    expect(() => validateEmail(null)).toThrow(TypeError);
    expect(() => validateEmail(undefined)).toThrow(TypeError);
    expect(() => validateEmail(123)).toThrow(TypeError);
  });
});
```

## Best Practices

*   **Coverage Focus**: Aim for high branch coverage, not just line coverage. Test all conditional paths.
*   **Meaningful Assertions**: Use specific assertions (`assertEqual`, `toEqual`) over generic ones (`assertTrue`).
*   **Test Names as Documentation**: A test name should describe the scenario and expected outcome.
*   **Fixture Reuse**: Use fixtures/setup methods for common test data to keep tests DRY.
*   **Mock Wisely**: Only mock what's necessary—external services, I/O, time-dependent functions.
*   **Fast Tests**: Unit tests should be fast. Mock slow dependencies.

## Notes

*   This skill generates unit tests, not integration or end-to-end tests.
*   Always verify generated tests compile/run and adjust imports as needed.
*   Consider adding generated tests to CI/CD pipelines for continuous validation.

## Trigger Phrases

Activate this skill when the user says things like:
- "Generate unit tests"
- "Write tests for this function"
- "Create a test suite"
- "Improve test coverage"

