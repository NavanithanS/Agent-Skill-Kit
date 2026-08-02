<!-- ASK:wiki-rules:start -->
## LLM Wiki & Knowledge Base Management

A persistent, LLM-maintained knowledge base lives in the `wiki/` directory. This is the single source of truth for architectural context and module guidelines.

**CRITICAL INSTRUCTION FOR ALL AGENTS:** 
You **MUST proactively construct and update the `wiki/`** immediately whenever you introduce new features, database schemas, API integrations, or architectural changes. Do not leave the system in an undocumented state; knowledge MUST be persisted here across operational runs.

### Automatic Retrieval Protocol
To effectively reference this knowledge in future runs and avoid redundant analysis:
1. **Initialize**: Read `wiki/index.md` at the start of complex requests to map out the current structure and available documentation.
2. **Navigate**: Use file tools to access detailed breakdowns under `wiki/architecture/`, `wiki/entities/`, `wiki/frontend/`, and `wiki/modules/`.
3. **Comply**: Read `wiki/SCHEMA.md` to understand formatting rules, update conventions, and query mechanics.
4. **Log**: Update the `wiki/log.md` with a timestamped note after making documented adjustments.

### Key Wiki Files
- `wiki/index.md` — master content catalog with links to every page (start here).
- `wiki/SCHEMA.md` — how to ingest sources, query, update, and lint the wiki.
- `wiki/log.md` — append-only history of wiki operations.
- `wiki/overview.md` — project summary, capabilities, and key numbers.
<!-- ASK:wiki-rules:end -->
