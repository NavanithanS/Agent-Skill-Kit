"""Sync command - Synchronize all skills to all agents."""

import shutil
from pathlib import Path

import click
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from ask.utils.skill_registry import get_all_skills
from ask.utils.filesystem import get_adapter, deploy_skill_link
from ask.utils.agent_registry import get_available_agents
from agents.universal.adapter import UniversalAdapter

console = Console()


@click.command()
@click.argument("target", type=click.Choice(["all"]), default="all", required=False)
def sync(target: str = "all"):
    """Sync all skills to all agents.

    Prompts for local or global destination.

    Examples:

        ask sync
        ask sync all
    """
    skills = get_all_skills()

    if not skills:
        console.print("[yellow]Warning:[/yellow] no skills found to sync.")
        return

    agents = get_available_agents()

    if not agents:
        console.print("[yellow]Warning:[/yellow] no agents found.")
        return

    # Ask for scope first
    console.print(f"\n[bold]Sync[/bold]  [dim]{len(skills)} skill(s) → {len(agents)} agent(s)[/dim]\n")
    console.print("[bold]Destination[/bold]")
    console.print("  [dim]0[/dim]  cancel")
    console.print("  [dim]1[/dim]  global  [dim](user home)[/dim]")
    console.print("  [dim]2[/dim]  local   [dim](project)[/dim]")

    choice_num = Prompt.ask(
        "Scope",
        choices=["0", "1", "2"],
        default="2"
    )

    if choice_num == "0":
        console.print("[dim]Cancelled.[/dim]")
        raise click.Abort()

    use_global = (choice_num == "1")
    scope_name = "global" if use_global else "local"

    console.print(f"\n[dim]Syncing to {scope_name}...[/dim]\n")

    # Pre-load adapters once to avoid repeated importlib calls
    universal_adapter = UniversalAdapter(use_global=use_global)
    adapters = {agent: get_adapter(agent, use_global=use_global) for agent in agents}

    # Results tracking
    results = {agent: {"copied": 0, "skipped": 0, "failed": 0} for agent in agents}

    for skill in skills:
        # 1. Write to Universal Source of Truth (reuse existing on conflict)
        u_result = universal_adapter.copy_skill(skill)
        if u_result["status"] not in ("copied", "conflict"):
            for agent in agents:
                if agent in skill.get("agents", []):
                    results[agent]["failed"] += 1
            console.print(f"  [red]✗[/red] {skill['name']} [dim]unexpected USoT status: {u_result['status']}[/dim]")
            continue

        u_path = Path(u_result["target"])

        # 2. Symlink each compatible agent to the USoT path
        for agent in agents:
            if agent not in skill.get("agents", []):
                continue

            adapter = adapters.get(agent)
            if not adapter:
                console.print(f"  [dim]–[/dim] {skill['name']} → {agent} [dim](no adapter, skipped)[/dim]")
                continue

            try:
                agent_target = adapter.get_target_path(skill)

                # Migrate any legacy hard-copied file/folder to a symlink
                # is_symlink() catches broken symlinks that .exists() misses
                if agent_target.exists() and not agent_target.is_symlink():
                    if agent_target.is_dir():
                        shutil.rmtree(agent_target)
                    else:
                        agent_target.unlink()
                elif agent_target.is_symlink():
                    # Stale symlink pointing to a deleted USoT — remove to re-link
                    agent_target.unlink()

                if not agent_target.exists() and not agent_target.is_symlink():
                    deploy_mode = deploy_skill_link(u_path, agent_target)
                    results[agent]["copied"] += 1
                    if deploy_mode == "copy":
                        console.print(f"  [green]✓[/green] {skill['name']} → {agent} [dim](copied, symlinks unavailable)[/dim]")
                else:
                    results[agent]["skipped"] += 1

            except Exception as e:
                results[agent]["failed"] += 1
                console.print(f"  [red]✗[/red] {skill['name']} → {agent} [dim]{e}[/dim]")

    # Summary table
    table = Table(title="Sync Summary", show_header=True, header_style="bold", box=None)
    table.add_column("Agent", style="cyan")
    table.add_column("Copied", style="green", justify="right")
    table.add_column("Skipped", style="yellow", justify="right")
    table.add_column("Failed", style="red", justify="right")

    for agent, counts in results.items():
        table.add_row(
            agent,
            str(counts["copied"]),
            str(counts["skipped"]),
            str(counts["failed"])
        )

    console.print()
    console.print(table)
