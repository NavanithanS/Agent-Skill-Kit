---
name: owasp-security-review
description: Conduct a thorough static security review of code, identifying vulnerabilities aligned with OWASP Top 10 risks, with severity ratings and remediation suggestions.
---

# OWASP Security Review

A skill for conducting comprehensive static security audits of code, identifying vulnerabilities aligned with OWASP Top 10 risks.

## Purpose

To perform evidence-based static security analysis of code, detecting potential vulnerabilities, misconfigurations, and security anti-patterns. Findings are classified by severity and mapped to OWASP categories with actionable remediation guidance.

## When to Use

- The user requests a security review, audit, or vulnerability check for code
- Changes involve authentication, data handling, external inputs, dependencies, or configurations
- During code reviews or PR assessments where security implications may exist
- When security concerns are raised about existing code
- Before deploying code to production environments

## How to Proceed

Perform a **static analysis only**—do not execute code. Follow this structured process:

### 1. Context Analysis

Review the provided code snippet, file, or diff and identify:
- Programming language and version
- Frameworks and libraries in use
- Key components (input handling, authentication, data storage, API endpoints)
- Trust boundaries and data flow patterns
- External dependencies and integrations

### 2. Vulnerability Checklist

Systematically scan for issues based on relevant OWASP Top 10 (2021) categories:

#### A01: Broken Access Control
- Missing authorization checks on sensitive operations
- Insecure Direct Object References (IDOR)
- Overly permissive role assignments
- Path traversal vulnerabilities
- CORS misconfigurations

#### A02: Cryptographic Failures
- Weak algorithms (MD5, SHA-1, DES, RC4)
- Hard-coded encryption keys or secrets
- Improper random number generation
- Missing encryption for sensitive data
- Weak key lengths

#### A03: Injection
- SQL injection (concatenated queries, no prepared statements)
- OS command injection
- LDAP injection
- XPath injection
- Template injection (SSTI)
- NoSQL injection
- Header injection

#### A04: Insecure Design
- Missing rate limiting
- Lack of input validation at business logic level
- Insufficient protection against brute force

#### A05: Security Misconfiguration
- Default credentials in code
- Verbose error messages exposing internals
- Unnecessary features enabled
- Permissive CORS policies
- Missing security headers

#### A06: Vulnerable and Outdated Components
- Outdated libraries with known CVEs
- Lack of dependency pinning
- Use of deprecated APIs

#### A07: Identification and Authentication Failures
- Weak password policies
- Missing multi-factor authentication hooks
- Session fixation vulnerabilities
- Improper session management
- Credential exposure in logs

#### A08: Software and Data Integrity Failures
- Insecure deserialization
- Unsigned updates or data
- Missing integrity checks on critical data

#### A09: Security Logging and Monitoring Failures
- Missing logging for authentication events
- Sensitive data in logs
- Insufficient audit trails for critical operations

#### A10: Server-Side Request Forgery (SSRF)
- Unvalidated URL inputs
- Missing allowlists for external requests

#### Additional Common Issues
- Hard-coded secrets (API keys, passwords, tokens)
- Insecure file handling (arbitrary file read/write)
- Excessive data exposure in API responses
- Missing input sanitization
- Race conditions in security-critical code

### 3. Severity Rating

Classify each finding using this scale:

| Severity | Description | Examples |
|----------|-------------|----------|
| **Critical** | Immediate exploitation risk with severe impact | RCE, SQL injection, authentication bypass |
| **High** | Direct exploitation possible | XSS, IDOR, exposed secrets |
| **Medium** | Risk under certain conditions or requires chaining | CSRF, improper error handling, weak crypto |
| **Low** | Best practice deviation, minimal direct risk | Verbose errors, missing headers, weak validation |
| **Info** | Observations and recommendations | Code quality, documentation gaps |

### 4. Optional Tool Integration

If available in the environment, suggest or invoke automated scanning tools:

- **Python**: Bandit (`bandit -r .`), Safety (`safety check`)
- **JavaScript/Node.js**: npm audit, Snyk, ESLint security plugins
- **Java**: SpotBugs with FindSecBugs, OWASP Dependency-Check
- **General**: Semgrep, CodeQL

### 5. Output Format

Present findings in a structured markdown table:

| Vulnerability | OWASP Category | Severity | Location (File:Line) | Description | Remediation |
|---------------|----------------|----------|----------------------|-------------|-------------|
| SQL Injection | A03: Injection | Critical | auth.py:42 | User input concatenated directly into query | Use parameterized queries with `cursor.execute(query, params)` |
| Hard-coded API Key | A02: Cryptographic Failures | High | config.js:15 | API key exposed in source code | Move to environment variables or secrets manager |
| Missing Auth Check | A01: Broken Access Control | High | routes.py:88 | Endpoint lacks authorization verification | Add `@requires_auth` decorator |

**If no issues are found**, explicitly state this and highlight positive security practices observed.

### 6. Summary and Next Steps

Provide:
- **Overall Risk Assessment**: High/Medium/Low based on aggregate findings
- **Priority Recommendations**: Top 3-5 actions to address immediately
- **Further Actions**: Suggest dynamic testing, penetration testing, or external security audits if warranted
- **Seek Confirmation**: Before suggesting code changes, confirm with the user

## Examples

### Example 1: SQL Injection Detection

**Code**:
```python
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)
```

**Finding**:
| Vulnerability | OWASP Category | Severity | Location | Description | Remediation |
|---------------|----------------|----------|----------|-------------|-------------|
| SQL Injection | A03: Injection | Critical | app.py:12 | User input directly interpolated into SQL query | Use parameterized query: `db.execute("SELECT * FROM users WHERE username = ?", (username,))` |

---

### Example 2: Hard-coded Secret

**Code**:
```javascript
const API_KEY = "sk_live_abc123xyz789";
const client = new Stripe(API_KEY);
```

**Finding**:
| Vulnerability | OWASP Category | Severity | Location | Description | Remediation |
|---------------|----------------|----------|----------|-------------|-------------|
| Hard-coded Secret | A02: Cryptographic Failures | High | payment.js:3 | Production API key exposed in source | Use `process.env.STRIPE_API_KEY` and configure via environment |

---

### Example 3: Missing Authorization

**Code**:
```python
@app.route('/admin/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    return jsonify({"status": "deleted"})
```

**Finding**:
| Vulnerability | OWASP Category | Severity | Location | Description | Remediation |
|---------------|----------------|----------|----------|-------------|-------------|
| Missing Authorization | A01: Broken Access Control | Critical | admin.py:45 | Admin endpoint lacks authentication and role verification | Add `@login_required` and `@admin_required` decorators |

## Best Practices

- **Prioritize Precision**: Only report findings with clear evidence in the code
- **Avoid False Positives**: When uncertain, note the potential issue but clarify assumptions
- **Context Matters**: Consider the application's threat model and deployment context
- **Be Constructive**: Focus on actionable remediation, not criticism
- **Stay Current**: Reference the latest OWASP guidelines and CVE databases

## References

- [OWASP Top 10 (2021)](https://owasp.org/Top10/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
- [NIST Secure Coding Guidelines](https://www.nist.gov/itl/ssd/software-quality-group/secure-software-development-project)

## Notes

- This skill performs **static analysis only**—runtime behavior cannot be assessed
- For comprehensive security, combine with dynamic testing (DAST) and penetration testing
- Consider the sensitivity of the codebase; some findings may require confidential handling
- Framework-specific security patterns may apply (e.g., Django ORM, Spring Security)

## Trigger Phrases

Activate this skill when the user says things like:
- "Perform a security audit"
- "Check for OWASP vulnerabilities"
- "Scan this code for security flaws"
- "Is this code secure?"

