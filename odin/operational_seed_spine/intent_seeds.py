"""Intent Seeds — operational routing signals for the Seed Spine.

Claim boundary: operational_seed_spine_routes_work_not_authority
candidate_only: true

Seeds are routing signals. They do not reason. They do not decide. They do not execute.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

CLAIM_BOUNDARY = "operational_seed_spine_routes_work_not_authority"


@dataclass
class IntentSeed:
    seed_id: str
    family: str
    trigger_shapes: List[str]
    input_requirements: List[str]
    output_shape: str
    preferred_surfaces: List[str]
    allowed_use: List[str]
    forbidden_use: List[str]
    qirc_event_hints: List[str]
    validator_expectations: List[str]
    proof_boundary: str
    token_budget_key: str
    fallback_behavior: str

    def to_dict(self) -> dict:
        return {
            "seed_id": self.seed_id,
            "family": self.family,
            "trigger_shapes": self.trigger_shapes,
            "input_requirements": self.input_requirements,
            "output_shape": self.output_shape,
            "preferred_surfaces": self.preferred_surfaces,
            "allowed_use": self.allowed_use,
            "forbidden_use": self.forbidden_use,
            "qirc_event_hints": self.qirc_event_hints,
            "validator_expectations": self.validator_expectations,
            "proof_boundary": self.proof_boundary,
            "token_budget_key": self.token_budget_key,
            "fallback_behavior": self.fallback_behavior,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }


INTENT_SEEDS: List[IntentSeed] = [
    IntentSeed(
        seed_id="repo_cognition",
        family="context",
        trigger_shapes=["repo", "codebase", "repo_cognition", "repo_intake"],
        input_requirements=["repo_context"],
        output_shape="repo_cognition_summary",
        preferred_surfaces=["handoff", "dev_mode"],
        allowed_use=["explore_repo", "summarize_structure", "identify_patterns"],
        forbidden_use=["app_apply", "external_send", "model_inference", "provider_execution"],
        qirc_event_hints=["work_seed_selected", "repo_cognition_started"],
        validator_expectations=["validate-operational-seed-spine"],
        proof_boundary=CLAIM_BOUNDARY,
        token_budget_key="medium",
        fallback_behavior="return_empty_cognition_summary",
    ),
    IntentSeed(
        seed_id="prompt_to_work",
        family="route",
        trigger_shapes=["prompt", "task", "instruction", "work_request"],
        input_requirements=["prompt_text", "work_context"],
        output_shape="work_packet_candidate",
        preferred_surfaces=["handoff", "dev_mode", "worker"],
        allowed_use=["compile_work_packet", "route_to_seed", "prepare_candidate"],
        forbidden_use=["app_apply", "external_send", "model_inference", "autonomous_execution"],
        qirc_event_hints=["work_seed_selected", "prompt_routed"],
        validator_expectations=["validate-operational-seed-spine"],
        proof_boundary=CLAIM_BOUNDARY,
        token_budget_key="small",
        fallback_behavior="return_unrouted_work_packet",
    ),
    IntentSeed(
        seed_id="code_change",
        family="compiler",
        trigger_shapes=["code", "edit", "fix", "implement", "code_change"],
        input_requirements=["file_path", "change_description"],
        output_shape="code_change_candidate",
        preferred_surfaces=["worker", "dev_mode"],
        allowed_use=["prepare_code_candidate", "scope_change", "bound_edit"],
        forbidden_use=["app_apply", "external_send", "model_inference", "hidden_execution"],
        qirc_event_hints=["work_seed_selected", "code_change_scoped"],
        validator_expectations=["validate-operational-seed-spine"],
        proof_boundary=CLAIM_BOUNDARY,
        token_budget_key="large",
        fallback_behavior="return_bounded_noop_candidate",
    ),
    IntentSeed(
        seed_id="review_audit",
        family="evidence",
        trigger_shapes=["review", "audit", "check", "verify", "review_audit"],
        input_requirements=["target_artifact", "review_axes"],
        output_shape="review_report_candidate",
        preferred_surfaces=["dev_mode", "handoff"],
        allowed_use=["prepare_review_candidate", "audit_artifact", "check_boundaries"],
        forbidden_use=["app_apply", "external_send", "model_inference", "security_certification"],
        qirc_event_hints=["work_seed_selected", "review_audit_started"],
        validator_expectations=["validate-operational-seed-spine"],
        proof_boundary=CLAIM_BOUNDARY,
        token_budget_key="audit",
        fallback_behavior="return_empty_review_candidate",
    ),
    IntentSeed(
        seed_id="proof_receipt",
        family="evidence",
        trigger_shapes=["proof", "receipt", "prove", "proof_receipt"],
        input_requirements=["proven_list", "not_proven_list"],
        output_shape="proof_packet_candidate",
        preferred_surfaces=["dev_mode", "handoff"],
        allowed_use=["compile_proof_packet", "bind_proof_receipt", "validate_boundaries"],
        forbidden_use=["app_apply", "external_send", "claim_without_receipt", "production_readiness_claim"],
        qirc_event_hints=["work_seed_selected", "proof_receipt_bound"],
        validator_expectations=["validate-operational-seed-spine"],
        proof_boundary=CLAIM_BOUNDARY,
        token_budget_key="small",
        fallback_behavior="return_empty_proof_packet",
    ),
    IntentSeed(
        seed_id="local_hub_ui",
        family="context",
        trigger_shapes=["ui", "hub", "local_hub", "local_hub_ui", "frontend"],
        input_requirements=["hub_status"],
        output_shape="hub_ui_candidate",
        preferred_surfaces=["local_hub", "dev_mode"],
        allowed_use=["prepare_hub_ui_candidate", "render_status_hint", "display_dev_mode"],
        forbidden_use=["app_apply", "external_send", "model_inference", "production_deploy"],
        qirc_event_hints=["work_seed_selected", "hub_ui_prepared"],
        validator_expectations=["validate-operational-seed-spine"],
        proof_boundary=CLAIM_BOUNDARY,
        token_budget_key="small",
        fallback_behavior="return_minimal_hub_status",
    ),
    IntentSeed(
        seed_id="provider_probe",
        family="route",
        trigger_shapes=["provider", "probe", "provider_probe", "model_probe"],
        input_requirements=["provider_id"],
        output_shape="provider_probe_candidate",
        preferred_surfaces=["dev_mode", "local_hub"],
        allowed_use=["probe_provider_status", "check_availability", "candidate_only_probe"],
        forbidden_use=["provider_execution", "model_inference", "app_apply", "external_network"],
        qirc_event_hints=["work_seed_selected", "provider_probe_initiated"],
        validator_expectations=["validate-operational-seed-spine"],
        proof_boundary=CLAIM_BOUNDARY,
        token_budget_key="tiny",
        fallback_behavior="return_provider_unavailable_candidate",
    ),
    IntentSeed(
        seed_id="execution_gate",
        family="boundary",
        trigger_shapes=["gate", "execution", "execution_gate", "guard"],
        input_requirements=["gate_context"],
        output_shape="gate_decision_candidate",
        preferred_surfaces=["dev_mode", "worker"],
        allowed_use=["check_gate_policy", "prepare_gate_candidate", "boundary_check"],
        forbidden_use=["app_apply", "external_send", "autonomous_execution", "bypass_gate"],
        qirc_event_hints=["work_seed_selected", "execution_gate_checked"],
        validator_expectations=["validate-operational-seed-spine"],
        proof_boundary=CLAIM_BOUNDARY,
        token_budget_key="tiny",
        fallback_behavior="return_gate_blocked_candidate",
    ),
    IntentSeed(
        seed_id="qirc_event",
        family="qirc",
        trigger_shapes=["qirc", "event", "channel", "qirc_event", "bus_event"],
        input_requirements=["event_type", "channel"],
        output_shape="qirc_hint_record",
        preferred_surfaces=["dev_mode"],
        allowed_use=["prepare_qirc_hint", "map_event_type", "hint_only_record"],
        forbidden_use=["emit_real_event", "mutate_bus", "authorize_action", "external_send"],
        qirc_event_hints=["work_seed_selected"],
        validator_expectations=["validate-operational-seed-spine"],
        proof_boundary=CLAIM_BOUNDARY,
        token_budget_key="tiny",
        fallback_behavior="return_empty_hint_record",
    ),
    IntentSeed(
        seed_id="release_closure",
        family="boundary",
        trigger_shapes=["release", "closure", "final", "release_closure"],
        input_requirements=["release_context"],
        output_shape="release_closure_candidate",
        preferred_surfaces=["handoff", "dev_mode"],
        allowed_use=["prepare_release_candidate", "scope_closure", "finalize_boundaries"],
        forbidden_use=["app_apply", "external_send", "autonomous_deploy", "production_release"],
        qirc_event_hints=["work_seed_selected", "release_closure_scoped"],
        validator_expectations=["validate-operational-seed-spine"],
        proof_boundary=CLAIM_BOUNDARY,
        token_budget_key="medium",
        fallback_behavior="return_noop_release_candidate",
    ),
    IntentSeed(
        seed_id="doc_architecture",
        family="context",
        trigger_shapes=["doc", "architecture", "design", "doc_architecture", "spec"],
        input_requirements=["doc_context"],
        output_shape="doc_candidate",
        preferred_surfaces=["handoff", "dev_mode"],
        allowed_use=["prepare_doc_candidate", "scope_architecture", "summarize_design"],
        forbidden_use=["app_apply", "external_send", "model_inference", "publish_without_review"],
        qirc_event_hints=["work_seed_selected", "doc_architecture_scoped"],
        validator_expectations=["validate-operational-seed-spine"],
        proof_boundary=CLAIM_BOUNDARY,
        token_budget_key="medium",
        fallback_behavior="return_empty_doc_candidate",
    ),
    IntentSeed(
        seed_id="debug_error_triage",
        family="evidence",
        trigger_shapes=["debug", "error", "triage", "debug_error_triage", "fix_error"],
        input_requirements=["error_context", "stack_trace"],
        output_shape="triage_candidate",
        preferred_surfaces=["dev_mode", "worker"],
        allowed_use=["triage_error", "scope_fix", "prepare_debug_candidate"],
        forbidden_use=["app_apply", "external_send", "model_inference", "production_rollback"],
        qirc_event_hints=["work_seed_selected", "debug_triage_started"],
        validator_expectations=["validate-operational-seed-spine"],
        proof_boundary=CLAIM_BOUNDARY,
        token_budget_key="small",
        fallback_behavior="return_empty_triage_candidate",
    ),
]

_SEED_INDEX: dict[str, IntentSeed] = {s.seed_id: s for s in INTENT_SEEDS}

REQUIRED_SEED_IDS = [
    "repo_cognition",
    "prompt_to_work",
    "code_change",
    "review_audit",
    "proof_receipt",
    "local_hub_ui",
    "provider_probe",
    "execution_gate",
    "qirc_event",
    "release_closure",
    "doc_architecture",
    "debug_error_triage",
]


def get_seed(seed_id: str) -> IntentSeed | None:
    return _SEED_INDEX.get(seed_id)
