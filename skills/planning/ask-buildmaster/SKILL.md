---
name: ask-buildmaster
description: Epic orchestration - PM + Tech Lead for planning and formatted execution.
triggers: ["plan this epic", "break into tickets", "project management"]
---

<critical_constraints>
1. ❌ NO clear scope? Ask "What problem does this solve?".
2. ❌ NO XL tickets (>5 days). MUST split them.
3. ✅ MUST define DoD with measurable criteria.
4. ✅ MUST add glue tickets (migrations, docs, CI).
5. ✅ MUST maintain `.docs/epic-context.md`.
</critical_constraints>

<heuristics>
- Vague input → Run Discovery Questions.
- Large feature → Tech Spec first, then Tickets.
- Scope creep → Create new ticket or kill feature.
- Session end → Update context bundle.
</heuristics>

<workflow>
1. Discovery
2. Tech Spec
3. Tickets
4. Execution
5. Tracking
6. Handoff
</workflow>

<templates>
## Epic: [Name]
Summary: [What + Why]  
DoD: [Criteria]  
Questions: [Pending]  

## Ticket
Type: Feat|Bug|Task|Spike  
Effort: XS(<2h)|S|M|L|XL(Split)  
AC: [Testable items]
</templates>

<glue_checklist>
- [ ] DB: migrations, seeds
- [ ] Docs: API, User, Env vars
- [ ] Ops: CI/CD, Flags, Alerts
- [ ] QA: Integration, E2E, Rollback
</glue_checklist>

<orchestration_modes>
- advisory: warn only
- blocking: refuse
- adaptive: escalate on repeat
</orchestration_modes>

<context_bundle>
Update `.docs/epic-context.md`:
- Phase, Status (Done/Todo)
- Decisions, Blockers, Risks
</context_bundle>
