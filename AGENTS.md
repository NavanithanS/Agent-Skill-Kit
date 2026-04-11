# Repository Guidelines

## Project Structure & Module Organization
- `ask/` contains the Python CLI and supporting utilities.
- `agents/` and `skills/` hold the source content that gets deployed to AI editors and agent runtimes.
- `.agents/`, `.claude/`, `.cursor/`, `.gemini/`, and `.agent/` mirror agent-specific output locations.
- `tests/` contains the pytest suite; `assets/`, `docs/`, `wiki/`, and `dist/` store site assets, generated docs, notes, and build artifacts.

## Build, Test, and Development Commands
- `pip install -e .` installs the CLI from source for local development.
- `pip install -e .[dev]` adds test-only dependencies such as `pytest` and `pytest-cov`.
- `ask list` shows available skills and is useful for validating metadata while iterating.
- `ask validate` checks the skill library for missing metadata, dependency issues, and other structural problems.
- `python -m pytest` runs the full test suite from `tests/`.

## Coding Style & Naming Conventions
- Use Python 3.9+ conventions with 4-space indentation and standard library-friendly, readable code.
- Prefer `snake_case` for functions, variables, modules, and test names; use `PascalCase` for classes.
- Keep skill names consistent with the repository pattern: `ask-<topic>-<role>` such as `ask-laravel-architect`.
- Match the existing doc style: short Markdown sections, direct language, and command examples in fenced code blocks.

## Testing Guidelines
- The project uses `pytest`; test files live in `tests/` and follow `test_*.py`.
- Name test functions `test_*` and keep fixtures in `tests/conftest.py` when they are shared.
- Add or update tests whenever CLI behavior, skill discovery, or deployment logic changes.
- Run targeted tests first when possible, then the full suite before opening a PR.

## Commit & Pull Request Guidelines
- Follow the existing conventional style seen in history: `feat:`, `fix:`, `chore:`, with optional scopes like `feat(cli): ...`.
- Keep commit messages imperative and specific to one change.
- PRs should include a short summary, the commands you ran, and screenshots only when a UI or docs site change is visible.
- Link related issues or follow-up tasks when relevant, and mention any behavior changes to deployed agent files.

## Agent-Specific Notes
- Treat `skills/` as the source of truth; update generated agent targets only when the deployment output must change.
- If a change affects docs or packaging, check that the README and generated outputs still match the source skill content.

## LLM Wiki Maintenance
- The repository relies on a compounding, agent-maintained knowledge base located in the `wiki/` directory.
- **Automatic Reference:** Agents should fetch and read `wiki/index.md` and related pages to gain context before executing complex tasks.
- **Proactive Updates:** Agents must proactively update the `wiki/` contents whenever new architectural decisions, structural changes, or significant project insights arise, ensuring the knowledge base remains current.
