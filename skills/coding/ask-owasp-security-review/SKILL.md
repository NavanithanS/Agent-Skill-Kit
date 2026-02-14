---
name: ask-owasp-security-review
description: >
  Use this skill when the user asks to review code for security vulnerabilities,
  audit a file for safety, or check for OWASP Top 10 risks.
  
  Triggers: "security audit", "is this secure", "check for vulnerabilities", "find security bugs".
  
  Do NOT use this skill for:
  - Dynamic Application Security Testing (DAST) or runtime analysis.
  - Generating new secure code from scratch (use a coding architect skill).
  - General code quality or linting (unless security-related).
  
  Capabilities:
  - Static analysis of detailed code snippets.
  - Mapping findings to OWASP Top 10 (2021).
  - Providing remediation code patterns.
---

# OWASP Security Review Protocol

## <critical_constraints>
1. ❌ **NO** code execution. Perform static analysis only.
2. ❌ **NO** false positives. Report only with clear evidence.
3. ✅ **MUST** map every finding to an [OWASP Top 10](https://owasp.org/Top10/) category.
4. ✅ **MUST** provide `Severity`, `Location`, and `Remediation` for every finding.
</critical_constraints>

## <process>
Follow these steps strictly:

1. **Context Analysis**:
   - Identify the language (Python, JS, Java, etc.) and framework.
   - Trace data flow from "Sources" (user input) to "Sinks" (DB, API, IO).

2. **<thinking> Vulnerability Scan**:
   - Mentally check against the **OWASP Checklist** below.
   - Does input bypass validation? (A03: Injection, A01: Broken Access Control)
   - Are secrets hardcoded? (A02: Cryptographic Failures)
   - Is there clear logging? (A09: Logging Failures)
   </thinking>

3. **Report Generation**:
   - If findings exist, format them in the standard Markdown Table in `security_report.md`.
   - If no findings, explicitly state "No immediate security risks found".

4. **<validation_gate>**:
   - Run: `python3 -m scripts.validate` (or reference the installed script path).
   - If exit code != 0, READ the error, FIX the report, and RE-RUN validation.
   </validation_gate>

5. **Remediation**:
   - For each Critical/High finding, provide a corrected code snippet.
   - Reference `assets/examples.md` for style if needed.
</process>

## <owasp_checklist>
- **A01 Broken Access Control**: IDOR, path traversal, missing authz.
- **A02 Cryptographic Failures**: Hardcoded keys, weak crypto (MD5/SHA1).
- **A03 Injection**: SQLi, OS Command Injection, SSTI.
- **A04 Insecure Design**: Missing rate limiting, no brute-force protection.
- **A05 Security Misconfiguration**: Default creds, verbose errors.
- **A06 Vulnerable Components**: Outdated libraries.
- **A07 Auth Failures**: Weak passwords, session fixation.
- **A08 Integrity Failures**: Insecure deserialization.
- **A09 Logging Failures**: Missing logs or PII in logs.
- **A10 SSRF**: Unvalidated URLs.
</owasp_checklist>

## <output_template>
### Security Audit Results

| Vulnerability | OWASP | Severity | Location | Description | Remediation |
|---------------|-------|----------|----------|-------------|-------------|
| [Name] | [Category] | [Critical/High/Med/Low] | [File:Line] | [Brief description] | [Actionable fix] |

### Summary
[Brief risk assessment]
</output_template>

## <examples>
See `assets/examples.md` for detailed case studies.
</examples>
