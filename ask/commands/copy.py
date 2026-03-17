"""Copy command - Copy skills to agent directories."""

import click
import json
import shutil
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from ask.utils.skill_registry import get_skill, get_all_skills, resolve_dependencies
from ask.utils.filesystem import get_adapter, get_safe_cwd, deploy_skill_link
from ask.utils.agent_registry import get_available_agents, get_agent_scopes

console = Console()

# Stack name → skill names that are relevant for that stack
STACK_SKILLS = {
    "laravel":  ["ask-laravel-architect", "ask-laravel-mechanic", "ask-vue-architect"],
    "vue":      ["ask-vue-architect", "ask-vue-mechanic"],
    "nextjs":   ["ask-nextjs-architect", "ask-shadcn-architect"],
    "react":    ["ask-shadcn-architect"],
    "flutter":  ["ask-flutter-architect", "ask-flutter-mechanic"],
    "fastapi":  ["ask-fastapi-architect"],
}


def _detect_stacks(cwd: Path) -> list:
    """Detect project stacks from filesystem signals in cwd."""
    stacks = []

    # PHP / Laravel
    composer = cwd / "composer.json"
    if composer.exists():
        try:
            data = json.loads(composer.read_text(encoding="utf-8"))
            deps = {**data.get("require", {}), **data.get("require-dev", {})}
            if any("laravel" in k for k in deps):
                stacks.append("laravel")
        except Exception:
            pass

    # JS / TS frameworks
    package = cwd / "package.json"
    if package.exists():
        try:
            data = json.loads(package.read_text(encoding="utf-8"))
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            if "next" in deps:
                stacks.append("nextjs")
            elif "vue" in deps:
                stacks.append("vue")
            elif "react" in deps:
                stacks.append("react")
        except Exception:
            pass

    # Flutter / Dart
    if (cwd / "pubspec.yaml").exists():
        stacks.append("flutter")

    # Python / FastAPI
    for fname in ("requirements.txt", "pyproject.toml"):
        fpath = cwd / fname
        if fpath.exists():
            try:
                if "fastapi" in fpath.read_text(encoding="utf-8").lower():
                    stacks.append("fastapi")
                    break
            except Exception:
                pass

    return stacks


def _fuzzy_match_skills(query: str, all_skills: list) -> list:
    """Substring match on skill name and description. Strips ask- prefix before matching."""
    q = query.lower().strip()
    q_bare = q[4:] if q.startswith("ask-") else q

    matches = []
    for s in all_skills:
        name = s.get("name", "").lower()
        name_bare = name[4:] if name.startswith("ask-") else name
        desc = s.get("description", "").lower()
        if q_bare in name_bare or q in name or q_bare in desc:
            matches.append(s)
    return matches


def prompt_skill_selection():
    """Interactive skill selection with search/filter and stack-aware suggestions.

    Returns:
        tuple: (selected_skills, is_all_flag) - List of skills and whether 'all' was selected
    """
    all_skills = get_all_skills()

    if not all_skills:
        console.print("[red]Error:[/red] no skills found in the skill library")
        raise click.Abort()

    console.print("\n[bold]Available Skills[/bold]  [dim]interactive[/dim]\n")

    # Feature 4: detect stacks and surface relevant skills
    cwd = get_safe_cwd()
    stacks = _detect_stacks(cwd)
    if stacks:
        suggested_names: list[str] = []
        for stack in stacks:
            suggested_names.extend(STACK_SKILLS.get(stack, []))
        # deduplicate, preserve order
        seen: set[str] = set()
        unique_suggestions = []
        for n in suggested_names:
            if n not in seen:
                seen.add(n)
                unique_suggestions.append(n)
        available_names = {s["name"] for s in all_skills}
        valid_suggestions = [n for n in unique_suggestions if n in available_names]
        if valid_suggestions:
            console.print(f"[dim]Detected: {', '.join(stacks)}[/dim]")
            console.print(f"[dim]Suggested: {', '.join(valid_suggestions)}[/dim]\n")

    # Feature 6: search/filter before rendering the list
    search = Prompt.ask("[dim]Search[/dim] (Enter to list all)", default="").strip()

    if search:
        display_skills = _fuzzy_match_skills(search, all_skills)
        if not display_skills:
            console.print(f"[dim]No matches for '{search}'. Showing all.[/dim]\n")
            display_skills = all_skills
        else:
            console.print(f"[dim]{len(display_skills)} match(es)[/dim]\n")
    else:
        display_skills = all_skills

    # Build table
    table = Table(show_header=True, header_style="bold", show_lines=False)
    table.add_column("#", style="dim", width=4)
    table.add_column("Name", style="cyan")
    table.add_column("Description")
    table.add_column("Category", style="dim")

    for idx, skill in enumerate(display_skills, 1):
        description = skill.get("description", "")
        display_desc = description[:100] + "..." if len(description) > 100 else description
        table.add_row(
            str(idx),
            skill.get("name", ""),
            display_desc,
            skill.get("category", "")
        )

    console.print(table)
    console.print()

    console.print("[dim]0 cancel · 1-{n} select · all copy all[/dim]\n".format(n=len(display_skills)))

    while True:
        choice = Prompt.ask("Skill", default="0")

        if choice == "0":
            console.print("[dim]Cancelled.[/dim]")
            raise click.Abort()

        if choice.lower() == "all":
            return display_skills, True

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(display_skills):
                selected_skill = display_skills[choice_num - 1]
                return [selected_skill], False
            else:
                console.print(f"[red]Enter 0–{len(display_skills)} or all[/red]")
        except ValueError:
            console.print("[red]Enter a number, all, or 0 to cancel[/red]")


def prompt_agent_selection(skills):
    """Interactive agent selection based on skill compatibility.

    Args:
        skills: List of selected skills

    Returns:
        str: Selected agent name
    """
    available_agents = get_available_agents()

    if not available_agents:
        console.print("[red]Error:[/red] no agents available")
        raise click.Abort()

    # Determine compatible agents
    if len(skills) == 1:
        # Single skill - show compatibility
        skill_agents = set(skills[0].get("agents", []))
        compatible_agents = [agent for agent in available_agents if agent == "universal" or agent in skill_agents]

        console.print(f"\n[bold]Select Agent[/bold]  [dim]{skills[0]['name']}[/dim]\n")
    else:
        # Multiple skills - show all agents
        compatible_agents = available_agents
        console.print(f"\n[bold]Select Agent[/bold]  [dim]{len(skills)} skills[/dim]\n")

    # Display table
    table = Table(show_header=True, header_style="bold", show_lines=False)
    table.add_column("#", style="dim", width=4)
    table.add_column("Agent", style="cyan")
    table.add_column("Compatible", style="green")

    for idx, agent in enumerate(available_agents, 1):
        if len(skills) == 1:
            is_compatible = agent in compatible_agents
            compat_display = "[green]✓[/green]" if is_compatible else "[dim]✗[/dim]"
        else:
            # For "all" skills, show count of compatible skills
            if agent == "universal":
                compat_count = len(skills)
            else:
                compat_count = sum(1 for s in skills if agent in s.get("agents", []))

            compat_display = f"[green]{compat_count}/{len(skills)}[/green]" if compat_count > 0 else f"[dim]0/{len(skills)}[/dim]"

        table.add_row(str(idx), agent, compat_display)

    console.print(table)
    console.print()

    console.print("[dim]0 cancel · 1-{n} select[/dim]\n".format(n=len(available_agents)))

    while True:
        choice = Prompt.ask("Agent", default="0")

        if choice == "0":
            console.print("[dim]Cancelled.[/dim]")
            raise click.Abort()

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(available_agents):
                selected_agent = available_agents[choice_num - 1]

                # Warn if incompatible (for single skill)
                if len(skills) == 1 and selected_agent not in compatible_agents:
                    console.print(f"[yellow]Warning:[/yellow] '{skills[0]['name']}' doesn't list '{selected_agent}' as supported.")
                    if not click.confirm("Copy anyway?", default=False):
                        continue

                return selected_agent
            else:
                console.print(f"[red]Enter 0–{len(available_agents)}[/red]")
        except ValueError:
            console.print("[red]Enter a number or 0 to cancel[/red]")


@click.command()
@click.argument("agent", required=False, type=click.Choice(get_available_agents(), case_sensitive=False))
@click.option("--skill", "-s", "skill_name", help="Specific skill to copy")
@click.option("--all", "-a", "copy_all", is_flag=True, help="Copy all compatible skills")
@click.option("--global", "use_global", is_flag=True, default=None, help="Copy to global (user home) location")
@click.option("--local", "use_local", is_flag=True, default=None, help="Copy to local (project) location")
@click.option("--overwrite", "-f", is_flag=True, help="Overwrite existing skill without prompting")
@click.pass_context
def copy(ctx, agent: str, skill_name: str, copy_all: bool, use_global: Optional[bool], use_local: Optional[bool], overwrite: bool):
    """Copy skills to an agent's directory.

    Run without arguments for interactive mode, or specify agent + skill/--all.

    Shows preview of both local and global paths, then asks which to use.
    Safe Copy: Never overwrites. Prompts for new name on conflict.

    Examples:

        ask copy

        ask copy codex --skill python-refactor

        ask copy universal --skill context-janitor --global

        ask copy gemini --skill my-skill --local

        ask copy claude --all
    """
    # Fail fast: mutually exclusive flags
    if use_global and use_local:
        console.print("[red]Error:[/red] --global and --local are mutually exclusive")
        raise click.Abort()

    # Interactive mode: no arguments provided
    if not agent and not skill_name and not copy_all:
        console.print("[bold]Copy[/bold]  [dim]interactive[/dim]")

        # Step 1: Select skill(s)
        skills, copy_all = prompt_skill_selection()

        # Step 2: Select agent
        agent = prompt_agent_selection(skills)

        # Continue to Step 3 (scope selection) below

    # Non-interactive mode: validate arguments
    else:
        # Try to get default agent from config
        if not agent:
            config = ctx.obj.get('config', {})
            agent = config.get('defaults', {}).get('agent')

        if not agent:
            console.print("[red]Error:[/red] AGENT required when using --skill or --all")
            console.print("[dim]Run 'ask copy' with no arguments for interactive mode[/dim]")
            raise click.Abort()

        if not skill_name and not copy_all:
            console.print("[red]Error:[/red] specify --skill <name> or --all")
            raise click.Abort()

        # Get skills to copy
        if copy_all:
            if agent == "universal":
                skills = get_all_skills()
            else:
                skills = [s for s in get_all_skills() if agent in s.get("agents", [])]

            if not skills:
                console.print(f"[dim]No skills found compatible with {agent}[/dim]")
                return
        else:
            skill = get_skill(skill_name)
            if not skill:
                # Feature 2: fuzzy fallback when exact name not found
                matches = _fuzzy_match_skills(skill_name, get_all_skills())
                if not matches:
                    console.print(f"[red]Error:[/red] skill not found: {skill_name}")
                    raise click.Abort()
                elif len(matches) == 1:
                    console.print(f"[dim]Using '{matches[0]['name']}' (matched '{skill_name}')[/dim]")
                    skill = matches[0]
                    skill_name = skill["name"]
                else:
                    console.print(f"[dim]{len(matches)} skills match '{skill_name}':[/dim]")
                    for i, m in enumerate(matches, 1):
                        console.print(f"  [dim]{i}[/dim]  {m['name']}")
                    idx_choice = Prompt.ask("Select", choices=[str(i) for i in range(1, len(matches) + 1)])
                    skill = matches[int(idx_choice) - 1]
                    skill_name = skill["name"]

            if agent != "universal" and agent not in skill.get("agents", []):
                console.print(f"[yellow]Warning:[/yellow] '{skill_name}' doesn't list '{agent}' as a supported agent.")
                if not click.confirm("Copy anyway?"):
                    raise click.Abort()

            # Resolve dependencies
            try:
                # Pre-load skills map for O(1) lookup
                all_skills_list = get_all_skills()
                skill_map = {s["name"]: s for s in all_skills_list}

                skills = resolve_dependencies(skill_name, skill_map=skill_map)

                if len(skills) > 1:
                    deps = [s["name"] for s in skills if s["name"] != skill_name]
                    console.print(f"[dim]+ dependencies: {', '.join(deps)}[/dim]")
            except ValueError as e:
                console.print(f"[red]Error:[/red] {e}")
                raise click.Abort()

    # Get supported scopes for this agent
    scopes = get_agent_scopes().get(agent, {"local": True, "global": True})

    # Guard against degenerate adapter config
    if not scopes["local"] and not scopes["global"]:
        console.print(f"[red]Error:[/red] agent '{agent}' has no supported scopes configured.")
        raise click.Abort()

    # Narrow preview to only the chosen scope when a flag was passed
    show_local = scopes["local"] and not use_global
    show_global = scopes["global"] and not use_local

    # Show dry run preview for available options
    console.print(f"\n[bold]Preview[/bold]  [dim]{len(skills)} skill(s) → {agent}[/dim]\n")

    # Build preview table
    table = Table(show_header=True, header_style="bold", show_lines=False)
    table.add_column("Skill")
    table.add_column("Type", style="dim")
    if show_local:
        table.add_column("Local (project)", style="cyan")
    if show_global:
        table.add_column("Global (user)", style="green")

    # Calculate project root once
    project_root = get_safe_cwd()

    from agents.universal.adapter import UniversalAdapter

    # Cache adapters for preview
    local_adapter = None
    local_universal = None
    if show_local:
        local_adapter = get_adapter(agent, use_global=False, project_root=project_root)
        local_universal = UniversalAdapter(use_global=False, project_root=project_root)

    global_adapter = None
    global_universal = None
    if show_global:
        global_adapter = get_adapter(agent, use_global=True)
        global_universal = UniversalAdapter(use_global=True)

    for skill in skills:
        row = [skill["name"]]

        is_dependency = skill_name and skill["name"] != skill_name and len(skills) > 1
        row.append("Dependency" if is_dependency else "Direct")

        if show_local and local_adapter:
            target = local_adapter.get_target_path(skill)
            exists = target.exists()
            row.append(f"{target} [yellow](exists)[/yellow]" if exists else str(target))

        if show_global and global_adapter:
            target = global_adapter.get_target_path(skill)
            exists = target.exists()
            row.append(f"{target} [yellow](exists)[/yellow]" if exists else str(target))

        table.add_row(*row)

    console.print(table)
    console.print()

    # Resolve scope: flag > auto (single option) > prompt
    if use_global:
        if not scopes["global"]:
            console.print(f"[red]Error:[/red] agent '{agent}' does not support global scope")
            raise click.Abort()
        scope_resolved = True
        scope_name = "global"
    elif use_local:
        if not scopes["local"]:
            console.print(f"[red]Error:[/red] agent '{agent}' does not support local scope")
            raise click.Abort()
        use_global = False
        scope_resolved = True
        scope_name = "local"
    elif scopes["global"] and not scopes["local"]:
        use_global = True
        scope_resolved = True
        scope_name = "global"
    elif scopes["local"] and not scopes["global"]:
        use_global = False
        scope_resolved = True
        scope_name = "local"
    else:
        scope_resolved = False

    if not scope_resolved:
        # Ask user to choose scope with numbered options
        console.print("[bold]Destination[/bold]")
        console.print("  [dim]0[/dim]  cancel")
        if scopes["global"]:
            console.print("  [dim]1[/dim]  global  [dim](user home)[/dim]")
        if scopes["local"]:
            console.print("  [dim]2[/dim]  local   [dim](project)[/dim]")

        valid_choices = ["0"]
        if scopes["global"]:
            valid_choices.append("1")
        if scopes["local"]:
            valid_choices.append("2")

        default = "1" if scopes["global"] else "2"

        choice_num = Prompt.ask(
            "Scope",
            choices=valid_choices,
            default=default
        )

        if choice_num == "0":
            console.print("[dim]Cancelled.[/dim]")
            raise click.Abort()
        elif choice_num == "1":
            use_global = True
            scope_name = "global"
        else:  # "2"
            use_global = False
            scope_name = "local"

    # Select adapter for chosen scope
    adapter = global_adapter if use_global else local_adapter
    universal_adapter = global_universal if use_global else local_universal

    if not universal_adapter:
        universal_adapter = UniversalAdapter(use_global=use_global, project_root=project_root)
    if not adapter and agent != "universal":
        adapter = get_adapter(agent, use_global=use_global, project_root=project_root)

    # Feature 5: upfront conflict scan — decide strategy before copying begins
    conflicts = []
    for s in skills:
        tp = universal_adapter.get_target_path(s)
        if tp and tp.exists():
            conflicts.append(s["name"])

    conflict_strategy = None  # None = ask per skill
    if overwrite:
        conflict_strategy = "overwrite"
    elif conflicts:
        console.print(f"\n[yellow]Warning:[/yellow] {len(conflicts)} skill(s) already installed: {', '.join(conflicts)}")
        console.print("[dim]1 skip all  2 overwrite all  3 ask per skill[/dim]")
        strategy_choice = Prompt.ask("Strategy", choices=["1", "2", "3"], default="1")
        if strategy_choice == "1":
            conflict_strategy = "skip"
        elif strategy_choice == "2":
            conflict_strategy = "overwrite"
        # else conflict_strategy stays None (ask per skill)

    # Copy skills
    console.print(f"\n[dim]Copying to {scope_name}...[/dim]\n")

    success_count = 0
    skip_count = 0
    fail_count = 0

    for skill in skills:
        try:
            name_to_use = skill.get("name")

            # 1. Write to Universal Source of Truth
            result = universal_adapter.copy_skill(skill)

            if result["status"] == "conflict":
                if conflict_strategy == "overwrite":
                    choice = "overwrite"
                elif conflict_strategy == "skip":
                    console.print(f"  [dim]–[/dim] {skill['name']} [dim]skipped[/dim]")
                    skip_count += 1
                    continue
                else:
                    # Per-skill prompt (conflict_strategy is None)
                    console.print(f"  [yellow]–[/yellow] '{skill['name']}' already exists")
                    choice = Prompt.ask(
                        "    use existing / overwrite / rename / skip",
                        choices=["use existing", "overwrite", "rename", "skip"],
                        default="use existing"
                    )

                if choice == "skip":
                    console.print(f"  [dim]–[/dim] {skill['name']} [dim]skipped[/dim]")
                    skip_count += 1
                    continue
                elif choice == "overwrite":
                    result = universal_adapter.copy_skill(skill, force=True)
                    if result["status"] != "copied":
                        console.print(f"  [red]✗[/red] {skill['name']} [dim]overwrite failed: {result.get('error', 'unknown')}[/dim]")
                        fail_count += 1
                        continue
                elif choice == "rename":
                    new_name = Prompt.ask("    new name")
                    name_to_use = new_name
                    result = universal_adapter.copy_skill(skill, new_name=new_name)
                    if result["status"] != "copied":
                        console.print(f"  [red]✗[/red] {skill['name']} [dim]rename failed: {result.get('error', 'unknown')}[/dim]")
                        fail_count += 1
                        continue
                else:  # "use existing"
                    pass

            u_path = Path(result["target"]) # Universal path

            # 2. Deploy to the specific chosen agent (unless it's universal itself)
            deploy_mode = None
            if agent != "universal" and adapter:
                agent_target = adapter.get_target_path(skill, name_to_use)

                # Remove legacy hard-copied file/folder to migrate to link.
                # Also remove stale/broken symlinks — is_symlink() catches
                # broken ones that .exists() misses.
                if agent_target.exists() and not agent_target.is_symlink():
                    if agent_target.is_dir():
                        shutil.rmtree(agent_target)
                    else:
                        agent_target.unlink()
                elif agent_target.is_symlink():
                    agent_target.unlink()

                if not agent_target.exists():
                    deploy_mode = deploy_skill_link(u_path, agent_target)

            # Print success
            if agent == "universal":
                console.print(f"  [green]✓[/green] {skill['name']} [dim]→ {u_path}[/dim]")
            elif deploy_mode == "copy":
                console.print(f"  [green]✓[/green] {skill['name']} → {agent} [dim](copied, symlinks unavailable)[/dim]")
            else:
                console.print(f"  [green]✓[/green] {skill['name']} → {agent}")
            success_count += 1

        except OSError as e:
            console.print(f"  [red]✗[/red] {skill['name']} [dim]{e}[/dim]")
            fail_count += 1

    # Summary
    console.print()
    parts = [f"{success_count} copied"]
    if skip_count:
        parts.append(f"{skip_count} skipped")
    if fail_count:
        parts.append(f"{fail_count} failed")
    console.print("[dim]" + " · ".join(parts) + "[/dim]")

    if success_count > 0:
        console.print("[dim]Tip: run ask update to keep skills current[/dim]")
