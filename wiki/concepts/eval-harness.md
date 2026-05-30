# Concept: Skill Eval Harness (`ask test`)

A two-layer system for verifying that skills actually *work* — not just that
their files are structurally valid (`ask validate`) or within token budget
(`ask skill lint`).

## Why it exists

Skills route by their `description` + `triggers`. Two failure modes silently
degrade a library:
1. A skill never fires when it should (bad description).
2. **Two similar skills compete for the same prompt** (e.g. `ask-laravel-architect`
   vs `ask-laravel-mechanic`) — the real, common false-positive source.

`ask validate` cannot catch either; you need to evaluate routing behaviour.

## Layer 1 — `ask test --triggers` (offline, default)

- **What it is:** a pure-stdlib TF-IDF cosine ranker over the whole library
  (`ask/utils/eval/trigger_scorer.py`). For each labeled prompt it ranks every
  skill and flags any *other* skill scoring within `--margin` (default 0.05) of
  the owning skill — a **collision**.
- **What it is NOT:** a model of how Claude/Gemini route. Real agents match
  semantically; this matches vocabulary. It is framed honestly as a **lexical
  pre-screen / collision audit**, not routing ground truth. (Validated early:
  TF-IDF cannot reliably separate the laravel architect/mechanic pair — which is
  exactly the point, so the tool reports collisions rather than pass/fail.)
- **CI-friendly:** no API key, deterministic, `--strict` exits non-zero on any
  collision or miss.
- **Buckets** (partition every prompt once): `clear` (owns its slot uncontested),
  `contested` (owns it but a sibling is within margin), `miss` (another skill tops it).
- **Negatives come from other skills' prompts**, not hand-written `should_not_fire`
  lists (those are trivially passed). Collisions between siblings are the signal.

### Eval format — `skills/<cat>/<skill>/tests/evals.yaml`

```yaml
should_fire:
  - "a paraphrased user prompt this skill should own"
```

Write prompts the way a *real user* would phrase them. Do **not** echo the
skill's own trigger phrases — that makes the audit circular and meaningless.

## Layer 2 — `ask test --behavior` (live model, planned)

Runs each skill as a system prompt against a live model with an **LLM-as-judge**
scoring output against assertions. Provider is **Anthropic-first via a pluggable
`Provider` interface** (Gemini/OpenAI/local plug in later). This is where true
"does it fire in a real agent" accuracy lives. Currently stubbed (exit 2).

## Key files

- `ask/utils/eval/trigger_scorer.py` — TF-IDF index, audit, bucket partition
- `ask/commands/test.py` — `ask test` command (table + `--json` + `--strict`)
- `tests/test_trigger_scorer.py` — unit tests
- Demo evals live in the laravel/vue architect+mechanic pairs.
