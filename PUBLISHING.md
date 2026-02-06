# Publishing to PyPI

This guide details how to build and publish `agent-skill-kit` (v0.1.3) to PyPI.

## Prerequisites

Ensure you have the build tools installed:
```bash
pip install --upgrade build twine
```

## 1. Build the Package

Run the build command from the project root. This creates the source distribution and wheel in `dist/`.

```bash
python3 -m build
```

**Verification:**
After building, verify that `agents` and `skills` are included in the wheel:
```bash
unzip -l dist/*.whl | grep "skills/"
unzip -l dist/*.whl | grep "agents/"
```
You should see lists of files inside `skills/` and `agents/`.

## 2. Test Publishing (Optional but Recommended)

Upload to TestPyPI first to ensure everything looks right.

```bash
python3 -m twine upload --repository testpypi dist/*
```

## 3. Publish to PyPI

When ready, upload to the real PyPI:

```bash
python3 -m twine upload dist/*
```

## Post-Release
After publishing, users can install the new version with:
```bash
pip install --upgrade agent-skill-kit
ask update --yes
```
