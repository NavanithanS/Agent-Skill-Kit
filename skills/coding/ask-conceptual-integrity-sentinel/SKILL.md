---
name: ask-conceptual-integrity-sentinel
description: Audit repos for architectural drift, dead code, and abstraction bloat.
triggers: ["study this repo", "audit for complexity", "why is codebase fragile", "find dead code"]
---

<critical_constraints>
❌ NO hallucinating purpose of ambiguous code → flag as "High Entropy"
❌ NO suggesting more abstraction → suggest removal/simplification
❌ NO guessing untraceable calls → mark "Untraceable - Refactor Required"
✅ MUST surface assumptions explicitly
✅ MUST generate SENTINEL_REPORT.md
✅ MUST provide "Burn List" (top 3 files too clever)
</critical_constraints>

<failure_modes>
- Assumption Drift: verify imports, don't assume from package.json
- Confusion Management: 500-line utils.js → flag, don't hallucinate
- Abstraction Bloat: 10-line logic in 3 class layers → "Premature Optimization"
</failure_modes>

<workflow>
1. Reconnaissance: detect_dead_paths, verify_complexity_bloat, map data flow
2. Interrogation: apply Simplicity Filter to every suggestion
3. Report: generate SENTINEL_REPORT.md
</workflow>

<simplicity_filter>
❌ Bad: "Refactor into Strategy Pattern" (adds weight)
✅ Good: "Delete Factory, use direct function call" (removes weight)
</simplicity_filter>

<output_format>
## SENTINEL_REPORT.md
- **Slop Index**: % of dead/redundant code
- **Critical Assumptions**: what I assumed (risks if wrong)
- **Burn List**: top 3 "too clever" files
- **Architecture Gaps**: missing tests, circular deps, no error boundaries
</output_format>

<heuristics>
- Low complexity/LOC ratio + large file → boilerplate/slop
- High complexity/LOC ratio + small file → code golf/unreadable
- Prop drilling >5 layers → architecture smell
</heuristics>
