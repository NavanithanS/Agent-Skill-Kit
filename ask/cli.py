"""Main CLI entry point for Agent Skill Kit."""

import click
from rich.console import Console

from ask import __version__
from ask.commands import create, copy, sync, update, list_skills, add_agent, remove, validate, skill
from ask.utils.logging import setup_logging
from ask.utils.config import load_config

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="ask")
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def main(ctx, verbose):
    """Agent Skill Kit - Manage AI agent skills.
    
    Create, manage, and distribute reusable skills across multiple AI agents.
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['config'] = load_config()
    setup_logging(verbose)


# Register commands
main.add_command(create.create)
main.add_command(copy.copy)
main.add_command(sync.sync)
main.add_command(update.update)
main.add_command(remove.remove)
main.add_command(validate.validate)
main.add_command(list_skills.list_cmd, name="list")
main.add_command(add_agent.add_agent)
main.add_command(skill.skill)


if __name__ == "__main__":
    main()
