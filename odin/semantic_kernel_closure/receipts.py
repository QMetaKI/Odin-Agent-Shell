"""Odin Kernel Receipt Map — describes receipt types in the kernel.

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

_RECEIPT_TYPES = [
    {
        "receipt_type_id": "structural_evidence",
        "receipt_type_name": "Structural Evidence",
        "description": "Repo-local deterministic proof that code, schema, packet, validator, or boundary exists.",
        "generalizable": True,
        "host_scoped": False,
        "external_required": False,
        "stages_using": [
            "universal_work",
            "context_capsule",
            "artifact_lens",
            "slot_contract",
            "gaptext",
            "modelworkpacket",
            "small_model_route",
            "critic_runtime",
            "response_packet",
            "final_gate",
            "trace_receipt_claim",
            "app_owned_apply_boundary",
        ],
    },
    {
        "receipt_type_id": "host_scoped_local_receipt",
        "receipt_type_name": "Host-Scoped Local Receipt",
        "description": "Evidence generated on one local host under explicit local-provider execution permission. Does not generalize.",
        "generalizable": False,
        "host_scoped": True,
        "external_required": False,
        "stages_using": [
            "provider_receipt",
        ],
    },
    {
        "receipt_type_id": "candidate_only_receipt",
        "receipt_type_name": "Candidate-Only Receipt",
        "description": "Receipt that is structural evidence but the underlying capability is advisory or gated.",
        "generalizable": True,
        "host_scoped": False,
        "external_required": False,
        "stages_using": [
            "critic_runtime",
            "candidate_artifact",
        ],
    },
    {
        "receipt_type_id": "external_receipt_required",
        "receipt_type_name": "External Receipt Required",
        "description": "Claim that cannot be satisfied by repo-local proof alone. Requires external audit, benchmark, or certification.",
        "generalizable": False,
        "host_scoped": False,
        "external_required": True,
        "stages_using": [],
        "examples": [
            "production_readiness",
            "security_certification",
            "model_benchmark",
        ],
    },
]


def build_kernel_receipt_map(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build kernel receipt map."""
    return {
        "artifact_kind": "odin_kernel_receipt_map",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "receipt_type_count": len(_RECEIPT_TYPES),
        "receipt_types": _RECEIPT_TYPES,
        "not_proven": NOT_PROVEN,
    }
