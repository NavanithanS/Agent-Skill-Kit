"""Skill registry utilities for discovering and parsing skills."""

from pathlib import Path
from typing import List, Dict, Optional

import yaml

from ask.utils.filesystem import get_skills_dir


def get_all_skills() -> List[Dict]:
    """
    Discover and parse all skills in the skills directory.
    
    Returns a list of skill dictionaries with their metadata.
    """
    skills_dir = get_skills_dir()
    skills = []
    
    if not skills_dir.exists():
        return skills
    
    # Walk through category directories
    for category_dir in skills_dir.iterdir():
        if not category_dir.is_dir() or category_dir.name.startswith("."):
            continue
        
        # Walk through skill directories in each category
        try:
            # Safely iterate
            for skill_dir in category_dir.iterdir():
                try:
                    if not skill_dir.is_dir() or skill_dir.name.startswith("."):
                        continue
                except (PermissionError, OSError):
                    continue
                
                skill_yaml = skill_dir / "skill.yaml"
                if skill_yaml.exists():
                    try:
                        skill = parse_skill(skill_yaml)
                        if skill:
                            skill["_path"] = str(skill_dir)
                            
                            # Detect instruction file (prefer SKILL.md)
                            skill_md = skill_dir / "SKILL.md"
                            readme_md = skill_dir / "README.md"
                            if skill_md.exists():
                                skill["_instruction_file"] = str(skill_md)
                            elif readme_md.exists():
                                skill["_instruction_file"] = str(readme_md)
                                
                            # Detect sidecars
                            ref_md = skill_dir / "reference.md"
                            if ref_md.exists():
                                skill["_reference"] = str(ref_md)
                                
                            ex_md = skill_dir / "examples.md"
                            if ex_md.exists():
                                skill["_examples"] = str(ex_md)
                                
                            # Detect scripts
                            scripts_dir = skill_dir / "scripts"
                            if scripts_dir.exists() and scripts_dir.is_dir():
                                skill["_scripts"] = str(scripts_dir)
                                
                            skills.append(skill)
                    except Exception:
                        # Skip malformed skills
                        pass
        except (PermissionError, OSError):
            continue
    
    return skills


def get_skill(name: str) -> Optional[Dict]:
    """
    Get a specific skill by name.
    
    Searches through all categories to find a skill with the matching name.
    """
    all_skills = get_all_skills()
    
    for skill in all_skills:
        if skill.get("name") == name:
            return skill
    
    return None


def parse_skill(skill_yaml_path: Path) -> Optional[Dict]:
    """
    Parse a skill.yaml file and return its contents.
    """
    try:
        with open(skill_yaml_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return None


def get_skill_readme(skill: Dict) -> Optional[str]:
    """
    Get the README.md content for a skill.
    """
    readme_path = skill.get("_instruction_file")
    if readme_path:
        path = Path(readme_path)
        if path.exists():
            return path.read_text(encoding="utf-8")
    return None
