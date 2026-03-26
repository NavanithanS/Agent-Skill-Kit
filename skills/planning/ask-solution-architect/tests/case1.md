# Test Case 1: Vague Request & Diagnostic Halt

## Scenario
The user provides a statement: "I want to build a better database."

## Expected Architect Output
1. The agent conducts an Intent Diagnostic inside a `<process>` block.
2. The agent determines the abstract is unclear and lacks necessary constraints.
3. The agent HALTS execution.
4. The agent asks 3 clarifying questions (e.g., "What is the primary scale/load expectation?", "What specific pain points are you trying to solve?", "What does 'better' mean in your context?").
5. The agent correctly avoids outputting a framework table until constraints are clear.
