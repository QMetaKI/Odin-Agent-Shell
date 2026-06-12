"""Materialization Ladder M0–M9.

Claim boundary: y_pattern_spine_candidate_only_no_app_apply_no_provider_no_runtime_authority
candidate_only: true
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

CLAIM_BOUNDARY = "y_pattern_spine_candidate_only_no_app_apply_no_provider_no_runtime_authority"


@dataclass
class YMaterializationLevel:
    level: str
    label: str
    description: str
    allowed_claims: List[str]
    forbidden_claims: List[str]

    def to_dict(self) -> dict:
        return {
            "level": self.level,
            "label": self.label,
            "description": self.description,
            "allowed_claims": self.allowed_claims,
            "forbidden_claims": self.forbidden_claims,
        }


MATERIALIZATION_LADDER: List[YMaterializationLevel] = [
    YMaterializationLevel(
        level="M0",
        label="intent_only",
        description="Intent captured only. No route selected.",
        allowed_claims=["intent_seed_present"],
        forbidden_claims=["route_selected", "work_prepared", "patch_ready"],
    ),
    YMaterializationLevel(
        level="M1",
        label="repo_route_identified",
        description="Repository route identified. Files and surfaces known.",
        allowed_claims=["intent_seed_present", "repo_route_identified"],
        forbidden_claims=["pattern_selected", "work_prepared", "patch_ready"],
    ),
    YMaterializationLevel(
        level="M2",
        label="pattern_profile_selected",
        description="Pattern and profile selected. Route hint available.",
        allowed_claims=["intent_seed_present", "repo_route_identified", "pattern_selected"],
        forbidden_claims=["depth_mode_selected", "work_prepared", "patch_ready"],
    ),
    YMaterializationLevel(
        level="M3",
        label="depth_mode_selected",
        description="Depth mode selected: minimal/normal/deep.",
        allowed_claims=["intent_seed_present", "repo_route_identified", "pattern_selected", "depth_mode_selected"],
        forbidden_claims=["expression_prepared", "patch_ready"],
    ),
    YMaterializationLevel(
        level="M4",
        label="expression_packet_prepared",
        description="Expression packet prepared. Human-readable projection available.",
        allowed_claims=["expression_packet_present", "normal_user_summary_available"],
        forbidden_claims=["shadow_candidate_prepared", "patch_ready"],
    ),
    YMaterializationLevel(
        level="M5",
        label="shadow_candidate_graph_prepared",
        description="Shadow candidate graph prepared. Compile-near shape visible.",
        allowed_claims=["shadow_candidate_shape_present"],
        forbidden_claims=["output_mode_selected", "patch_ready"],
    ),
    YMaterializationLevel(
        level="M6",
        label="output_mode_selected",
        description="Output mode selected: patch/report/response.",
        allowed_claims=["output_mode_present"],
        forbidden_claims=["worker_prompt_scoped", "patch_ready"],
    ),
    YMaterializationLevel(
        level="M7",
        label="worker_prompt_scoped",
        description="Worker prompt scoped. Token budget applied.",
        allowed_claims=["worker_prompt_present", "token_budget_applied"],
        forbidden_claims=["candidate_patch_prepared"],
    ),
    YMaterializationLevel(
        level="M8",
        label="candidate_patch_prepared",
        description="Candidate patch prepared. Not applied. App owns apply decision.",
        allowed_claims=["candidate_patch_present"],
        forbidden_claims=["app_applied", "external_sent", "production_verified"],
    ),
    YMaterializationLevel(
        level="M9",
        label="external_receipt_required",
        description="External receipt required for further claims.",
        allowed_claims=["external_receipt_required_flag_set"],
        forbidden_claims=["production_verified", "security_certified", "deployed"],
    ),
]

_LEVEL_MAP: Dict[str, YMaterializationLevel] = {lv.level: lv for lv in MATERIALIZATION_LADDER}


def get_level(level: str) -> Optional[YMaterializationLevel]:
    return _LEVEL_MAP.get(level)


def list_levels() -> List[str]:
    return [lv.level for lv in MATERIALIZATION_LADDER]
