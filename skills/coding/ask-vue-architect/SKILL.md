---
name: ask-vue-architect
description: Vue 3 scaffolding for Laravel Inertia, Nuxt, or Vite. Composition API + TypeScript.
triggers: ["create vue component", "scaffold vue page", "vue best practices", "composition api"]
---

<critical_constraints>
❌ NO `<a href="">` → causes full reload, use `<Link>`
❌ NO axios.post for forms → use `useForm` from Inertia
❌ NO hardcoded URLs → use `route()` helper (Ziggy)
✅ MUST use `<script setup lang="ts">`
✅ MUST detect stack flavor before scaffolding
</critical_constraints>

<detection>
Check project for:
- `inertiajs/inertia-laravel` or `resources/js/Pages` → Inertia (priority)
- `nuxt.config.ts` → Nuxt (auto-imports)
- `vite.config.ts` only → Vite SPA (manual imports, vue-router)
</detection>

<inertia_rules>
Props: from Laravel Controller, not fetched in onMounted
```ts
defineProps<{ user: App.Models.User; errors: Record<string, string> }>();
```

Links: `<Link href="/dashboard">` (not `<a>`)

Forms:
```ts
const form = useForm({ email: '', password: '' });
form.post(route('login'), { onFinish: () => form.reset('password') });
```

Errors: `:error="form.errors.email"`

Global state: `usePage().props.auth.user`
</inertia_rules>

<persistent_layouts>
```ts
import AppLayout from '@/Layouts/AppLayout.vue';
defineOptions({ layout: AppLayout });
```
</persistent_layouts>

<state_management>
- Local: `ref()` for UI state
- Global (Inertia): `usePage()` for auth, flash messages
- Complex client-side: Pinia (Setup Store syntax)
</state_management>
