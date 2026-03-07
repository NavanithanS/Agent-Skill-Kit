---
name: ask-parallel-auditor
description: Orchestrator skill that splits a target repository into chunks and runs multiple audit subagents in parallel to bypass context limits.
---

# ask-parallel-auditor

An orchestrator skill designed to bypass single-agent context limits by chunking repositories and spawning parallel subagents to conduct massive audits.

## Purpose

When executing a repository-wide security scan, architectural audit, or massive refactor, a single AI agent will quickly blow out its context window if it tries to read hundreds of files sequentially.

`ask-parallel-auditor` implements the **Hierarchical Multi-Agent System (HMAS)** pattern. It acts as the Strategy Layer Orchestrator. It does not read the files itself. Instead, it chunks the repository and spawns multiple, isolated subagents (like `ask-owasp-security-review`).

<critical_constraints>
❌ STRICTLY NO attempting to audit the files yourself sequentially. Your context window will fail.
❌ STRICTLY NO modifying source code or logic.
✅ MUST explicitly chunk the target files into logical groupings.
✅ MUST delegate the auditing task to parallel background workers/subagents.
✅ MUST aggregate the structural output from the subagents into a unified `PARALLEL_AUDIT_REPORT.md`.
</critical_constraints>

<workflow>
1. **Analyze target**: List the target files and directories.
2. **Chunking**: Group files into 5-10 file chunks to prevent subagent context blowout.
3. **Execution**: Generate shell commands to spawn specialized subagents (e.g., `ask-owasp-security-review`) on the distinct chunks.
4. **Aggregation**: Wait for output JSONs, concatenate, and synthesize the `PARALLEL_AUDIT_REPORT.md`.
</workflow>

## Usage

You invoke this skill when you need a comprehensive scan of a large project.

1. Tell the agent to "Run a parallel audit on the `src/` directory".
2. The orchestrator chunk the `src/` directory.
3. The orchestrator spawns background bash/python scripts to kick off identical subagents assigned to different chunks.
4. The orchestrator waits for the subagents to return their JSON/Markdown findings.
5. The orchestrator merges the results.

## Examples

### After (Parallel Orchestration)
The orchestrator splits the 80 files into 4 chunks. It spawns 4 background workers. 30 seconds later, it receives 4 JSON reports and synthesizes them for you perfectly.

## Best Practices

- Make sure subagents being spawned are highly constrained (e.g., `disallowedTools: Write, Edit`) to prevent rogue autonomous destruction.
- Use `ask-context-janitor` on the aggregated results if the final report is still too massive.
