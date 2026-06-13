"""Deterministic trace and receipt builders for FINAL-PR-09 Operational Spine.

Claim boundary: final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply
candidate_only: true

All IDs are deterministic SHA256 — no uuid, no random, no non-deterministic timestamps.
"""
from __future__ import annotations

import hashlib
import json

CLAIM_BOUNDARY = "final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply"


def _sha256_id(prefix: str, payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    h = hashlib.sha256(raw.encode()).hexdigest()[:16]
    return f"{prefix}{h}"


def build_trace_ref(
    work_id: str,
    spine_id: str,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> str:
    """Build a deterministic trace ref ID.

    Returns a string with prefix 'operational_trace_'.
    """
    return _sha256_id(
        "operational_trace_",
        {
            "work_id": work_id,
            "spine_id": spine_id,
            "generated_at_utc": generated_at_utc,
            "ref_type": "trace",
        },
    )


def build_receipt_ref(
    work_id: str,
    spine_id: str,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> str:
    """Build a deterministic receipt ref ID.

    Returns a string with prefix 'operational_receipt_'.
    """
    return _sha256_id(
        "operational_receipt_",
        {
            "work_id": work_id,
            "spine_id": spine_id,
            "generated_at_utc": generated_at_utc,
            "ref_type": "receipt",
        },
    )


def build_proof_refs(
    work_id: str,
    spine_id: str,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> list[str]:
    """Build a list of deterministic proof ref IDs.

    Returns a list of proof ref ID strings covering the core
    operational spine proof categories.
    """
    proof_categories = [
        "candidate_only_proof",
        "local_only_proof",
        "no_app_apply_proof",
        "no_external_send_proof",
        "claim_boundary_proof",
        "deterministic_route_proof",
    ]
    refs = []
    for category in proof_categories:
        ref_id = _sha256_id(
            "operational_proof_",
            {
                "work_id": work_id,
                "spine_id": spine_id,
                "generated_at_utc": generated_at_utc,
                "proof_category": category,
            },
        )
        refs.append(ref_id)
    return refs
