"""Odin Kernel Map — constant map of kernel components.

Claim boundary: semantic_kernel_closure_compiles_odin_kernel_ir_not_runtime_completion
candidate_only: true
"""
from __future__ import annotations

KERNEL_MAP: dict = {
    "kernel_id": "odin_semantic_kernel_v711",
    "candidate_only": True,
    "claim_boundary": "semantic_kernel_closure_compiles_odin_kernel_ir_not_runtime_completion",
    "stages": [
        "universal_work",
        "context_capsule",
        "artifact_lens",
        "slot_contract",
        "gaptext",
        "modelworkpacket",
        "small_model_route",
        "provider_receipt",
        "critic_runtime",
        "candidate_artifact",
        "response_packet",
        "final_gate",
        "trace_receipt_claim",
        "app_owned_apply_boundary",
    ],
    "ir_objects": [
        "UniversalWorkIR",
        "ContextIR",
        "ArtifactLensIR",
        "SlotIR",
        "GaptextIR",
        "ModelWorkIR",
        "RouteIR",
        "ProviderReceiptIR",
        "CriticIR",
        "CandidateIR",
        "ResponseIR",
        "FinalGateIR",
        "ReceiptIR",
        "ClaimIR",
        "SemanticBusEventIR",
        "AgentHandoffIR",
    ],
    "forbidden_authority": [
        "app_apply",
        "external_send",
        "live_inference_without_receipt",
        "agent_autonomy",
        "odin_apply",
    ],
    "not_proven": [
        "production_readiness",
        "live_model_inference",
        "app_state_mutation",
        "external_send_authority",
    ],
}


def build_kernel_map() -> dict:
    """Return the kernel map constant."""
    return KERNEL_MAP
