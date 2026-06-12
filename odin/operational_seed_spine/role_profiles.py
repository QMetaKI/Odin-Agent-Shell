"""Role Profiles — bounded behavioral contracts for seed spine work.

Claim boundary: operational_seed_spine_routes_work_not_authority
candidate_only: true

Role profiles are not personas. They are not runtime actors.
They are bounded behavioral contracts that shape work routing.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

CLAIM_BOUNDARY = "operational_seed_spine_routes_work_not_authority"

FORBIDDEN_PROFILE_IDS = frozenset([
    "thor", "odin", "loki", "maria", "michael", "y", "mjolnir", "q", "qstar",
])


@dataclass
class RoleProfile:
    role_profile_id: str
    family: str
    allowed_use: List[str]
    forbidden_use: List[str]
    review_axes: List[str]
    output_shape: str
    claim_boundary: str = CLAIM_BOUNDARY

    def __post_init__(self) -> None:
        if self.role_profile_id in FORBIDDEN_PROFILE_IDS:
            raise ValueError(f"Forbidden role_profile_id: {self.role_profile_id!r}")

    def to_dict(self) -> dict:
        return {
            "role_profile_id": self.role_profile_id,
            "family": self.family,
            "allowed_use": self.allowed_use,
            "forbidden_use": self.forbidden_use,
            "review_axes": self.review_axes,
            "output_shape": self.output_shape,
            "claim_boundary": self.claim_boundary,
            "candidate_only": True,
        }


ROLE_PROFILES: List[RoleProfile] = [
    RoleProfile(
        role_profile_id="builder",
        family="compiler",
        allowed_use=["prepare_code_candidate", "scope_implementation", "compile_work_packet"],
        forbidden_use=["app_apply", "external_send", "autonomous_execution", "model_inference"],
        review_axes=["scope_boundary", "candidate_only", "no_hidden_authority"],
        output_shape="implementation_candidate",
        claim_boundary=CLAIM_BOUNDARY,
    ),
    RoleProfile(
        role_profile_id="reviewer",
        family="evidence",
        allowed_use=["audit_artifact", "check_boundaries", "prepare_review_candidate"],
        forbidden_use=["app_apply", "external_send", "approve_production", "security_certification"],
        review_axes=["completeness", "boundary_integrity", "proof_coverage", "scope_control"],
        output_shape="review_report_candidate",
        claim_boundary=CLAIM_BOUNDARY,
    ),
    RoleProfile(
        role_profile_id="guard",
        family="boundary",
        allowed_use=["check_gate_policy", "boundary_check", "scope_guard"],
        forbidden_use=["app_apply", "external_send", "bypass_gate", "autonomous_enforcement"],
        review_axes=["boundary_integrity", "no_hidden_authority", "candidate_only"],
        output_shape="gate_decision_candidate",
        claim_boundary=CLAIM_BOUNDARY,
    ),
    RoleProfile(
        role_profile_id="router",
        family="route",
        allowed_use=["select_seed_route", "map_work_context", "deterministic_routing"],
        forbidden_use=["app_apply", "external_send", "model_inference", "autonomous_routing"],
        review_axes=["determinism", "fallback_visibility", "selection_priority_clarity"],
        output_shape="seed_route",
        claim_boundary=CLAIM_BOUNDARY,
    ),
    RoleProfile(
        role_profile_id="materializer",
        family="compiler",
        allowed_use=["compile_work_capsule", "bind_capsule_fields", "prepare_materialization"],
        forbidden_use=["app_apply", "external_send", "execute_capsule", "model_inference"],
        review_axes=["capsule_completeness", "determinism", "candidate_only"],
        output_shape="seed_work_capsule",
        claim_boundary=CLAIM_BOUNDARY,
    ),
    RoleProfile(
        role_profile_id="proof_binder",
        family="evidence",
        allowed_use=["compile_proof_packet", "bind_proof_receipt", "list_not_proven"],
        forbidden_use=["claim_without_receipt", "production_readiness_claim", "external_send"],
        review_axes=["proof_completeness", "not_proven_accuracy", "boundary_integrity"],
        output_shape="proof_packet",
        claim_boundary=CLAIM_BOUNDARY,
    ),
    RoleProfile(
        role_profile_id="scope_compressor",
        family="economy",
        allowed_use=["compress_scope", "token_budget_check", "scope_trim"],
        forbidden_use=["app_apply", "external_send", "model_inference", "silent_scope_drop"],
        review_axes=["compression_visibility", "budget_accuracy", "no_silent_truncation"],
        output_shape="compressed_scope_candidate",
        claim_boundary=CLAIM_BOUNDARY,
    ),
    RoleProfile(
        role_profile_id="lineage_tracker",
        family="evidence",
        allowed_use=["track_artifact_lineage", "bind_source_reference", "audit_chain"],
        forbidden_use=["app_apply", "external_send", "mutate_lineage", "forge_receipt"],
        review_axes=["lineage_integrity", "source_accuracy", "chain_completeness"],
        output_shape="lineage_record",
        claim_boundary=CLAIM_BOUNDARY,
    ),
    RoleProfile(
        role_profile_id="devmode_explainer",
        family="context",
        allowed_use=["explain_dev_mode", "surface_candidate_info", "display_boundaries"],
        forbidden_use=["app_apply", "external_send", "overclaim_capability", "mislead_user"],
        review_axes=["copy_accuracy", "no_overclaim", "boundary_clarity"],
        output_shape="dev_mode_explanation",
        claim_boundary=CLAIM_BOUNDARY,
    ),
    RoleProfile(
        role_profile_id="risk_scanner",
        family="safety",
        allowed_use=["scan_for_boundary_violations", "check_forbidden_patterns", "flag_risk"],
        forbidden_use=["app_apply", "external_send", "autonomous_remediation", "security_certification"],
        review_axes=["violation_detection", "false_positive_rate", "boundary_accuracy"],
        output_shape="risk_scan_candidate",
        claim_boundary=CLAIM_BOUNDARY,
    ),
]

REQUIRED_ROLE_PROFILE_IDS = [
    "builder",
    "reviewer",
    "guard",
    "router",
    "materializer",
    "proof_binder",
    "scope_compressor",
    "lineage_tracker",
    "devmode_explainer",
    "risk_scanner",
]

_PROFILE_INDEX: dict[str, RoleProfile] = {p.role_profile_id: p for p in ROLE_PROFILES}


def get_role_profile(role_profile_id: str) -> RoleProfile | None:
    return _PROFILE_INDEX.get(role_profile_id)
