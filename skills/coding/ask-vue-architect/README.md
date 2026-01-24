# Vue Architect

Expert scaffolding for Vue 3. Specialized for Laravel Inertia stacks, but supports Nuxt/Vite. Enforces Composition API & TypeScript.

## 1. Environment & Stack Detection
**CRITICAL:** Before creating files, identify the "Flavor" of Vue being used.

* **Flavor A: Laravel Inertia (Priority)**
    * **Check:** `composer.json` has `inertiajs/inertia-laravel` OR `resources/js/Pages` directory exists.
    * **Rule:** You are in a Monolith. Routing is handled by Laravel, but navigation is handled by Inertia.
* **Flavor B: Nuxt**
    * **Check:** `nuxt.config.ts` exists.
    * **Rule:** Use Auto-imports and `pages/` directory.
* **Flavor C: Vite SPA**
    * **Check:** `vite.config.ts` exists but no Inertia/Nuxt.
    * **Rule:** Manual imports required. Use `vue-router`.

## 2. "The Golden Standard" Component Blueprint
When asked to create a component or page:

### Step A: The Script (Logic & Props)
* **Syntax:** ALWAYS use `<script setup lang="ts">`.
* **Props (Inertia Mode):**
    * Do not fetch data in `onMounted`. Expect data to be passed as props from the Laravel Controller.
    * Define props using strict types:
      ```ts
      defineProps<{
          user: App.Models.User; // Use namespace if types are generated
          errors: Record<string, string>;
      }>();
      ```

### Step B: The Template (View & View Navigation)
* **Links:**
    * ❌ **FORBIDDEN:** `<a href="/dashboard">` (Causes full page reload).
    * ✅ **REQUIRED:** `import { Link } from '@inertiajs/vue3';` -> `<Link href="/dashboard">`.
* **Forms (Inertia Mode):**
    * ❌ **Avoid:** Manually creating `ref` for each field and calling `axios.post`.
    * ✅ **REQUIRED:** Use the Inertia form helper:
      ```ts
      import { useForm } from '@inertiajs/vue3';

      const form = useForm({
          email: '',
          password: '',
          remember: false,
      });

      const submit = () => {
          form.post(route('login'), {
              onFinish: () => form.reset('password'),
          });
      };
      ```
    * **Validation:** Bind errors directly: `:error="form.errors.email"`.

### Step C: State Management & Composables
* **Shared State:** Use `usePage()` to access global data (User, Flash Messages, CSRF).
    ```ts
    import { usePage } from '@inertiajs/vue3';
    const user = computed(() => usePage().props.auth.user);
    ```
* **Local State:** Use `ref()` for UI state (modals, dropdowns).
* **Global Store:** Use **Pinia** (Setup Store syntax) only for complex client-side interactions (e.g., shopping cart, media player) that persist across navigation.

## 3. Layouts & Persistence (Inertia Special)
* **Trigger:** User asks for a "Sidebar" or "Audio Player" that doesn't reload.
* **Action:** Use Persistent Layouts.
    ```ts
    // In your Page component
    import AppLayout from '@/Layouts/AppLayout.vue';
    
    defineOptions({
        layout: AppLayout,
    });
    ```

## 4. Ziggy Routing
* **Rule:** If the `ziggy-js` library is detected (standard in Laravel), NEVER hardcode URLs like `axios.post('/api/user')`.
* **Correct:** Use the `route()` helper: `form.post(route('users.store'))`.
