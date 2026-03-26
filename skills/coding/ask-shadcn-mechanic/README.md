---
name: ask-shadcn-mechanic
description: Expert maintenance skill for shadcn/ui. Handles component customization, responsive layout debugging, and Form/Zod wiring while strictly enforcing UI/UX design integrity.
globs: 
  - "components/ui/**/*.tsx"
  - "components/ui/**/*.ts"
  - "tailwind.config.js"
  - "lib/utils.ts"
  - "app/**/*.tsx"
---

# Shadcn/UI Mechanic

## Goal
To properly maintain, debug, and extend existing shadcn/ui components without breaking their accessibility, layout structure, or standard design languages. 

## Detection
Active when:
1. The user asks to debug a responsive layout issue (Tailwind classes).
2. The user wants to modify an existing shadcn component (e.g., adding a variant).
3. Form validation or Zod schema wiring is broken.
4. Dark mode styling or Z-Index overlapping is failing.

## Critical Rules (Must Follow)

1.  **Variant Customization (CVA)**
    * ALWAYS use `class-variance-authority` (cva) within `components/ui/[component].tsx` to add new visual states.
    * Do not inject arbitrary logic or inline styles into the file headers.

2.  **Layout Debugging**
    * Carefully map standard breakpoints (`sm:`, `md:`, `lg:`) before arbitrarily altering padding margins.
    * Use Semantic colors defined in `tailwind.config.js` (`bg-background`, `border-border`) at all times.

3.  **Form & Validation Wiring**
    * Ensure the `<Form>` context is correctly wrapping the components.
    * Zod Resolver bindings must precisely map to the `<FormField>` `name` prop.
    * Use standard `<FormMessage />` for error handling.

4.  **Tailwind Merge (cn)**
    * ALWAYS utilize `cn()` for merging parent `className` props safely without causing collision bugs.

## Example Interaction

**User:** "Add a ghost-warning variant to my button."

**❌ Weak Response:** 
"Okay, just pass `className='bg-transparent text-yellow-500 hover:bg-yellow-100/10'` to the button where you use it."

**✅ Shadcn Mechanic Response:**
"Let's add that to the Button component's variants so it's reusable."
*(Opens components/ui/button.tsx, adds the semantic classes to the `cva` definition, and updates the `ButtonProps` interface)*
