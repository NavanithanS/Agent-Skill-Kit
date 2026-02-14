from typing import Any, List
import asyncio
from mcp.server.fastmcp import FastMCP

from ask.utils.skill_registry import get_all_skills, get_skill, get_skill_readme

# Initialize the FastMCP server
mcp = FastMCP("Agent Skill Kit")

@mcp.tool()
async def list_skills() -> str:
    """
    List all available agent skills.
    
    Returns a formatted string of skill names and descriptions.
    """
    skills = get_all_skills()
    if not skills:
        return "No skills found."
        
    output = ["Available Skills:"]
    for s in skills:
        name = s.get("name", "Unknown")
        desc = s.get("description", "No description").strip().split("\n")[0] # First line only
        output.append(f"- {name}: {desc}")
        
    return "\n".join(output)

@mcp.tool()
async def get_skill(name: str) -> str:
    """
    Retrieve the full protocol and instructions for a specific skill.
    
    Args:
        name: The name of the skill (e.g., 'ask-owasp-security-review')
        
    Returns:
        The content of the SKILL.md file, including frontmatter and instructions.
    """
    skill = get_skill(name)
    if not skill:
        return f"Error: Skill '{name}' not found."
        
    # Prefer SKILL.md content
    readme = get_skill_readme(skill)
    if not readme:
        return "Error: Skill instructions not found."
        
    return readme

@mcp.tool()
async def search_skills(query: str) -> str:
    """
    Search for skills relevant to a specific task or keyword.
    
    Args:
        query: The search query (e.g., "find bugs", "optimize python")
        
    Returns:
        A list of matching skills with descriptions.
    """
    from ask.utils.search import search_skills as find_skills
    results = find_skills(query)
    
    if not results:
        return f"No skills found matching '{query}'."
        
    output = [f"Found {len(results)} skills matching '{query}':"]
    for s in results:
        name = s.get("name")
        desc = s.get("description", "").strip().split("\n")[0]
        output.append(f"- {name}: {desc}")
        
    return "\n".join(output)

if __name__ == "__main__":
    try:
        mcp.run()
    except KeyboardInterrupt:
        pass

