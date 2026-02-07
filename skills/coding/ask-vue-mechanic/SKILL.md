---
name: ask-vue-mechanic
description: Vue 3 + Inertia maintenance. Fixes navigation reloads, prop mismatches, reactivity loss.
triggers: ["fix vue reactivity", "debug inertia reload", "form not submitting", "trace vue data flow"]
---

<critical_constraints>
❌ NO `<a href="">` → use `<Link>` to prevent full page reload
❌ NO destructuring props → loses reactivity, use `toRefs(props)` or `props.name`
❌ NO forgetting `.value` → `count.value++` not `count++`
✅ MUST trace upstream to Laravel Controller for missing props
✅ MUST run `php artisan optimize:clear` after route changes
</critical_constraints>

<silent_reload_fix>
Symptom: Full page refresh (white flash) on link click
Cause: Used `<a>` tag instead of Inertia Link
Fix: `<Link href="/users">` instead of `<a href="/users">`
</silent_reload_fix>

<prop_tunnel_debug>
1. Vue DevTools → inspect Inertia root component props
2. Check Laravel Controller → is data passed in `Inertia::render()`?
3. Check `HandleInertiaRequests` middleware for global data
</prop_tunnel_debug>

<ziggy_routing>
Error: `'users.show' is not in the route list`
Fix 1: `php artisan optimize:clear`
Fix 2: Check route in `routes/web.php` has `->name('users.show')`
Fix 3: Pass params: `route('users.show', user.id)`
</ziggy_routing>

<form_debugging>
Symptom: Submit → spinner → nothing happens (no error shown)
Cause: 422 validation error, but UI not displaying it
Fix: Add error binding `<div v-if="form.errors.email">{{ form.errors.email }}</div>`
</form_debugging>

<reactivity_loss>
- Destructuring: `const { name } = props` → use `props.name` directly
- Ref value: `count++` → `count.value++`
</reactivity_loss>

<console_noise>
IGNORE: `[Intervention] non-passive event listener` (benign)
ATTACK: `Prop "user" expects Object, got Array` → Laravel returned [] not {}
</console_noise>
