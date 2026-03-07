---
name: ask-ast-mapper
description: Read-only subagent for generating lightweight AST dependency maps and structural overviews of directories.
---

# ask-ast-mapper

A read-only subagent tool designed to cheaply and quickly map the dependencies and Abstract Syntax Tree (AST) structure of a repository without requiring heavy LLM deductive reasoning for every file.

## Purpose

When tackling large repository refactoring or analyzing architecture, the "orchestrator" AI agent often struggles to hold the full repository structure in its context window. Opening and reading every file consumes thousands of tokens and can cause the agent to lose its core instructions.

The `ask-ast-mapper` is a specialized, read-only subagent skill. It is expressly designed to be run by a fast, low-cost model (e.g., Claude Haiku). Its single purpose is to grep through directories, read files, map class definitions, function signatures, and imports, and return a minified `ast_map.json` or concise Markdown equivalent to the parent orchestrator.

<critical_constraints>
❌ STRICTLY NO modifying source code or logic.
❌ STRICTLY NO executing the application code.
✅ MUST explicitly hunt for `import` statements, `class` definitions, and public `function`/`def` signatures.
✅ MUST output the resulting map as a concise JSON or nested markdown structure.
</critical_constraints>

<tools_allowlist>
✅ Read
✅ Grep
✅ Glob
✅ Subprocess (for readonly utilities like tree, grep)
</tools_allowlist>

<tools_denylist>
❌ Write
❌ Edit
❌ git commit/push
❌ Replace
</tools_denylist>

## Usage

This skill enforces the **Principle of Least Privilege**.

1. The orchestrator encounters a need to understand a module's dependencies.
2. The orchestrator triggers or dictates the use of the `ask-ast-mapper` skill to analyze a specific directory.
3. The mapper uses `grep`, `glob`, or CLI AST tools to build the map.
4. The mapper returns *only* the structural map.

## Examples

### After (What ask-ast-mapper provides)
```json
{
  "user_controller.ts": {
    "imports": ["UserService"],
    "methods": ["createUser", "getUser"]
  },
  "user_service.ts": {
    "imports": ["UserRepository"],
    "methods": ["create", "find"]
  }
}
```

## Best Practices

- **Strictly Read-Only**: This skill disables all write, edit, and commit capabilities. Do not attempt to use it to modify code.
- **Limit Scope**: Ask the mapper to map specific directories (e.g., `src/auth`) rather than the entire `src/` folder if the repository is massive.
- **Use as a Subagent**: Deploy this alongside a heavier skill (like `ask-system-architect-prime`) to handle the reconnaissance phase.
