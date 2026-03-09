"""Agent Skill Kit - CLI toolkit for managing AI agent skills."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = "0.4.2"
except PackageNotFoundError:
    __version__ = "unknown"
__author__ = "Nava"
