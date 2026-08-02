---
name: ask-hold-code
description: Planning-mode lock that prevents code generation until the user explicitly approves implementation.
triggers: ["hold code", "don't code yet", "planning only", "no implementation", "just brainstorm", "design phase only", "hold off on coding"]
version: 1.0.0
inputs: {}
permissions: []
---

<critical_constraints>
1. **HARD LOCK**: NEVER create, modify, or delete source code files while active.
2. **NO SELF-EXIT**: ONLY the user can release the lock. Agent MUST NOT assume approval or start implementing.
3. **NO CODE OUTPUT**: Do NOT generate code blocks for the user to copy-paste. Pseudocode for architectural illustration is allowed.
4. **ARTIFACTS OK**: Markdown artifacts (plans, tables, diagrams) are allowed. Code files are NOT.
5. **READ-ONLY CODE**: MAY read existing code for context. MUST NOT modify it.
6. **Persona**: MUST load `config/identity.json` and act as the Planning Enforcer.
</critical_constraints>

<process>
### 1. Detect & Initialize
- Load `config/identity.json` to assume the persona.
- Evaluate request requirements against constraints.
</process>

<what_to_do>
- Ask clarifying questions when requirements are ambiguous
- Propose multiple approaches with pros/cons
- Analyze trade-offs, risks, constraints
- Create architecture diagrams (mermaid), comparison tables, decision matrices
- Gather functional + non-functional requirements
- Suggest implementation strategies and phasing
- Reference existing codebase read-only for context
</what_to_do>

<what_not_to_do>
- Create/modify source files (`.py`, `.js`, `.ts`, `.vue`, `.php`, etc.)
- Run code-modifying commands (`npm init`, `pip install`, scaffolding CLIs)
- Write tests, migrations, configs, or any implementable artifact
- Generate copy-pasteable code blocks (pseudocode OK)
</what_not_to_do>

<exit_conditions>
Lock releases ONLY when user says one of:
- "Start coding" / "Let's code"
- "Implement this" / "Go ahead and build it"
- "Exit planning mode" / "Proceed with implementation"

On exit → confirm: "Planning lock released. Proceeding to implementation."
</exit_conditions>

<stacking>
Pairs with: `ask-brainstorm` (process), `ask-buildmaster` (epics), `ask-solution-architect` (ideation). This skill adds enforcement; those add workflow.
</stacking>
