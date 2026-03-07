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
✅ MUST look for and utilize official `shadcn/skills` for complex component implementation
</critical_constraints>

<detection>
Active when: `components/ui/` exists, `components.json` exists, or user asks for a shadcn component
</detection>

<cli_v4_features>
`shadcn/cli v4` introduces new capabilities that MUST be used when appropriate.

- **Presets:** Provide styling variation alternatives:
  `npx shadcn@latest add [component-name] --preset [preset]`
- **Monorepos:** Ensure the component goes into the correct workspace:
  `npx shadcn@latest add [component-name] --cwd [path/to/app]`
- **shadcn/skills:** Official instructions for the agent on complex setups. Rely on these instead of heuristic generation when possible.
</cli_v4_features>

<cli_first>
Missing component? Don't write from scratch:
`npx shadcn@latest add [component-name]` (use `--cwd` if in a monorepo workspace, e.g., `--cwd apps/web`)
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
