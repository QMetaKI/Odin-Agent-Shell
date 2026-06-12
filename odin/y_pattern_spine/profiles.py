"""Y Route Hint — candidate route selection profiles.

Claim boundary: y_pattern_spine_candidate_only_no_app_apply_no_provider_no_runtime_authority
candidate_only: true
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

CLAIM_BOUNDARY = "y_pattern_route_hint_candidate_only_not_authority"


@dataclass
class YRouteHint:
    route_hint_id: str
    input_kind: str
    candidate_routes: List[str]
    evidence_required: List[str]
    selected_route: str
    selection_reason: str
    confidence: float
    hole_density: float
    center_first_posture: bool
    token_budget_hint: str
    claim_boundary: str = CLAIM_BOUNDARY
    materialization_level: Optional[str] = None
    not_proven: Optional[List[str]] = None

    def __post_init__(self) -> None:
        if self.not_proven is None:
            self.not_proven = _DEFAULT_NOT_PROVEN[:]

    def to_dict(self) -> dict:
        return {
            "route_hint_id": self.route_hint_id,
            "input_kind": self.input_kind,
            "candidate_routes": self.candidate_routes,
            "evidence_required": self.evidence_required,
            "selected_route": self.selected_route,
            "selection_reason": self.selection_reason,
            "confidence": self.confidence,
            "hole_density": self.hole_density,
            "center_first_posture": self.center_first_posture,
            "token_budget_hint": self.token_budget_hint,
            "materialization_level": self.materialization_level,
            "not_proven": self.not_proven,
            "claim_boundary": self.claim_boundary,
        }


_DEFAULT_NOT_PROVEN = [
    "model_inference",
    "provider_execution",
    "event_core_runtime",
    "app_apply",
    "external_send",
    "production_readiness",
]

DEMO_ROUTE_HINT: dict = {
    "artifact_kind": "y_route_explanation_demo",
    "candidate_only": True,
    "input_kind": "demo_universal_work",
    "candidate_routes": [
        "direct_response_packet",
        "work_capsule_then_response_packet",
        "defer_for_missing_evidence",
    ],
    "selected_route": "work_capsule_then_response_packet",
    "selection_reason": "center_first_route_with_low_overclaim_risk",
    "materialization_level": "M7",
    "token_budget_hint": "minimal",
    "normal_user_summary": "Odin prepared the work before returning a candidate.",
    "dev_mode_summary": "Y Pattern Spine selected a work capsule route based on evidence requirements and claim boundary.",
    "not_proven": [
        "model_inference",
        "provider_execution",
        "event_core_runtime",
        "app_apply",
        "external_send",
        "production_readiness",
    ],
    "claim_boundary": "y_pattern_route_hint_candidate_only_not_authority",
}


def build_route_hint_demo() -> dict:
    return dict(DEMO_ROUTE_HINT)
