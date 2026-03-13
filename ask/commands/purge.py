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


def _collect_targets(adapter, agent_name: str, scope: str, all_skills: bool, targets: list):
    """Helper to collect matching skill paths from an adapter's target directory."""
    if (
        isinstance(adapter, BaseAdapter)
        and hasattr(adapter, 'target_dir')
        and adapter.target_dir
        and adapter.target_dir.is_dir()
    ):
        for item in adapter.target_dir.iterdir():
            if all_skills or item.name.startswith("ask-"):
                targets.append({"agent": agent_name, "scope": scope, "path": item})


@click.command()
@click.argument("agent", required=False)  # Fix #4: validate at runtime, not import time
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
@click.option("--all-skills", is_flag=True, help="Purge all skills, not just those starting with 'ask-'")
def purge(agent: str, yes: bool, all_skills: bool = False):
    """Clean up ask-* skills from agent directories.

    If AGENT is provided, purges ask-* skills from that agent.
    If omitted, asks interactively which agent to purge from.
    The 'universal' agent refers to the .agents/skills/ directory.

    Only deletes files/folders starting with the 'ask-' prefix by default.
    Use --all-skills to delete all items in the skill directory.
    """
    # Fix #4: resolve agent list at runtime
    agents_list = sorted(list(set(get_available_agents() + ["universal"])))

    # Validate agent argument if provided
    if agent and agent not in agents_list and agent != "all":
        valid = ", ".join(agents_list)
        raise click.BadParameter(
            f"'{agent}' is not a valid agent. Choose from: {valid}, all",
            param_hint="'AGENT'"
        )

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

    # Fix #2: copy list to avoid mutating the shared agents_list reference
    agents_to_process = list(agents_list) if agent == "all" else [agent]
    if agent == "all":
        # Preserve USoT when purging "all" — user must select 'universal' explicitly
        agents_to_process = [a for a in agents_to_process if a != "universal"]

    targets_found = []

    # Fix #6: clear, non-glob scan label
    scan_label = "all" if all_skills else "'ask-*'"
    with console.status(f"Scanning for {scan_label} skills..."):
        for ag in agents_to_process:
            # Fix #3: deduplicated using the helper
            _collect_targets(get_adapter(ag, use_global=False), ag, "Local", all_skills, targets_found)
            _collect_targets(get_adapter(ag, use_global=True), ag, "Global", all_skills, targets_found)

    if not targets_found:
        prefix_msg = "any" if all_skills else "ask-*"
        console.print(f"\n[green]✨ No {prefix_msg} skills found to purge in the selected agent(s).[/green]")

        if agent == "all":
            console.print("[dim]Note: 'all' excludes 'universal' (USoT) to protect your Source of Truth.[/dim]")
            # Check if universal has skills and surface a targeted hint
            usot_targets = []
            _collect_targets(get_adapter("universal", use_global=False), "universal", "Local", True, usot_targets)
            _collect_targets(get_adapter("universal", use_global=True), "universal", "Global", True, usot_targets)
            if usot_targets:
                skill_names = ", ".join(sorted({t["path"].name for t in usot_targets}))
                console.print(f"[yellow]💡 Found in USoT:[/yellow] [cyan]{skill_names}[/cyan]")
                console.print("[yellow]   Run:[/yellow] [bold]ask purge universal[/bold] [dim]to remove them.[/dim]")
        elif not all_skills:
            console.print("[dim]Note: Only searching for 'ask-' prefixed skills. Use --all-skills to see everything.[/dim]")

        return

    # Fix #1: dynamic label respects --all-skills
    skill_label = "skill(s)" if all_skills else "'ask-*' skill(s)"
    console.print(f"\n[bold]Found {len(targets_found)} {skill_label} to purge:[/bold]")
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
