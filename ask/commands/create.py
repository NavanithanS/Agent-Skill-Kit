"""Create command - Interactive skill creation wizard."""

import click
from rich.console import Console
from rich.prompt import Prompt, Confirm

from ask.utils.filesystem import get_skills_dir, safe_create_dir
from ask.utils.validators import validate_skill_name
from ask.utils.agent_registry import get_available_agents

console = Console()

CATEGORIES = ["coding", "planning", "tooling"]

SKILL_YAML_TEMPLATE = """name: {name}
version: 1.0.0
category: {category}
description: {description}
tags: {tags}
agents:
{agents}
"""

README_TEMPLATE = """# {title}

{description}

## Purpose

Describe the purpose and goals of this skill.

## Usage

Explain how to use this skill effectively.

## Examples

Provide examples of the skill in action.

## Notes

Any additional notes or considerations.
"""


@click.group()
def create():
    """Create new skills or components."""
    pass


@create.command(name="skill")
@click.option("--name", "-n", help="Skill name (kebab-case)")
@click.option("--category", "-c", type=click.Choice(CATEGORIES), help="Skill category")
@click.option("--description", "-d", help="Short description")
def skill(name: str, category: str, description: str):
    """Create a new skill interactively."""
    console.print("\n[bold]Create Skill[/bold]  [dim]new skill for Agent Skill Kit[/dim]\n")
    
    # Get skill name
    if not name:
        name = Prompt.ask(
            "\n[bold]Skill name[/bold] (kebab-case, e.g., python-refactor)"
        )
    
    # Validate name
    if not validate_skill_name(name):
        console.print("[red]Error:[/red] invalid skill name — use lowercase letters, numbers, and hyphens only.")
        raise click.Abort()
    
    # Enforce/Suggest 'ask-' prefix
    if not name.startswith("ask-"):
        suggested_name = f"ask-{name}"
        if Confirm.ask(f"\n[dim]Recommended:[/dim] Add 'ask-' prefix? (Use '{suggested_name}')", default=True):
            name = suggested_name
            console.print(f"Using name: [cyan]{name}[/cyan]")
    
    # Get category
    if not category:
        console.print("\n[bold]Categories:[/bold]")
        for i, cat in enumerate(CATEGORIES, 1):
            console.print(f"  {i}. {cat}")
        category = Prompt.ask(
            "\n[bold]Category[/bold]",
            choices=CATEGORIES,
            default="coding"
        )
    
    # Get description
    if not description:
        description = Prompt.ask(
            "\n[bold]Description[/bold] (short summary)"
        )
    
    # Get tags
    tags_input = Prompt.ask(
        "\n[bold]Tags[/bold] (comma-separated)",
        default=""
    )
    tags = [t.strip() for t in tags_input.split(",") if t.strip()]
    
    # Confirm creation
    console.print("\n[bold]Summary[/bold]")
    console.print(f"  [dim]name[/dim]         {name}")
    console.print(f"  [dim]category[/dim]     {category}")
    console.print(f"  [dim]description[/dim]  {description}")
    console.print(f"  [dim]tags[/dim]         {', '.join(tags) if tags else '—'}")
    
    if not Confirm.ask("\nCreate this skill?", default=True):
        console.print("[dim]Cancelled.[/dim]")
        raise click.Abort()

    # Create skill directory
    skills_dir = get_skills_dir()
    skill_path = skills_dir / category / name

    if skill_path.exists():
        console.print(f"[red]Error:[/red] skill already exists: {skill_path}")
        raise click.Abort()
    
    safe_create_dir(skill_path)
    safe_create_dir(skill_path / "scripts")
    safe_create_dir(skill_path / "tests")

    # Create skill.yaml
    tags_yaml = "\n".join(f"  - {tag}" for tag in tags) if tags else "[]"
    agents_yaml = "\n".join(f"  - {agent}" for agent in get_available_agents())
    skill_yaml_content = SKILL_YAML_TEMPLATE.format(
        name=name,
        category=category,
        description=description,
        tags=f"\n{tags_yaml}" if tags else "[]",
        agents=agents_yaml
    )
    
    (skill_path / "skill.yaml").write_text(skill_yaml_content, encoding="utf-8")
    
    # Create SKILL.md
    title = name.replace("-", " ").title()
    readme_content = README_TEMPLATE.format(
        title=title,
        description=description
    )

    (skill_path / "SKILL.md").write_text(readme_content, encoding="utf-8")

    console.print(f"\n[green]✓[/green] Skill created  [dim]{skill_path}[/dim]")
    console.print(f"  [dim]{skill_path}/skill.yaml[/dim]")
    console.print(f"  [dim]{skill_path}/SKILL.md[/dim]")
    console.print(f'\n[dim]Tip: ask your agent to "improve the skill {name} with more examples"[/dim]')

