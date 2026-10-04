---
title: Output Formats for Understanding Agent Work
type: concept
tags: [skills, explanation, ste100, diagrams, html, writing]
updated: 2026-10-04
sources: 3
---

# Concept: Output Formats for Understanding Agent Work

Agents now do more of the work, so people spend more time reading what agents produce.
Two skills make that output easier to understand:

- [`ask-ste-writing`](../../skills/coding/ask-ste-writing/) controls how the prose is written.
- [`ask-explaining-code`](../../skills/coding/ask-explaining-code/) chooses the format of an explanation.

`ask-explaining-code` declares `depends_on: [ask-ste-writing]`, so `ask copy ask-explaining-code` installs both.

## Source

Andrej Karpathy, [X post](https://x.com/karpathy/status/2105819303471976479) on understanding LLM output (ingested 2026-10-04). It ranks output formats by how easy they are to understand:
STE prose < diagrams < HTML pages < explainer videos. Its main point: code is now cheap, so a large, disposable explainer is worth making.

## Decisions

| Decision | Reason |
|---|---|
| STE is its own skill, not a section of `ask-explaining-code` | The rules apply to all agent prose (PR text, runbooks, summaries). Both skills together would exceed the 500-token limit. |
| "80% STE", not the full specification | The full specification has about 900 approved words. Structural limits (sentence length, verb forms) give most of the gain. The word list is a guide only. |
| Format ladder, not "always draw an ASCII diagram" | The old rule forced a diagram on one-line answers. The ladder goes up only when complexity needs it: prose → diagram → HTML. |
| HTML goes to the OS temp dir by default | Explainers are disposable. Writing them into the repo would add noise to `git status`. |
| Video is offer-only | It needs external tools or API keys (manim, TTS). It does not work the same on all 5 agent targets. |
| Category `coding/` | `workflows/` is not a valid category (`validators.py`). |

## STE limits used

These limits come from the ASD-STE100 writing rules:

- Procedural sentence: max 20 words. Descriptive sentence: max 25 words.
- Paragraph: max 6 sentences, one topic. Noun cluster: max 3 words.
- One instruction per sentence.
- No progressive (`-ing`) tense, no perfect tense, no passive voice in procedures.

`skills/coding/ask-ste-writing/scripts/check_ste.py` checks sentence length, paragraph length and the plain-word table.
Its passive and progressive checks are regex heuristics, so it reports them as advisories only.

## Trigger audit notes

The first eval run showed real routing gaps. For example, "this runbook is too wordy" matched no vocabulary in the STE skill.
The fix was to change the skill descriptions and triggers, not the eval prompts.
After the fix, all 10 prompts route to their own skill. 2 prompts are contested: the owner is top, but within the 0.05 margin.

Watch for these overlaps:
- `ask-explaining-code` and `ask-bug-finder` on "help me understand what X is doing".
- `ask-ste-writing` and `ask-refactoring-readability` on "readable".

## Gotchas

- `ask update` and MCP `get_skill` do not install dependencies (see [../entities/skill.md](../entities/skill.md)). So `ask-explaining-code` puts the key STE limits inline and does not rely on `ask-ste-writing` being installed.
- `skills/*/tests/*.py` are not part of `pytest tests/` or CI. Run `python -m pytest skills/coding/ask-ste-writing/tests` by hand.
- A `skill.yaml` description that contains `: ` must be quoted. Otherwise YAML parsing fails and `scripts/add_skill_frontmatter.py` crashes.

See also: [eval-harness.md](eval-harness.md), [../entities/skill.md](../entities/skill.md).
