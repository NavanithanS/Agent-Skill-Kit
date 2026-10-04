---
title: STE Writing
description: 'Rewrites wordy docs, runbooks, PR descriptions and summaries in ~80% ASD-STE100, a controlled language: short sentences, active voice, plain words.'
---

# STE Writing

A skill that makes agent output easier to read. It applies the core rules of ASD-STE100 Simplified Technical English, a controlled language first made for aircraft maintenance manuals.

## Purpose

Agents now do more of the work, so people spend more time reading what agents produce: summaries, PR descriptions, runbooks, explanations. STE puts hard limits on sentence length, verb forms and word choice. LLMs know the specification well, so the request "write in STE" works without a long prompt.

The full specification is strict (about 900 approved words). This skill applies "80% STE": the structural rules are strict, the word list is a guide. The idea comes from [Andrej Karpathy's post](https://x.com/karpathy/status/2105819303471976479) on tools for understanding LLM output.

## The rules

| Rule | Limit |
|------|-------|
| Procedural sentence | max 20 words |
| Descriptive sentence | max 25 words |
| Paragraph | max 6 sentences, one topic |
| Noun cluster | max 3 words |
| Instructions per sentence | 1 (unless the actions are simultaneous) |

**Verbs:** use commands and the simple present, past and future. Do not use the progressive (`-ing`), the perfect tense, or the passive voice in procedures.

**Words:** one word has one meaning. Use the same word for the same thing every time. Use the plain word: *use*, not *utilize*; *before*, not *prior to*; *make sure*, not *ensure*.

**Safety notes:** give the command first, then the risk. `WARNING:` means a risk of data loss or a security risk. `CAUTION:` means a risk of a breaking change or damage.

## Example

Original:

> It is imperative that the operator ensures the hydraulic reservoir is replenished prior to commencing operation.

STE (13 words, procedural limit 20):

> Make sure that the hydraulic reservoir is full before you start the operation.

## Checker script

`scripts/check_ste.py` checks a draft against the limits and the plain-word table. It ignores code blocks.

```bash
python scripts/check_ste.py docs/runbook.md
git log -1 --format=%B | python scripts/check_ste.py
python scripts/check_ste.py steps.md --procedural   # 20-word limit everywhere
```

It exits with status 1 when it finds a violation. Passive voice and the progressive tense are reported as advisories only, because the regex checks cannot be sure.

## Related skills

- `ask-explaining-code` depends on this skill and uses these rules for its prose.

## Sources

- ASD-STE100 specification: [asd-ste100.org](https://www.asd-ste100.org)
