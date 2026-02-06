"""Copy command - Copy skills to agent directories."""

import click
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from ask.utils.skill_registry import get_skill, get_all_skills
from ask.utils.filesystem import get_adapter
from ask.utils.agent_registry import get_available_agents, get_agent_scopes

console = Console()


def prompt_skill_selection():
    """Interactive skill selection with numbered menu.
    
    Returns:
        tuple: (selected_skills, is_all_flag) - List of skills and whether 'all' was selected
    """
    all_skills = get_all_skills()
    
    if not all_skills:
        console.print("[red]❌ No skills found in the skill library[/red]")
        raise click.Abort()
    
    # Display header
    console.print("\n[bold cyan]📚 Available Skills[/bold cyan]\n")
    
    # Build table
    table = Table(show_header=True, header_style="bold", show_lines=True)
    table.add_column("#", style="dim", width=4)
    table.add_column("Name", style="cyan")
    table.add_column("Description")
    table.add_column("Category", style="magenta")
    
    for idx, skill in enumerate(all_skills, 1):
        description = skill.get("description", "")
        # Show up to ~100 chars (approx 2 lines)
        display_desc = description[:100] + "..." if len(description) > 100 else description
        table.add_row(
            str(idx),
            skill.get("name", ""),
            display_desc,
            skill.get("category", "")
        )
    
    console.print(table)
    console.print()
    
    # Prompt for selection
    console.print("[bold]Choose a skill:[/bold]")
    console.print("  [dim]0[/dim] Cancel")
    console.print("  [green]1-{}[/green] Select skill by number".format(len(all_skills)))
    console.print("  [yellow]all[/yellow] Copy all skills")
    console.print()
    
    while True:
        choice = Prompt.ask("Enter choice", default="0")
        
        if choice == "0":
            console.print("[yellow]Cancelled.[/yellow]")
            raise click.Abort()
        
        if choice.lower() == "all":
            return all_skills, True
        
        # Try to parse as number
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(all_skills):
                selected_skill = all_skills[choice_num - 1]
                return [selected_skill], False
            else:
                console.print(f"[red]Invalid choice. Please enter 0-{len(all_skills)} or 'all'[/red]")
        except ValueError:
            console.print(f"[red]Invalid input. Please enter a number, 'all', or '0' to cancel[/red]")


def prompt_agent_selection(skills):
    """Interactive agent selection based on skill compatibility.
    
    Args:
        skills: List of selected skills
        
    Returns:
        str: Selected agent name
    """
    available_agents = get_available_agents()
    
    if not available_agents:
        console.print("[red]❌ No agents available[/red]")
        raise click.Abort()
    
    # Determine compatible agents
    if len(skills) == 1:
        # Single skill - show compatibility
        skill_agents = set(skills[0].get("agents", []))
        compatible_agents = [agent for agent in available_agents if agent in skill_agents]
        
        console.print(f"\n[bold cyan]🤖 Select Agent for '{skills[0]['name']}'[/bold cyan]\n")
    else:
        # Multiple skills - show all agents
        compatible_agents = available_agents
        console.print(f"\n[bold cyan]🤖 Select Target Agent ({len(skills)} skills)[/bold cyan]\n")
    
    # Display table
    table = Table(show_header=True, header_style="bold", show_lines=True)
    table.add_column("#", style="dim", width=4)
    table.add_column("Agent", style="cyan")
    table.add_column("Compatible", style="green")
    
    for idx, agent in enumerate(available_agents, 1):
        if len(skills) == 1:
            is_compatible = agent in compatible_agents
            compat_display = "[green]✓[/green]" if is_compatible else "[dim]✗[/dim]"
        else:
            # For "all" skills, show count of compatible skills
            compat_count = sum(1 for s in skills if agent in s.get("agents", []))
            compat_display = f"[green]{compat_count}/{len(skills)}[/green]" if compat_count > 0 else "[dim]0/{len(skills)}[/dim]"
        
        table.add_row(str(idx), agent, compat_display)
    
    console.print(table)
    console.print()
    
    # Prompt for selection
    console.print("[bold]Choose target agent:[/bold]")
    console.print("  [dim]0[/dim] Cancel")
    console.print(f"  [green]1-{len(available_agents)}[/green] Select agent by number")
    console.print()
    
    while True:
        choice = Prompt.ask("Enter choice", default="0")
        
        if choice == "0":
            console.print("[yellow]Cancelled.[/yellow]")
            raise click.Abort()
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(available_agents):
                selected_agent = available_agents[choice_num - 1]
                
                # Warn if incompatible (for single skill)
                if len(skills) == 1 and selected_agent not in compatible_agents:
                    console.print(f"[yellow]⚠️  '{skills[0]['name']}' doesn't list '{selected_agent}' as supported.[/yellow]")
                    if not click.confirm("Copy anyway?", default=False):
                        continue
                
                return selected_agent
            else:
                console.print(f"[red]Invalid choice. Please enter 0-{len(available_agents)}[/red]")
        except ValueError:
            console.print("[red]Invalid input. Please enter a number or '0' to cancel[/red]")


@click.command()
@click.argument("agent", required=False, type=click.Choice(get_available_agents(), case_sensitive=False))
@click.option("--skill", "-s", "skill_name", help="Specific skill to copy")
@click.option("--all", "-a", "copy_all", is_flag=True, help="Copy all compatible skills")
def copy(agent: str, skill_name: str, copy_all: bool):
    """Copy skills to an agent's directory.
    
    Run without arguments for interactive mode, or specify agent + skill/--all.
    
    Shows preview of both local and global paths, then asks which to use.
    Safe Copy: Never overwrites. Prompts for new name on conflict.
    
    Examples:
    
        ask copy
        
        ask copy codex --skill python-refactor
        
        ask copy gemini --skill my-skill
        
        ask copy claude --all
    """
    # Interactive mode: no arguments provided
    if not agent and not skill_name and not copy_all:
        console.print("[bold magenta]🚀 Interactive Copy Wizard[/bold magenta]")
        
        # Step 1: Select skill(s)
        skills, copy_all = prompt_skill_selection()
        
        # Step 2: Select agent
        agent = prompt_agent_selection(skills)
        
        # Continue to Step 3 (scope selection) below
    
    # Non-interactive mode: validate arguments
    else:
        if not agent:
            console.print("[red]❌ AGENT argument required when using --skill or --all flags[/red]")
            console.print("[dim]Tip: Run 'ask copy' with no arguments for interactive mode[/dim]")
            raise click.Abort()
        
        if not skill_name and not copy_all:
            console.print("[red]❌ Specify --skill <name> or --all[/red]")
            raise click.Abort()
        
        # Get skills to copy
        if copy_all:
            skills = [s for s in get_all_skills() if agent in s.get("agents", [])]
            if not skills:
                console.print(f"[yellow]No skills found compatible with {agent}[/yellow]")
                return
        else:
            skill = get_skill(skill_name)
            if not skill:
                console.print(f"[red]❌ Skill not found: {skill_name}[/red]")
                raise click.Abort()
            
            if agent not in skill.get("agents", []):
                console.print(f"[yellow]⚠️  Skill '{skill_name}' doesn't list '{agent}' as a supported agent.[/yellow]")
                if not click.confirm("Copy anyway?"):
                    raise click.Abort()
            
            skills = [skill]
    
    # Get supported scopes for this agent
    scopes = get_agent_scopes().get(agent, {"local": True, "global": True})
    
    # Show dry run preview for available options
    console.print(f"\n[bold]📦 Preview: Copying {len(skills)} skill(s) to {agent}[/bold]\n")
    
    # Build preview table
    table = Table(show_header=True, header_style="bold", show_lines=True)
    table.add_column("Skill")
    
    if scopes["local"]:
        table.add_column("Local (project)", style="cyan")
    if scopes["global"]:
        table.add_column("Global (user)", style="green")
    
    for skill in skills:
        row = [skill["name"]]
        
        if scopes["local"]:
            adapter = get_adapter(agent, use_global=False)
            target = adapter.get_target_path(skill)
            exists = target.exists()
            status = f"[yellow](exists)[/yellow]" if exists else ""
            row.append(f"{target} {status}")
        
        if scopes["global"]:
            adapter = get_adapter(agent, use_global=True)
            target = adapter.get_target_path(skill)
            exists = target.exists()
            status = f"[yellow](exists)[/yellow]" if exists else ""
            row.append(f"{target} {status}")
        
        table.add_row(*row)
    
    console.print(table)
    console.print()
    
    # Ask user to choose scope with numbered options
    console.print("[bold]Choose destination:[/bold]")
    console.print("  [dim]0[/dim] Cancel")
    if scopes["global"]:
        console.print("  [green]1[/green] Global (user home directory)")
    if scopes["local"]:
        console.print("  [cyan]2[/cyan] Local (project directory)")
    
    # Build valid choices
    valid_choices = ["0"]
    if scopes["global"]:
        valid_choices.append("1")
    if scopes["local"]:
        valid_choices.append("2")
    
    default = "2" if scopes["local"] else "1"
    
    choice_num = Prompt.ask(
        "Enter choice",
        choices=valid_choices,
        default=default
    )
    
    # Map number to action
    if choice_num == "0":
        console.print("[yellow]Cancelled.[/yellow]")
        raise click.Abort()
    elif choice_num == "1":
        use_global = True
        scope_name = "global"
    else:  # "2"
        use_global = False
        scope_name = "local"
    
    # Get adapter for chosen scope
    adapter = get_adapter(agent, use_global=use_global)
    
    # Copy skills
    console.print(f"\n[bold]Copying to {scope_name}...[/bold]\n")
    
    success_count = 0
    skip_count = 0
    
    for skill in skills:
        try:
            result = adapter.copy_skill(skill)
            
            if result["status"] == "copied":
                console.print(f"  [green]✓[/green] {skill['name']} → {result['target']}")
                success_count += 1
            elif result["status"] == "conflict":
                # Prompt user for new name
                console.print(f"  [yellow]⚠️  '{skill['name']}' already exists[/yellow]")
                
                new_name = Prompt.ask(
                    "    Enter new name (or 'skip')",
                    default="skip"
                )
                
                if new_name.lower() == "skip":
                    console.print(f"  [yellow]○[/yellow] {skill['name']} skipped")
                    skip_count += 1
                else:
                    # Copy with new name
                    result = adapter.copy_skill(skill, new_name=new_name)
                    if result["status"] == "copied":
                        console.print(f"  [green]✓[/green] {skill['name']} → {result['target']}")
                        success_count += 1
                    else:
                        console.print(f"  [red]✗[/red] Failed: {result.get('error', 'Unknown')}")
                        
        except Exception as e:
            console.print(f"  [red]✗[/red] {skill['name']}: {e}")
    
    # Summary
    console.print()
    console.print(f"[green]Done![/green] {success_count} copied, {skip_count} skipped.")
    
    if success_count > 0:
        console.print(f"\n[bold yellow]💡 Tip:[/bold yellow] Keep these skills up to date by running [cyan]ask update[/cyan] periodically.")
