"""Claude Code adapter - transforms skills for Claude Code."""

from pathlib import Path
from typing import Dict

from agents.base import BaseAdapter
from ask.utils.skill_registry import get_skill_readme


class ClaudeAdapter(BaseAdapter):
    """Adapter for Claude Code command format.
    
    Paths:
    - Local (project): .claude/commands/<skill-name>.md
    - Global (user):   ~/.claude/commands/<skill-name>.md
    """
    
    def __init__(self, use_global: bool = False, project_root: Path = None):
        if use_global:
            self.target_dir = Path.home() / ".claude" / "commands"
        else:
            from ask.utils.filesystem import get_safe_cwd
            root = project_root or get_safe_cwd()
            self.target_dir = root / ".claude" / "commands"
    
    def get_target_path(self, skill: Dict, name: str = None) -> Path:
        """Get the target path for a skill."""
        skill_name = name or skill.get("name", "unknown")
        return self.target_dir / f"{skill_name}.md"
    
    def transform(self, skill: Dict) -> str:
        """
        Transform a skill into Claude Code format.
        
        Claude Code uses markdown command files.
        """
        name = skill.get("name", "Unknown")
        description = skill.get("description", "")
        readme = get_skill_readme(skill) or ""
        
        sections = [f"# {name.replace('-', ' ').title()}", "", description, "", "---", "", readme]
        
        # Add references to external files if they exist
        skill_name = name
        
        if skill.get("_reference"):
            sections.append(f"\n> [!NOTE]\n> For detailed API documentation, see: `.scripts/{skill_name}/reference.md`")
            
        if skill.get("_examples"):
             sections.append(f"\n> [!TIP]\n> For usage examples, see: `.scripts/{skill_name}/examples.md`")
             
        if skill.get("_scripts"):
             sections.append(f"\n> [!IMPORTANT]\n> This skill uses helper scripts located in: `.scripts/{skill_name}/scripts/`")

        return "\n".join(sections) + "\n"

    def install_resources(self, skill: Dict, target_dir: Path, dry_run: bool = False, force: bool = False) -> Dict[str, bool]:
        """
        Install scripts and sidecar files to a hidden .scripts directory.
        """
        import shutil
        
        skill_name = skill.get("name")
        if not skill_name:
            return {"conflict": False}
            
        # Define storage location for this skill's resources
        storage_dir = target_dir / ".scripts" / skill_name
        
        scripts_src = skill.get("_scripts")
        ref_src = skill.get("_reference")
        ex_src = skill.get("_examples")
        
        # Check for conflicts
        conflicts = []
        if not force:
            if scripts_src and (storage_dir / "scripts").exists():
                conflicts.append(f"Directory exists: {storage_dir / 'scripts'}")
            if ref_src and (storage_dir / "reference.md").exists():
                conflicts.append(f"File exists: {storage_dir / 'reference.md'}")
            if ex_src and (storage_dir / "examples.md").exists():
                 conflicts.append(f"File exists: {storage_dir / 'examples.md'}")
             
        if conflicts:
            return {"conflict": True, "details": ", ".join(conflicts)}
            
        if dry_run:
            return {"conflict": False}

        # Perform Installation
        if scripts_src:
            dest_scripts = storage_dir / "scripts"
            # Parent dir might not exist yet if this is the first resource
            dest_scripts.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(scripts_src, dest_scripts)
            
        if ref_src:
            dest_ref = storage_dir / "reference.md"
            dest_ref.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ref_src, dest_ref)
            
        if ex_src:
            dest_ex = storage_dir / "examples.md"
            dest_ex.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ex_src, dest_ex)
            
        return {"conflict": False}
