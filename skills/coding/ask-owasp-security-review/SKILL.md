---
name: ask-owasp-security-review
description: Static security analysis auditing for OWASP Top 10 risks.
version: 1.0.0
permissions:
  - filesystem:read
inputs:
  code: {required: true}
---

# OWASP Security Review Protocol

## <critical_constraints>
1. ❌ **NO** execution/dynamic analysis.
2. ❌ **NO** false positives. Evidence required.
3. ✅ **MUST** map to [OWASP Top 10](https://owasp.org/Top10/).
4. ✅ **MUST** provide `Severity`, `Location`, `Remediation`.
</critical_constraints>

## <process>
1. **Analyze**: Identify language/framework. Trace Source → Sink.
2. **Scan**:
   - Injection/Broken Access.
   - Hardcoded Secrets.
   - Logging Failures.
3. **Report**: Format findings (Markdown Table). If none, "No risks found".
4. **Remediate**: Provide code fixes for Critical/High.
</process>

## <owasp_checklist>
- **A01 Broken Access**: IDOR, traversal.
- **A02 Crypto**: Weak keys/algos.
- **A03 Injection**: SQLi, XSS, Cmd.
- **A04 Design**: No rate limiting.
- **A05 Misconfig**: Default creds.
- **A06 Components**: Old libs.
- **A07 Auth**: Weak pwd.
- **A08 Integrity**: Deserialization.
- **A09 Logging**: Missing/PII.
- **A10 SSRF**: Unvalidated URLs.
</owasp_checklist>

## <output_template>
### Security Audit

| Vuln | OWASP | Sev | Loc | Desc | Fix |
|------|-------|-----|-----|------|-----|
| Name | Cat | High | File:10 | Issue | Fix |

### Summary
[Assessment]
</output_template>
