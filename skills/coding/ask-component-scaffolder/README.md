---
name: ask-component-scaffolder
description: Standardizes UI component creation by generating a consistent folder structure and files.
---

# Component Scaffolder

Standardizes UI component creation.

## Purpose

To maintain consistency in the frontend codebase by ensuring all new components follow the same structure and typing patterns.

## When to Use

- **Trigger**: "Create a new `Button` component."
- **Trigger**: "Scaffold a `Header`."
- **Trigger**: Any request to create a new UI component (React/Vue/Angular).

## Usage

Use the provided script to generate the component structure.

```bash
python skills/coding/ask-component-scaffolder/scripts/scaffold_component.py --name "ComponentName"
```

## Generated Structure

For a component named `MyComponent`, the following will be created:

```
MyComponent/
├── index.tsx          # Component logic + Prop types
├── styles.module.css  # CSS Modules styles
└── Component.test.tsx # Basic unit test
```

## Guidelines

-   **Props**: Always define a `Props` interface.
-   **Styles**: Use CSS Modules to prevent global namespace pollution.
-   **Tests**: Every component must have at least one test ensuring it renders.
