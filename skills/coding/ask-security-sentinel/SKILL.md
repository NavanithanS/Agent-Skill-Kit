---
name: ask-security-sentinel
description: Pre-flight security checker. Scans for exposed secrets and vulnerable patterns.
---

## 1. Secret Scanning
**Trigger:** Before any `git commit` or `deploy`.
* **Scan:** Look for patterns resembling:
    * `sk_live_...` (Stripe)
    * `ghp_...` (GitHub)
    * `ey...` (JWTs)
* **Action:** If found, HALT immediately and warn the user to move it to `.env`.

## 2. Vulnerability Check
* **SQL Injection:** Check for raw DB queries using variables directly (e.g., `DB::select("SELECT * FROM users WHERE id = $id")`).
    * *Correction:* Enforce bindings: `DB::select("...", [$id])`.
* **XSS:** Check for `{!! $variable !!}` in Blade. Ensure the user *explicitly* confirmed it is safe HTML.
