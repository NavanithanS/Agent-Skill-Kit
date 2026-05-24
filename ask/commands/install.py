"""Install command - Install skills from remote git repositories."""

import click
import shutil
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from typing import Optional

from ask.utils.git import fetch_remote_skills
from ask.utils.skill_registry import get_all_skills
from ask.utils.filesystem import get_adapter, get_safe_cwd, deploy_skill_link
from ask.utils.agent_registry import get_agent_scopes
from ask.commands.copy import prompt_agent_selection
from agents.universal.adapter import UniversalAdapter

console = Console()

@click.command()
@click.argument("source")
@click.option("--global", "use_global", is_flag=True, default=None, help="Install to global (user home) location")
@click.option("--local", "use_local", is_flag=True, default=None, help="Install to local (project) location")
@click.option("--overwrite", "-f", is_flag=True, help="Overwrite existing skill without prompting")
@click.pass_context
def install(ctx, source: str, use_global: Optional[bool], use_local: Optional[bool], overwrite: bool):
    """
    Install skills from a remote Git repository.
    
    Supports GitHub shorthands (org/repo) and full git URLs.
    
    Examples:
    
        ask install my-org/ai-skills
        ask install https://github.com/my-org/ai-skills.git
    """
    if use_global and use_local:
        console.print("[red]Error:[/red] --global and --local are mutually exclusive")
        raise click.Abort()

    # 1. Fetch Remote Skills
    console.print(f"[dim]Fetching skills from {source}...[/dim]")
    try:
        remote_dir = fetch_remote_skills(source)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise click.Abort()
        
    # 2. Parse Skills
    remote_skills = get_all_skills(base_path=remote_dir)
    if not remote_skills:
        console.print(f"[yellow]Warning:[/yellow] No valid skills found in {source}")
        return

    # 3. Interactive Selection (if multiple)
    if len(remote_skills) == 1:
        skills_to_install = remote_skills
        console.print(f"[dim]Found 1 skill: {skills_to_install[0]['name']}[/dim]")
    else:
        console.print(f"\n[bold]Found {len(remote_skills)} Skills in {source}[/bold]\n")
        table = Table(show_header=True, header_style="bold", box=None)
        table.add_column("#", style="dim", width=4)
        table.add_column("Name", style="cyan")
        table.add_column("Description")
        
        for idx, skill in enumerate(remote_skills, 1):
            desc = skill.get("description", "")
            if len(desc) > 80:
                desc = desc[:77] + "..."
            table.add_row(str(idx), skill.get("name", ""), desc)
            
        console.print(table)
        console.print("\n[dim]0 cancel · 1-{n} select · all install all[/dim]".format(n=len(remote_skills)))
        
        choice = Prompt.ask("Select", default="all")
        if choice == "0":
            console.print("[dim]Cancelled.[/dim]")
            raise click.Abort()
        elif choice.lower() == "all":
            skills_to_install = remote_skills
        else:
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(remote_skills):
                    skills_to_install = [remote_skills[choice_num - 1]]
                else:
                    console.print("[red]Invalid selection[/red]")
                    raise click.Abort()
            except ValueError:
                console.print("[red]Invalid input[/red]")
                raise click.Abort()
                
    # 4. Agent Selection
    agent = prompt_agent_selection(skills_to_install)
    
    # 5. Scope Selection
    scopes = get_agent_scopes().get(agent, {"local": True, "global": True})
    
    if use_global:
        if not scopes["global"]:
            console.print(f"[red]Error:[/red] agent '{agent}' does not support global scope")
            raise click.Abort()
    elif use_local:
        if not scopes["local"]:
            console.print(f"[red]Error:[/red] agent '{agent}' does not support local scope")
            raise click.Abort()
    elif scopes["global"] and not scopes["local"]:
        use_global = True
    elif scopes["local"] and not scopes["global"]:
        use_local = True
    else:
        # Prompt
        console.print("\n[bold]Destination[/bold]")
        console.print("  [dim]1[/dim]  global  [dim](user home)[/dim]")
        console.print("  [dim]2[/dim]  local   [dim](project)[/dim]")
        choice_num = Prompt.ask("Scope", choices=["1", "2"], default="1")
        if choice_num == "1":
            use_global = True
        else:
            use_global = False
            
    # 6. Installation Loop
    project_root = get_safe_cwd()
    adapter = None
    if agent != "universal":
        adapter = get_adapter(agent, use_global=use_global, project_root=project_root)
    universal_adapter = UniversalAdapter(use_global=use_global, project_root=project_root)
    
    conflict_strategy = "overwrite" if overwrite else None
    
    console.print(f"\n[dim]Installing to {'global' if use_global else 'local'}...[/dim]\n")
    
    success_count = 0
    
    for skill in skills_to_install:
        try:
            name_to_use = skill.get("name")
            
            # Universal Adapter first
            result = universal_adapter.copy_skill(skill)
            
            if result["status"] == "conflict":
                if conflict_strategy == "overwrite":
                    result = universal_adapter.copy_skill(skill, force=True)
                elif conflict_strategy == "skip":
                    console.print(f"  [dim]–[/dim] {skill['name']} [dim]skipped[/dim]")
                    continue
                else:
                    console.print(f"  [yellow]–[/yellow] '{skill['name']}' already exists")
                    while True:
                        choice = Prompt.ask(
                            "    use existing / overwrite / rename / skip / view diff",
                            choices=["use existing", "overwrite", "rename", "skip", "view diff", "v"],
                            default="use existing"
                        )
                        if choice in ["view diff", "v"]:
                            from ask.utils.diff import show_diff
                            new_content = universal_adapter.transform(skill)
                            show_diff(Path(result["target"]), new_content)
                        else:
                            break
                    if choice == "skip":
                        continue
                    elif choice == "overwrite":
                        result = universal_adapter.copy_skill(skill, force=True)
                    elif choice == "rename":
                        name_to_use = Prompt.ask("    new name")
                        result = universal_adapter.copy_skill(skill, new_name=name_to_use)
            
            u_path = Path(result["target"])
            
            # Agent-specific deployment
            if agent != "universal" and adapter:
                agent_target = adapter.get_target_path(skill, name_to_use)
                if agent_target.exists() and not agent_target.is_symlink():
                    if agent_target.is_dir():
                        shutil.rmtree(agent_target)
                    else:
                        agent_target.unlink()
                elif agent_target.is_symlink():
                    agent_target.unlink()
                
                if not agent_target.exists():
                    deploy_skill_link(u_path, agent_target)
                    
            console.print(f"  [green]✓[/green] {skill['name']}")
            success_count += 1
            
        except Exception as e:
            console.print(f"  [red]✗[/red] {skill['name']} [dim]{e}[/dim]")
            
    console.print(f"\n[dim]Installed {success_count} skill(s).[/dim]")
