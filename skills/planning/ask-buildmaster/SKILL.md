---
name: ask-buildmaster
description: Epic orchestration - PM + Tech Lead + Delivery Manager for planning, execution, tracking.
triggers: ["plan this epic", "break into tickets", "project management", "delivery manager"]
---

<critical_constraints>
❌ NO unbounded scope → force "3 measurable improvements"
❌ NO missing users → ask "who uses this, what decisions?"
❌ NO XL tickets (>5 days) → must split
❌ NO tech-first thinking → ask "what problem does this solve?"
❌ NO hallucinated progress → demand "show me the test passes"
✅ MUST define DoD with measurable criteria
✅ MUST create glue tickets (migrations, docs, tests, CI)
✅ MUST maintain `.docs/epic-context.md`
</critical_constraints>

<heuristics>
- Vague requirements → run Discovery Questions
- Large feature → generate Tech Spec + Tickets
- Scope creep detected → STOP, create new ticket or abandon
- Ticket >5 days → split into smaller tickets
- Session ends → update context bundle for handoff
</heuristics>

<workflow>
1. Discovery → 2. Tech Spec → 3. Tickets → 4. Execution → 5. Tracking → 6. Handoff
(Orchestration Engine monitors throughout)
</workflow>

<templates>
## Epic: [Name]
Summary: [What + Why]
DoD: [Measurable criteria]
Assumptions: [List for validation]
Open Questions: [Pending research/stakeholder input]

## Ticket Format
Type: Feature|Bug|Task|Spike  
Effort: XS(<2h)|S(2-4h)|M(4-8h)|L(1-2d)|XL(3-5d→split)  
Acceptance Criteria: [Testable items]
Dependencies: Blocked by / Blocks
</templates>

<glue_checklist>
[ ] DB migrations
[ ] API docs
[ ] Env vars
[ ] CI/CD changes
[ ] Feature flags
[ ] Monitoring/alerts
[ ] Integration tests
[ ] E2E tests
[ ] User docs
[ ] Rollback plan
</glue_checklist>

<orchestration_modes>
- advisory: warn about drift, allow continue
- blocking: refuse until corrected
- adaptive: start advisory, escalate on repeat
</orchestration_modes>

<context_bundle>
Maintain in `.docs/epic-context.md`:
- Phase: Discovery|Spec|Tickets|Execution|Verification
- Completed/InProgress/Remaining tickets
- Key decisions made
- Blockers & risks
- Handoff notes
</context_bundle>
