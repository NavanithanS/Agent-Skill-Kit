"""Universal adapter - The Universal Source of Truth for skills."""

from pathlib import Path
from typing import Dict, Optional, Any
import shutil

from agents.base import BaseAdapter


class UniversalAdapter(BaseAdapter):
    """Adapter for the Universal format.
    
    Paths:
    - Local: .agents/skills/
    - Global: ~/.agents/skills/
    """
    
    def __init__(self, use_global: bool = False, project_root: Optional[Path] = None):
        if use_global:
            self.target_dir = Path.home() / ".agents" / "skills"
        else:
            from ask.utils.filesystem import get_safe_cwd
            root = project_root or get_safe_cwd()
            self.target_dir = root / ".agents" / "skills"
            
    def get_target_path(self, skill: Dict, name: str = None) -> Path:
        """Get the target path for a skill."""
        skill_name = name or skill.get("name", "unknown")
        # Universal adapter stores skills in folders just like Antigravity
        return self.target_dir / skill_name / "SKILL.md"
        
    def transform(self, skill: Dict) -> str:
        """Transform a skill into Universal format (which is raw SKILL.md content)."""
        content = skill.get("content", "")
        if not content:
            # Fallback to reconstructing if content is missing
            name = skill.get("name", "Unknown")
            description = skill.get("description", "")
            from ask.utils.skill_registry import get_skill_readme
            readme = get_skill_readme(skill) or ""
            
            content = f"---\nname: {name}\ndescription: {description}\n---\n\n{readme}"
            
        return content

    def install_resources(self, skill: Dict, target_dir: Path, dry_run: bool = False, force: bool = False) -> Dict[str, Any]:
        """Install scripts and sidecar files."""
        
        skill_name = skill.get("name")
        if not skill_name:
            return {"conflict": False}
            
        skill_path_str = skill.get("_path")
        if not skill_path_str:
            return {"conflict": False}
            
        skill_path = Path(skill_path_str)
        
        # In universal adapter, resources go alongside SKILL.md
        # target_dir is .agents/skills/<skill-name>
        conflicts = []
        resources_to_copy = ["scripts", "reference", "images", "assets", "examples.md", "reference.md"]
        
        for resource in resources_to_copy:
            src = skill_path / resource
            dst = target_dir / resource
            if src.exists() and dst.exists() and not force:
                conflicts.append(f"Resource exists: {dst}")

        if conflicts:
            return {"conflict": True, "details": ", ".join(conflicts)}
            
        if dry_run:
            return {"conflict": False}
            
        for resource in resources_to_copy:
            src = skill_path / resource
            dst = target_dir / resource
            if src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                if src.is_dir():
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    if dst.exists():
                        if dst.is_dir():
                            shutil.rmtree(dst)
                        else:
                            dst.unlink()
                    shutil.copy2(src, dst)
                    
        return {"conflict": False}
