"""Remove command - Remove skills from agent directories."""

import click
from rich.console import Console
from rich.prompt import Confirm

from ask.utils.filesystem import get_adapter
from ask.utils.agent_registry import get_available_agents

console = Console()


@click.command()
@click.argument("agent", required=False, type=click.Choice(get_available_agents(), case_sensitive=False))
@click.option("--skill", "-s", "skill_name", required=True, help="Name of the skill to remove")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def remove(agent: str, skill_name: str, yes: bool):
    """Remove a skill from an agent (or all agents).
    
    If AGENT is provided (e.g., 'gemini'), removes the skill only from that agent.
    If AGENT is omitted, checks ALL agents and removes the skill from any that have it.
    
    Checks both Local (project) and Global (user) scopes.
    """
    agents_to_process = [agent] if agent else get_available_agents()
    
    targets_found = []
    
    # 1. Scan for the skill
    with console.status(f"Scanning for '{skill_name}'..."):
        for ag in agents_to_process:
            # Check Local
            adapter_local = get_adapter(ag, use_global=False)
            if adapter_local:
                path_local = adapter_local.get_target_path({"name": skill_name})
                if path_local and path_local.exists():
                    targets_found.append({
                        "agent": ag,
                        "scope": "Local",
                        "path": path_local,
                        "adapter": adapter_local
                    })

            # Check Global
            adapter_global = get_adapter(ag, use_global=True)
            if adapter_global:
                path_global = adapter_global.get_target_path({"name": skill_name})
                if path_global and path_global.exists():
                    targets_found.append({
                        "agent": ag,
                        "scope": "Global",
                        "path": path_global,
                        "adapter": adapter_global
                    })
    
    if not targets_found:
        console.print(f"[yellow]Skill '{skill_name}' not found in any checked agents.[/yellow]")
        return
    
    # 2. Show Summary
    console.print(f"\n[bold]Found '{skill_name}' in:[/bold]")
    for target in targets_found:
        console.print(f"  - [cyan]{target['agent']}[/cyan] ({target['scope']}): [dim]{target['path']}[/dim]")
    console.print()
    
    # 3. Confirm
    if not yes:
        if not Confirm.ask("Are you sure you want to [red]permanently remove[/red] these files?"):
            console.print("Cancelled.")
            raise click.Abort()
    
    # 4. Delete
    success_count = 0
    for target in targets_found:
        result = target['adapter'].remove_skill({"name": skill_name})
        
        if result["status"] == "removed":
            console.print(f"  [green]✓[/green] Removed from {target['agent']} ({target['scope']})")
            success_count += 1
        elif result["status"] == "not_found":
            console.print(f"  [yellow]?[/yellow] {target['agent']} ({target['scope']}): Already gone?")
        else:
            console.print(f"  [red]✗[/red] Failed to remove from {target['agent']}: {result.get('error')}")
            
    console.print(f"\n[green]Done![/green] Removed {success_count} file(s).")
