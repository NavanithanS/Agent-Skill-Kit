---
name: ask-component-scaffolder
description: Generate consistent UI component folder structure and files.
triggers: ["create component", "scaffold ui", "generate component", "add react component"]
---

<critical_constraints>
✅ MUST define Props interface
✅ MUST use CSS Modules (prevent global pollution)
✅ MUST include at least one test (renders correctly)
</critical_constraints>

<usage>
```bash
python skills/coding/ask-component-scaffolder/scripts/scaffold_component.py --name "ComponentName"
```
</usage>

<structure>
ComponentName/
├── index.tsx          # Component + Props interface
├── styles.module.css  # CSS Modules
└── Component.test.tsx # Basic render test
</structure>

<guidelines>
- Props: Always define interface
- Styles: CSS Modules only
- Tests: Every component must have ≥1 render test
</guidelines>
