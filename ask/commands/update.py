"""Update command - Update installed skills to the latest version."""

import click
import shutil
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from typing import List, Dict, Any

from ask.utils.skill_registry import get_skill, get_all_skills
from ask.utils.filesystem import get_adapter
from ask.utils.agent_registry import get_available_agents

console = Console()

def _scan_for_updates() -> List[Dict[str, Any]]:
    """Scan all agents and scopes for available skill updates."""
    available_agents = get_available_agents()
    source_skills_map = {s["name"]: s for s in get_all_skills()}
    updates_found = []
    
    for agent in available_agents:
        # Check both local and global scopes
        for scope_name, scope_bool in [("local", False), ("global", True)]:
            adapter = get_adapter(agent, use_global=scope_bool)
            if not adapter:
                continue
                
            installed = adapter.list_installed_skills()
            
            for skill_name, current_ver in installed.items():
                source_skill = source_skills_map.get(skill_name)
                
                # If skill exists in source
                if source_skill:
                    latest_ver = source_skill.get("version", "0.0.0")
                    
                    needs_update = False
                    if current_ver == "0.0.0":
                        needs_update = True
                    elif current_ver != latest_ver:
                        needs_update = True
                        
                    if needs_update:
                        updates_found.append({
                            "agent": agent,
                            "skill": skill_name,
                            "scope": scope_name,
                            "current": current_ver,
                            "latest": latest_ver,
                            "source_skill": source_skill,
                            "adapter": adapter
                        })
    return updates_found

@click.command()
@click.option("--yes", "-y", is_flag=True, help="Auto-confirm all updates")
def update(yes: bool):
    """
    Update installed skills to the latest version.
    
    Scans all agents for installed skills, checks their versions against
    the source repository, and interactively updates them.
    
    Safe Update Strategy:
    1. Backs up existing 'SKILL.md' to 'SKILL.md.bak'
    2. Overwrites with new version
    3. Option to clean up backup after success
    """
    
    # 1. Scan Phase
    console.print("[bold cyan]🔍 Scanning for updates...[/bold cyan]")
    updates_found = _scan_for_updates()

    if not updates_found:
        console.print("[green]✨ All skills are up to date![/green]")
        return




    # 2. Display Table
    table = Table(title="Available Updates", show_header=True, header_style="bold")
    table.add_column("#", style="dim", width=4)
    table.add_column("Agent", style="cyan")
    table.add_column("Skill", style="bold white")
    table.add_column("Current", style="yellow")
    table.add_column("Latest", style="green")
    table.add_column("Location", style="blue")
    
    for idx, item in enumerate(updates_found, 1):
        table.add_row(
            str(idx),
            item["agent"],
            item["skill"],
            item["current"],
            item["latest"],
            item["scope"]
        )
    
    console.print(table)
    
    # 3. Selection
    if yes:
        selected_indices = range(len(updates_found))
    else:
        console.print("\n[bold]Select skills to update:[/bold]")
        console.print("  [green]all[/green]  Update all (default)")
        console.print("  [dim]0[/dim]    Cancel")
        console.print(f"  [cyan]1-{len(updates_found)}[/cyan] specific number(s) (comma separated)")
        
        choice = Prompt.ask("Choice", default="all")
        
        if choice == "0":
            console.print("[yellow]Cancelled.[/yellow]")
            return
        elif choice.lower() == "all":
            selected_indices = range(len(updates_found))
        else:
            try:
                # Parse "1, 3, 5"
                selected_indices = []
                parts = choice.split(",")
                for p in parts:
                    idx = int(p.strip()) - 1
                    if 0 <= idx < len(updates_found):
                        selected_indices.append(idx)
                    else:
                        console.print(f"[yellow]Ignoring invalid index: {p}[/yellow]")
            except ValueError:
                console.print("[red]Invalid input[/red]")
                return

    if not selected_indices:
        console.print("[yellow]No skills selected.[/yellow]")
        return

    # Ask for cleanup preference once
    auto_delete_backup = False
    if not yes:
        auto_delete_backup = click.confirm("Delete backups after successful update?", default=False)
    
    # 4. Execution
    console.print("\n[bold]🚀 Updating...[/bold]\n")
    
    success_count = 0
    
    for idx in selected_indices:
        item = updates_found[idx]
        adapter = item["adapter"]
        skill = item["source_skill"]
        skill_name = item["skill"]
        agent = item["agent"]
        
        target_path = adapter.get_target_path(skill)
        backup_path = target_path.with_suffix(".md.bak")
        
        try:
            # A. Backup
            if target_path.exists():
                # Overwrite existing backup if any
                shutil.copy2(target_path, backup_path)
            
            # B. Update (Force Copy)
            result = adapter.copy_skill(skill, force=True)
            
            if result["status"] == "copied":
                console.print(f"  [green]✓[/green] Updated {agent}/{skill_name}")
                success_count += 1
                
                # C. Cleanup determined by global preference
                if auto_delete_backup:
                     backup_path.unlink(missing_ok=True)
                     console.print("    [dim]Backup deleted[/dim]")
                else:
                     console.print(f"    [dim]Backup saved to {backup_path.name}[/dim]")
            else:
                console.print(f"  [red]✗[/red] Failed to update {skill_name}: {result.get('reason')}")
                
        except PermissionError:
             console.print(f"  [red]✗[/red] Permission denied updating {skill_name}")
        except OSError as e:
             console.print(f"  [red]✗[/red] OS Error updating {skill_name}: {e}")
        except Exception as e:
            console.print(f"  [red]✗[/red] Unexpected error updating {skill_name}: {e}")
            
    console.print(f"\n[green]Done! Updated {success_count} skill(s).[/green]")
