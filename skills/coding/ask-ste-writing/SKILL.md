---
name: ask-ste-writing
description: Rewrite wordy docs, runbooks, PR descriptions, summaries in ~80% ASD-STE100 (controlled language). Short sentences, active voice, plain words.
triggers: ["write in STE", "simplified technical english", "plain english", "too wordy", "make this easier to read"]
---

<critical_constraints>
❌ NO procedural sentence over 20 words
❌ NO descriptive sentence over 25 words
❌ NO paragraph over 6 sentences or with more than one topic
❌ NO noun cluster over 3 words ("connection pool timeout setting" → "the pool timeout")
✅ MUST give one instruction per sentence (unless the actions are simultaneous)
✅ MUST use the same word for the same thing every time
</critical_constraints>

<verbs>
✅ Command: "Restart the server." ✅ Simple present/past/future: "The job runs." "The job ran." "The job will run."
❌ Progressive (-ing): "The job is running." Use -ing only inside a name ("load balancing").
❌ Perfect: "The job has run." ❌ Passive in procedures: "The cache must be cleared." → "Clear the cache."
</verbs>

<words>
One word, one meaning. Use the plain word:
utilize→use · prior to→before · ensure→make sure · approximately→about
commence→start · in order to→to · terminate→stop · subsequently→then
Keep technical names (API, mutex). Define one once if the reader may not know it.
</words>

<style>
- Keep articles ("the", "a"); no telegram style.
- Use vertical lists for complex text or for steps.
- Put the action first, then the reason.
- Safety notes: give the command first, then the risk.
  `WARNING:` risk of data loss or a security risk. `CAUTION:` risk of a breaking change or damage.
</style>

<softening>
Default "80% STE": limits and verb rules are strict; use the word list where it keeps precision.
Never trade correctness or a needed technical term for a word rule.
Check a draft: `python scripts/check_ste.py <file>` (or stdin).
</softening>

Credit: STE idea from Andrej Karpathy, https://x.com/karpathy/status/2105819303471976479
