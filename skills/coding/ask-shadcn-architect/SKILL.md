---
name: ask-shadcn-architect
description: Enforce shadcn/ui patterns, imports, and CLI-first component usage.
triggers: ["shadcn button", "style component", "new ui element", "shadcn component"]
---

<critical_constraints>
❌ NO custom `<button>` if shadcn Button exists → import from @/components/ui
❌ NO manual implementation of standard components → use CLI
❌ NO hardcoded colors → use semantic (bg-primary, text-muted-foreground)
✅ MUST check @/components/ui first before creating
✅ MUST use cn() utility for className merging
✅ MUST use lucide-react for icons
</critical_constraints>

<detection>
Active when: `components/ui/` exists OR `components.json` exists
</detection>

<cli_first>
Missing component? Don't write from scratch:
`npx shadcn@latest add [component-name]`
</cli_first>

<style_merging>
❌ Bad: `className={\`bg-red-500 ${className}\`}`
✅ Good: `className={cn("bg-red-500", className)}`
</style_merging>

<example>
User: "Make a red delete button"

❌ Weak:
```tsx
<button className="bg-red-500 text-white p-2 rounded">Delete</button>
```

✅ Correct:
```tsx
import { Button } from "@/components/ui/button"
<Button variant="destructive">Delete</Button>
```
</example>

<theming>
Use semantic colors from tailwind.config.js:
- bg-primary, text-muted-foreground
- NOT bg-blue-600, text-gray-500
→ Ensures dark mode compatibility
</theming>
