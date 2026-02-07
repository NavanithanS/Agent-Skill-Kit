import pytest
from pathlib import Path
from agents.gemini.adapter import GeminiAdapter
from agents.claude.adapter import ClaudeAdapter
from agents.base import BaseAdapter

class MockAdapter(BaseAdapter):
    """Mock adapter for testing base functionality."""
    def __init__(self, target_dir):
        self.target_dir = target_dir
        
    def get_target_path(self, skill, name=None):
        skill_name = name or skill.get("name")
        return self.target_dir / skill_name / "SKILL.md"
        
    def transform(self, skill):
        return f"Mock content for {skill.get('name')}"

def test_gemini_transform():
    """Test Gemini adapter transformation logic."""
    adapter = GeminiAdapter()
    skill = {
        "name": "test-skill",
        "version": "1.0.0",
        "description": "A test skill",
        # Mocking get_skill_readme return value by patching or ensuring structure?
        # Since transform calls get_skill_readme, we rely on skill dict structure or mocking.
        # But get_skill_readme reads from disk. Let's mock it or just check structure.
    }
    
    # We can't easily mock get_skill_readme without patching, 
    # but we can rely on it returning empty string if file missing.
    content = adapter.transform(skill)
    
    assert "name: test-skill" in content
    assert "version: 1.0.0" in content
    assert "description: A test skill" in content
    assert "---" in content

def test_claude_transform():
    """Test Claude adapter transformation logic."""
    adapter = ClaudeAdapter()
    skill = {
        "name": "test-skill",
        "description": "A test skill",
    }
    content = adapter.transform(skill)
    
    assert "# Test Skill" in content
    assert "A test skill" in content

def test_base_copy_skill(tmp_path):
    """Test safe copy logic in BaseAdapter."""
    target_dir = tmp_path / "target"
    adapter = MockAdapter(target_dir)
    
    skill = {"name": "test-skill"}
    
    # 1. First copy (success)
    result = adapter.copy_skill(skill)
    assert result["status"] == "copied"
    assert (target_dir / "test-skill" / "SKILL.md").exists()
    assert (target_dir / "test-skill" / "SKILL.md").read_text() == "Mock content for test-skill"
    
    # 2. Duplicate copy (conflict)
    result = adapter.copy_skill(skill)
    assert result["status"] == "conflict"
    
    # 3. Force copy (success)
    result = adapter.copy_skill(skill, force=True)
    assert result["status"] == "copied"
    
    # 4. Dry run (no change)
    skill_new = {"name": "new-skill"}
    result = adapter.copy_skill(skill_new, dry_run=True)
    assert result["status"] == "dry-run"
    assert not (target_dir / "new-skill").exists()

def test_install_resources(tmp_path):
    """Test resource installation logic."""
    # Create source skill with resources
    skill_dir = tmp_path / "source_skill"
    skill_dir.mkdir()
    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "helper.py").write_text("print('hello')")
    
    skill = {
        "name": "test-skill",
        "_path": str(skill_dir),
        "_scripts": str(scripts_dir)
    }
    
    # Target directory
    target_dir = tmp_path / "target"
    
    # Use Gemini adapter (which copies resources structure)
    adapter = GeminiAdapter()
    
    # Install resources
    result = adapter.install_resources(skill, target_dir)
    assert result["conflict"] is False
    assert (target_dir / "scripts" / "helper.py").exists()
