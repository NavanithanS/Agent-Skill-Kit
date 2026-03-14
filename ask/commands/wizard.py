"""Wizard command - Interactive guided workflow for copy, purge, sync, and update."""

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from ask.utils.skill_registry import get_all_skills
from ask.utils.agent_registry import get_available_agents

console = Console()

ACTIONS = [
    ("copy",   "Copy skills to one or more agents"),
    ("purge",  "Remove ask-* skills from agent directories"),
    ("sync",   "Sync all skills to all agents"),
    ("update", "Update already-installed skills"),
]


# ---------------------------------------------------------------------------
# Shared prompts
# ---------------------------------------------------------------------------

def _prompt_action() -> str:
    console.print(Panel("[bold cyan]🧙 ASK Wizard[/bold cyan]\nGuided workflow — copy, purge, sync, or update.", expand=False))
    console.print()

    table = Table(show_header=False, box=None, padding=(0, 2))
    for idx, (_, label) in enumerate(ACTIONS, 1):
        table.add_row(f"[dim]{idx}[/dim]", label)
    console.print(table)
    console.print()

    while True:
        choice = Prompt.ask("Choose action", default="0")
        if choice == "0":
            console.print("[yellow]Cancelled.[/yellow]")
            raise click.Abort()
        try:
            n = int(choice)
            if 1 <= n <= len(ACTIONS):
                return ACTIONS[n - 1][0]
        except ValueError:
            pass
        console.print(f"[red]Enter 1–{len(ACTIONS)} or 0 to cancel.[/red]")


def _prompt_skill_multi_select() -> list:
    """Multi-select skills by number. Returns list of skill dicts."""
    all_skills = get_all_skills()
    if not all_skills:
        console.print("[red]❌ No skills found in the skill library.[/red]")
        raise click.Abort()

    console.print("\n[bold cyan]📚 Select Skills[/bold cyan]\n")
    table = Table(show_header=True, header_style="bold", show_lines=False)
    table.add_column("#", style="dim", width=4)
    table.add_column("Name", style="cyan")
    table.add_column("Category", style="magenta")
    table.add_column("Description")

    for idx, skill in enumerate(all_skills, 1):
        desc = skill.get("description", "")
        table.add_row(
            str(idx),
            skill.get("name", ""),
            skill.get("category", ""),
            desc[:70] + "…" if len(desc) > 70 else desc,
        )
    console.print(table)
    console.print()
    console.print("[dim]Enter numbers separated by commas (e.g. 1,3) or 'all'[/dim]")

    while True:
        raw = Prompt.ask("Skills").strip()
        if raw == "0":
            raise click.Abort()
        if raw.lower() == "all":
            return all_skills
        try:
            indices = [int(x.strip()) for x in raw.split(",")]
            if all(1 <= i <= len(all_skills) for i in indices):
                return [all_skills[i - 1] for i in indices]
        except ValueError:
            pass
        console.print(f"[red]Enter numbers 1–{len(all_skills)}, comma-separated, or 'all'.[/red]")


def _prompt_agent_multi_select() -> list:
    """Multi-select agents by number. Returns list of agent name strings."""
    agents = get_available_agents()
    if not agents:
        console.print("[red]❌ No agents found.[/red]")
        raise click.Abort()

    console.print("\n[bold cyan]🤖 Select Agents[/bold cyan]\n")
    table = Table(show_header=False, box=None, padding=(0, 2))
    for idx, agent in enumerate(agents, 1):
        table.add_row(f"[dim]{idx}[/dim]", f"[cyan]{agent}[/cyan]")
    console.print(table)
    console.print()
    console.print("[dim]Enter numbers separated by commas (e.g. 1,2) or 'all'[/dim]")

    while True:
        raw = Prompt.ask("Agents").strip()
        if raw == "0":
            raise click.Abort()
        if raw.lower() == "all":
            return agents
        try:
            indices = [int(x.strip()) for x in raw.split(",")]
            if all(1 <= i <= len(agents) for i in indices):
                return [agents[i - 1] for i in indices]
        except ValueError:
            pass
        console.print(f"[red]Enter numbers 1–{len(agents)}, comma-separated, or 'all'.[/red]")


def _prompt_scope() -> bool:
    """Returns True for global, False for local."""
    console.print("\n[bold]Choose scope:[/bold]")
    console.print("  [green]1[/green] Global (user home  ~/.agents/skills/)")
    console.print("  [cyan]2[/cyan]  Local  (project    .agents/skills/)")
    console.print()

    while True:
        choice = Prompt.ask("Scope", choices=["0", "1", "2"], default="1")
        if choice == "0":
            raise click.Abort()
        return choice == "1"


# ---------------------------------------------------------------------------
# Action runners
# ---------------------------------------------------------------------------

def _run_copy_wizard(ctx):
    from ask.commands.copy import copy as copy_cmd

    selected_skills = _prompt_skill_multi_select()
    selected_agents = _prompt_agent_multi_select()
    use_global = _prompt_scope()

    scope_label = "global" if use_global else "local"

    console.print(f"\n[bold]📦 Preview[/bold]")
    console.print(f"  Skills : {', '.join(s['name'] for s in selected_skills)}")
    console.print(f"  Agents : {', '.join(selected_agents)}")
    console.print(f"  Scope  : {scope_label}\n")

    if not click.confirm("Execute?", default=True):
        console.print("[yellow]Cancelled.[/yellow]")
        return

    for agent in selected_agents:
        console.rule(f"[cyan]{agent}[/cyan]")
        for skill in selected_skills:
            ctx.invoke(
                copy_cmd,
                agent=agent,
                skill_name=skill["name"],
                copy_all=False,
                use_global=use_global,
                use_local=not use_global,
                overwrite=False,
            )


def _run_purge_wizard(ctx):
    from ask.commands.purge import purge as purge_cmd

    agents = sorted(set(get_available_agents() + ["universal"]))
    console.print("\n[bold cyan]🗑️  Select Agent to Purge[/bold cyan]\n")
    table = Table(show_header=False, box=None, padding=(0, 2))
    for idx, agent in enumerate(agents, 1):
        table.add_row(f"[dim]{idx}[/dim]", f"[cyan]{agent}[/cyan]")
    table.add_row("[yellow]all[/yellow]", "All agents (except universal)")
    console.print(table)
    console.print()

    while True:
        raw = Prompt.ask("Agent", default="0").strip()
        if raw == "0":
            raise click.Abort()
        if raw.lower() == "all":
            target = "all"
            break
        try:
            n = int(raw)
            if 1 <= n <= len(agents):
                target = agents[n - 1]
                break
        except ValueError:
            pass
        console.print(f"[red]Enter 1–{len(agents)}, 'all', or 0 to cancel.[/red]")

    ctx.invoke(purge_cmd, agent=target, yes=False, all_skills=False)


def _run_sync_wizard(ctx):
    from ask.commands.sync import sync as sync_cmd

    console.print("\n[bold cyan]🔄 Sync All Skills → All Agents[/bold cyan]")
    console.print("[dim]Syncs every skill in the library to every installed agent.[/dim]")
    console.print("[dim]You will be prompted for scope (global/local) next.[/dim]\n")
    if not click.confirm("Proceed?", default=True):
        console.print("[yellow]Cancelled.[/yellow]")
        return
    ctx.invoke(sync_cmd, target="all")


def _run_update_wizard(ctx):
    from ask.commands.update import update as update_cmd

    console.print("\n[bold cyan]🔄 Update Installed Skills[/bold cyan]")
    console.print("[dim]This will update all already-installed skills to their latest version.[/dim]\n")
    if not click.confirm("Proceed?", default=True):
        console.print("[yellow]Cancelled.[/yellow]")
        return
    ctx.invoke(update_cmd)


# ---------------------------------------------------------------------------
# Command
# ---------------------------------------------------------------------------

@click.command()
@click.pass_context
def wizard(ctx):
    """Interactive guided workflow — copy, purge, sync, or update skills."""
    action = _prompt_action()

    if action == "copy":
        _run_copy_wizard(ctx)
    elif action == "purge":
        _run_purge_wizard(ctx)
    elif action == "sync":
        _run_sync_wizard(ctx)
    elif action == "update":
        _run_update_wizard(ctx)
