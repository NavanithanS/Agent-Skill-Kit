import click
from pathlib import Path
from rich.console import Console

from ask.utils.skill_registry import get_all_skills, get_skill

console = Console()

@click.command(name="validate")
@click.option("--skill", help="Validate a specific skill by name")
@click.pass_context
def validate(ctx, skill):
    """Validate skill structure and metadata."""
    
    if skill:
        skills = [get_skill(skill)]
        if not skills[0]:
            console.print(f"[red]Error:[/red] skill '{skill}' not found.")
            return
    else:
        skills = get_all_skills()

    console.print(f"[dim]Validating {len(skills)} skills...[/dim]\n")
    
    issues = 0
    passed = 0
    
    for s in skills:
        skill_name = s.get("name", "Unknown")
        skill_path = Path(s.get("_path", ""))
        
        errors = []
        
        # 1. Naming Convention
        if not skill_name.startswith("ask-"):
            errors.append("Name must start with 'ask-'")
        if not skill_name.islower() or "_" in skill_name:
             errors.append("Name must be kebab-case (lowercase with hyphens)")
            
        # 2. Required Files & Directories (Gold Standard)
        if not (skill_path / "skill.yaml").exists():
             errors.append("Missing skill.yaml")
        
        if not (skill_path / "SKILL.md").exists():
             errors.append("Missing SKILL.md (README.md is deprecated)")

        if not (skill_path / "scripts").exists():
             errors.append("Missing 'scripts/' directory (Required for Validation Gates)")
             
        if not (skill_path / "tests").exists():
             errors.append("Missing 'tests/' directory (Required for Operational Excellence)")

        # 3. Metadata Structure
        if not s.get("version"):
            errors.append("Missing 'version' in skill.yaml")
        
        if not s.get("agents"):
             errors.append("Missing 'agents' list in skill.yaml")

        # Report
        if errors:
            issues += 1
            console.print(f"  [red]✗[/red] {skill_name}")
            for err in errors:
                console.print(f"    [dim]{err}[/dim]")
        else:
            passed += 1
            if ctx.obj.get('verbose'):
                console.print(f"  [green]✓[/green] {skill_name}")

    # Check for circular dependencies globally
    console.print("\n[dim]Validating dependency chains...[/dim]")
    all_skills_map = {s["name"]: s for s in get_all_skills()}

    dep_issues = 0
    for s in skills:
        try:
            from ask.utils.skill_registry import resolve_dependencies
            resolve_dependencies(s.get("name"), skill_map=all_skills_map)
        except ValueError as e:
            dep_issues += 1
            issues += 1
            console.print(f"  [red]✗[/red] circular dependency: [dim]{e}[/dim]")

    if dep_issues == 0:
        console.print("  [green]✓[/green] dependency chains OK")

    console.print(f"\n[dim]{passed} passed · {issues} failed[/dim]")

    if issues > 0:
        raise click.Abort()
