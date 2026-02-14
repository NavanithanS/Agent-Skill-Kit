# OWASP Security Review Examples

## Example 1: SQL Injection Detection

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

## Example 2: Hard-coded Secret

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

## Example 3: Missing Authorization

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
