"""Y Selection Score — bounded route scoring object.

Claim boundary: y_pattern_spine_candidate_only_no_app_apply_no_provider_no_runtime_authority
candidate_only: true
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

CLAIM_BOUNDARY = "y_pattern_spine_candidate_only_no_app_apply_no_provider_no_runtime_authority"


@dataclass
class YSelectionScore:
    route_id: str
    route_score: float
    confidence: float
    hole_density: float
    evidence_basis: List[str]
    selection_reason: str
    claim_boundary: str = CLAIM_BOUNDARY

    def __post_init__(self) -> None:
        self.route_score = max(0.0, min(1.0, self.route_score))
        self.confidence = max(0.0, min(1.0, self.confidence))
        self.hole_density = max(0.0, min(1.0, self.hole_density))

    def to_dict(self) -> dict:
        return {
            "route_id": self.route_id,
            "route_score": self.route_score,
            "confidence": self.confidence,
            "hole_density": self.hole_density,
            "evidence_basis": self.evidence_basis,
            "selection_reason": self.selection_reason,
            "claim_boundary": self.claim_boundary,
        }


def score_route(
    route_id: str,
    evidence: List[str],
    *,
    base_score: float = 0.7,
    evidence_boost: float = 0.05,
    hole_penalty: float = 0.1,
) -> YSelectionScore:
    score = min(1.0, base_score + len(evidence) * evidence_boost)
    confidence = min(1.0, 0.6 + len(evidence) * 0.04)
    hole_density = max(0.0, 0.4 - len(evidence) * hole_penalty)
    return YSelectionScore(
        route_id=route_id,
        route_score=round(score, 3),
        confidence=round(confidence, 3),
        hole_density=round(hole_density, 3),
        evidence_basis=list(evidence),
        selection_reason="evidence_weighted_score",
    )
