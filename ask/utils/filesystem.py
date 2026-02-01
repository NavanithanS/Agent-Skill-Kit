"""Filesystem utilities for Agent Skill Kit."""

import os
import shutil
import importlib
from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """Get the Agent Skill Kit project root directory."""
    current = Path(__file__).resolve()
    
    # 1. Dev Mode: Look for pyproject.toml
    for parent in current.parents:
        if (parent / "pyproject.toml").exists():
            return parent
            
    # 2. Package Mode: Fallback to the directory containing the 'ask' package
    # filesystem.py is in locally installed ask/utils/filesystem.py
    # ask package root is current.parent.parent
    # We return the directory CONTAINING ask (e.g. site-packages)
    # so that root / "skills" finds the sibling skills package
    return current.parent.parent.parent


def get_skills_dir() -> Path:
    """Get the skills directory."""
    return get_project_root() / "skills"


def get_agents_dir() -> Path:
    """Get the agents directory."""
    return get_project_root() / "agents"


def safe_create_dir(path: Path) -> None:
    """Create a directory and all parents safely."""
    path.mkdir(parents=True, exist_ok=True)


def safe_copy_file(src: Path, dst: Path, force: bool = False) -> dict:
    """
    Safely copy a file, handling conflicts.
    
    Returns:
        dict with keys: status ('copied', 'skipped', 'renamed'), target
    """
    if dst.exists() and not force:
        return {"status": "skipped", "target": str(dst)}
    
    dst.parent.mkdir(parents=True, exist_ok=True)
    
    shutil.copy2(src, dst)
    return {"status": "copied", "target": str(dst)}


def get_adapter(agent_name: str, use_global: bool = False):
    """
    Dynamic adapter loader for agent-specific transformations.
    
    Uses importlib to dynamically load the adapter module from agents/<agent_name>/adapter.py.
    Expected class name: <AgentName>Adapter (e.g., GeminiAdapter, ClaudeAdapter).
    """
    try:
        # 1. Dynamically import the module
        module_name = f"agents.{agent_name}.adapter"
        module = importlib.import_module(module_name)
        
        # 2. Construct the expected class name
        # e.g. "gemini" -> "GeminiAdapter", "claude_code" -> "ClaudeCodeAdapter"
        class_name = f"{agent_name.replace('-', '_').replace(' ', '').title().replace('_', '')}Adapter"
        
        # 3. Get the class from the module
        adapter_class = getattr(module, class_name)
        
        # 4. Instantiate and return
        return adapter_class(use_global=use_global)
        
    except (ImportError, AttributeError) as e:
        # Fallback or error logging could go here
        # print(f"DEBUG: Failed to load adapter for {agent_name}: {e}")
        return None
