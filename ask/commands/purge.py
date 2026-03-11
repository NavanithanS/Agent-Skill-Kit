"""Purge command - Clean up ask-* skills from agent directories."""

import click
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table
import shutil

from ask.utils.filesystem import get_adapter
from ask.utils.agent_registry import get_available_agents
from agents.base import BaseAdapter

console = Console()


@click.command()
@click.argument("agent", required=False, type=click.Choice(get_available_agents() + ["universal"], case_sensitive=False))
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def purge(agent: str, yes: bool):
    """Clean up ask-* skills from agent directories.

    If AGENT is provided, purges ask-* skills from that agent.
    If omitted, asks interactively which agent to purge from.
    The 'universal' agent refers to the .agents/skills/ directory.

    Only deletes files/folders starting with the 'ask-' prefix.
    """
    agents_list = get_available_agents()
    if "universal" not in agents_list:
        agents_list.append("universal")

    if not agent:
        console.print("\n[bold cyan]🗑️  Agent Purge Wizard[/bold cyan]\n")
        
        table = Table(show_header=True, header_style="bold")
        table.add_column("#", style="dim", width=4)
        table.add_column("Agent", style="cyan")
        
        for idx, ag in enumerate(agents_list, 1):
            table.add_row(str(idx), ag)
            
        console.print(table)
        console.print("\n[bold]Choose an agent to clean:[/bold]")
        console.print("  [dim]0[/dim] Cancel")
        console.print(f"  [green]1-{len(agents_list)}[/green] Select agent by number")
        console.print("  [yellow]all[/yellow] Purge ask-* from ALL agents (except universal)")
        console.print()
        
        while True:
            choice = Prompt.ask("Enter choice", default="0")
            
            if choice == "0":
                console.print("[yellow]Cancelled.[/yellow]")
                raise click.Abort()
                
            if choice.lower() == "all":
                agent = "all"
                break
                
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(agents_list):
                    agent = agents_list[choice_num - 1]
                    break
                else:
                    console.print(f"[red]Invalid choice. Enter 0-{len(agents_list)} or 'all'[/red]")
            except ValueError:
                console.print("[red]Invalid input. Enter a number, 'all', or '0' to cancel[/red]")

    agents_to_process = agents_list if agent == "all" else [agent]
    if agent == "all":
        # Usually we want to preserve universal skills when purging all legacy agents
        if "universal" in agents_to_process:
            agents_to_process.remove("universal")

    targets_found = []

    with console.status("Scanning for ask-* skills..."):
        for ag in agents_to_process:
            # Check Local
            adapter_local = get_adapter(ag, use_global=False)
            if isinstance(adapter_local, BaseAdapter) and hasattr(adapter_local, 'target_dir') and adapter_local.target_dir and adapter_local.target_dir.is_dir():
                for item in adapter_local.target_dir.iterdir():
                    if item.name.startswith("ask-"):
                        targets_found.append({
                            "agent": ag,
                            "scope": "Local",
                            "path": item
                        })

            # Check Global
            adapter_global = get_adapter(ag, use_global=True)
            if isinstance(adapter_global, BaseAdapter) and hasattr(adapter_global, 'target_dir') and adapter_global.target_dir and adapter_global.target_dir.is_dir():
                for item in adapter_global.target_dir.iterdir():
                    if item.name.startswith("ask-"):
                        targets_found.append({
                            "agent": ag,
                            "scope": "Global",
                            "path": item
                        })

    if not targets_found:
        console.print(f"\n[green]✨ No 'ask-*' skills found to purge in the selected agent(s).[/green]")
        return

    console.print(f"\n[bold]Found {len(targets_found)} 'ask-*' skill(s) to purge:[/bold]")
    for target in targets_found:
        console.print(f"  - [cyan]{target['agent']}[/cyan] ({target['scope']}): [dim]{target['path']}[/dim]")
    console.print()

    if not yes:
        if not Confirm.ask("Are you sure you want to [red]permanently delete[/red] these items?"):
            console.print("Cancelled.")
            raise click.Abort()

    success_count = 0
    fail_count = 0
    for target in targets_found:
        path = target['path']
        try:
            if path.is_file() or path.is_symlink():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
            console.print(f"  [green]✓[/green] Deleted: {path.name} from {target['agent']} ({target['scope']})")
            success_count += 1
        except OSError as e:
            console.print(f"  [red]✗[/red] Failed to delete {path.name}: {e}")
            fail_count += 1

    console.print(f"\n[green]Purge complete![/green] Deleted {success_count} item(s).")
    if fail_count > 0:
        console.print(f"[red]Failed to delete {fail_count} item(s).[/red]")
