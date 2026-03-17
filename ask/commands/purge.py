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
        console.print("\n[bold]Purge[/bold]  [dim]remove ask-* skills from agent directories[/dim]\n")

        table = Table(show_header=False, box=None, padding=(0, 2))
        for idx, ag in enumerate(agents_list, 1):
            table.add_row(f"[dim]{idx}[/dim]", ag)

        console.print(table)
        console.print()
        console.print("[dim]0 cancel · 1-{n} select · all purge all (except universal)[/dim]\n".format(n=len(agents_list)))

        while True:
            choice = Prompt.ask("Agent", default="0")

            if choice == "0":
                console.print("[dim]Cancelled.[/dim]")
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
                    console.print(f"[red]Enter 0–{len(agents_list)} or all[/red]")
            except ValueError:
                console.print("[red]Enter a number, all, or 0 to cancel[/red]")

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
        console.print(f"\n[green]✓[/green] No {prefix_msg} skills found to purge.")

        if agent == "all":
            console.print("[dim]'all' excludes 'universal' (USoT). Run: ask purge universal to remove those.[/dim]")
            usot_targets = []
            _collect_targets(get_adapter("universal", use_global=False), "universal", "Local", True, usot_targets)
            _collect_targets(get_adapter("universal", use_global=True), "universal", "Global", True, usot_targets)
            if usot_targets:
                skill_names = ", ".join(sorted({t["path"].name for t in usot_targets}))
                console.print(f"[dim]Found in USoT: {skill_names}[/dim]")
        elif not all_skills:
            console.print("[dim]Only searched 'ask-*' prefixed skills. Use --all-skills to see everything.[/dim]")

        return

    skill_label = "skill(s)" if all_skills else "'ask-*' skill(s)"
    console.print(f"\n[bold]Found {len(targets_found)} {skill_label} to purge:[/bold]")
    for target in targets_found:
        console.print(f"  [dim]{target['agent']}[/dim] ({target['scope']})  {target['path']}")
    console.print()

    if not yes:
        if not Confirm.ask("Permanently delete these items?"):
            console.print("[dim]Cancelled.[/dim]")
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
            console.print(f"  [green]✓[/green] {path.name} [dim]from {target['agent']} ({target['scope']})[/dim]")
            success_count += 1
        except OSError as e:
            console.print(f"  [red]✗[/red] {path.name} [dim]{e}[/dim]")
            fail_count += 1

    parts = [f"{success_count} deleted"]
    if fail_count:
        parts.append(f"{fail_count} failed")
    console.print("\n[dim]" + " · ".join(parts) + "[/dim]")
