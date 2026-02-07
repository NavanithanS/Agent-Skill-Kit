import pytest
from ask.utils.skill_registry import resolve_dependencies, get_skill, get_all_skills

def test_resolve_dependencies_simple(tmp_skills_dir):
    """Test resolving simple dependency chain: A -> B"""
    # Create Child Skill B
    coding = tmp_skills_dir / "coding"
    coding.mkdir()
    
    b_dir = coding / "skill-b"
    b_dir.mkdir()
    (b_dir / "skill.yaml").write_text("name: skill-b\nversion: 1.0.0", encoding="utf-8")
    
    # Create Parent Skill A -> B
    a_dir = coding / "skill-a"
    a_dir.mkdir()
    (a_dir / "skill.yaml").write_text("name: skill-a\nversion: 1.0.0\ndepends_on:\n  - skill-b", encoding="utf-8")
    
    # Refresh cache
    all_skills = get_all_skills()
    skill_map = {s["name"]: s for s in all_skills}
    
    resolved = resolve_dependencies("skill-a", skill_map=skill_map)
    assert len(resolved) == 2
    assert resolved[0]["name"] == "skill-b"  # Dependency comes first
    assert resolved[1]["name"] == "skill-a"

def test_resolve_dependencies_circular(tmp_skills_dir):
    """Test detecting circular dependency: A -> B -> A"""
    coding = tmp_skills_dir / "coding"
    coding.mkdir()
    
    # Skill A -> B
    a_dir = coding / "skill-a"
    a_dir.mkdir()
    (a_dir / "skill.yaml").write_text("name: skill-a\ndepends_on:\n  - skill-b", encoding="utf-8")
    
    # Skill B -> A
    b_dir = coding / "skill-b"
    b_dir.mkdir()
    (b_dir / "skill.yaml").write_text("name: skill-b\ndepends_on:\n  - skill-a", encoding="utf-8")
    
    all_skills = get_all_skills()
    skill_map = {s["name"]: s for s in all_skills}
    
    with pytest.raises(ValueError, match="Circular dependency"):
        resolve_dependencies("skill-a", skill_map=skill_map)

def test_resolve_dependencies_missing(tmp_skills_dir):
    """Test resolving with missing dependency."""
    coding = tmp_skills_dir / "coding"
    coding.mkdir()
    
    a_dir = coding / "skill-a"
    a_dir.mkdir()
    (a_dir / "skill.yaml").write_text("name: skill-a\ndepends_on:\n  - missing-skill", encoding="utf-8")
    
    all_skills = get_all_skills()
    skill_map = {s["name"]: s for s in all_skills}
    
    # Missing dependencies are currently silently ignored by design 
    # (recursive call returns empty list) or could be enhanced to warn.
    # Current implementation: resolve_dependencies("missing") -> []
    
    resolved = resolve_dependencies("skill-a", skill_map=skill_map)
    assert len(resolved) == 1
    assert resolved[0]["name"] == "skill-a"
