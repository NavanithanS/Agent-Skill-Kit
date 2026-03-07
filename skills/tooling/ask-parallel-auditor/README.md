# ask-parallel-auditor

An orchestrator skill designed to bypass single-agent context limits by chunking repositories and spawning parallel subagents to conduct massive audits.

## Purpose

When executing a repository-wide security scan, architectural audit, or massive refactor, a single AI agent will quickly blow out its context window if it tries to read hundreds of files sequentially.

`ask-parallel-auditor` implements the **Hierarchical Multi-Agent System (HMAS)** pattern. It acts as the Strategy Layer Orchestrator. It does not read the files itself. Instead, it chunks the repository and spawns multiple, isolated subagents (like `ask-owasp-security-review`) operating in parallel across isolated Git worktrees.

## Usage

You invoke this skill when you need a comprehensive scan of a large project.

1. Tell the agent to "Run a parallel audit on the `src/` directory".
2. The orchestrator chunk the `src/` directory.
3. The orchestrator spawns background bash/python scripts to kick off identical subagents assigned to different chunks.
4. The orchestrator waits for the subagents to return their JSON/Markdown findings.
5. The orchestrator merges the results into a massive `PARALLEL_AUDIT_REPORT.md`.

## Features

- **Chunking Logic**: Groups files logically (by directory or by size) before delegation.
- **Git Worktree Isolation**: Ensures subagents operate in isolated physical directories so they don't corrupt the main contextual workspace or conflict over file locks.
- **Subagent Routing**: Delegates to specialized subagents for the actual labor.
- **Result Aggregation**: Compiles massive subagent outputs into a unified report.

## Examples

### Before (Single Agent Failure)
The agent opens 80 files sequentially, forgets its core instructions around file 40, hallucinates code, and crashes with a token exhaustion error.

### After (Parallel Orchestration)
The orchestrator splits the 80 files into 4 chunks. It spawns 4 background workers. 30 seconds later, it receives 4 JSON reports and synthesizes them for you perfectly.

## Best Practices

- Make sure subagents being spawned are highly constrained (e.g., `disallowedTools: Write, Edit`) to prevent rogue autonomous destruction.
- Use `ask-context-janitor` on the aggregated results if the final report is still too massive.
