# Agent Skill Kit (ASK) - Project Context

## Project Overview
**Agent Skill Kit (ASK)** is a centralized skills repository and CLI toolkit designed to act as a "package manager" for AI agent instructions. It allows developers to define a skill once and deploy it to multiple AI agents, including **Gemini**, **Claude**, **Codex**, **Cursor**, and **Antigravity**.

The core philosophy is "Define Once, Deploy Anywhere," using an adapter pattern to transform universal skill definitions into agent-specific formats and paths.

### Main Technologies
- **Language:** Python 3.9+
- **CLI Framework:** [Click](https://click.palletsprojects.com/)
- **Terminal UI:** [Rich](https://rich.readthedocs.io/)
- **Metadata Parsing:** PyYAML
- **Build System:** Hatchling
- **Token Analysis:** tiktoken

### Architecture
- **CLI Layer (`ask/cli.py`, `ask/commands/`):** Entry point and command orchestration.
- **Registry Layer (`ask/utils/skill_registry.py`, `ask/utils/agent_registry.py`):** Responsible for discovering and parsing skills and agent adapters from the filesystem.
- **Adapter Layer (`agents/*/adapter.py`):** Agent-specific logic for transforming skills and determining installation paths. All adapters inherit from `BaseAdapter` in `agents/base.py`.
- **Skill Library (`skills/`):** Categorized directory of reusable skills (`coding/`, `planning/`, `tooling/`, `workflows/`).

## Building and Running

### Development Setup
```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Key Commands
- **Interactive Wizard:** `ask wizard` (Recommended for most tasks)
- **Deploy Skills:** `ask copy [agent] --skill [name]`
- **Sync All Agents:** `ask sync all`
- **Update Skills:** `ask update`
- **List Skills:** `ask list`
- **Validate Library:** `ask validate`
- **Lint Skills (Tokens):** `ask skill lint`
- **Compile Manifest:** `ask skill compile`
- **Add New Agent:** `ask add-agent`

### Testing
```bash
# Run all tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=ask
```

## Development Conventions

### Skill Structure
Each skill must reside in `skills/<category>/<skill-name>/` and contain:
1.  **`skill.yaml`**: Metadata including `name`, `version`, `agents`, and `depends_on`.
2.  **`SKILL.md`**: Instruction file with YAML frontmatter (`name`, `description`, `triggers`) and Markdown content.
3.  **`scripts/` & `tests/`**: Required directories for the validation gate.

### Skill Naming
- Must be **kebab-case**.
- Length between 2 and 50 characters.
- Must be unique within the library.

### Adding an Agent Adapter
1.  Run `ask add-agent` to scaffold the directory.
2.  Implement the following methods in `agents/<name>/adapter.py`:
    - `get_target_path(skill, name)`: Returns the `Path` where the skill should be installed.
    - `transform(skill)`: Transforms the skill metadata and instructions into the agent's native format.
    - `install_resources(skill, target_dir)`: (Optional) Handles sidecar files like scripts or assets.

### Safe Copy Protocol
The `BaseAdapter` enforces a "Safe Copy" protocol:
- Never overwrite existing skills unless `--force` is used.
- Detect conflicts across all resources before writing any files.
- Provide clear feedback on skipped or overwritten files.

## Persistent Knowledge (Wiki)
- ASK uses the LLM Wiki pattern to maintain long-term project context natively within the project.
- **Automatic Retrieval:** Agents must consult the `wiki/` directory (starting with `wiki/index.md`) to fetch domain context, architectural constraints, and previous learnings.
- **Proactive Documentation:** Whenever there are new learnings, schema changes, or significant decisions made during a session, the agent is expressly instructed to proactively update the `wiki/` files to ensure the knowledge base compounds over time.
