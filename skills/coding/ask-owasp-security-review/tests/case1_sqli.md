# Test Case: Basic SQL Injection Detection

## Input
"Review this code for security issues:"
```python
def login(user, password):
    sql = "SELECT * FROM users WHERE user = '" + user + "' AND password = '" + password + "'"
    return db.execute(sql)
```

## Expected Output
- **Vulnerability**: SQL Injection
- **OWASP Category**: A03: Injection
- **Remediation**: Use parameterized queries
