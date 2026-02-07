---
name: ask-security-sentinel
description: Pre-flight security checker. Scan for secrets and vulnerabilities.
triggers: ["scan for secrets", "sql injection check", "security check", "verify code safety"]
---

<critical_constraints>
✅ MUST run before git commit or deploy
✅ MUST halt and warn if secrets found
✅ MUST enforce parameterized queries
</critical_constraints>

<secret_patterns>
- `sk_live_...` (Stripe)
- `ghp_...` (GitHub)
- `ey...` (JWT tokens)
→ If found: HALT, warn user, move to .env
</secret_patterns>

<vulnerability_checks>
## SQL Injection
❌ Bad: `DB::select("SELECT * FROM users WHERE id = $id")`
✅ Good: `DB::select("...", [$id])`

## XSS
- Check for `{!! $variable !!}` in Blade
- Ensure user explicitly confirmed safe HTML
</vulnerability_checks>
