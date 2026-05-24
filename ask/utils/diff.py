"""Utility functions for displaying file diffs."""

import difflib
from pathlib import Path
from rich.console import Console
from rich.syntax import Syntax

console = Console()

def show_diff(target_path: Path, new_content: str):
    """
    Generate and print a unified diff between an existing file and new content.
    """
    if not target_path.exists():
        console.print(f"[dim]File {target_path} does not exist yet. No diff available.[/dim]")
        return

    try:
        old_content = target_path.read_text(encoding="utf-8")
    except Exception as e:
        console.print(f"[red]Error reading existing file to generate diff: {e}[/red]")
        return

    old_lines = old_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)

    diff = list(difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=f"a/{target_path.name}",
        tofile=f"b/{target_path.name}",
        n=3
    ))

    if not diff:
        console.print("[dim]No differences found.[/dim]")
        return

    diff_text = "".join(diff)
    syntax = Syntax(diff_text, "diff", theme="ansi_dark", background_color="default")
    
    console.print()
    console.print(syntax)
    console.print()
