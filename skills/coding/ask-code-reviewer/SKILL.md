# AI Code Reviewer

A skill that enables the AI to perform comprehensive code reviews, focusing on logic, style, performance, and security.

## Purpose

To provide actionable, constructive feedback on code changes, ensuring high quality, maintainability, and security before code is merged or finalized. This skill helps developers catch bugs early and improve their coding standards.

## Usage

When asked to review code (e.g., "Review this file", "Check my changes", "Do a code review"), follow this process:

1.  **Understand the Context**:
    *   Identify the language and framework being used.
    *   Look for the specific changes made (if a diff is provided) or the entire file context.
    *   Understand the *intent* of the code (what is it trying to facilitate?).

2.  **Analyze the Code**:
    *   **Correctness**: Does the code do what it's supposed to do? Are there logical errors or edge cases handled?
    *   **Style & Readability**: Does it follow standard conventions (PEP 8, ESLint, Google Style Guides)? Is it readable and well-named?
    *   **Performance**: Are there obvious inefficiencies (O(n^2) loops, redundant calculations, memory leaks)?
    *   **Security**: Are there vulnerabilities (SQL injection, XSS, hardcoded secrets, unsafe inputs)?
    *   **Maintainability**: Is the code DRY (Don't Repeat Yourself)? Is it modular?

3.  **Provide Feedback**:
    *   **Be Constructive**: Frame feedback as suggestions, not commands. Use "Consider..." or "It might be better to..."
    *   **Prioritize**: Highlight critical issues (bugs, security) first. Mention style nitpicks last.
    *   **Explain Why**: Don't just say "change this"; explain *why* the change is beneficial.
    *   **Provide Examples**: Show a code snippet of the suggested improvement.

## Examples

**User Request**: "Review this python function"

```python
def process_data(data):
    l = []
    for i in range(len(data)):
        if data[i] > 5:
            l.append(data[i] * 2)
    return l
```

**AI Response**:

> **Code Review Feedback**
>
> The function logic is correct, but there are opportunities to improve readability and performance (Pythonic style).
>
> 1.  **Variable Naming**: `l` is ambiguous. Consider `results` or `processed_values`.
> 2.  **Iteration**: Python allows iterating directly over elements.
> 3.  **List Comprehension**: This pattern is perfect for a list comprehension.
>
> **Suggested Refactor**:
>
> ```python
> def process_data(data):
>     """Processes data by doubling values greater than 5."""
>     return [x * 2 for x in data if x > 5]
> ```

## Best Practices

*   **Diff-Aware**: If reviewing a diff, focus primarily on the *changed* lines, but check for context (e.g., did a variable change name that breaks usage elsewhere?).
*   **Tone**: maintain a helpful, collaborative tone.
*   **Balance**: Don't overwhelm the user with trivial comments if the logic is fundamentally flawed. Fix the big rocks first.
*   **Completeness**: If the code looks great, say so! "LGTM" (Looks Good To Me) is valuable feedback too.

## Notes

*   This skill complements linters and static analysis tools; it does not replace them.
*   Focus on "human-level" insight—design patterns, intent, and edge cases that tools might miss.
