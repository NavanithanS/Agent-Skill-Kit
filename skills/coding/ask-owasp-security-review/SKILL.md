---
name: ask-owasp-security-review
description: Static security audit aligned with OWASP Top 10, with severity ratings and remediation.
triggers: ["security audit", "owasp vulnerabilities", "security review", "is this secure"]
---

<critical_constraints>
❌ NO code execution → static analysis only
❌ NO false positives → report only with clear evidence
❌ NO findings without remediation
✅ MUST map findings to OWASP category
✅ MUST provide severity + location + fix
✅ MUST confirm with user before suggesting changes
</critical_constraints>

<owasp_checklist>
A01 Broken Access Control: IDOR, path traversal, missing authz, CORS
A02 Cryptographic Failures: MD5/SHA1, hardcoded keys, weak random
A03 Injection: SQL, OS cmd, LDAP, template (SSTI), NoSQL
A04 Insecure Design: no rate limit, no brute-force protection
A05 Security Misconfiguration: default creds, verbose errors, permissive CORS
A06 Vulnerable Components: outdated deps, known CVEs
A07 Auth Failures: weak passwords, session fixation, creds in logs
A08 Integrity Failures: insecure deserialization, unsigned updates
A09 Logging Failures: missing auth logs, PII in logs
A10 SSRF: unvalidated URLs, no allowlists
</owasp_checklist>

<severity_scale>
Critical: RCE, SQLi, auth bypass
High: XSS, IDOR, exposed secrets
Medium: CSRF, weak crypto, improper error handling
Low: best practice deviation, missing headers
Info: observations, recommendations
</severity_scale>

<output_format>
| Vulnerability | OWASP | Severity | Location | Description | Remediation |
|---------------|-------|----------|----------|-------------|-------------|
| SQL Injection | A03 | Critical | auth.py:42 | Input in query | Parameterized queries |
</output_format>

<tools>
Python: bandit, safety
JS: npm audit, Snyk
Java: SpotBugs+FindSecBugs
General: Semgrep, CodeQL
</tools>

<heuristics>
- f-string in SQL → likely injection
- API key in source → hardcoded secret
- @route without @auth → missing authorization
- request.get(user_url) → potential SSRF
</heuristics>
