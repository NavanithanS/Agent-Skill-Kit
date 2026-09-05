---
title: Hold Code — Agent Skill Kit
description: Planning-mode lock that prevents code generation until the user explicitly approves implementation.
---

# Hold Code

A planning-mode lock that prevents an agent from generating code until you explicitly approve the design.

## Purpose

Coding agents tend to jump straight to implementation, which wastes a turn when the design is still unsettled and makes it harder to change direction afterwards. This skill enforces a hard gate: the agent may research, ask questions, and propose a design, but it must not write or edit code until you say so.

## When to Use

Trigger this skill when the user:

- Says "hold code", "don't code yet", "planning only", or "design phase only"
- Wants to explore an approach before committing to it
- Is reviewing architecture, trade-offs, or requirements
- Has been burned by an agent implementing the wrong thing quickly

## Behaviour

While the lock is active the agent **may**:

- Read files, search the codebase, and inspect dependencies
- Ask clarifying questions
- Propose designs, trade-offs, and implementation plans
- Sketch pseudocode or interface shapes *for discussion*

While the lock is active the agent **must not**:

- Create, edit, or delete source files
- Run commands that mutate the working tree
- Present a plan and then implement it in the same turn

## Releasing the Lock

The lock lifts only on an explicit approval from you — for example "approved", "go ahead", or "implement it". Ambiguous encouragement ("looks good") is deliberately not enough, because that is the phrase most likely to be said while still thinking out loud.

## Install

```bash
ask copy claude --skill ask-hold-code
```

Supported agents: Claude Code, Codex, Gemini CLI, Cursor, Antigravity.

## Related

- [`ask-brainstorm`](../ask-brainstorm/) — explores intent and requirements before implementation
- [`ask-solution-architect`](../ask-solution-architect/) — structured multi-perspective ideation
