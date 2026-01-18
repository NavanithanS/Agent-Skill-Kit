from ask.cli import main

def test_cli_version(runner):
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "ask" in result.output

def test_list_skills_help(runner):
    result = runner.invoke(main, ["list", "--help"])
    assert result.exit_code == 0

def test_remove_help(runner):
    result = runner.invoke(main, ["remove", "--help"])
    assert result.exit_code == 0
    assert "Remove a skill" in result.output
