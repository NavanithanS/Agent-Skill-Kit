"""TF-IDF lexical scorer for the offline trigger/collision audit.

WHAT THIS IS
    A pure-stdlib TF-IDF cosine ranker over the skill library. Given a prompt,
    it ranks every skill by lexical similarity to that skill's
    `description` + `triggers`.

WHAT THIS IS NOT
    It is not a model of how Claude/Gemini actually route. Real agents match
    semantically; this matches vocabulary. Its job is to surface *collisions* —
    pairs of skills (e.g. an architect and its mechanic sibling) that compete
    for the same prompts — so authors can disambiguate descriptions before a
    real agent has to. Absolute "does it fire" accuracy is Layer 2's job.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

# A non-target skill scoring within this cosine distance of the target on the
# target's own prompt is treated as a collision (a lexical false-positive risk).
DEFAULT_COLLISION_MARGIN = 0.05

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> List[str]:
    return _TOKEN_RE.findall(text.lower())


def _skill_document(skill: Dict) -> str:
    """The searchable surface of a skill: what an orchestrator reads to route."""
    parts = [skill.get("description", "") or ""]
    parts.extend(skill.get("triggers", []) or [])
    return " ".join(parts)


@dataclass
class TriggerIndex:
    """An in-memory TF-IDF index over the skill library."""

    idf: Dict[str, float] = field(default_factory=dict)
    skill_vectors: Dict[str, Dict[str, float]] = field(default_factory=dict)

    def _vectorize(self, tokens: List[str]) -> Dict[str, float]:
        tf: Dict[str, int] = {}
        for tok in tokens:
            tf[tok] = tf.get(tok, 0) + 1
        return {tok: count * self.idf.get(tok, 0.0) for tok, count in tf.items()}

    @staticmethod
    def _cosine(a: Dict[str, float], b: Dict[str, float]) -> float:
        if not a or not b:
            return 0.0
        common = set(a) & set(b)
        numerator = sum(a[t] * b[t] for t in common)
        norm_a = math.sqrt(sum(v * v for v in a.values()))
        norm_b = math.sqrt(sum(v * v for v in b.values()))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return numerator / (norm_a * norm_b)

    def score(self, prompt: str) -> List[Tuple[str, float]]:
        """Rank every skill against `prompt`, highest cosine first."""
        prompt_vec = self._vectorize(_tokenize(prompt))
        ranked = [
            (name, self._cosine(prompt_vec, vec))
            for name, vec in self.skill_vectors.items()
        ]
        ranked.sort(key=lambda pair: (-pair[1], pair[0]))
        return ranked


def build_index(skills: List[Dict]) -> TriggerIndex:
    """Build a TF-IDF index from a list of skill dicts (name/description/triggers)."""
    documents: Dict[str, List[str]] = {
        skill["name"]: _tokenize(_skill_document(skill))
        for skill in skills
        if skill.get("name")
    }

    n_docs = len(documents)
    doc_freq: Dict[str, int] = {}
    for tokens in documents.values():
        for token in set(tokens):
            doc_freq[token] = doc_freq.get(token, 0) + 1

    # Smoothed IDF keeps common filler words ("the", "code") from dominating.
    idf = {
        token: math.log(n_docs / (1 + freq)) + 1.0
        for token, freq in doc_freq.items()
    }

    index = TriggerIndex(idf=idf)
    index.skill_vectors = {
        name: index._vectorize(tokens) for name, tokens in documents.items()
    }
    return index


def load_evals(skill: Dict) -> Optional[Dict]:
    """Load a skill's tests/evals.yaml, if present.

    Format (Layer 1):
        should_fire:
          - "a paraphrased user prompt this skill should own"
          - "another"
    """
    path_str = skill.get("_path")
    if not path_str:
        return None
    evals_path = Path(path_str) / "tests" / "evals.yaml"
    if not evals_path.exists():
        return None
    try:
        with open(evals_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data if isinstance(data, dict) else None
    except Exception:
        return None


@dataclass
class PromptResult:
    skill: str
    prompt: str
    target_score: float
    top_skill: str
    top_score: float
    runner_up_skill: Optional[str]
    runner_up_score: float
    collisions: List[Tuple[str, float]]  # (competing_skill, score) within margin

    @property
    def is_hit(self) -> bool:
        """True when the skill cleanly owns the top slot for its own prompt."""
        return self.top_skill == self.skill

    @property
    def has_collision(self) -> bool:
        return bool(self.collisions)


@dataclass
class AuditReport:
    results: List[PromptResult]
    margin: float

    @property
    def total_prompts(self) -> int:
        return len(self.results)

    # The three buckets below partition every result exactly once:
    # a prompt is clear, OR it tops its slot but is contested, OR it misses.
    @property
    def clean(self) -> List[PromptResult]:
        return [r for r in self.results if r.is_hit and not r.has_collision]

    @property
    def contested(self) -> List[PromptResult]:
        return [r for r in self.results if r.is_hit and r.has_collision]

    @property
    def misses(self) -> List[PromptResult]:
        return [r for r in self.results if not r.is_hit]

    @property
    def collisions(self) -> List[PromptResult]:
        """All prompts with any collision (overlaps misses) — for strict/CI gating."""
        return [r for r in self.results if r.has_collision]

    def collision_pairs(self) -> Dict[Tuple[str, str], int]:
        """How often each (skill, competitor) pair collides, undirected."""
        pairs: Dict[Tuple[str, str], int] = {}
        for r in self.results:
            for competitor, _score in r.collisions:
                key = tuple(sorted((r.skill, competitor)))
                pairs[key] = pairs.get(key, 0) + 1
        return pairs


def run_trigger_audit(
    skills: List[Dict],
    margin: float = DEFAULT_COLLISION_MARGIN,
) -> AuditReport:
    """Run the offline collision audit over every skill that ships an evals.yaml.

    For each labeled `should_fire` prompt we check whether the owning skill tops
    the library ranking, and whether any *other* skill scores within `margin` —
    the honest signal here is collision between similar skills, not absolute
    pass/fail.
    """
    index = build_index(skills)
    results: List[PromptResult] = []

    for skill in skills:
        name = skill.get("name")
        if not name:
            continue
        evals = load_evals(skill)
        if not evals:
            continue
        for prompt in evals.get("should_fire", []) or []:
            ranked = index.score(prompt)
            if not ranked:
                # The audited skill is always in the index, so this is
                # unreachable today; guard against future refactors that could
                # build the index from a different skill set.
                continue
            score_by_name = dict(ranked)
            target_score = score_by_name.get(name, 0.0)
            top_skill, top_score = ranked[0]
            runner_up_skill, runner_up_score = (
                ranked[1] if len(ranked) > 1 else (None, 0.0)
            )

            collisions = [
                (other, score)
                for other, score in ranked
                if other != name and score >= target_score - margin
            ]

            results.append(
                PromptResult(
                    skill=name,
                    prompt=prompt,
                    target_score=target_score,
                    top_skill=top_skill,
                    top_score=top_score,
                    runner_up_skill=runner_up_skill,
                    runner_up_score=runner_up_score,
                    collisions=collisions,
                )
            )

    return AuditReport(results=results, margin=margin)
