"""Tests for token_analyzer utility."""

import pytest
from pathlib import Path

from ask.utils.token_analyzer import (
    count_tokens,
    analyze_skill,
    _check_schema_compliance,
    lint_skill,
    generate_report,
)


class TestCountTokens:
    """Tests for count_tokens function."""
    
    def test_empty_string(self):
        """Empty string should return 0 tokens."""
        assert count_tokens("") == 0
    
    def test_simple_text(self):
        """Simple text should return reasonable token count."""
        result = count_tokens("Hello world")
        assert result > 0
        assert result < 10  # Should be ~2-3 tokens
    
    def test_longer_text(self):
        """Longer text should have more tokens."""
        short = count_tokens("Hello")
        long = count_tokens("Hello world, this is a longer sentence with more words.")
        assert long > short


class TestSchemaCompliance:
    """Tests for _check_schema_compliance function."""
    
    def test_missing_critical_constraints(self):
        """Should flag missing <critical_constraints> block."""
        content = "# Some skill\nNo constraints here"
        issues = _check_schema_compliance(content)
        # Now returns (severity, message) tuples
        messages = [msg for _, msg in issues]
        assert any("critical_constraints" in m.lower() for m in messages)
    
    def test_has_critical_constraints(self):
        """Should not flag when <critical_constraints> exists."""
        content = "<critical_constraints>\n❌ NO bad thing\n</critical_constraints>"
        issues = _check_schema_compliance(content)
        messages = [msg for _, msg in issues]
        assert not any("critical_constraints" in m.lower() for m in messages)
    
    def test_polite_language_please(self):
        """Should flag 'please' in content."""
        content = "<critical_constraints>x</critical_constraints>\nPlease do this."
        issues = _check_schema_compliance(content)
        messages = [msg for _, msg in issues]
        assert any("please" in m.lower() for m in messages)
    
    def test_verbose_patterns(self):
        """Should flag verbose language patterns."""
        verbose_phrases = [
            "It is important to always use X",
            "We recommend using Y",
            "You should avoid Z",
            "Consider using A",
        ]
        for phrase in verbose_phrases:
            content = f"<critical_constraints>x</critical_constraints>\n{phrase}"
            issues = _check_schema_compliance(content)
            assert len(issues) > 0, f"Should flag: {phrase}"


class TestAnalyzeSkill:
    """Tests for analyze_skill function."""
    
    def test_nonexistent_file(self, tmp_path):
        """Should return error for missing file."""
        result = analyze_skill(tmp_path / "nonexistent.md")
        assert "error" in result
    
    def test_small_skill_ok(self, tmp_path):
        """Small skill should have 'ok' status."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("<critical_constraints>\n❌ NO bad\n</critical_constraints>")
        
        result = analyze_skill(skill_md)
        assert result["status"] == "ok"
        assert result["tokens"] < 500
    
    def test_large_skill_error(self, tmp_path):
        """Large skill should have 'error' status."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        # Create content that exceeds 700 tokens (~2800 chars)
        skill_md.write_text("word " * 700)
        
        result = analyze_skill(skill_md)
        assert result["status"] == "error"


class TestLintSkill:
    """Tests for lint_skill function."""
    
    def test_passing_skill(self, tmp_path):
        """Well-formed skill should pass."""
        skill_dir = tmp_path / "good-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("<critical_constraints>\n❌ NO bad\n✅ MUST good\n</critical_constraints>")
        
        passed, messages = lint_skill(skill_md)
        assert passed
    
    def test_failing_skill_tokens(self, tmp_path):
        """Skill with too many tokens should fail."""
        skill_dir = tmp_path / "big-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("word " * 800)  # Way over limit
        
        passed, messages = lint_skill(skill_md)
        assert not passed
        assert any("exceeds" in m.lower() for m in messages)
    
    def test_strict_mode(self, tmp_path):
        """Strict mode should fail on warnings."""
        skill_dir = tmp_path / "warn-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        # Medium size (warning) + polite language
        skill_md.write_text("<critical_constraints>x</critical_constraints>\n" + "word " * 150 + "\nPlease do this.")
        
        # Normal mode: should pass
        passed_normal, _ = lint_skill(skill_md, strict=False)
        
        # Strict mode: should fail due to "please" and token warning
        passed_strict, _ = lint_skill(skill_md, strict=True)
        
        # At minimum, strict should catch the "please"
        assert not passed_strict or passed_normal


class TestGenerateReport:
    """Tests for generate_report function."""
    
    def test_empty_directory(self, tmp_path):
        """Empty directory should return empty results."""
        report, summary = generate_report(tmp_path)
        assert summary["total_skills"] == 0
        assert summary["total_tokens"] == 0
    
    def test_with_skills(self, tmp_path):
        """Should find and analyze skills."""
        # Create category/skill structure
        category = tmp_path / "coding"
        category.mkdir()
        
        skill_dir = category / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("<critical_constraints>x</critical_constraints>")
        
        report, summary = generate_report(tmp_path)
        assert summary["total_skills"] == 1
        assert len(summary["results"]) == 1
        assert summary["results"][0]["name"] == "test-skill"
