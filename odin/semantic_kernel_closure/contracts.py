"""Odin Kernel Contract Map — input/output contracts between pipeline stages.

Claim boundary: semantic_kernel_closure_compiles_odin_kernel_ir_not_runtime_completion
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "semantic_kernel_closure_compiles_odin_kernel_ir_not_runtime_completion"

NOT_PROVEN = [
    "production_readiness",
    "live_model_inference",
    "app_state_mutation",
    "external_send_authority",
]

_CONTRACTS = [
    {
        "contract_id": "work_to_context",
        "from_stage": "universal_work",
        "to_stage": "context_capsule",
        "input_type": "UniversalWorkInput",
        "output_type": "ContextIR",
        "required_fields": ["input_text", "candidate_only"],
        "forbidden_fields": ["app_apply", "external_send"],
    },
    {
        "contract_id": "context_to_lens",
        "from_stage": "context_capsule",
        "to_stage": "artifact_lens",
        "input_type": "ContextIR",
        "output_type": "ArtifactLensIR",
        "required_fields": ["context_capsule", "candidate_only"],
        "forbidden_fields": ["app_apply", "external_send"],
    },
    {
        "contract_id": "lens_to_slot",
        "from_stage": "artifact_lens",
        "to_stage": "slot_contract",
        "input_type": "ArtifactLensIR",
        "output_type": "SlotIR",
        "required_fields": ["artifact_view", "candidate_only"],
        "forbidden_fields": ["app_apply", "external_send"],
    },
    {
        "contract_id": "slot_to_gaptext",
        "from_stage": "slot_contract",
        "to_stage": "gaptext",
        "input_type": "SlotIR",
        "output_type": "GaptextIR",
        "required_fields": ["slot_contract", "candidate_only"],
        "forbidden_fields": ["app_apply", "external_send"],
    },
    {
        "contract_id": "gaptext_to_mwp",
        "from_stage": "gaptext",
        "to_stage": "modelworkpacket",
        "input_type": "GaptextIR",
        "output_type": "ModelWorkIR",
        "required_fields": ["gaptext_output", "candidate_only"],
        "forbidden_fields": ["app_apply", "external_send"],
    },
    {
        "contract_id": "mwp_to_route",
        "from_stage": "modelworkpacket",
        "to_stage": "small_model_route",
        "input_type": "ModelWorkIR",
        "output_type": "RouteIR",
        "required_fields": ["model_work_packet", "route_hint", "candidate_only"],
        "forbidden_fields": ["app_apply", "external_send"],
    },
    {
        "contract_id": "route_to_provider",
        "from_stage": "small_model_route",
        "to_stage": "provider_receipt",
        "input_type": "RouteIR",
        "output_type": "ProviderReceiptIR",
        "required_fields": ["route_plan", "candidate_only"],
        "forbidden_fields": ["app_apply", "external_send", "live_inference_without_flag"],
    },
    {
        "contract_id": "provider_to_critic",
        "from_stage": "provider_receipt",
        "to_stage": "critic_runtime",
        "input_type": "ProviderReceiptIR",
        "output_type": "CriticIR",
        "required_fields": ["provider_receipt", "candidate_only"],
        "forbidden_fields": ["app_apply", "external_send", "final_authority"],
    },
    {
        "contract_id": "critic_to_candidate",
        "from_stage": "critic_runtime",
        "to_stage": "candidate_artifact",
        "input_type": "CriticIR",
        "output_type": "CandidateIR",
        "required_fields": ["critic_packet", "not_authority", "candidate_only"],
        "forbidden_fields": ["app_apply", "external_send"],
    },
    {
        "contract_id": "candidate_to_response",
        "from_stage": "candidate_artifact",
        "to_stage": "response_packet",
        "input_type": "CandidateIR",
        "output_type": "ResponseIR",
        "required_fields": ["candidate_artifact", "candidate_only"],
        "forbidden_fields": ["app_apply", "external_send"],
    },
    {
        "contract_id": "response_to_gate",
        "from_stage": "response_packet",
        "to_stage": "final_gate",
        "input_type": "ResponseIR",
        "output_type": "FinalGateIR",
        "required_fields": ["response_packet", "candidate_only"],
        "forbidden_fields": ["app_apply", "external_send"],
    },
    {
        "contract_id": "gate_to_receipt",
        "from_stage": "final_gate",
        "to_stage": "trace_receipt_claim",
        "input_type": "FinalGateIR",
        "output_type": "ReceiptIR",
        "required_fields": ["gate_result", "candidate_only"],
        "forbidden_fields": ["app_apply", "external_send"],
    },
    {
        "contract_id": "receipt_to_app_boundary",
        "from_stage": "trace_receipt_claim",
        "to_stage": "app_owned_apply_boundary",
        "input_type": "ReceiptIR",
        "output_type": "AppDecision",
        "required_fields": ["receipt", "not_proven", "candidate_only"],
        "forbidden_fields": ["odin_apply", "odin_external_send"],
    },
]


def build_kernel_contract_map(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build kernel contract map."""
    return {
        "artifact_kind": "odin_kernel_contract_map",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "contract_count": len(_CONTRACTS),
        "contracts": _CONTRACTS,
        "not_proven": NOT_PROVEN,
    }
