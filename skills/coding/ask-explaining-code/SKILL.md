---
name: ask-explaining-code
description: Explain code, diffs, agent changes step by step, with analogies - STE prose, diagrams, or HTML explainer.
triggers: ["explain this code", "help me understand", "walk me through", "explain this diff", "what did you change", "diagram how this connects"]
---

<critical_constraints>
❌ NO jargon without explanation
❌ NO restating code in English only
✅ MUST pick the format by complexity (format_ladder)
✅ MUST write prose to ask-ste-writing rules (~80% STE: ≤20-25 words/sentence, active voice, plain words)
✅ MUST use concrete examples with real values
✅ MUST explain "why", not only "what"
</critical_constraints>

<scope>
Code, diffs, PRs, and your own changes.
</scope>

<format_ladder>
Use the lowest step that is clear. Go up if the reader asks or is lost.
1. Prose: one function or one small concept.
2. Diagram: flow, state, call stack, module structure. ASCII inline; Mermaid if it renders.
3. HTML: multi-part systems, large diffs, comparisons, or when asked.
   - One self-contained .html file. No build step. CDN only if needed.
   - Disposable: write it to the OS temp dir (or a user-named path), not the repo. Give the path; do not paste it in chat.
4. Video: only if asked (needs external tools or API keys).
</format_ladder>

<html_style>
Reference-sheet layout: labelled panels (A, B, C…), one topic each.
Annotate real code or diff lines. Tables over prose. ✓/✗ columns for before/after.
Title block: topic, source files, commit.
</html_style>

<response_structure>
1. Summary (1-2 sentences)
2. One everyday analogy
3. Diagram or HTML path (per ladder)
4. Step-by-step walkthrough (numbered)
5. Pitfalls (⚠️)
</response_structure>

<ascii_pattern>
State: [Idle] --request--> [Loading] --success--> [Done]
                               |--error--> [Error]
</ascii_pattern>

Credit: Format ladder from Andrej Karpathy, https://x.com/karpathy/status/2105819303471976479
