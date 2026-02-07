---
name: ask-nextjs-architect
description: Next.js 14+ scaffolding. App Router, Server Components, Server Actions, SEO.
triggers: ["nextjs page", "server action", "app router", "nextjs component"]
---

<critical_constraints>
❌ NO `useEffect` for initial data fetch → use async Server Components
❌ NO API routes for simple forms → use Server Actions
❌ NO manual `<title>` tags → use Metadata API
❌ NO `next/router` → use `next/navigation`
✅ MUST detect App vs Pages Router first
✅ MUST default to Server Components
</critical_constraints>

<detection>
- `app/` directory → App Router (default Server Components)
- `pages/` only → Pages Router (legacy, suggest migration)
</detection>

<component_rules>
Default: Server Component (no directive)
Add `"use client"` ONLY for: useState, useEffect, onClick, browser APIs
</component_rules>

<data_fetching>
```tsx
// app/dashboard/page.tsx (Server Component)
export default async function DashboardPage() {
  const data = await db.query('...');  // Direct DB access OK
  return <ClientComponent data={data} />;
}
```
</data_fetching>

<server_actions>
```tsx
// actions.ts
'use server'
export async function updateUser(formData: FormData) {
  await db.user.update({ where: { name: formData.get('name') } });
  revalidatePath('/profile');
}
```
</server_actions>

<navigation>
- Links: `import Link from 'next/link'`
- Server redirect: `import { redirect } from 'next/navigation'`
- Client navigation: `import { useRouter } from 'next/navigation'`
</navigation>

<seo>
```tsx
export const metadata: Metadata = {
  title: 'Dashboard',
  description: 'User statistics',
};
```
</seo>
