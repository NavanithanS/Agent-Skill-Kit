# Concept: MCP Server (`ask mcp serve`)

Exposes the ASK skill library to any MCP-capable agent so it can **discover and
pull skills at runtime** — turning ASK from a build-time deploy tool into a live
capability backbone. An agent that realises mid-task it needs a capability can
search for it, fetch the instruction body, and use it inline.

## Philosophy: provider, not installer

The server is **read-only**. It never writes to the user's filesystem. Agents
receive skill content and use it ephemerally. This makes it safe to expose by
default and sidesteps conflict/backup concerns. (Persistent installation remains
the job of `ask copy` / `ask install`.)

## Tools exposed

| Tool | Args | Returns |
|------|------|---------|
| `list_skills` | — | Full catalog, metadata only (no bodies) |
| `search_skills` | `query`, `limit=5` | Top lexical matches with relevance scores |
| `get_skill` | `name` | A skill's full instruction body for inline use |

`search_skills` ranks using the **same TF-IDF index as `ask test`**
(`ask/utils/eval/trigger_scorer.build_index`), so search relevance and the
trigger audit agree on what each skill is "about".

> **Limitation (v1):** discovery is **lexical**, not semantic. A query phrased
> with different vocabulary than a skill's description may not surface it
> ("make my schema changes safe" vs `ask-db-migration-assistant`). Embedding-
> based semantic search is future work — the same line the eval harness draws
> between its Layer 1 lexical proxy and Layer 2 model-based accuracy.

## Architecture (testable seam)

- `ask/utils/provider.py` — pure functions (`list_skills_payload`,
  `search_skills_payload`, `get_skill_payload`). **No MCP dependency**, fully
  unit-tested (`tests/test_provider.py`).
- `ask/mcp_server.py` — thin FastMCP wrapper; `build_server()` registers the
  three tools, `serve(transport)` runs it. The `mcp` SDK is an **optional
  dependency** (`pip install "agent-skill-kit[mcp]"`); a missing import raises a
  clear install hint.
- `ask/commands/mcp_cmd.py` — `ask mcp serve` (run), `ask mcp tools` (inspect),
  `ask mcp probe <query>` (dry-run search without a server).

## Client config

```json
{
  "mcpServers": {
    "agent-skill-kit": { "command": "ask", "args": ["mcp", "serve"] }
  }
}
```

## Relationship to the eval harness

Both features lean on the same routing index — Layer 1 of [the eval
harness](eval-harness.md) scores `should_fire` prompts against it; the MCP
server's `search_skills` ranks live queries against it. Hardening that index
improves both at once.
