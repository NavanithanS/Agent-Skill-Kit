"""Skill management commands - lint, profile, compile."""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table

from ask.utils.filesystem import get_skills_dir
from ask.utils.skill_registry import get_all_skills

console = Console()


@click.group()
def skill():
    """Skill management and optimization commands."""
    pass


@skill.command()
@click.option("--strict", is_flag=True, help="Treat warnings as errors")
@click.argument("skill_name", required=False)
def lint(strict: bool, skill_name: str):
    """
    Lint skill files for schema compliance and token limits.
    
    Checks:
    - Token count (≤500 OK, 501-700 warning, >700 error)
    - Required <critical_constraints> block
    - Verbose language patterns
    
    Examples:
        ask skill lint                    # Lint all skills
        ask skill lint ask-fastapi        # Lint specific skill
        ask skill lint --strict           # Fail on warnings
    """
    try:
        from ask.utils.token_analyzer import lint_skill, analyze_skill
    except ImportError:
        console.print("[yellow]⚠️ tiktoken not installed. Run: pip install tiktoken[/yellow]")
        return
    
    skills_dir = get_skills_dir()
    
    if skill_name:
        # Find specific skill
        skill_path = None
        for skill_md in skills_dir.rglob("SKILL.md"):
            if skill_md.parent.name == skill_name:
                skill_path = skill_md
                break
        
        if not skill_path:
            console.print(f"[red]Skill not found: {skill_name}[/red]")
            raise SystemExit(1)
        
        passed, messages = lint_skill(skill_path, strict=strict)
        for msg in messages:
            console.print(msg)
        
        if not passed:
            raise SystemExit(1)
    else:
        # Lint all skills
        console.print("[bold cyan]🔍 Linting all skills...[/bold cyan]\n")
        
        all_passed = True
        total = 0
        failed = 0
        
        for skill_md in sorted(skills_dir.rglob("SKILL.md")):
            total += 1
            passed, messages = lint_skill(skill_md, strict=strict)
            
            if not passed:
                all_passed = False
                failed += 1
                console.print(f"[red]✗ {skill_md.parent.name}[/red]")
                for msg in messages:
                    console.print(f"  {msg}")
            else:
                # Only show passing if verbose or has warnings
                analysis = analyze_skill(skill_md)
                if analysis.get("issues") or analysis.get("status") == "warning":
                    console.print(f"[yellow]⚠ {skill_md.parent.name}[/yellow]")
                    for msg in messages:
                        console.print(f"  {msg}")
        
        console.print(f"\n[bold]Results: {total - failed}/{total} passed[/bold]")
        
        if not all_passed:
            raise SystemExit(1)
        else:
            console.print("[green]✅ All skills passed![/green]")


@skill.command()
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def profile(as_json: bool):
    """
    Generate token usage report for all skills.
    
    Shows token count, status, and distribution across all skills.
    Useful for identifying optimization targets.
    
    Examples:
        ask skill profile
        ask skill profile --json
    """
    try:
        from ask.utils.token_analyzer import generate_report
    except ImportError:
        console.print("[yellow]⚠️ tiktoken not installed. Run: pip install tiktoken[/yellow]")
        return
    
    skills_dir = get_skills_dir()
    
    console.print("[bold cyan]📊 Token Usage Report[/bold cyan]\n")
    
    report, summary = generate_report(skills_dir)
    
    if as_json:
        import json
        console.print(json.dumps(summary, indent=2, default=str))
    else:
        # Rich table output
        table = Table(title="Skill Token Analysis", show_header=True, header_style="bold")
        table.add_column("Category", style="dim", width=10)
        table.add_column("Skill", style="cyan", width=32)
        table.add_column("Tokens", justify="right", width=8)
        table.add_column("Status", width=8)
        
        for r in summary["results"]:
            status_style = {"ok": "green", "warning": "yellow", "error": "red"}[r["status"]]
            status_icon = {"ok": "✅", "warning": "⚠️", "error": "🔴"}[r["status"]]
            table.add_row(
                r["category"],
                r["name"],
                str(r["tokens"]),
                f"[{status_style}]{status_icon}[/{status_style}]"
            )
        
        console.print(table)
        console.print()
        console.print(f"[bold]Total:[/bold] {summary['total_skills']} skills | {summary['total_tokens']} tokens | Avg: {summary['average_tokens']}")
        console.print(f"[green]✅ OK: {summary['ok_count']}[/green] | [yellow]⚠️ Warning: {summary['warning_count']}[/yellow] | [red]🔴 Error: {summary['error_count']}[/red]")


@skill.command()
@click.option("--output", "-o", default="skills/manifest.json", help="Output path")
def compile(output: str):
    """
    Compile skill metadata into manifest.json for routing.
    
    Generates a lightweight JSON file containing skill names,
    descriptions, and triggers for orchestrator routing.
    
    Examples:
        ask skill compile
        ask skill compile -o dist/manifest.json
    """
    import json
    
    skills = get_all_skills()
    
    if not skills:
        console.print("[yellow]No skills found.[/yellow]")
        return
    
    manifest = {
        "version": "2.0.0",
        "generated": __import__("datetime").datetime.now().isoformat(),
        "skills": []
    }
    
    for skill in skills:
        entry = {
            "name": skill.get("name"),
            "description": skill.get("description", ""),
            "category": Path(skill.get("_path", "")).parent.name,
            "triggers": skill.get("triggers", []),
            "path": str(Path(skill.get("_path", "")).relative_to(get_skills_dir())) if skill.get("_path") else None,
        }
        manifest["skills"].append(entry)
    
    # Sort by name
    manifest["skills"].sort(key=lambda x: x["name"])
    
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    console.print(f"[green]✅ Compiled {len(skills)} skills to {output_path}[/green]")
