"""Agent Skill Kit - CLI toolkit for managing AI agent skills."""

from importlib.metadata import version, PackageNotFoundError

try:
    # Read the installed distribution's version rather than hardcoding it, so
    # `ask --version` can never drift from pyproject.toml.
    __version__ = version("agent-skill-kit")
except PackageNotFoundError:
    # Running from a source checkout without an install.
    __version__ = "unknown"

__author__ = "Navanithan S"
