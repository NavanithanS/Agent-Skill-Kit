---
name: ask-code-reviewer
description: >
  Use this skill when the user asks to review code, check a PR, or analyze a file for bugs and improvements.
  Triggers: "review my code", "check this PR", "analyze for bugs", "code review".
  
  Do NOT use this skill for:
  - Automating the fix (use `ask-python-refactor` or similar).
  - Generation of new features.

  Capabilities:
  - Detailed static analysis for Correctness, Security, Performance, and Style.
  - Prioritized feedback (Critical > Performance > Style).
---

# Code Review Protocol

## <critical_constraints>
1. ❌ **NO** commands. Frame suggestions as questions or considerations ("Consider using...", "X might be safer...").
2. ❌ **NO** unexplained changes. Always explain *why* a change improves the code.
3. ✅ **MUST** prioritize Critical Issues (Bugs/Security) over Style/Nitpicks.
4. ✅ **MUST** use the provided `assets/report_template.md` format.
5. ✅ **MUST** be constructive and empathetic.
</critical_constraints>

## <process>
1. **Context Analysis**:
   - Identify the language and framework.
   - Purpose of the code (Script? API Endpoint? UI Component?).

2. **<thinking> Deep Scan**:
   - Open `assets/checklist.md` and mentally cross-reference.
   - **Correctness**: Look for logical flaws, edge cases (null/empty), race conditions.
   - **Security**: Scan for Injection, XSS, Hardcoded Secrets (OWASP Top 10).
   - **Performance**: valid O(n) vs O(n^2), N+1 queries, memory leaks.
   - **Style/Readability**: Naming conventions, specific language idioms (Pythonic/Idiomatic JS).
   </thinking>

3. **Draft Report**:
   - Group findings by severity (Critical -> Improvements -> Nitpicks).
   - For every finding, provide:
     - **Location** (File:Line).
     - **Problem Description**.
     - **Suggested Fix** (Code Block).

4. **<validation_gate>**:
   - Verify the tone is constructive.
   - Verify all critical issues have a suggested fix.
   - Run `python3 -m scripts.validate` (Placeholder).
   </validation_gate>

5. **Final Output**:
   - Present the Markdown report.
</process>

## <templates>
See `assets/report_template.md` for the required output structure.
</templates>
