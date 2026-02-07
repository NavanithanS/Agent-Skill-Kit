"""Add-agent command - Scaffold a new agent adapter."""

import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from ask.utils.filesystem import get_project_root

console = Console()

ADAPTER_TEMPLATE = '''"""{{agent_title}} adapter - transforms skills for {{agent_title}}."""

from pathlib import Path
from typing import Dict

from agents.base import BaseAdapter
from ask.utils.skill_registry import get_skill_readme


class {{class_name}}Adapter(BaseAdapter):
    """Adapter for {{agent_title}} format.
    
    Paths:
    - Local: {{local_path}}
    - Global: {{global_path}}
    """
    
    def __init__(self, use_global: bool = False):
        if use_global:
            self.target_dir = Path.home() / "{{global_dir}}"
        else:
            self.target_dir = Path.cwd() / "{{local_dir}}"
    
    def get_target_path(self, skill: Dict, name: str = None) -> Path:
        """Get the target path for a skill."""
        skill_name = name or skill.get("name", "unknown")
        return self.target_dir / f"{skill_name}.md"
    
    def transform(self, skill: Dict) -> str:
        """Transform a skill into {{agent_title}} format."""
        name = skill.get("name", "Unknown")
        description = skill.get("description", "")
        readme = get_skill_readme(skill) or ""
        
        content = f"""# {name.replace("-", " ").title()}

{description}

---

{readme}
"""
        return content
'''


@click.command(name="add-agent")
@click.argument("agent_name", required=False)
@click.option("--local-path", "-l", help="Local (project) path, e.g. .cursor/rules")
@click.option("--global-path", "-g", help="Global (user) path, e.g. ~/.cursor/rules")
def add_agent(agent_name: str, local_path: str, global_path: str):
    """Add support for a new AI code editor.
    
    AGENT_NAME is the name of the agent (e.g., cursor, windsurf, aider).
    
    This command scaffolds the adapter and registers it automatically.
    
    Examples:
    
        ask add-agent cursor
        
        ask add-agent windsurf --local-path .windsurf/rules --global-path ~/.windsurf/rules
    """
    if not agent_name:
        console.print(Panel.fit(
            "[bold cyan]🔌 Add Agent Wizard[/bold cyan]\n\n"
            "Add support for a new AI code editor/agent",
            border_style="cyan"
        ))
        agent_name = Prompt.ask("\n[bold]Agent Name[/bold] (e.g. cursor, windsurf)")
        
    if not agent_name:
        console.print("[red]❌ Agent name is required.[/red]")
        raise click.Abort()

    agent_name = agent_name.lower()
    
    # Security: Validate agent name to prevent path traversal
    if not agent_name.replace("-", "").replace("_", "").isalnum():
        console.print("[red]❌ Invalid agent name. Use only letters, numbers, hyphens, and underscores.[/red]")
        raise click.Abort()

    agent_title = agent_name.replace("-", " ").replace("_", " ").title()
    class_name = agent_title.replace(" ", "")
    
    console.print(f"\n[bold]🔌 Adding new agent: {agent_title}[/bold]\n")
    
    # Get paths if not provided
    if not local_path:
        local_path = Prompt.ask(
            f"Local path (project directory)",
            default=f".{agent_name}/skills"
        )
    
    if not global_path:
        global_path = Prompt.ask(
            f"Global path (user home)",
            default=f"~/.{agent_name}/skills"
        )
    
    # Parse paths for template
    local_dir = local_path.lstrip("./")
    global_dir = global_path.replace("~/", "").lstrip("./")
    
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  Agent: [cyan]{agent_name}[/cyan]")
    console.print(f"  Local: [cyan]{local_path}[/cyan]")
    console.print(f"  Global: [cyan]{global_path}[/cyan]")
    
    if not Confirm.ask("\nCreate adapter?", default=True):
        console.print("[yellow]Cancelled.[/yellow]")
        raise click.Abort()
    
    project_root = get_project_root()
    
    # 1. Create adapter directory and file
    adapter_dir = project_root / "agents" / agent_name
    adapter_dir.mkdir(parents=True, exist_ok=True)
    
    adapter_content = ADAPTER_TEMPLATE.replace("{{agent_name}}", agent_name)
    adapter_content = adapter_content.replace("{{agent_title}}", agent_title)
    adapter_content = adapter_content.replace("{{class_name}}", class_name)
    adapter_content = adapter_content.replace("{{local_path}}", local_path)
    adapter_content = adapter_content.replace("{{global_path}}", global_path)
    adapter_content = adapter_content.replace("{{local_dir}}", local_dir)
    adapter_content = adapter_content.replace("{{global_dir}}", global_dir)
    
    adapter_file = adapter_dir / "adapter.py"
    adapter_file.write_text(adapter_content)
    console.print(f"  [green]✓[/green] Created {adapter_file.relative_to(project_root)}")
    
    
    console.print(f"\n[green]✅ Agent '{agent_name}' added successfully![/green]")
    console.print(f"\nTest it with:")
    console.print(f"  [dim]ask copy {agent_name} --skill bug-finder[/dim]")
    
    # AI suggestion
    console.print(f"\n[bold yellow]💡 Tip:[/bold yellow] For better adapter, ask your AI agent:")
    console.print(f'   [dim]"Review and improve the {agent_name} adapter with correct paths and format"[/dim]')

