# Next.js Architect

Expert scaffolding for Next.js 14+ (App Router) projects. Enforces the use of Server Components, Server Actions, and strict TypeScript patterns.

## 1. Environment & Stack Detection
**CRITICAL:** Before writing code, identify the project structure.

*   **Flavor A: App Router (Standard)**
    *   **Check:** `app/` directory exists.
    *   **Rule:** Default to **Server Components**. Use "use client" only when interactivity is required.
*   **Flavor B: Pages Router (Legacy)**
    *   **Check:** `pages/` directory exists AND NO `app/` directory.
    *   **Rule:** Use `getServerSideProps` / `getStaticProps`. **Warn the user** that this is legacy and suggest App Router if appropriate.

## 2. "The Golden Standard" Component Blueprint
When asked to create a page or component:

### Step A: The Component Type
*   **Default:** All components are **Server Components** by default.
*   **Interactive:** Add `"use client"` at the very top if and ONLY if you use:
    *   `useState`, `useEffect`
    *   Event events (`onClick`)
    *   Browser APIs (`window`, `localStorage`)

### Step B: Data Fetching (App Router)
*   ❌ **FORBIDDEN:** `useEffect` for initial data fetching.
*   ✅ **REQUIRED:** Async Server Components.
    ```tsx
    // app/dashboard/page.tsx
    export default async function DashboardPage() {
      const data = await db.query('...'); // Direct DB access is allowed in Server Components!
      
      return <ClientComponent data={data} />;
    }
    ```

### Step C: Server Actions (Mutations)
*   ❌ **Avoid:** API Routes (`app/api/...`) for simple form submissions.
*   ✅ **REQUIRED:** Use Server Actions for mutations.
    ```tsx
    // actions.ts
    'use server'
    
    export async function updateUser(formData: FormData) {
      const name = formData.get('name');
      await db.user.update({ where: { name } });
      revalidatePath('/profile');
    }
    ```

## 3. Routing & Navigation
*   **Links:**
    *   ALWAYS use `import Link from 'next/link'`.
    *   Usage: `<Link href="/about">About</Link>`
*   **Navigation:**
    *   **Server Component:** `import { redirect } from 'next/navigation'`
    *   **Client Component:** `import { useRouter } from 'next/navigation'` (NOT `next/router`)

## 4. Metadata & SEO
*   Never manually add `<title>` tags to the `head`.
*   Use the Metadata API in `page.tsx` or `layout.tsx`.
    ```tsx
    import { Metadata } from 'next';
    
    export const metadata: Metadata = {
      title: 'Dashboard',
      description: 'User statistics',
    };
    ```

## 5. UI & Styling
*   If `tailwind.config.ts` is present, use utility classes. 
*   Ideally, suggest **clsx** or **tailwind-merge** for conditional classes.
