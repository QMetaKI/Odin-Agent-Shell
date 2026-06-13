"""Model Role Authority Matrix — FINAL-PR-10++.

Claim boundary: final_pr_10_boundary_gated_release_operationalization_not_release_certification
candidate_only: true
app_owned_apply: true

Defines authority limits for all model roles in the Odin system.
Model roles are work routing plans — not authority grants.
Local provider candidate remains disabled by default.
"""
from __future__ import annotations

import hashlib
import json

_CLAIM_BOUNDARY = "final_pr_10_boundary_gated_release_operationalization_not_release_certification"
_GENERATED_AT = "2026-01-01T00:00:00Z"

_FORBIDDEN_FOR_ALL = [
    "app_apply",
    "app_state_mutation",
    "external_send",
    "public_network",
    "truth_authority",
    "release_certification",
    "security_certification",
    "production_readiness_claim",
]


def _make_id(role_id: str) -> str:
    digest = hashlib.sha256(f"model_role_authority_{role_id}".encode()).hexdigest()[:16]
    return f"model_role_authority_{role_id}_{digest}"


_ROLES = [
    # 3B roles
    {
        "role_id": "3b_scout",
        "model_tier": "3b",
        "allowed_inputs": ["work_context", "trigger_shape", "repo_summary"],
        "allowed_outputs": ["route_hint", "scout_candidate"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "candidate_route_suggestion_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "3b_extractor",
        "model_tier": "3b",
        "allowed_inputs": ["raw_text", "work_context"],
        "allowed_outputs": ["extracted_fields", "slot_values"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "field_extraction_candidate_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "3b_classifier",
        "model_tier": "3b",
        "allowed_inputs": ["input_text", "classification_schema"],
        "allowed_outputs": ["class_candidate", "confidence_score"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "classification_candidate_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "3b_router",
        "model_tier": "3b",
        "allowed_inputs": ["work_packet", "route_schema"],
        "allowed_outputs": ["route_decision_candidate"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "route_decision_candidate_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "3b_slot_filler",
        "model_tier": "3b",
        "allowed_inputs": ["slot_schema", "work_context"],
        "allowed_outputs": ["filled_slot_candidate"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "slot_fill_candidate_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "3b_quick_critic",
        "model_tier": "3b",
        "allowed_inputs": ["candidate_artifact", "critic_criteria"],
        "allowed_outputs": ["critic_verdict_candidate"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "quick_critic_candidate_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "3b_style_check",
        "model_tier": "3b",
        "allowed_inputs": ["candidate_text", "style_criteria"],
        "allowed_outputs": ["style_check_candidate"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "style_check_candidate_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "3b_refusal_boundary_check",
        "model_tier": "3b",
        "allowed_inputs": ["candidate_artifact", "boundary_criteria"],
        "allowed_outputs": ["boundary_check_result_candidate"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "boundary_check_candidate_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    # 7B roles
    {
        "role_id": "7b_writer",
        "model_tier": "7b",
        "allowed_inputs": ["work_context", "output_contract", "seed_route"],
        "allowed_outputs": ["draft_candidate"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "draft_writing_candidate_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "7b_synthesizer",
        "model_tier": "7b",
        "allowed_inputs": ["multi_source_context", "synthesis_schema"],
        "allowed_outputs": ["synthesis_candidate"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "synthesis_candidate_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "7b_planner",
        "model_tier": "7b",
        "allowed_inputs": ["work_context", "planning_schema"],
        "allowed_outputs": ["plan_candidate"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "planning_candidate_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "7b_repo_reasoner",
        "model_tier": "7b",
        "allowed_inputs": ["repo_context", "reasoning_schema"],
        "allowed_outputs": ["repo_reasoning_candidate"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "repo_reasoning_candidate_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "7b_candidate_composer",
        "model_tier": "7b",
        "allowed_inputs": ["projection_set", "output_contract"],
        "allowed_outputs": ["composed_candidate"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "candidate_composition_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "7b_refiner",
        "model_tier": "7b",
        "allowed_inputs": ["draft_candidate", "refinement_criteria"],
        "allowed_outputs": ["refined_candidate"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "candidate_refinement_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "7b_complex_critic",
        "model_tier": "7b",
        "allowed_inputs": ["candidate_artifact", "complex_critic_criteria"],
        "allowed_outputs": ["complex_critic_verdict_candidate"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "complex_critic_candidate_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    # Hybrid roles
    {
        "role_id": "hybrid_3b_scout_7b_synthesize_3b_check",
        "model_tier": "3b_7b_hybrid",
        "allowed_inputs": ["work_context", "output_contract"],
        "allowed_outputs": ["hybrid_candidate_artifact"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "hybrid_candidate_route_plan_not_benchmark",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "hybrid_3b_extract_7b_compose_3b_boundary_critic",
        "model_tier": "3b_7b_hybrid",
        "allowed_inputs": ["raw_input", "output_contract"],
        "allowed_outputs": ["hybrid_composed_candidate"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "hybrid_extract_compose_candidate_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "hybrid_7b_draft_3b_slot_check_7b_refine",
        "model_tier": "3b_7b_hybrid",
        "allowed_inputs": ["work_context", "slot_schema", "refinement_criteria"],
        "allowed_outputs": ["hybrid_refined_candidate"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "hybrid_draft_check_refine_candidate_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "hybrid_no_model_precompute_3b_route_7b_candidate_final_gate",
        "model_tier": "3b_7b_hybrid",
        "allowed_inputs": ["work_context"],
        "allowed_outputs": ["hybrid_precompute_route_candidate"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "hybrid_precompute_route_candidate_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    # Special roles
    {
        "role_id": "deterministic_no_model_worker",
        "model_tier": "no_model",
        "allowed_inputs": ["work_context", "deterministic_rules"],
        "allowed_outputs": ["deterministic_candidate"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "deterministic_candidate_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "mock_provider",
        "model_tier": "mock",
        "allowed_inputs": ["modelworkpacket"],
        "allowed_outputs": ["mock_candidate_artifact"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL,
        "authority_limit": "mock_deterministic_candidate_only",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness"],
    },
    {
        "role_id": "local_provider_candidate",
        "model_tier": "local_candidate",
        "allowed_inputs": ["modelworkpacket"],
        "allowed_outputs": ["local_provider_candidate_artifact"],
        "forbidden_actions": _FORBIDDEN_FOR_ALL + ["provider_execution_without_receipt"],
        "authority_limit": "local_provider_candidate_disabled_by_default",
        "candidate_only_required": True,
        "final_gate_required": True,
        "receipt_required": True,
        "disabled_by_default": True,
        "not_proven": ["live_model_inference", "real_model_benchmark", "production_readiness", "provider_execution"],
    },
]


def build_model_role_authority_matrix() -> dict:
    """Build the model role authority matrix.

    All roles are work routing plans — not authority grants.
    Every role forbids app_apply, external_send, and truth_authority.
    Local provider candidate remains disabled by default.
    """
    roles = {}
    for role in _ROLES:
        rid = role["role_id"]
        roles[rid] = dict(
            role,
            model_role_authority_id=_make_id(rid),
            claim_boundary=_CLAIM_BOUNDARY,
        )

    return json.loads(json.dumps({
        "artifact_kind": "odin_final_pr_10_model_role_authority_matrix",
        "candidate_only": True,
        "app_owned_apply": True,
        "claim_boundary": _CLAIM_BOUNDARY,
        "generated_at_utc": _GENERATED_AT,
        "axioms": [
            "Model roles are work routing plans — not authority grants.",
            "Hybrid plan is not an empirical benchmark.",
            "Local provider candidate remains disabled by default.",
            "Every role forbids app_apply, external_send, and truth_authority.",
        ],
        "role_count": len(roles),
        "roles": roles,
        "forbidden_for_all_roles": _FORBIDDEN_FOR_ALL,
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "real_model_benchmark",
            "app_state_mutation",
            "external_send_authority",
            "security_certification",
            "release_certification",
        ],
        "final_pr_11_remains_deferred": True,
    }))
