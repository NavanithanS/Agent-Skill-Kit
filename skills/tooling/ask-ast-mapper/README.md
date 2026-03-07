# ask-ast-mapper

A read-only subagent tool designed to cheaply and quickly map the dependencies and Abstract Syntax Tree (AST) structure of a repository without requiring heavy LLM deductive reasoning for every file.

## Purpose

When tackling large repository refactoring or analyzing architecture, the "orchestrator" AI agent often struggles to hold the full repository structure in its context window. Opening and reading every file consumes thousands of tokens and can cause the agent to lose its core instructions.

The `ask-ast-mapper` is a specialized, read-only subagent skill. It is expressly designed to be run by a fast, low-cost model (e.g., Claude Haiku). Its single purpose is to grep through directories, read files, map class definitions, function signatures, and imports, and return a minified `ast_map.json` or concise Markdown equivalent to the parent orchestrator.

## Usage

This skill enforces the **Principle of Least Privilege**.

1. The orchestrator encounters a need to understand a module's dependencies.
2. The orchestrator triggers or dictates the use of the `ask-ast-mapper` skill to analyze a specific directory.
3. The mapper uses `grep`, `glob`, or CLI AST tools to build the map.
4. The mapper returns *only* the structural map.

## Examples

### Before (What an orchestrator struggles with)
Reading `user_controller.ts` (500 lines), `user_service.ts` (300 lines), and `user_repository.ts` (400 lines) entirely into context just to find out `user_controller` calls `user_service.create()`.

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
