import yaml
from ask.utils.skill_registry import get_all_skills, get_skill, parse_skill, get_skill_readme

def test_get_all_skills_empty(tmp_skills_dir):
    """Test get_all_skills returns empty list when no skills exist."""
    skills = get_all_skills()
    assert skills == []

def test_get_all_skills_discovery(tmp_skills_dir):
    """Test discovering skills across categories."""
    # Setup category structure
    coding = tmp_skills_dir / "coding"
    coding.mkdir()
    
    # Create valid skill
    skill_dir = coding / "test-skill"
    skill_dir.mkdir()
    (skill_dir / "skill.yaml").write_text("name: test-skill\nversion: 1.0.0", encoding="utf-8")
    (skill_dir / "SKILL.md").write_text("Instruction content", encoding="utf-8")
    
    # Create invalid skill (no metadata)
    bad_dir = coding / "bad-skill"
    bad_dir.mkdir()
    
    skills = get_all_skills()
    assert len(skills) == 1
    assert skills[0]["name"] == "test-skill"
    assert skills[0]["_path"] == str(skill_dir)

def test_get_skill(tmp_skills_dir):
    """Test retrieving a specific skill by name."""
    coding = tmp_skills_dir / "coding"
    coding.mkdir()
    
    skill_dir = coding / "my-skill"
    skill_dir.mkdir()
    (skill_dir / "skill.yaml").write_text("name: my-skill\nversion: 2.0.0", encoding="utf-8")
    
    skill = get_skill("my-skill")
    assert skill is not None
    assert skill["name"] == "my-skill"
    assert skill["version"] == "2.0.0"
    
    missing = get_skill("non-existent")
    assert missing is None

def test_parse_skill(tmp_path):
    """Test parsing skill.yaml files."""
    valid_yaml = tmp_path / "valid.yaml"
    valid_yaml.write_text("name: test\nlist: [a, b]", encoding="utf-8")
    
    data = parse_skill(valid_yaml)
    assert data["name"] == "test"
    assert data["list"] == ["a", "b"]
    
    invalid_yaml = tmp_path / "invalid.yaml"
    invalid_yaml.write_text("name: test\n  indent: error", encoding="utf-8")
    
    data = parse_skill(invalid_yaml)
    assert data is None

def test_get_skill_readme(tmp_skills_dir):
    """Test retrieving SKILL.md or README.md content."""
    coding = tmp_skills_dir / "coding"
    coding.mkdir()
    
    # Case 1: SKILL.md preference
    s1 = coding / "s1"
    s1.mkdir()
    (s1 / "skill.yaml").write_text("name: s1", encoding="utf-8")
    (s1 / "SKILL.md").write_text("# S1 Instructions", encoding="utf-8")
    (s1 / "README.md").write_text("# Ignore this", encoding="utf-8")
    
    # Case 2: README.md fallback
    s2 = coding / "s2"
    s2.mkdir()
    (s2 / "skill.yaml").write_text("name: s2", encoding="utf-8")
    (s2 / "README.md").write_text("# S2 Instructions", encoding="utf-8")
    
    # Re-scan to populate internal paths
    get_all_skills()
    
    skill1 = get_skill("s1")
    content1 = get_skill_readme(skill1)
    assert content1 == "# S1 Instructions"
    
    skill2 = get_skill("s2")
    content2 = get_skill_readme(skill2)
    assert content2 == "# S2 Instructions"
