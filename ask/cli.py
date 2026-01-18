"""Main CLI entry point for Agent Skill Kit."""

import click
from rich.console import Console

from ask import __version__
from ask.commands import create, copy, sync, list_skills, add_agent, remove

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="ask")
@click.pass_context
def main(ctx):
    """Agent Skill Kit - Manage AI agent skills.
    
    Create, manage, and distribute reusable skills across multiple AI agents.
    """
    ctx.ensure_object(dict)


# Register commands
main.add_command(create.create)
main.add_command(copy.copy)
main.add_command(sync.sync)
main.add_command(remove.remove)
main.add_command(list_skills.list_cmd, name="list")
main.add_command(add_agent.add_agent)


if __name__ == "__main__":
    main()
