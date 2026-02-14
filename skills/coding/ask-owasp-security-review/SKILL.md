---
name: ask-owasp-security-review
description: >
  Static security analysis for code, auditing for OWASP Top 10 risks.
  Triggers: "security audit", "is this secure", "check for vulnerabilities".
  
  Capabilities:
  - Static analysis of code snippets.
  - Mapping findings to OWASP Top 10 (2021).
  - Providing remediation code patterns.
---

# OWASP Security Review Protocol

## <critical_constraints>
1. ❌ **NO** code execution or dynamic analysis.
2. ❌ **NO** false positives. Only report with evidence.
3. ✅ **MUST** map findings to [OWASP Top 10](https://owasp.org/Top10/).
4. ✅ **MUST** provide `Severity`, `Location`, and `Remediation`.
</critical_constraints>

## <process>
1. **Context Analysis**: Identify language/framework. Trace data flow (Source → Sink).
2. **<thinking> Vulnerability Scan**:
   - Check input validation (Injection, Broken Access).
   - Check for hardcoded secrets (Cryptographic Failures).
   - Check logging (Logging Failures).
   </thinking>
3. **Report Generation**: Format findings in Markdown Table. If none, state "No immediate risks found".
4. **<validation_gate>**: Run validation script. Ensure no errors.
5. **Remediation**: Provide corrected code for Critical/High issues.
</process>

## <owasp_checklist>
- **A01 Broken Access**: IDOR, path traversal.
- **A02 Crypto Failures**: Weak keys/algos.
- **A03 Injection**: SQLi, XSS, Command Injection.
- **A04 Insecure Design**: No rate limiting.
- **A05 Misconfig**: Default creds, verbose errors.
- **A06 Vulnerable Components**: Old libs.
- **A07 Auth Failures**: Weak passwords.
- **A08 Integrity**: Insecure deserialization.
- **A09 Logging**: Missing/PII logs.
- **A10 SSRF**: Unvalidated URLs.
</owasp_checklist>

## <output_template>
### Security Audit Results

| Vuln | OWASP | Sev | Loc | Desc | Fix |
|------|-------|-----|-----|------|-----|
| Name | Cat | High | File:10 | Issue | Fix |

### Summary
[Risk assessment]
</output_template>

## <examples>
See `assets/examples.md`.
</examples>
