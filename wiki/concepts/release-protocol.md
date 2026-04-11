# Release Protocol

When bumping the version of Agent Skill Kit (ASK) for a new release, it is critical to ensure that all version strings across the project are synchronized. If these are missed, deployment endpoints (like Homebrew) or internal CLI checks will fail or report incorrect versions.

## Version Bump Checklist

Whenever you prepare a new release (e.g. bumping `0.8.0` to `0.8.1`), you **MUST** update the version string exactly in the following files:

1. **`pyproject.toml`**
   - Update `version = "X.Y.Z"` under `[project]`.

2. **`ask/__init__.py`**
   - Update `__version__ = "X.Y.Z"`.

3. **`agent-skill-kit.rb`** (Root Homebrew Tap Formula)
   - Update `url "https://files.pythonhosted.org/packages/source/a/agent-skill-kit/agent_skill_kit-X.Y.Z.tar.gz"`.
   - Update `version "X.Y.Z"`.
   - Update within the test block: `assert_match "X.Y.Z", shell_output("#{bin}/ask --version")`.

4. **`Formula/agent-skill-kit.rb`** (Homebrew Core Formula)
   - Update `url "https://pypi.io/packages/source/a/agent-skill-kit/agent_skill_kit-X.Y.Z.tar.gz"`.

5. **`CHANGELOG.md`**
   - Add a new `## [X.Y.Z] - YYYY-MM-DD` section detailing changes.

6. **`RELEASE_NOTES.md`**
   - Add a new `## vX.Y.Z` section highlighting themes and key updates.

Always use a global workspace search (e.g., `grep_search` for the old version number) to confirm you haven't missed any hardcoded instances!
