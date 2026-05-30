"""Smoke tests for the MCP server wrapper (skipped if `mcp` is not installed)."""

import pytest

mcp = pytest.importorskip("mcp", reason="optional `mcp` dependency not installed")


def test_build_server_registers_three_tools():
    from ask.mcp_server import build_server

    server = build_server()
    # FastMCP exposes registered tools via its tool manager.
    import asyncio

    tools = asyncio.run(server.list_tools())
    names = {t.name for t in tools}
    assert {"list_skills", "search_skills", "get_skill"} <= names


def test_tool_specs_match_registered_tools():
    """The offline TOOL_SPECS (used by `ask mcp tools`) must not drift from the
    actual server tool surface."""
    import asyncio

    from ask.mcp_server import build_server, TOOL_SPECS

    registered = {t.name for t in asyncio.run(build_server().list_tools())}
    documented = {t["name"] for t in TOOL_SPECS}
    assert documented == registered
