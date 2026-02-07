---
name: ask-shadcn-architect
description: Strictly enforces shadcn/ui patterns, imports, and CLI usage when creating or modifying React UI components.
globs: 
  - "components/ui/**/*.tsx"
  - "components/ui/**/*.ts"
  - "tailwind.config.js"
  - "lib/utils.ts"
---

# Shadcn/UI Architect

## Goal
Ensure all UI components strictly adhere to the project's shadcn/ui configuration, preventing custom style bloat and ensuring consistency.

## Detection
Active when:
1. The user asks to create a new UI component.
2. The user asks to style a button, card, dialog, or input.
3. The project contains a `components/ui` directory or a `components.json` file.

## Critical Rules (Must Follow)

1.  **Reuse Before creating**
    * ALWAYS check `@/components/ui` (or the configured alias) first.
    * If a component (e.g., `Button`, `Card`) already exists, import it: `import { Button } from "@/components/ui/button"`.
    * **Do not** create a generic HTML `<button className="...">` if the shadcn `Button` component exists.

2.  **The "CLI-First" Mental Model**
    * If a standard component (like `Accordion`, `Dialog`, `Sheet`) is missing, DO NOT write it from scratch.
    * **Action:** Instruct the user to run: `npx shadcn@latest add [component-name]` OR run it yourself if you have shell access.
    * *Reasoning:* Manual implementation often misses accessibility primitives (Radix UI) and animation constants.

3.  **Style Merging**
    * ALWAYS use the `cn()` utility (usually in `@/lib/utils`) when accepting a `className` prop.
    * ❌ Bad: `className={`bg-red-500 ${className}`}`
    * ✅ Good: `className={cn("bg-red-500", className)}`

4.  **Iconography**
    * Unless specified otherwise, use `lucide-react` for icons, as it is the default standard for shadcn/ui.

5.  **Theming & Variables**
    * Use semantic colors defined in `tailwind.config.js` (e.g., `bg-primary`, `text-muted-foreground`) rather than hardcoded hex or arbitrary Tailwind colors (e.g., `bg-blue-600`).
    * This ensures the component works automatically in Dark Mode.

## Example Interaction

**User:** "Make me a red delete button."

**❌ Weak Response:**
Creates a `<button className="bg-red-500 text-white p-2 rounded">Delete</button>`

**✅ Shadcn Architect Response:**
```tsx
import { Button } from "@/components/ui/button"

export function DeleteButton() {
  return (
    <Button variant="destructive">
      Delete
    </Button>
  )
}
```

*(Note: Uses the existing 'destructive' variant instead of hardcoded red classes)*

## Trigger Phrases

Activate this skill when the user says things like:
- "Add a button using shadcn"
- "Style this component"
- "Create a new UI element"
- "How do I use this shadcn component?"

