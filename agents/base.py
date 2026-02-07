"""Base adapter class with safe copy logic."""

from pathlib import Path
from typing import Dict
from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    """Base class for all agent adapters with safe copy behavior."""
    
    target_dir: Path = None
    
    @abstractmethod
    def get_target_path(self, skill: Dict, name: str = None) -> Path:
        """Get the target path for a skill."""
        pass

    @abstractmethod
    def transform(self, skill: Dict) -> str:
        """Transform skill into agent-specific format."""
        pass
    
    def list_installed_skills(self) -> Dict[str, str]:
        """
        List all installed skills and their versions.
        
        Returns:
            Dict[skill_name, version_string]
            e.g. {'my-skill': '1.0.1', 'legacy-skill': '0.0.0'}
        """
        installed = {}
        if not self.target_dir or not self.target_dir.exists():
            return installed
            
        # Assuming standard structure: target_dir / skill_name / SKILL.md
        try:
            for item in self.target_dir.iterdir():
                try:
                    if not item.is_dir():
                        continue
                except (PermissionError, OSError):
                    continue
                    
                skill_file = item / "SKILL.md"
                if skill_file.exists():
                    version = self._parse_skill_version(skill_file)
                    installed[item.name] = version
        except (PermissionError, OSError):
            pass
        return installed

    def _parse_skill_version(self, skill_file: Path) -> str:
        """Parse version from SKILL.md frontmatter."""
        try:
            content = skill_file.read_text(encoding="utf-8")
            lines = content.splitlines()
            # Frontmatter must start on the first line
            if not lines or lines[0].strip() != "---":
                return "0.0.0"
                
            for line in lines[1:]:
                stripped = line.strip()
                if stripped == "---":
                    # End of frontmatter
                    break
                if stripped.startswith("version:"):
                    return stripped.split(":", 1)[1].strip()
        except Exception:
            pass
        return "0.0.0"

    def install_resources(self, skill: Dict, target_dir: Path, dry_run: bool = False, force: bool = False) -> Dict[str, bool]:
        """
        Install additional resources (scripts, references, etc.).
        Override in subclasses to handle these.
        
        Args:
            skill: The skill data
            target_dir: Where to install
            dry_run: If True, only check for conflicts
            force: If True, overwrite existing resources
            
        Returns:
            Dict indicating status, e.g., {"conflict": True, "details": "..."}
        """
        return {"conflict": False}

    def install(self, skill: Dict) -> Dict:
        """
        Install a skill (new method to replace copy_skill eventually).
        Defaults to the simple behavior of writing a single file.
        """
        status = self.copy_skill(skill)
        return status

    def copy_skill(self, skill: Dict, dry_run: bool = False, new_name: str = None, force: bool = False) -> Dict:
        """
        Copy a skill to the agent's directory with safe copy behavior.
        
        Safe Copy Rules:
        - NEVER overwrite existing files UNLESS force=True
        - If same name exists: return conflict status (caller prompts for new name)
        - Never delete existing user folders
        - Check ALL resources for conflicts before writing anything
        
        Args:
            skill: Skill dictionary with metadata
            dry_run: If True, don't actually copy
            new_name: Optional new name if renaming due to conflict
            force: If True, overwrite existing main file and resources
        
        Returns:
            status dict with: status, target, would_conflict (for dry-run)
        """
        # Use new_name if provided (for conflict resolution)
        name_to_use = new_name or skill.get("name")
        target = self.get_target_path(skill, name_to_use)
        
        # 1. Check main file conflict
        if target.exists() and not force:
            if dry_run:
                return {
                    "status": "dry-run",
                    "target": str(target),
                    "would_conflict": True,
                    "reason": "Main file exists"
                }
            return {
                "status": "conflict",
                "target": str(target),
                "reason": "Main file exists"
            }
            
        # 2. Check resource conflicts
        # We pass target.parent because resources usually live relative to the command or in a fixed spot
        resource_status = self.install_resources(skill, target.parent, dry_run=True, force=force)
        
        # If force is True, we generally ignore resource conflicts unless they are blocking errors
        if resource_status.get("conflict") and not force:
             if dry_run:
                return {
                    "status": "dry-run",
                    "target": str(target),
                    "would_conflict": True,
                    "reason": f"Resources conflict: {resource_status.get('details')}"
                }
             return {
                "status": "conflict",
                "target": str(target),
                "reason": f"Resources conflict: {resource_status.get('details')}"
            }
        
        if dry_run:
            return {"status": "dry-run", "target": str(target), "would_conflict": False}
        
        # Ensure parent directory exists
        target.parent.mkdir(parents=True, exist_ok=True)
        
        # Transform and write (Core Instruction)
        content = self.transform(skill)
        target.write_text(content, encoding="utf-8")
        
        # Install resources (if any)
        self.install_resources(skill, target.parent, dry_run=False, force=force)
        
        return {"status": "copied", "target": str(target)}

    def remove_skill(self, skill: Dict, name: str = None) -> Dict:
        """
        Remove a skill from the agent's directory.
        
        Args:
            skill: Skill dictionary (must at least contain 'name')
            name: Optional specific name (overrides skill['name'])
            
        Returns:
            status dict with: status ('removed', 'not_found', 'error'), target
        """
        name_to_use = name or skill.get("name")
        target = self.get_target_path(skill, name_to_use)
        
        if not target.exists():
            return {"status": "not_found", "target": str(target)}
            
        try:
            if target.is_dir():
                import shutil
                shutil.rmtree(target)
            else:
                target.unlink()
            return {"status": "removed", "target": str(target)}
        except Exception as e:
            return {"status": "error", "error": str(e), "target": str(target)}
