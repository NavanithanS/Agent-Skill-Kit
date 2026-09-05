# Release Protocol

When bumping the version of Agent Skill Kit (ASK) for a new release, it is critical to ensure that all version strings across the project are synchronized. If these are missed, deployment endpoints (like Homebrew) or internal CLI checks will fail or report incorrect versions.

## Version Bump Checklist

Whenever you prepare a new release (e.g. bumping `0.8.0` to `0.8.1`), you **MUST** update the version string exactly in the following files:

1. **`pyproject.toml`**
   - Update `version = "X.Y.Z"` under `[project]`.

2. **`ask/__init__.py`** — *no longer needs a manual bump.*
   - As of v0.10.0 this reads the installed distribution version via
     `importlib.metadata.version("agent-skill-kit")`, so `ask --version` follows
     `pyproject.toml` automatically. Do **not** reintroduce a hardcoded
     `__version__`; that was the drift bug this protocol existed to work around.
   - After bumping, run `pip install -e .` so the local metadata refreshes, then
     confirm with `ask --version`.

2b. **`CITATION.cff`**
   - Update `version: X.Y.Z`.

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

7. **`skills/manifest.json`**
   - Regenerate via `ask skill compile` to pick up any new or changed skills.

8. **`README.md`**
   - The skill table is generated between `<!-- SKILLS:START -->` / `<!-- SKILLS:END -->`.
     Run `python3 scripts/generate_site.py` rather than editing it by hand.

9. **`TWEET.md`**
   - Rewrite for the new release; it still holds the previous version's copy.

10. **Wiki version references**
   - `wiki/overview.md` ("Current version: **vX.Y.Z**") and the `overview.md`
     line in `wiki/index.md` both name the version.

Always use a global workspace search (e.g., `grep_search` for the old version number) to confirm you haven't missed any hardcoded instances. Expect legitimate hits in `CHANGELOG.md`, `RELEASE_NOTES.md`, `wiki/log.md` and any `> **vX.Y.Z** fix:` notes — those are history and must not be rewritten.

## Publishing

Releases are automated: `.github/workflows/release.yml` fires on `release: published`, builds, uploads to PyPI with `secrets.PYPI_API_TOKEN`, then pushes the updated formula to the `NavanithanS/homebrew-Agent-Skill-Kit` tap. So publishing means **tag and create a GitHub Release** — do not run `twine` by hand.

A PyPI version can never be reused, so verify `ask --version`, `python -m build`, and the full test suite *before* creating the release.

## Related

- [Overview](../overview.md) — current version and CLI commands
- [Skill entity](../entities/skill.md) — skill lifecycle includes version bumping
- [Skills catalog](../skills-catalog.md) — verify skill count after adding new skills
