"""Odin Semantic Kernel Closure Report — combined report.

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


def build_semantic_kernel_closure_report(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build combined semantic kernel closure report."""
    from .ir import build_odin_work_ir
    from .pipeline import build_semantic_kernel_pipeline
    from .contracts import build_kernel_contract_map
    from .receipts import build_kernel_receipt_map

    ir = build_odin_work_ir(generated_at_utc=generated_at_utc)
    pipeline = build_semantic_kernel_pipeline(generated_at_utc=generated_at_utc)
    contracts = build_kernel_contract_map(generated_at_utc=generated_at_utc)
    receipts = build_kernel_receipt_map(generated_at_utc=generated_at_utc)

    return {
        "artifact_kind": "odin_semantic_kernel_closure_report",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "summary": {
            "ir_objects": ir["ir_object_count"],
            "pipeline_stages": pipeline["stage_count"],
            "contracts": contracts["contract_count"],
            "receipt_types": receipts["receipt_type_count"],
        },
        "ir": ir,
        "pipeline": pipeline,
        "contracts": contracts,
        "receipts": receipts,
        "not_proven": NOT_PROVEN,
    }
