# Add Agent

How to add support for new AI code editors to Agent Skill Kit.

## Quick Start (CLI)

Use the `ask add-agent` command to automatically scaffold a new agent:

```bash
# Interactive mode
ask add-agent cursor

# With explicit paths
ask add-agent windsurf --local-path .windsurf/rules --global-path ~/.windsurf/rules
```

This will:
1. Create the adapter file at `agents/<name>/adapter.py`
2. Register it in `filesystem.py`
3. Add it to `copy.py`

## Manual Process

### What to Look For

- **Local path**: Project-specific location (usually `.agent-name/`)
- **Global path**: User-wide location (usually `~/.agent-name/`)
- **File format**: Markdown, YAML frontmatter, JSON, etc.
- **File structure**: Single file vs folder with SKILL.md

## Step 2: Create the Adapter

Create a new file at `agents/<agent-name>/adapter.py`:

```python
"""<Agent> adapter - transforms skills for <Agent>."""

from pathlib import Path
from typing import Dict

from agents.base import BaseAdapter
from ask.utils.skill_registry import get_skill_readme


class <Agent>Adapter(BaseAdapter):
    """Adapter for <Agent> format.
    
    Paths:
    - Local: .<agent>/skills/<skill-name>/SKILL.md
    - Global: ~/.<agent>/skills/<skill-name>/SKILL.md
    """
    
    def __init__(self, use_global: bool = False):
        if use_global:
            self.target_dir = Path.home() / ".<agent>" / "skills"
        else:
            self.target_dir = Path.cwd() / ".<agent>" / "skills"
    
    def get_target_path(self, skill: Dict, name: str = None) -> Path:
        """Get the target path for a skill."""
        skill_name = name or skill.get("name", "unknown")
        # Adjust based on agent's format:
        # For folder-based: return self.target_dir / skill_name / "SKILL.md"
        # For file-based:   return self.target_dir / f"{skill_name}.md"
        return self.target_dir / skill_name / "SKILL.md"
    
    def transform(self, skill: Dict) -> str:
        """Transform skill to agent's format."""
        name = skill.get("name", "Unknown")
        description = skill.get("description", "")
        readme = get_skill_readme(skill) or ""
        
        # Adjust format based on agent requirements:
        # - YAML frontmatter for Gemini/Antigravity style
        # - Plain markdown for Codex/Claude style
        
        content = f"""---
name: {name}
description: {description}
---

{readme}
"""
        return content
```

## Step 3: Register in filesystem.py

Add the adapter loader function in `ask/utils/filesystem.py`:

```python
def _get_<agent>_adapter(use_global: bool):
    from agents.<agent>.adapter import <Agent>Adapter
    return <Agent>Adapter(use_global=use_global)
```

And add to the `adapters` dictionary in `get_adapter()`:

```python
adapters = {
    "codex": _get_codex_adapter,
    "gemini": _get_gemini_adapter,
    "claude": _get_claude_adapter,
    "antigravity": _get_antigravity_adapter,
    "<agent>": _get_<agent>_adapter,  # Add this line
}
```

## Step 4: Register in copy.py

Update `ask/commands/copy.py`:

### Add to SUPPORTED_AGENTS

```python
SUPPORTED_AGENTS = ["codex", "gemini", "claude", "antigravity", "<agent>"]
```

### Add to AGENT_SCOPES

```python
AGENT_SCOPES = {
    "codex": {"local": False, "global": True},
    "gemini": {"local": True, "global": True},
    "claude": {"local": True, "global": True},
    "antigravity": {"local": True, "global": True},
    "<agent>": {"local": True, "global": True},  # Add this line
}
```

## Step 5: Update Documentation

Update `README.md` to include the new agent in the Supported Agents table.

## Step 6: Test

```bash
# Verify the agent appears in copy command
ask copy <agent> --skill bug-finder

# The preview should show correct paths
# Choose local or global and verify the file is created
```

## Example: Adding Cursor

### 1. Research
Cursor uses `.cursorrules` file for project rules and `~/.cursor/rules/` for global.

### 2. Create Adapter

```python
# agents/cursor/adapter.py
class CursorAdapter(BaseAdapter):
    def __init__(self, use_global: bool = False):
        if use_global:
            self.target_dir = Path.home() / ".cursor" / "rules"
        else:
            self.target_dir = Path.cwd() / ".cursor" / "rules"
    
    def get_target_path(self, skill: Dict, name: str = None) -> Path:
        skill_name = name or skill.get("name", "unknown")
        return self.target_dir / f"{skill_name}.md"
```

### 3. Register & Test

Follow steps 3-6 above.

## Notes

- Always inherit from `BaseAdapter` to get safe copy behavior
- The `transform()` method handles format conversion
- Each agent may have unique requirements—check their docs
- Consider whether the agent uses single files or skill folders
