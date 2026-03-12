"""Agent registry - Dynamic agent discovery and management."""

from typing import List, Dict

from ask.utils.filesystem import get_project_root


def get_available_agents() -> List[str]:
    """
    Discover available agents by scanning the agents/ directory.
    
    Returns list of agent names (e.g., ['codex', 'gemini', 'claude', 'antigravity'])
    """
    agents_dir = get_project_root() / "agents"
    agents = []
    
    if not agents_dir.exists():
        return agents
    
    for item in agents_dir.iterdir():
        if item.is_dir() and not item.name.startswith(("_", ".")):
            # Check if it has an adapter.py
            if (item / "adapter.py").exists():
                agents.append(item.name)
    
    return sorted(agents)


def get_agent_scopes() -> Dict[str, Dict[str, bool]]:
    """
    Get the supported scopes (local/global) for each agent.
    
    This reads from adapter files to determine capabilities.
    For now, returns defaults - can be enhanced to parse adapters.
    """
    agents = get_available_agents()
    scopes = {}
    
    for agent in agents:
        # Default: both local and global supported
        # Codex is special - global only
        if agent == "codex":
            scopes[agent] = {"local": True, "global": True}
        else:
            scopes[agent] = {"local": True, "global": True}
    
    return scopes
