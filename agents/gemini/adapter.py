"""Gemini CLI adapter - transforms skills for Gemini CLI."""

from pathlib import Path
from typing import Dict

from agents.base import BaseAdapter
from ask.utils.skill_registry import get_skill_readme


class GeminiAdapter(BaseAdapter):
    """Adapter for Gemini CLI skill format.
    
    Paths:
    - Local (project): .gemini/skills/<skill-name>/SKILL.md
    - Global (user):   ~/.gemini/skills/<skill-name>/SKILL.md
    """
    
    def __init__(self, use_global: bool = False):
        if use_global:
            self.target_dir = Path.home() / ".gemini" / "skills"
        else:
            self.target_dir = Path.cwd() / ".gemini" / "skills"
    
    def get_target_path(self, skill: Dict, name: str = None) -> Path:
        """Get the target path for a skill."""
        skill_name = name or skill.get("name", "unknown")
        return self.target_dir / skill_name / "SKILL.md"
    
    def transform(self, skill: Dict) -> str:
        """
        Transform a skill into Gemini CLI format.
        
        Gemini CLI uses SKILL.md with YAML frontmatter.
        """
        name = skill.get("name", "Unknown")
        description = skill.get("description", "")
        readme = get_skill_readme(skill) or ""
        
        content = f"""---
name: {name}
description: {description}
---

{readme}
"""
        return content

    def install_resources(self, skill: Dict, target_dir: Path, dry_run: bool = False) -> Dict[str, bool]:
        """
        Install scripts and sidecar files to the skill directory.
        """
        import shutil
        
        skill_path_str = skill.get("_path")
        if not skill_path_str:
            return {"conflict": False}
            
        skill_path = Path(skill_path_str)
        conflicts = []
        resources_to_copy = ["scripts", "reference", "images", "assets", "examples.md", "reference.md"]
        
        # Check conflicts
        for resource in resources_to_copy:
            src = skill_path / resource
            dst = target_dir / resource
            if src.exists() and dst.exists():
                 conflicts.append(f"Resource exists: {dst}")

        if conflicts:
            return {"conflict": True, "details": ", ".join(conflicts)}
            
        if dry_run:
            return {"conflict": False}
            
        # Perform Copy
        for resource in resources_to_copy:
            src = skill_path / resource
            dst = target_dir / resource
            
            if src.exists():
                if src.is_dir():
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
                    
        return {"conflict": False}
