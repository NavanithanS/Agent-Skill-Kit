# Contributing to Agent Skill Kit (ASK)

Thank you for your interest in improving the Agent Skill Kit! We welcome contributions of all kinds, including new skills, bug fixes, documentation improvements, and new agent adapters.

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/NavanithanS/Agent-Skill-Kit.git
   cd Agent-Skill-Kit
   ```

2. **Set up development environment**
   We recommend using a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Run tests**
   Ensure everything is working correctly:
   ```bash
   pytest tests/
   ```

## 🛠 Adding a New Skill

1. Run the skill creator wizard:
   ```bash
   ask create skill
   ```
2. Follow the prompts to generate the scaffold.
3. Edit the `SKILL.md` with your prompt engineering expertise.
4. Verify it works by copying it to an agent and testing it.

## 🔌 Adding a New Agent Adapter

1. Run the agent scaffold wizard:
   ```bash
   ask add-agent
   ```
2. Implement the `transform` and `get_target_path` methods in the generated adapter file.
3. Add tests in `tests/test_adapters.py`.

## 🧪 Testing Guidelines

- We use `pytest` for testing.
- New features must include unit tests.
- Bug fixes must include a regression test.
- Run `pytest --cov=ask` to check coverage.

## 📝 Code Style

- Follow PEP 8 guidelines.
- Use type hints for function arguments and return values.
- Add docstrings to all public modules, classes, and functions.
- Run `black` and `isort` before committing.

## 📦 Pull Request Process

1. Create a new branch for your feature/fix.
2. Commit your changes with clear messages.
3. Push to your fork and submit a Pull Request.
4. Ensure CI passes.

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.
