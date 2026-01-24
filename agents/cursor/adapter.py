"""Cursor adapter - transforms skills for Cursor AI."""

from pathlib import Path
from typing import Dict

from agents.base import BaseAdapter
from ask.utils.skill_registry import get_skill_readme


class CursorAdapter(BaseAdapter):
    """Adapter for Cursor AI format.
    
    Paths:
    - Local: .cursor/rules/<skill-name>.md
    - Global: ~/.cursor/rules/<skill-name>.md
    
    Format:
    Cursor uses Markdown files in the .cursor/rules directory.
    """
    
    def __init__(self, use_global: bool = False):
        if use_global:
            self.target_dir = Path.home() / ".cursor" / "rules"
        else:
            self.target_dir = Path.cwd() / ".cursor" / "rules"
    
    def get_target_path(self, skill: Dict, name: str = None) -> Path:
        """Get the target path for a skill."""
        skill_name = name or skill.get("name", "unknown")
        # Cursor rules are typically markdown files
        return self.target_dir / f"{skill_name}.md"
    
    def transform(self, skill: Dict) -> str:
        """Transform a skill into Cursor format."""
        name = skill.get("name", "Unknown")
        description = skill.get("description", "")
        readme = get_skill_readme(skill) or ""
        
        # Cursor reads the markdown file directly.
        # We include the description at the top.
        content = f"""# {name}

{description}

---

{readme}
"""
        # Add references to sidecar files if they exist
        skill_name = name
        if skill.get("_scripts") or skill.get("_reference") or skill.get("_examples"):
             content += f"\n\n> [!NOTE]\n> This skill uses auxiliary resources located in: `.cursor/rules/.scripts/{skill_name}/`"
             
        return content

    def install_resources(self, skill: Dict, target_dir: Path, dry_run: bool = False) -> Dict[str, bool]:
        """
        Install scripts and sidecar files to .cursor/rules/.scripts/<skill-name>/
        """
        import shutil
        
        skill_name = skill.get("name")
        if not skill_name:
            return {"conflict": False}
            
        skill_path_str = skill.get("_path")
        if not skill_path_str:
            return {"conflict": False}
        
        skill_path = Path(skill_path_str)
        
        # Cursor rules are flat files in .cursor/rules/
        # We want to store resources in .cursor/rules/.scripts/<skill-name>/
        # target_dir is .cursor/rules/
        storage_dir = target_dir / ".scripts" / skill_name
        
        conflicts = []
        resources_to_copy = ["scripts", "reference", "images", "assets", "examples.md", "reference.md"]
        
        # Check conflicts
        for resource in resources_to_copy:
            src = skill_path / resource
            dst = storage_dir / resource
            if src.exists() and dst.exists():
                 conflicts.append(f"Resource exists: {dst}")

        if conflicts:
            return {"conflict": True, "details": ", ".join(conflicts)}
            
        if dry_run:
            return {"conflict": False}
            
        # Perform Copy
        for resource in resources_to_copy:
            src = skill_path / resource
            dst = storage_dir / resource
            
            if src.exists():
                # Ensure storage dir exists
                dst.parent.mkdir(parents=True, exist_ok=True)
                
                if src.is_dir():
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
                    
        return {"conflict": False}
