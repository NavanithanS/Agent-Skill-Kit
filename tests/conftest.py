import pytest
from click.testing import CliRunner

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def tmp_skills_dir(tmp_path, monkeypatch):
    """Create a temporary skills directory structure."""
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    
    # Mock get_skills_dir to return this tmp path
    def mock_get_skills_dir():
        return skills_dir
        
    monkeypatch.setattr("ask.utils.filesystem.get_skills_dir", mock_get_skills_dir)
    # Also patch where it's imported in skill_registry
    monkeypatch.setattr("ask.utils.skill_registry.get_skills_dir", mock_get_skills_dir)
    return skills_dir

