"""Claude Code adapter - transforms skills for Claude Code."""

from pathlib import Path
from typing import Dict

from agents.base import BaseAdapter
from ask.utils.skill_registry import get_skill_readme


class ClaudeAdapter(BaseAdapter):
    """Adapter for Claude Code command format.
    
    Paths:
    - Local (project): .claude/skills/<skill-name>/SKILL.md
    - Global (user):   ~/.claude/skills/<skill-name>/SKILL.md
    """
    
    def __init__(self, use_global: bool = False, project_root: Path = None):
        if use_global:
            self.target_dir = Path.home() / ".claude" / "skills"
        else:
            from ask.utils.filesystem import get_safe_cwd
            root = project_root or get_safe_cwd()
            self.target_dir = root / ".claude" / "skills"
    
    def get_target_path(self, skill: Dict, name: str = None) -> Path:
        """Get the target path for a skill."""
        skill_name = name or skill.get("name", "unknown")
        return self.target_dir / skill_name / "SKILL.md"
    
    def transform(self, skill: Dict) -> str:
        """
        Transform a skill into Claude Code format.
        
        Claude Code uses SKILL.md files within a dedicated subdirectory.
        """
        name = skill.get("name", "Unknown")
        description = skill.get("description", "")
        readme = get_skill_readme(skill) or ""
        
        # Strip existing frontmatter from readme if present to prevent parsing issues
        if readme.startswith("---"):
            end_idx = readme.find("---", 3)
            if end_idx != -1:
                readme = readme[end_idx+3:].lstrip()
        
        # Build YAML frontmatter
        frontmatter = [
            "---",
            f'name: "{name}"',
            f'description: "{description}"'
        ]
        
        if skill.get("triggers"):
            triggers_str = ", ".join(f'"{t}"' for t in skill["triggers"])
            frontmatter.append(f'triggers: [{triggers_str}]')
            
        frontmatter.append("---\n")
        
        sections = frontmatter + [readme]
        
        # Add references to external files if they exist (now relative to the skill dir)
        if skill.get("_reference"):
            sections.append(f"\n> [!NOTE]\n> For detailed API documentation, see: `reference.md`")
            
        if skill.get("_examples"):
             sections.append(f"\n> [!TIP]\n> For usage examples, see: `examples.md`")
             
        if skill.get("_scripts"):
             sections.append(f"\n> [!IMPORTANT]\n> This skill uses helper scripts located in: `scripts/`")

        return "\n".join(sections) + "\n"

    def install_resources(self, skill: Dict, target_dir: Path, dry_run: bool = False, force: bool = False) -> Dict[str, bool]:
        """
        Install all skills resources (scripts, assets, tests, etc.) to the skill's directory.
        """
        import shutil
        import os
        
        # Ensure name exists
        skill_name = skill.get("name")
        if not skill_name:
            return {"conflict": False}
            
        # With the new skills/ structure, the target_dir (target.parent) 
        # is the skill's own directory (e.g. ~/.claude/skills/my-skill)
        storage_dir = target_dir
        
        source_dir = skill.get("_path")
        if not source_dir:
            return {"conflict": False}
            
        source_path = Path(source_dir)
        if not source_path.exists():
            return {"conflict": False}
            
        # Check for conflicts
        conflicts = []
        if not force:
            for item in source_path.iterdir():
                if item.name.lower() in ["skill.md", "readme.md"]:
                    continue
                
                target_item = storage_dir / item.name
                if target_item.exists():
                    conflicts.append(f"Resource exists: {target_item}")
             
        if conflicts:
            return {"conflict": True, "details": ", ".join(conflicts)}
            
        if dry_run:
            return {"conflict": False}

        # Perform Installation
        storage_dir.mkdir(parents=True, exist_ok=True)
        
        for item in source_path.iterdir():
            if item.name.lower() in ["skill.md", "readme.md"]:
                continue
                
            target_item = storage_dir / item.name
            
            if item.is_dir():
                if target_item.exists():
                    shutil.rmtree(target_item)
                shutil.copytree(item, target_item)
            else:
                shutil.copy2(item, target_item)
            
        return {"conflict": False}
