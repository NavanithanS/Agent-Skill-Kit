---
title: OWASP Security Review — Agent Skill Kit
description: Conduct a thorough static security review of code, identifying vulnerabilities aligned with OWASP Top 10 risks, with severity ratings and remediation…
---

# OWASP Security Review

A skill that performs a thorough static security review of code, identifying vulnerabilities aligned with the OWASP Top 10, with severity ratings and concrete remediation suggestions.

## Purpose

To catch security defects during code review rather than in production. The skill reads source without executing it, maps each finding to an OWASP Top 10 category, assigns a severity, and proposes a specific fix — so a reviewer gets an actionable report instead of a generic warning list.

## When to Use

Trigger this skill when the user:

- Asks for a security review, audit, or vulnerability scan of code
- Says "check this for security issues" or "is this safe?"
- Is preparing a release, a pull request, or a compliance review
- Has written code that handles authentication, user input, file paths, database queries, or secrets

## What It Checks

Findings are mapped to the OWASP Top 10 risk categories, including:

| Risk | Examples the skill looks for |
|---|---|
| Broken access control | Missing authorization checks, insecure direct object references |
| Cryptographic failures | Hardcoded keys, weak hashing, secrets in source |
| Injection | SQL/NoSQL/command injection, unsanitized user input |
| Insecure design | Missing rate limits, unsafe defaults |
| Security misconfiguration | Debug flags in production, permissive CORS |
| Vulnerable components | Known-bad dependency versions |
| Identification & auth failures | Weak session handling, missing MFA paths |
| Software & data integrity | Unsigned updates, unsafe deserialization |
| Logging & monitoring failures | Silent exception handling, unlogged auth events |
| Server-side request forgery | Unvalidated outbound URLs |

## Output

Each finding is reported with:

- **Severity** — critical / high / medium / low
- **Location** — file and line
- **OWASP category** — the mapped Top 10 risk
- **Remediation** — the specific change to make, not a general principle

## Install

```bash
ask copy ask-owasp-security-review --agent claude
```

Supported agents: Claude Code, Codex, Gemini CLI, Cursor, Antigravity.

## Notes

This is a **static** review. It reads code and does not execute it, so it will not find runtime-only issues, and it is not a substitute for dependency scanning, penetration testing, or a human security review of high-risk systems.
