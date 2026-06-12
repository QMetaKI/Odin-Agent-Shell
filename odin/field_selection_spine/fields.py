"""Field definitions for FINAL-PR-07 Field Selection Spine.

Scores are bounded route hints. They are not truth, probability, authority, or execution.
"""
from __future__ import annotations

from dataclasses import dataclass

CLAIM_BOUNDARY = "field_selection_scores_routes_not_truth"


def bound_score(value: float) -> float:
    return round(max(0.0, min(1.0, float(value))), 3)


@dataclass(frozen=True)
class FieldSignal:
    field_id: str
    field_name: str
    signal_weight: float
    evidence_list: list[str]
    suppression_reason: str | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "signal_weight", bound_score(self.signal_weight))
        object.__setattr__(self, "evidence_list", list(self.evidence_list))

    def to_dict(self) -> dict:
        return {
            "field_id": self.field_id,
            "field_name": self.field_name,
            "signal_weight": self.signal_weight,
            "evidence_list": list(self.evidence_list),
            "suppression_reason": self.suppression_reason,
        }


@dataclass(frozen=True)
class DominantField:
    field_id: str
    confidence: float
    review_axes_applied: list[str]
    why_trace_id: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", bound_score(self.confidence))
        object.__setattr__(self, "review_axes_applied", list(self.review_axes_applied))

    def to_dict(self) -> dict:
        return {
            "field_id": self.field_id,
            "confidence": self.confidence,
            "review_axes_applied": list(self.review_axes_applied),
            "why_trace_id": self.why_trace_id,
        }


@dataclass(frozen=True)
class SuppressedField:
    field_id: str
    suppression_reason: str

    def to_dict(self) -> dict:
        return {"field_id": self.field_id, "suppression_reason": self.suppression_reason}


FIELD_DEFINITIONS: dict[str, dict] = {
    "scope_control": {"field_name": "Scope Control", "related_review_axis": "scope", "default_evidence_requirement": ["work_type"], "candidate_only_boundary": CLAIM_BOUNDARY},
    "claim_boundary_integrity": {"field_name": "Claim Boundary Integrity", "related_review_axis": "claim_boundary", "default_evidence_requirement": ["claim_boundary"], "candidate_only_boundary": CLAIM_BOUNDARY},
    "repo_reality_alignment": {"field_name": "Repo Reality Alignment", "related_review_axis": "repo_reality", "default_evidence_requirement": ["repo_evidence"], "candidate_only_boundary": CLAIM_BOUNDARY},
    "runtime_truth_alignment": {"field_name": "Runtime Truth Alignment", "related_review_axis": "runtime_truth", "default_evidence_requirement": ["runtime_receipt"], "candidate_only_boundary": CLAIM_BOUNDARY},
    "locality_preservation": {"field_name": "Locality Preservation", "related_review_axis": "locality", "default_evidence_requirement": ["local_only"], "candidate_only_boundary": CLAIM_BOUNDARY},
    "candidate_integrity": {"field_name": "Candidate Integrity", "related_review_axis": "candidate_integrity", "default_evidence_requirement": ["candidate_only"], "candidate_only_boundary": CLAIM_BOUNDARY},
    "evidence_sufficiency": {"field_name": "Evidence Sufficiency", "related_review_axis": "evidence", "default_evidence_requirement": ["evidence_items"], "candidate_only_boundary": CLAIM_BOUNDARY},
    "token_efficiency": {"field_name": "Token Efficiency", "related_review_axis": "token_efficiency", "default_evidence_requirement": ["token_budget"], "candidate_only_boundary": CLAIM_BOUNDARY},
    "app_authority_boundary": {"field_name": "App Authority Boundary", "related_review_axis": "app_authority", "default_evidence_requirement": ["app_owned_apply"], "candidate_only_boundary": CLAIM_BOUNDARY},
    "release_readiness_boundary": {"field_name": "Release Readiness Boundary", "related_review_axis": "release_readiness", "default_evidence_requirement": ["release_deferred"], "candidate_only_boundary": CLAIM_BOUNDARY},
}

FIELD_IDS = list(FIELD_DEFINITIONS.keys())
