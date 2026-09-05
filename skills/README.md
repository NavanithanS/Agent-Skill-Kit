---
title: "Skill library — 42 agent skills for Claude Code, Codex, Gemini CLI and Cursor"
description: "Browse all 42 Agent Skill Kit skills across coding, planning, tooling. Each installs to Claude Code, Codex, Gemini CLI, Cursor or Antigravity with one command."
---

# Skill library

All 42 skills in [Agent Skill Kit](https://navanithans.github.io/Agent-Skill-Kit/), across 3 categories. Every skill installs to any of 5 agents with a single command:

```bash
ask copy claude --skill <skill-name>
```

Prefer a UI? Use the [interactive command builder](https://navanithans.github.io/Agent-Skill-Kit/docs/).

## Coding (26)

### [ask-bug-finder](coding/ask-bug-finder/)

Best practices for systematic bug hunting and debugging

```bash
ask copy claude --skill ask-bug-finder
```

### [ask-code-reviewer](coding/ask-code-reviewer/)

An AI code reviewer that provides constructive feedback on code changes.

```bash
ask copy claude --skill ask-code-reviewer
```

### [ask-commit-assistance](coding/ask-commit-assistance/)

Assist with code review and staging. NEVER automatically commits.

```bash
ask copy claude --skill ask-commit-assistance
```

### [ask-component-scaffolder](coding/ask-component-scaffolder/)

Standardizes UI component creation by generating a consistent folder structure and files.

```bash
ask copy claude --skill ask-component-scaffolder
```

### [ask-conceptual-integrity-sentinel](coding/ask-conceptual-integrity-sentinel/)

Principal-level engineering agent that audits repositories for architectural drift, bloated abstractions, and "dead code."

```bash
ask copy claude --skill ask-conceptual-integrity-sentinel
```

### [ask-db-migration-assistant](coding/ask-db-migration-assistant/)

Ensures safe database schema updates by requiring migration and rollback scripts before execution.

```bash
ask copy claude --skill ask-db-migration-assistant
```

### [ask-docker-expert](coding/ask-docker-expert/)

Expert guidance on Docker, Docker Compose, and container optimization. Focuses on multi-stage builds and security.

```bash
ask copy claude --skill ask-docker-expert
```

### [ask-effective-llm-coder](coding/ask-effective-llm-coder/)

Guides the agent in effective LLM-assisted coding using best practices for declarative workflows, simplicity, tenacity, and iterative refinement.

```bash
ask copy claude --skill ask-effective-llm-coder
```

### [ask-explaining-code](coding/ask-explaining-code/)

Explains code using analogies, ASCII diagrams, and step-by-step walkthroughs

```bash
ask copy claude --skill ask-explaining-code
```

### [ask-fastapi-architect](coding/ask-fastapi-architect/)

Expert scaffolding for FastAPI projects. Enforces Pydantic V2, Async Database patterns, and Dependency Injection.

```bash
ask copy claude --skill ask-fastapi-architect
```

### [ask-flutter-architect](coding/ask-flutter-architect/)

Senior Flutter skill using FVM. Enforces project-specific standards: Provider, Layer-First Architecture, Stream-based Services, and strict coding conventions.

```bash
ask copy claude --skill ask-flutter-architect
```

### [ask-flutter-mechanic](coding/ask-flutter-mechanic/)

Maintenance skill for Flutter projects using FVM. Handles clean builds, iOS/Android specific fixes, asset generation, and release protocols.

```bash
ask copy claude --skill ask-flutter-mechanic
```

### [ask-impact-sentinel](coding/ask-impact-sentinel/)

Guidelines for impact analysis, breaking change detection, strategic database design, and comprehensive database indexing review.

```bash
ask copy claude --skill ask-impact-sentinel
```

### [ask-laravel-architect](coding/ask-laravel-architect/)

Senior scaffolding skill. Handles SQL vs Mongo (Jenssegers/Official), SoftDeletes, and strict API standards.

```bash
ask copy claude --skill ask-laravel-architect
```

### [ask-laravel-mechanic](coding/ask-laravel-mechanic/)

Senior maintenance skill. Enforces "Zero Data Loss" policies and handles Mongo/SQL debugging.

```bash
ask copy claude --skill ask-laravel-mechanic
```

### [ask-nextjs-architect](coding/ask-nextjs-architect/)

Expert scaffolding for Next.js 14+ (App Router). Enforces Server Components, Server Actions, and SEO best practices.

```bash
ask copy claude --skill ask-nextjs-architect
```

### [ask-owasp-security-review](coding/ask-owasp-security-review/)

Conduct a thorough static security review of code, identifying vulnerabilities aligned with OWASP Top 10 risks, with severity ratings and remediation suggestions.

```bash
ask copy claude --skill ask-owasp-security-review
```

### [ask-python-refactor](coding/ask-python-refactor/)

Best practices and guidelines for Python code refactoring

```bash
ask copy claude --skill ask-python-refactor
```

### [ask-readme-gardener](coding/ask-readme-gardener/)

Keeps documentation in sync with code by updating the README.md when features or APIs are added.

```bash
ask copy claude --skill ask-readme-gardener
```

### [ask-refactoring-readability](coding/ask-refactoring-readability/)

Refactor code to enhance readability, following principles like DRY, meaningful names, and modularization.

```bash
ask copy claude --skill ask-refactoring-readability
```

### [ask-security-sentinel](coding/ask-security-sentinel/)

Pre-flight security checker. Scans for exposed secrets and vulnerable patterns properly.

```bash
ask copy claude --skill ask-security-sentinel
```

### [ask-shadcn-architect](coding/ask-shadcn-architect/)

Strictly enforces shadcn/ui patterns, imports, and CLI usage when creating or modifying React UI components.

```bash
ask copy claude --skill ask-shadcn-architect
```

### [ask-shadcn-mechanic](coding/ask-shadcn-mechanic/)

Expert maintenance skill for shadcn/ui. Handles component customization, responsive layout debugging, and Form/Zod wiring while strictly enforcing UI/UX design integrity.

```bash
ask copy claude --skill ask-shadcn-mechanic
```

### [ask-unit-test-generation](coding/ask-unit-test-generation/)

Automates creation of comprehensive unit tests for functions or classes, emphasizing coverage of edge cases and assertions.

```bash
ask copy claude --skill ask-unit-test-generation
```

### [ask-vue-architect](coding/ask-vue-architect/)

Expert scaffolding for Vue 3. Specialized for Laravel Inertia stacks, but supports Nuxt/Vite. Enforces Composition API & TypeScript.

```bash
ask copy claude --skill ask-vue-architect
```

### [ask-vue-mechanic](coding/ask-vue-mechanic/)

Expert maintenance skill for Vue 3 within Laravel Inertia. Fixes navigation reloads, prop mismatches, and reactivity issues.

```bash
ask copy claude --skill ask-vue-mechanic
```

## Planning (6)

### [ask-adr-logger](planning/ask-adr-logger/)

Automatically records Architectural Decision Records (ADRs) when a significant technical decision is made.

```bash
ask copy claude --skill ask-adr-logger
```

### [ask-brainstorm](planning/ask-brainstorm/)

Explores user intent, requirements, and design before implementation. Required before any creative work.

```bash
ask copy claude --skill ask-brainstorm
```

### [ask-buildmaster](planning/ask-buildmaster/)

Smart Epic Orchestration Agent - Acts as PM + Tech Lead + Delivery Manager for epic planning, execution, and delivery.

```bash
ask copy claude --skill ask-buildmaster
```

### [ask-hold-code](planning/ask-hold-code/)

Planning-mode lock that prevents code generation until the user explicitly approves implementation.

```bash
ask copy claude --skill ask-hold-code
```

### [ask-project-memory](planning/ask-project-memory/)

Maintains a 'Project Brain' by recording architectural decisions and tech stack choices in a memory file.

```bash
ask copy claude --skill ask-project-memory
```

### [ask-solution-architect](planning/ask-solution-architect/)

Master Ideation and Strategic Architecture skill. Executes professional, multi-perspective ideation sessions utilizing SCAMPER, Six Hats, and Design Thinking.

```bash
ask copy claude --skill ask-solution-architect
```

## Tooling (10)

### [ask-add-agent](tooling/ask-add-agent/)

How to add support for new AI code editors to Agent Skill Kit

```bash
ask copy claude --skill ask-add-agent
```

### [ask-ast-mapper](tooling/ask-ast-mapper/)

Read-only subagent designed to generate lightweight AST (Abstract Syntax Tree) dependency maps.

```bash
ask copy claude --skill ask-ast-mapper
```

### [ask-context-janitor](tooling/ask-context-janitor/)

Aggressive token optimizer and context summarizer for AI orchestrators

```bash
ask copy claude --skill ask-context-janitor
```

### [ask-parallel-auditor](tooling/ask-parallel-auditor/)

Orchestrator skill that splits a target repository into chunks and runs multiple audit subagents in parallel.

```bash
ask copy claude --skill ask-parallel-auditor
```

### [ask-pdf-processing](tooling/ask-pdf-processing/)

PDF text extraction, form filling, and merging using pypdf and pdfplumber

```bash
ask copy claude --skill ask-pdf-processing
```

### [ask-skill-capture](tooling/ask-skill-capture/)

Meta-skill. Analyzes the current session's lessons and saves them as a permanent reusable skill.

```bash
ask copy claude --skill ask-skill-capture
```

### [ask-skill-creator](tooling/ask-skill-creator/)

Teaches AI agents how to create skills for Agent Skill Kit

```bash
ask copy claude --skill ask-skill-creator
```

### [ask-smart-booking-test](tooling/ask-smart-booking-test/)

An advanced autonomous testing skill for verifying end-to-end booking flows. Specializes in Flights, Movies, and Tours with integrated Payment Gateway testing.

```bash
ask copy claude --skill ask-smart-booking-test
```

### [ask-system-architect-prime](tooling/ask-system-architect-prime/)

Principal Software Architect for repository audits, complexity analysis, and actionable refactoring recommendations

```bash
ask copy claude --skill ask-system-architect-prime
```

### [ask-wiki-init](tooling/ask-wiki-init/)

Scaffolds the LLM Wiki pattern into any project — a persistent, compounding knowledge base maintained by AI agents.

```bash
ask copy claude --skill ask-wiki-init
```

---

[Documentation](https://navanithans.github.io/Agent-Skill-Kit/) · [Command builder](https://navanithans.github.io/Agent-Skill-Kit/docs/) · [GitHub](https://github.com/NavanithanS/Agent-Skill-Kit) · [PyPI](https://pypi.org/project/agent-skill-kit/)
