from typing import List, Dict
from ask.utils.skill_registry import get_all_skills

def search_skills(query: str) -> List[Dict]:
    """
    Search for skills matching the query string.
    
    Args:
        query: Search term (e.g., "security", "refactor")
        
    Returns:
        List of matching skill dictionaries, ranked by relevance.
    """
    query = query.lower().strip()
    all_skills = get_all_skills()
    results = []
    
    for skill in all_skills:
        name = skill.get("name", "").lower()
        desc = skill.get("description", "").lower()
        triggers = [t.lower() for t in skill.get("triggers", [])]
        
        score = 0
        
        # Exact name match
        if query == name:
            score += 100
        # Partial name match
        elif query in name:
            score += 50
            
        # Trigger match
        if query in triggers:
            score += 30
        for trigger in triggers:
            if query in trigger:
                score += 20
                
        # Description match
        if query in desc:
            score += 10
            
        if score > 0:
            results.append({
                "skill": skill,
                "score": score
            })
            
    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return [r["skill"] for r in results]
