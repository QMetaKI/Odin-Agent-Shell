"""Deterministic coherence scoring. Scores are route hints only."""
from __future__ import annotations

from dataclasses import dataclass

from odin.field_selection_spine.fields import bound_score
from odin.field_selection_spine.hole_density import calculate_hole_density
from odin.field_selection_spine.review_axes import REVIEW_AXIS_IDS


@dataclass(frozen=True)
class CoherenceScore:
    overall_score: float
    axis_scores: dict[str, float]
    hole_density: float
    evidence_requirement_met: bool
    route_confidence: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "overall_score", bound_score(self.overall_score))
        object.__setattr__(self, "axis_scores", {k: bound_score(v) for k, v in self.axis_scores.items()})
        object.__setattr__(self, "hole_density", bound_score(self.hole_density))
        object.__setattr__(self, "route_confidence", bound_score(self.route_confidence))

    def to_dict(self) -> dict:
        return {
            "overall_score": self.overall_score,
            "axis_scores": dict(self.axis_scores),
            "hole_density": self.hole_density,
            "evidence_requirement_met": self.evidence_requirement_met,
            "route_confidence": self.route_confidence,
        }


def score_coherence(required_evidence: list[str], evidence_items: list[str], context: dict | None = None) -> CoherenceScore:
    context = context or {}
    evidence_text = "\n".join(str(item).lower() for item in evidence_items)
    axis_scores: dict[str, float] = {}
    for axis_id in REVIEW_AXIS_IDS:
        score = 0.5
        if axis_id in evidence_text:
            score = 1.0
        elif axis_id in {"claim_boundary", "candidate_integrity"} and context.get("candidate_only", True) is True:
            score = 0.9
        elif axis_id == "app_authority" and context.get("app_owned_apply", True) is True:
            score = 0.9
        elif axis_id == "locality" and context.get("local_only", True) is True:
            score = 0.9
        elif axis_id == "repo_reality" and (context.get("repo_evidence") or "selected_seed_id" in evidence_text):
            score = 0.9
        elif axis_id == "release_readiness" and context.get("release_deferred", True) is True:
            score = 0.85
        axis_scores[axis_id] = bound_score(score)
    hole_density = calculate_hole_density(required_evidence, evidence_items)
    average = sum(axis_scores.values()) / len(axis_scores) if axis_scores else 0.0
    overall = bound_score(average * (1.0 - hole_density))
    return CoherenceScore(overall, axis_scores, hole_density, hole_density == 0.0, overall)
