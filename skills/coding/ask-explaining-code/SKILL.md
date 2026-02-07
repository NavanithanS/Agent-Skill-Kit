---
name: ask-explaining-code
description: Explain code via analogies, ASCII diagrams, step-by-step walkthroughs.
triggers: ["explain this code", "how does this work", "walk me through", "break down this logic"]
---

<critical_constraints>
❌ NO jargon without explanation
❌ NO skipping "obvious" parts
❌ NO restating code in English only
✅ MUST use concrete examples with actual values
✅ MUST include ASCII diagram for structure/flow
✅ MUST explain "why" not just "what"
</critical_constraints>
 
<response_structure>
1. Quick Summary (1-2 sentences)
2. Big Picture Analogy
3. ASCII Diagram (structure/flow)
4. Step-by-Step Walkthrough (numbered)
5. Key Concepts
6. Common Pitfalls (⚠️)
</response_structure>

<analogies>
| Concept | Analogy |
|---------|---------|
| Variables | Labeled boxes |
| Functions | Vending machines (in→process→out) |
| Loops | Assembly line workers |
| Conditionals | Forks in road with signs |
| Classes | Cookie cutters (templates) |
| APIs | Restaurant menu |
| Caching | Frequently used items on desk |
| Recursion | Russian nesting dolls |
| Async | Ordering delivery while doing other things |
| Indexes | Book index (quick lookup) |
</analogies>

<ascii_patterns>
Flow: Start → Check → Process → End
           ↓
         Error? → Retry

State: [Idle] --request--> [Loading] --success--> [Done]
                               |--error--> [Error]

Call Stack:
main()
  └─ processData()
      └─ validate() ← executing
</ascii_patterns>

<heuristics>
- Follow-up questions → go deeper
- User seems lost → simpler analogies
- Complex nesting → draw box diagram
- Recursion → show tree expansion
</heuristics>
