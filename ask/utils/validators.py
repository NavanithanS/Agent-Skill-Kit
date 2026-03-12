"""Validation utilities for Agent Skill Kit."""

import re


def validate_skill_name(name: str) -> bool:
    """
    Validate a skill name.
    
    Rules:
    - Lowercase letters, numbers, and hyphens only
    - Must start with a letter
    - Must be between 2 and 50 characters
    """
    if not name:
        return False
    
    if len(name) < 2 or len(name) > 50:
        return False
    
    pattern = r'^[a-z][a-z0-9-]*$'
    return bool(re.match(pattern, name))


def validate_category(category: str) -> bool:
    """Validate a skill category."""
    valid_categories = ["coding", "planning", "tooling"]
    return category in valid_categories


def validate_version(version: str) -> bool:
    """Validate a semantic version string."""
    pattern = r'^\d+\.\d+\.\d+$'
    return bool(re.match(pattern, version))
