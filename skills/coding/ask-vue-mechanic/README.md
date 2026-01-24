# Vue Mechanic

Expert maintenance skill for Vue 3 within Laravel Inertia. Fixes navigation reloads, prop mismatches, and reactivity issues.

## 1. The "Inertia Flow" Protocol
**Trigger:** "Page is reloading full screen", "Props are missing", or "Back button is broken".

### A. The "Silent Reload" Check
* **Symptom:** Clicking a link causes a full browser refresh (white flash) instead of a smooth SPA transition.
* **Diagnosis:** You likely used a standard HTML `<a>` tag.
* **Fix:** Replace with `<Link>`:
    * ❌ `<a href="/users">Users</a>`
    * ✅ `<Link href="/users">Users</Link>`

### B. The "Prop Tunnel" Check
* **Symptom:** "My component didn't get the user data."
* **Action:** Trace the data upstream to the Laravel Controller.
    1.  **Check Vue DevTools:** Inspect the `Inertia` root component properties.
    2.  **Check Controller:** Open the Laravel Controller for this route.
        ```php
        // Is the data actually passed?
        return Inertia::render('Dashboard', [
            'user' => User::all() // <--- Check this line
        ]);
        ```
    3.  **Check Middleware:** If the data is global (like `auth.user`), check `app/Http/Middleware/HandleInertiaRequests.php`.

## 2. The "Ziggy & Forms" Protocol
**Trigger:** "Route not found" or "Form isn't showing errors".

### A. Routing (Ziggy)
* **Symptom:** Console error: `Uncaught Error: 'users.show' is not in the route list.`
* **Fix 1:** Run `php artisan optimize:clear` to refresh the route cache.
* **Fix 2:** Check if the route exists in `routes/web.php` and has a `->name('users.show')`.
* **Fix 3:** If the route requires a parameter, ensure you passed it: `route('users.show', user.id)`.

### B. Form Submission (`useForm`)
* **Symptom:** User clicks submit, loading spinner shows, then stops. No error message, nothing happens.
* **Diagnosis:** Server validation failed (`422 Unprocessable Entity`), but the UI isn't displaying the error message.
* **Fix:** Check the template for the error binding:
    ```html
    <div v-if="form.errors.email" class="text-red-500">{{ form.errors.email }}</div>
    ```

## 3. The "Reactivity Loss" Protocol (Standard Vue)
**Trigger:** "Input isn't typing" or "Value won't update".

1.  **Destructuring:** Did you do `const { name } = props`?
    * **Fix:** Reactivity is lost. Use `props.name` directly in template, or `toRefs(props)` in script.
2.  **Ref vs Value:** In `<script setup>`, did you forget `.value`?
    * **Fix:** `count.value++`, not `count++`.

## 4. Console Noise Filter
When debugging, ignore these benign warnings, but **ATTACK** these errors:

* **IGNORE:** `[Intervention] ... non-passive event listener` (Usually harmless scrolling lib).
* **ATTACK:** `Prop "user" expects a Object, got Array`.
    * *Cause:* Laravel returned `[]` (empty array) for a user, but Vue expected `{}`.
    * *Fix:* Adjust Laravel resource to return `null` or empty object, or adjust Vue prop type.
