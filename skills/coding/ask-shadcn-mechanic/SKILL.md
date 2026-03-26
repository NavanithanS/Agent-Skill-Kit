---
name: ask-shadcn-mechanic
description: Expert maintenance skill for shadcn/ui. Handles component customization, responsive layout debugging, and Form/Zod wiring while strictly enforcing UI/UX design integrity.
---

---
name: ask-shadcn-mechanic
description: shadcn/ui maintenance, customization, layout debugging, Form/Zod wiring, and design integrity.
triggers: ["fix layout", "add variant", "debug tailwind", "update shadcn", "dark mode bug", "fix form validation", "responsive shadcn issue"]
---

<critical_constraints>
❌ NO arbitrary inline styles (`style={{...}}`) → Always use Tailwind utilities and `cn()`.
❌ NO breaking a11y → Preserve Radix UI accessibility primitives (aria-attributes, focus management) when modifying components.
✅ MUST use `class-variance-authority` (cva) when expanding standard components with new visual variants.
✅ MUST verify responsive breakpoints (`sm:`, `md:`, `lg:`) and target dark mode (`dark:`) when resolving layout/color bugs.
✅ MUST utilize `tailwind-merge` (via `cn()`) gracefully when overriding styles from parent components.
</critical_constraints>

<design_integrity>
shadcn has distinct UI/UX aesthetics (e.g., standard rounded corners, muted backgrounds, clear visual hierarchy). 
- Keep padding and gaps consistent with shadcn's default `p-6`, `p-4`, and `gap-4`.
- Enforce visual hierarchy utilizing `text-muted-foreground` for secondary text and `font-medium` for emphasis.
- Forbid hardcoding exact colors (like `bg-zinc-900`) and mandate CSS variables (`bg-background`, `border-border`, `ring-ring`) so that light/dark mode transitions remain flawless.
- Reference the structures used in the official shadcn blocks library (e.g., Dashboards, Authentication pages) when scaffolding or fixing complete layouts.
</design_integrity>

<variant_expansion>
To add new visual states to a component (e.g., a "ghost-success" button):
1. Locate the `cva()` definition in the component (e.g., `components/ui/button.tsx`).
2. Add the new styles into the `variants` object.
3. Update the corresponding Props interface to allow the new variant.
4. DO NOT tack on conditional classes at the implementation level if a variant is more appropriate.
</variant_expansion>

<layout_mechanics>
- **Flex/Grid Issues:** Navigate standard Tailwind layout issues when composing shadcn Cards, Grids, and Dialogs.
- **Responsive Layouts:** Fix collapsed menus and mobile overlays by checking standard breakpoints.
- **Z-Index Overlaps:** Resolve overlapping elements (e.g., Select dropdowns getting hidden behind sticky headers) by carefully applying `z-40`, `z-50` to the specific Popover/Dropdown wrapper using `className={cn(..., "z-50")}`.
</layout_mechanics>

<form_wiring>
Forms use `react-hook-form` and `zod`.
- Debug the connection between the `zodResolver`, the `<Form>` context, `<FormField>`, `<FormControl>`, and `<FormMessage>`. 
- Ensure `name` bindings in `FormField` perfectly match the Zod schema keys.
</form_wiring>

<component_upgrades>
When shadcn/ui releases an update to a custom-modified component:
1. Re-run `npx shadcn@latest add [component]` in a temp directory or backup the old component.
2. Diff the changes and carefully overwrite.
3. Re-apply any custom `cva` variants to the new file.
</component_upgrades>
