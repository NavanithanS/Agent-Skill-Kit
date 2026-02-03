"""Create command - Interactive skill creation wizard."""

import os
from pathlib import Path

import click
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from ask.utils.filesystem import get_skills_dir, safe_create_dir
from ask.utils.validators import validate_skill_name
from ask.utils.agent_registry import get_available_agents

console = Console()

CATEGORIES = ["coding", "reasoning", "tooling", "other"]

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
    console.print(Panel.fit(
        "[bold cyan]🛠 Skill Creator[/bold cyan]\n\n"
        "Create a new skill for Agent Skill Kit",
        border_style="cyan"
    ))
    
    # Get skill name
    if not name:
        name = Prompt.ask(
            "\n[bold]Skill name[/bold] (kebab-case, e.g., python-refactor)"
        )
    
    # Validate name
    if not validate_skill_name(name):
        console.print("[red]❌ Invalid skill name. Use lowercase letters, numbers, and hyphens only.[/red]")
        raise click.Abort()
    
    # Enforce/Suggest 'ask-' prefix
    if not name.startswith("ask-"):
        suggested_name = f"ask-{name}"
        if Confirm.ask(f"\n[yellow]Recommended:[/yellow] Add 'ask-' prefix? (Use '{suggested_name}')", default=True):
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
    console.print("\n[bold]Summary:[/bold]")
    console.print(f"  Name: [cyan]{name}[/cyan]")
    console.print(f"  Category: [cyan]{category}[/cyan]")
    console.print(f"  Description: [cyan]{description}[/cyan]")
    console.print(f"  Tags: [cyan]{', '.join(tags) if tags else 'none'}[/cyan]")
    
    if not Confirm.ask("\nCreate this skill?", default=True):
        console.print("[yellow]Cancelled.[/yellow]")
        raise click.Abort()
    
    # Create skill directory
    skills_dir = get_skills_dir()
    skill_path = skills_dir / category / name
    
    if skill_path.exists():
        console.print(f"[red]❌ Skill already exists: {skill_path}[/red]")
        raise click.Abort()
    
    safe_create_dir(skill_path)
    
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
    
    # Create README.md
    title = name.replace("-", " ").title()
    readme_content = README_TEMPLATE.format(
        title=title,
        description=description
    )
    
    (skill_path / "README.md").write_text(readme_content, encoding="utf-8")
    
    console.print(f"\n[green]✅ Skill created successfully![/green]")
    console.print(f"   Location: [cyan]{skill_path}[/cyan]")
    console.print(f"\n   Edit your skill:")
    console.print(f"   • [dim]{skill_path}/skill.yaml[/dim]")
    console.print(f"   • [dim]{skill_path}/README.md[/dim]")
    
    # AI suggestion
    console.print(f"\n[bold yellow]💡 Tip:[/bold yellow] For richer content, ask your AI agent:")
    console.print(f'   [dim]"Improve the skill {name} with more examples and best practices"[/dim]')

