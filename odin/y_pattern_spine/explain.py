"""Y Projection Set — human/expression/machine projections.

Claim boundary: y_pattern_spine_candidate_only_no_app_apply_no_provider_no_runtime_authority
candidate_only: true
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

CLAIM_BOUNDARY = "y_pattern_spine_candidate_only_no_app_apply_no_provider_no_runtime_authority"


@dataclass
class YProjectionSet:
    projection_id: str
    human_clear_projection: str
    expression_projection: str
    machine_projection: dict
    lineage_trace: str
    work_state_ref: Optional[str]
    claim_boundary: str = CLAIM_BOUNDARY
    not_proven: Optional[List[str]] = None

    def __post_init__(self) -> None:
        if self.not_proven is None:
            self.not_proven = [
                "production_readiness",
                "live_model_inference",
                "app_state_mutation",
                "external_send_authority",
            ]

    def to_dict(self) -> dict:
        return {
            "projection_id": self.projection_id,
            "human_clear_projection": self.human_clear_projection,
            "expression_projection": self.expression_projection,
            "machine_projection": self.machine_projection,
            "lineage_trace": self.lineage_trace,
            "work_state_ref": self.work_state_ref,
            "not_proven": self.not_proven,
            "claim_boundary": self.claim_boundary,
        }


def build_projection_set_demo() -> YProjectionSet:
    return YProjectionSet(
        projection_id="demo_projection_set",
        human_clear_projection="Odin prepared a work capsule using center-first routing and minimal token budget.",
        expression_projection="Route 'work_capsule_then_response_packet' selected via evidence: repo_route_identified, pattern_selected.",
        machine_projection={
            "artifact_kind": "y_projection_set_machine",
            "candidate_only": True,
            "route_id": "work_capsule_then_response_packet",
            "materialization_level": "M7",
            "token_budget": "minimal",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        lineage_trace="y_center_first_routing + y_candidate_set_routing + evidence: [repo_route_identified, pattern_selected]",
        work_state_ref="demo_universal_work_capsule",
    )
