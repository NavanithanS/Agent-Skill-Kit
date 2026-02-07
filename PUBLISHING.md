# Publishing Guide

This guide details how to release `agent-skill-kit` using GitHub Actions.

## Prerequisites

1.  **Secrets**: Ensure these Repository Secrets are set in GitHub:
    - `PYPI_API_TOKEN`: Token for PyPI publishing.
    - `TAP_GITHUB_TOKEN`: A Personal Access Token (Classic) with specific permissions:
        - Scopes: `repo` (to push to the separate `homebrew-Agent-Skill-Kit` repository).
        - **Why?** The default `GITHUB_TOKEN` cannot push to other repositories.

## Release Process

The entire process is automated when you publish a GitHub Release.

1.  **Bump Version**:
    - Update `version` in `pyproject.toml`.
    - Retrieve the changes: `git add pyproject.toml && git commit -m "Bump version to vX.Y.Z" && git push`.

2.  **Create Release**:
    - Go to GitHub -> Releases -> Draft a new release.
    - Tag version: `vX.Y.Z` (must match `pyproject.toml`).
    - Publish Release.

3.  **Automation**:
    The `.github/workflows/release.yml` workflow will trigger:
    - **Step 1**: Build the package.
    - **Step 2**: Publish to PyPI.
    - **Step 3**: Update the Homebrew Formula in the `homebrew-Agent-Skill-Kit` repository.

## Manual Fallback

If CI fails, you can run manually:

1.  **Build**: `python3 -m build`
2.  **PyPI**: `python3 -m twine upload dist/*`
3.  **Homebrew**: `scripts/update_homebrew.py --push`
