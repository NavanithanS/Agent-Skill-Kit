"""Skill evaluation harness command (`ask test`).

Layer 1 — `--triggers` (default): an offline, dependency-free lexical
    collision audit. Flags skills whose descriptions/triggers compete for the
    same prompts. CI-friendly, no API key.

Layer 2 — `--behavior` (planned): runs each skill against a live model with an
    LLM-as-judge for real trigger accuracy and output correctness.
"""

import click
from rich.console import Console
from rich.table import Table

from ask.utils.skill_registry import get_all_skills
from ask.utils.eval import load_evals, run_trigger_audit
from ask.utils.eval.trigger_scorer import DEFAULT_COLLISION_MARGIN

console = Console()


def _verdict(result) -> str:
    if not result.is_hit:
        return "[red]✗ miss[/red]"
    if result.has_collision:
        return "[yellow]⚠ collision[/yellow]"
    return "[green]✓ clear[/green]"


def _run_trigger_audit(skill_name, margin, as_json):
    skills = get_all_skills()
    if skill_name:
        skills_with_evals = [s for s in skills if s.get("name") == skill_name]
        if not skills_with_evals:
            console.print(f"[red]Error:[/red] skill not found: {skill_name}")
            raise SystemExit(1)
        # Score against the WHOLE library so collisions are detected, but only
        # report prompts owned by the requested skill.
        report = run_trigger_audit(skills, margin=margin)
        report.results = [r for r in report.results if r.skill == skill_name]
    else:
        report = run_trigger_audit(skills, margin=margin)

    # A tally of un-audited skills is only meaningful for a whole-library run;
    # in single-skill mode it would just count unrelated skills as noise.
    if skill_name:
        uncovered = []
    else:
        covered = {r.skill for r in report.results}
        uncovered = [
            s["name"]
            for s in skills
            if s.get("name") and s["name"] not in covered and not load_evals(s)
        ]

    if as_json:
        import json

        payload = {
            "kind": "trigger_audit_lexical_prescreen",
            "margin": report.margin,
            "total_prompts": report.total_prompts,
            "clean": len(report.clean),
            "contested": len(report.contested),
            "misses": len(report.misses),
            "collisions": len(report.collisions),
            "uncovered_skills": uncovered,
            "results": [
                {
                    "skill": r.skill,
                    "prompt": r.prompt,
                    "target_score": round(r.target_score, 4),
                    "top_skill": r.top_skill,
                    "top_score": round(r.top_score, 4),
                    "verdict": "miss"
                    if not r.is_hit
                    else ("collision" if r.has_collision else "clear"),
                    "collisions": [
                        {"skill": c, "score": round(s, 4)} for c, s in r.collisions
                    ],
                }
                for r in report.results
            ],
            "collision_pairs": [
                {"skills": list(pair), "count": count}
                for pair, count in sorted(
                    report.collision_pairs().items(), key=lambda kv: -kv[1]
                )
            ],
        }
        console.print(json.dumps(payload, indent=2))
        return report

    if report.total_prompts == 0:
        console.print(
            "[yellow]No evals found.[/yellow] Add a "
            "[cyan]tests/evals.yaml[/cyan] with a [cyan]should_fire[/cyan] list "
            "to a skill, then re-run."
        )
        return report

    console.print("[bold]Trigger Audit[/bold] [dim](Layer 1)[/dim]\n")
    console.print(
        "[dim]Lexical pre-screen (TF-IDF) — flags skills competing for the same "
        "prompts.\nThis is a vocabulary proxy, not how a real agent routes. "
        "Run [cyan]ask test --behavior[/cyan] for live trigger accuracy.[/dim]\n"
    )

    table = Table(show_header=True, header_style="bold", box=None)
    table.add_column("Skill", style="cyan", width=28)
    table.add_column("Prompt", width=42, overflow="fold")
    table.add_column("Top match", width=24)
    table.add_column("Verdict", width=12)

    for r in report.results:
        if r.is_hit:
            top_cell = f"[green]{r.top_skill}[/green] {r.top_score:.2f}"
        else:
            top_cell = f"[red]{r.top_skill}[/red] {r.top_score:.2f}"
        table.add_row(r.skill, r.prompt, top_cell, _verdict(r))

    console.print(table)
    console.print()

    pairs = report.collision_pairs()
    if pairs:
        console.print("[bold yellow]Collision pairs[/bold yellow] [dim](competing skills)[/dim]")
        for (a, b), count in sorted(pairs.items(), key=lambda kv: -kv[1]):
            console.print(f"  [yellow]⚠[/yellow] {a} [dim]↔[/dim] {b}  [dim]×{count}[/dim]")
        console.print()

    console.print(
        f"[dim]{report.total_prompts} prompts · "
        f"[green]{len(report.clean)} clear[/green]  "
        f"[yellow]{len(report.contested)} contested[/yellow]  "
        f"[red]{len(report.misses)} miss[/red][/dim]"
    )
    if uncovered:
        console.print(
            f"[dim]{len(uncovered)} skills have no evals.yaml "
            f"(not audited).[/dim]"
        )

    return report


@click.command(name="test")
@click.argument("skill_name", required=False)
@click.option(
    "--triggers",
    "mode_triggers",
    is_flag=True,
    help="Offline lexical collision audit (default).",
)
@click.option(
    "--behavior",
    "mode_behavior",
    is_flag=True,
    help="Live-model behavioral eval (Layer 2 — not yet implemented).",
)
@click.option(
    "--margin",
    type=float,
    default=DEFAULT_COLLISION_MARGIN,
    show_default=True,
    help="Cosine margin within which a competing skill counts as a collision.",
)
@click.option("--json", "as_json", is_flag=True, help="Emit machine-readable JSON.")
@click.option(
    "--strict",
    is_flag=True,
    help="Exit non-zero if any collision or miss is found (for CI).",
)
def test(skill_name, mode_triggers, mode_behavior, margin, as_json, strict):
    """
    Evaluate skills.

    By default runs the offline trigger/collision audit: a TF-IDF lexical
    pre-screen that flags skills whose descriptions compete for the same
    prompts. Define expected prompts in each skill's tests/evals.yaml:

    \b
        should_fire:
          - "a paraphrased user prompt this skill should own"

    Examples:

    \b
        ask test                       # audit the whole library
        ask test ask-laravel-architect # audit one skill
        ask test --strict              # fail CI on collisions/misses
        ask test --json                # machine-readable output
    """
    if mode_behavior:
        console.print(
            "[yellow]`ask test --behavior` is Layer 2 and not yet implemented.[/yellow]\n"
            "[dim]It will run each skill against a live model with an LLM-as-judge.\n"
            "For now, use the offline trigger audit: [cyan]ask test --triggers[/cyan].[/dim]"
        )
        raise SystemExit(2)

    report = _run_trigger_audit(skill_name, margin, as_json)

    if strict and (report.collisions or report.misses):
        raise SystemExit(1)
