import click
import yaml
from pathlib import Path
from rich.console import Console

from ask.utils.skill_registry import get_all_skills, get_skill, get_skills_dir

console = Console()

@click.command(name="validate")
@click.option("--skill", help="Validate a specific skill by name")
def validate(skill):
    """Validate skill structure and metadata."""
    
    if skill:
        skills = [get_skill(skill)]
        if not skills[0]:
            console.print(f"[red]Skill '{skill}' not found.[/red]")
            return
    else:
        skills = get_all_skills()

    console.print(f"Validating {len(skills)} skills...\n")
    
    issues = 0
    passed = 0
    
    for s in skills:
        skill_name = s.get("name", "Unknown")
        skill_path = Path(s.get("_path", ""))
        
        errors = []
        
        # 1. Naming Convention
        if not skill_name.startswith("ask-"):
            errors.append("Name must start with 'ask-'")
            
        # 2. Required Files
        if not (skill_path / "skill.yaml").exists():
             errors.append("Missing skill.yaml")
        
        if not (skill_path / "SKILL.md").exists() and not (skill_path / "README.md").exists():
             errors.append("Missing SKILL.md or README.md")

        # 3. Metadata Structure
        if not s.get("version"):
            errors.append("Missing 'version' in skill.yaml")
        
        if not s.get("agents"):
             errors.append("Missing 'agents' list in skill.yaml")

        # Report
        if errors:
            issues += 1
            console.print(f"[bold red]❌ {skill_name}[/bold red]")
            for err in errors:
                console.print(f"  - {err}")
        else:
            passed += 1
            # Only show success in verbose mode? 
            # console.print(f"[green]✓ {skill_name}[/green]")

    console.print(f"\n[bold]Result:[/bold] {passed} passed, {issues} failed.")
    
    # Check for circular dependencies globally
    console.print(f"\n[bold]Validating dependency chains...[/bold]")
    all_skills_map = {s["name"]: s for s in get_all_skills()}
    
    for s in skills:
        try:
            from ask.utils.skill_registry import resolve_dependencies
            resolve_dependencies(s.get("name"), skill_map=all_skills_map)
        except ValueError as e:
             issues += 1
             console.print(f"  [red]Circular Dependency:[/red] {e}")

    if issues > 0:
        raise click.Abort()
