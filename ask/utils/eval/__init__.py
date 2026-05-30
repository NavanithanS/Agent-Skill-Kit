"""Skill evaluation harness.

Layer 1 (this package): offline, dependency-free trigger/collision audit.
    A TF-IDF lexical pre-screen over the skill library. It does NOT measure
    how a real agent routes (LLMs route semantically) — it flags skills whose
    descriptions/triggers compete for the same prompts. Treat the numbers as a
    lexical proxy, not routing ground truth.

Layer 2 (future): `ask test --behavior` runs the skill against a live model
    with an LLM-as-judge for true trigger accuracy and output correctness.
"""

from ask.utils.eval.trigger_scorer import (
    TriggerIndex,
    build_index,
    load_evals,
    run_trigger_audit,
)

__all__ = [
    "TriggerIndex",
    "build_index",
    "load_evals",
    "run_trigger_audit",
]
