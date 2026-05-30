"""`ask mcp` — expose the skill library to MCP-capable agents.

Provider model: read-only tools (list / search / get). Agents pull skills at
runtime and use them inline; nothing is written to disk.
"""

import json

import click
from rich.console import Console

from ask.utils.provider import search_skills_payload

console = Console()


@click.group()
def mcp():
    """Run ASK as an MCP server so agents can discover skills at runtime."""
    pass


@mcp.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio"]),
    default="stdio",
    show_default=True,
    help="Transport to serve on.",
)
def serve(transport):
    """
    Start the MCP server (blocking).

    Point an MCP-capable agent at this command. It exposes three read-only
    tools: list_skills, search_skills, get_skill. No filesystem mutation.

    Example MCP client config:

    \b
        {
          "mcpServers": {
            "agent-skill-kit": { "command": "ask", "args": ["mcp", "serve"] }
          }
        }
    """
    # The `mcp` dependency is imported lazily inside run_server(), so guard the
    # call itself — not just the module import — to surface the install hint.
    from ask.mcp_server import serve as run_server

    try:
        run_server(transport=transport)
    except ImportError as exc:
        from rich.markup import escape

        console.print(f"[red]Error:[/red] {escape(str(exc))}")
        raise SystemExit(1)


@mcp.command(name="tools")
@click.option("--json", "as_json", is_flag=True, help="Emit JSON.")
def tools(as_json):
    """List the tools this server exposes (no server needed — for inspection)."""
    # Imported from the server module (no `mcp` dep required) so there is a
    # single source of truth for the tool surface.
    from ask.mcp_server import TOOL_SPECS as spec

    if as_json:
        console.print(json.dumps(spec, indent=2))
        return
    console.print("[bold]MCP tools[/bold] [dim](provider model — read-only)[/dim]\n")
    for t in spec:
        sig = ", ".join(t["args"])
        console.print(f"  [cyan]{t['name']}[/cyan]([dim]{sig}[/dim])")
        console.print(f"    [dim]{t['summary']}[/dim]")


@mcp.command(name="probe")
@click.argument("query")
@click.option("--limit", default=5, show_default=True)
def probe(query, limit):
    """Dry-run search_skills locally (no server) to preview what an agent sees."""
    results = search_skills_payload(query, limit=limit)
    if not results:
        console.print("[dim]No matches.[/dim]")
        return
    for r in results:
        console.print(
            f"  [cyan]{r['name']}[/cyan]  [dim]{r['score']}[/dim]  "
            f"[dim]{r['description']}[/dim]"
        )
