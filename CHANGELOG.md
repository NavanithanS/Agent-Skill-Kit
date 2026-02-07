# Release Notes v0.1.6

## 🚀 New Features

### Skill Dependencies
- **Recursive Resolution:** `ask copy` now automatically installs dependencies defined in `skill.yaml`'s `depends_on` field.
- **Cycle Detection:** Intelligent circular dependency detection prevents infinite loops.
- **O(N) Performance:** Optimized resolution algorithm using in-memory caching.
- **Preview:** `ask copy` preview now clearly distinguishes between "Direct" (requested) and "Dependency" (auto-included) skills.

### Configuration & UX
- **Config File:** Support for `~/.askconfig.yaml` to set default agents and preferences.
- **Verbose Mode:** Added `--verbose` flag for detailed logging.
- **Search command:** `ask list` now supports `--search` and filtering by category/agent.
- **Validate command:** New `ask validate` command to check skill integrity and dependency correctness.

## 🛡 Security & Quality
- **Safe Copy:** Improved conflict resolution (prompt to rename/skip) prevents accidental overwrites.
- **Input Validation:** Hardened `add-agent` against path traversal.
- **Error Handling:** Graceful handling of file permissions and malformed configs.

## 🐛 Fixes
- Fixed potential path traversal in `add-agent` command.
- Removed duplicate logging in `copy.py`.
- Improved error messages for "no skills found".

## 📦 Internal
- Refactored `skill_registry` for better performance.
- Comprehensive unit tests added for dependency logic.
