"""Base adapter class with safe copy logic."""

from pathlib import Path
from typing import Dict


class BaseAdapter:
    """Base class for all agent adapters with safe copy behavior."""
    
    target_dir: Path = None
    
    def get_target_path(self, skill: Dict, name: str = None) -> Path:
        """Get the target path for a skill. Override in subclasses."""
        raise NotImplementedError
    
    def transform(self, skill: Dict) -> str:
        """Transform skill to agent format. Override in subclasses."""
        raise NotImplementedError
    
    def copy_skill(self, skill: Dict, dry_run: bool = False, new_name: str = None) -> Dict:
        """
        Copy a skill to the agent's directory with safe copy behavior.
        
        Safe Copy Rules:
        - NEVER overwrite existing files
        - If same name exists: return conflict status (caller prompts for new name)
        - Never delete existing user folders
        
        Args:
            skill: Skill dictionary with metadata
            dry_run: If True, don't actually copy
            new_name: Optional new name if renaming due to conflict
        
        Returns:
            status dict with: status, target, would_conflict (for dry-run)
        """
        # Use new_name if provided (for conflict resolution)
        name_to_use = new_name or skill.get("name")
        target = self.get_target_path(skill, name_to_use)
        
        # Check for conflict
        if target.exists():
            if dry_run:
                return {
                    "status": "dry-run",
                    "target": str(target),
                    "would_conflict": True
                }
            return {
                "status": "conflict",
                "target": str(target)
            }
        
        if dry_run:
            return {"status": "dry-run", "target": str(target), "would_conflict": False}
        
        # Ensure parent directory exists
        target.parent.mkdir(parents=True, exist_ok=True)
        
        # Transform and write
        content = self.transform(skill)
        target.write_text(content)
        
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
