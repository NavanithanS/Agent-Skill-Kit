"""MCP server — exposes the ASK skill library to any MCP-capable agent.

Thin wrapper over `ask.utils.provider`. Read-only by design (*provider, not
installer*): agents discover and pull skill content at runtime and use it
inline. Nothing is written to the user's filesystem, so the server is safe to
expose by default.

Tools:
    list_skills()        -> full catalog (metadata only)
    search_skills(query) -> top lexical matches with relevance scores
    get_skill(name)      -> a skill's full instruction body for inline use

The `mcp` SDK is an optional dependency (`pip install "agent-skill-kit[mcp]"`).
"""

from __future__ import annotations

from typing import List, Dict, Optional

from ask.utils.provider import (
    list_skills_payload,
    search_skills_payload,
    get_skill_payload,
)

# Single source of truth for the tool surface, importable WITHOUT the optional
# `mcp` dependency so `ask mcp tools` can describe the server offline. Keep this
# in sync with the @server.tool() functions in build_server().
TOOL_SPECS = [
    {"name": "list_skills", "args": [], "summary": "Full skill catalog (metadata only)."},
    {"name": "search_skills", "args": ["query", "limit=5"], "summary": "Top lexical matches with scores."},
    {"name": "get_skill", "args": ["name"], "summary": "A skill's full instruction body."},
]


def build_server(name: str = "agent-skill-kit"):
    """Construct and return a configured FastMCP server.

    Raises a clear ImportError if the optional `mcp` dependency is missing.
    """
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover - exercised via the CLI guard
        raise ImportError(
            "The MCP server needs the optional `mcp` dependency. "
            'Install it with: pip install "agent-skill-kit[mcp]"'
        ) from exc

    server = FastMCP(name)

    @server.tool()
    def list_skills() -> List[Dict]:
        """List every available skill (name, description, category, triggers)."""
        return list_skills_payload()

    @server.tool()
    def search_skills(query: str, limit: int = 5) -> List[Dict]:
        """Find skills matching a free-text need, ranked by relevance.

        Use this when you realise mid-task you need a capability — e.g.
        "scaffold a fastapi service" or "review code for security issues".
        """
        return search_skills_payload(query, limit=limit)

    @server.tool()
    def get_skill(name: str) -> Optional[Dict]:
        """Fetch a skill's full instruction body so you can apply it inline.

        Returns null if no skill matches `name`; call search_skills first if
        you are unsure of the exact name.
        """
        return get_skill_payload(name)

    return server


def serve(transport: str = "stdio") -> None:
    """Run the MCP server (blocking). Defaults to stdio transport."""
    build_server().run(transport=transport)
