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
    
    def __init__(self, use_global: bool = False, project_root: Path = None):
        if use_global:
            self.target_dir = Path.home() / ".gemini" / "skills"
        else:
            from ask.utils.filesystem import get_safe_cwd
            root = project_root or get_safe_cwd()
            self.target_dir = root / ".gemini" / "skills"
    
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
        version = skill.get("version", "0.0.0")
        readme = get_skill_readme(skill) or ""
        
        content = f"""---
name: {name}
version: {version}
description: {description}
---

{readme}
"""
        return content

    def install_resources(self, skill: Dict, target_dir: Path, dry_run: bool = False, force: bool = False) -> Dict[str, bool]:
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
            if src.exists() and dst.exists() and not force:
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
                # If force is True and dst exists, we should probably clean it up first if it's a dir,
                # or just let copy/copytree handle it (shutil.copytree requires empty dst usually)
                if force and dst.exists():
                    if dst.is_dir():
                        shutil.rmtree(dst)
                    else:
                        dst.unlink()

                if src.is_dir():
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
                    
        return {"conflict": False}
