---
name: ask-add-agent
description: Add support for new AI editors to Agent Skill Kit.
triggers: ["add agent support", "create adapter", "register new tool", "extend skill kit"]
---

<critical_constraints>
❌ NO adapters without BaseAdapter inheritance
❌ NO skipping filesystem.py registration
❌ NO skipping copy.py registration
✅ MUST create agents/<name>/adapter.py
✅ MUST update SUPPORTED_AGENTS and AGENT_SCOPES
✅ MUST test with `ask copy <agent> --skill bug-finder`
</critical_constraints>

<workflow>
1. Research: find local path (.agent/) and global path (~/.agent/)
2. Create: agents/<name>/adapter.py inheriting BaseAdapter
3. Register: add loader function in filesystem.py
4. Register: add to SUPPORTED_AGENTS and AGENT_SCOPES in copy.py
5. Document: update README.md supported agents table
6. Test: `ask copy <agent> --skill bug-finder`
</workflow>

<adapter_template>
```python
from pathlib import Path
from typing import Dict
from agents.base import BaseAdapter
from ask.utils.skill_registry import get_skill_readme

class ExampleAdapter(BaseAdapter):
    def __init__(self, use_global: bool = False):
        if use_global:
            self.target_dir = Path.home() / ".example" / "skills"
        else:
            self.target_dir = Path.cwd() / ".example" / "skills"
    
    def get_target_path(self, skill: Dict, name: str = None) -> Path:
        skill_name = name or skill.get("name", "unknown")
        return self.target_dir / skill_name / "SKILL.md"
    
    def transform(self, skill: Dict) -> str:
        return f"---\nname: {skill['name']}\n---\n\n{get_skill_readme(skill)}"
```
</adapter_template>

<filesystem_registration>
```python
def _get_example_adapter(use_global: bool):
    from agents.example.adapter import ExampleAdapter
    return ExampleAdapter(use_global=use_global)
```
</filesystem_registration>
