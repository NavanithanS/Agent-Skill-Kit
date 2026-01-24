"""Codex adapter - transforms skills for OpenAI Codex CLI."""

from pathlib import Path
from typing import Dict

from agents.base import BaseAdapter
from ask.utils.skill_registry import get_skill_readme


class CodexAdapter(BaseAdapter):
    """Adapter for Codex CLI skill format.
    
    Paths (from OpenAI documentation):
    - Local (project): codex.md in repository root (single file per project)
    - Global (user):   ~/.codex/instructions.md (single file)
    
    Note: Codex uses single instruction files, not folders.
    We append skill content to the instructions file.
    """
    
    def __init__(self, use_global: bool = False, project_root: Path = None):
        if use_global:
            # Global: ~/.codex/instructions.md
            self.target_dir = Path.home() / ".codex"
            self.target_file = "instructions.md"
        else:
            # Local: codex.md in project root
            self.target_dir = project_root or Path.cwd()
            self.target_file = "codex.md"
    
    def get_target_path(self, skill: Dict, name: str = None) -> Path:
        """Get the target path for a skill."""
        # Codex uses a single file, so we create per-skill files in a subdirectory
        skill_name = name or skill.get("name", "unknown")
        return self.target_dir / "instructions" / f"{skill_name}.md"
    
    def transform(self, skill: Dict) -> str:
        """
        Transform a skill into Codex format.
        
        Codex uses simple markdown instruction files.
        """
        name = skill.get("name", "Unknown")
        description = skill.get("description", "")
        readme = get_skill_readme(skill) or ""
        
        content = f"""# {name.replace("-", " ").title()}

{description}

---

{readme}
"""
        return content

    def install_resources(self, skill: Dict, target_dir: Path, dry_run: bool = False) -> Dict[str, bool]:
        """
        Install scripts and sidecar files to the instructions directory.
        """
        import shutil
        
        skill_path_str = skill.get("_path")
        if not skill_path_str:
            return {"conflict": False}
            
        skill_path = Path(skill_path_str)
        # Codex skills go into instructions/filename.md, so we copy resources to instructions/
        # target_dir in install_resources is the PARENT of the skill file
        # For codex, get_target_path returns .../instructions/<skill>.md
        # So target_dir passed here is .../instructions/
        
        dest_dir = target_dir
        
        conflicts = []
        resources_to_copy = ["scripts", "reference", "images", "assets", "examples.md", "reference.md"]
        
        # Check conflicts
        for resource in resources_to_copy:
            src = skill_path / resource
            dst = dest_dir / resource
            if src.exists() and dst.exists():
                 conflicts.append(f"Resource exists: {dst}")

        if conflicts:
            return {"conflict": True, "details": ", ".join(conflicts)}
            
        if dry_run:
            return {"conflict": False}
            
        # Perform Copy
        for resource in resources_to_copy:
            src = skill_path / resource
            dst = dest_dir / resource
            
            if src.exists():
                if src.is_dir():
                    # Check if dir exists before copytree (shutil.copytree dirs_exist_ok=True requires python 3.8+)
                    # safe_copy logic handles this but here we are manual.
                    # Given we checked conflicts, we assume we can write or merge.
                    # For safety in python <3.8 or if conflict logic missed something:
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
                    
        return {"conflict": False}
