---
title: Wiki Init
description: Scaffolds the LLM Wiki pattern into any project — a persistent, compounding knowledge base maintained by AI agents.
---

# Wiki Init

A skill that scaffolds the LLM Wiki pattern into any project — a persistent, compounding knowledge base that AI agents build and maintain themselves.

## Purpose

Agents start every session with no memory of the last one, so the same context gets rediscovered repeatedly: why a module is structured a certain way, which approach was already tried and rejected, what a bug actually turned out to be. The LLM Wiki pattern fixes this by giving the project a `wiki/` directory that agents read before making decisions and update after learning something.

## When to Use

Trigger this skill when the user:

- Wants agents to retain context across sessions
- Says "set up a wiki", "add a knowledge base", or "make the agent remember"
- Is onboarding a project where architectural rationale lives only in people's heads
- Keeps re-explaining the same background to an agent

## What It Creates

```
wiki/
├── index.md        # Entry point — agents read this first
├── log.md          # Append-only record of what was learned and when
├── architecture/   # How the system is put together, and why
├── decisions/      # Choices made, alternatives rejected, rationale
└── concepts/       # Domain terms and project-specific ideas
```

It also adds the instruction block that tells agents to **read `wiki/index.md` before architectural decisions** and to **update the relevant page plus `wiki/log.md`** whenever they learn something durable.

## Why It Compounds

The value is in the write path, not the read path. A wiki that agents only read goes stale within weeks. The pattern works because updating it is part of the agent's normal workflow, so the knowledge base grows as a side effect of doing the work rather than as a separate documentation chore.

## Install

```bash
ask copy claude --skill ask-wiki-init
```

Supported agents: Claude Code, Codex, Gemini CLI, Cursor, Antigravity.

## Related

- [`ask-project-memory`](../../planning/ask-project-memory/) — records architectural decisions and stack choices
- [`ask-adr-logger`](../../planning/ask-adr-logger/) — writes formal Architectural Decision Records
