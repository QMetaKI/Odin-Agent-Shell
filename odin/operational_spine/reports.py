"""Operational Spine report builder for FINAL-PR-09.

Claim boundary: final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply
candidate_only: true

Builds and saves JSON reports from operational spine results.
No model execution, no provider calls, no app state mutations.
"""
from __future__ import annotations

import hashlib
import json
import pathlib

CLAIM_BOUNDARY = "final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply"

_NOT_PROVEN = [
    "production_readiness",
    "live_model_inference",
    "app_state_mutation",
    "external_send_authority",
]


def _sha256_id(prefix: str, payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    h = hashlib.sha256(raw.encode()).hexdigest()[:16]
    return f"{prefix}{h}"


def build_operational_spine_report(
    result: dict,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build an operational spine report from a result dict.

    Returns a candidate-only report dict. No execution, no app state.
    """
    work_id = result.get("work_id", "unknown_work_id")
    spine_id = result.get("spine_id", "unknown_spine_id")

    report_id = _sha256_id(
        "operational_report_",
        {
            "work_id": work_id,
            "spine_id": spine_id,
            "generated_at_utc": generated_at_utc,
        },
    )

    # Extract key summary fields from result
    status = result.get("status", "unknown")
    candidate_only = result.get("candidate_only", True)
    claim_boundary = result.get("claim_boundary", CLAIM_BOUNDARY)
    not_proven = result.get("not_proven", list(_NOT_PROVEN))

    # Summarize sub-packets present in result
    packets_present = []
    for key in (
        "handoff_context",
        "universal_work",
        "validation_result",
        "context_capsule",
        "artifact_lens",
        "slot_contract",
        "gaptext",
        "precompute_result",
        "modelworkpacket",
        "small_model_route_plan",
        "model_role_assignment",
        "seed_route",
        "field_selection",
        "projection_candidate",
        "provider_seam_packet",
        "candidate_artifact",
        "final_gate",
        "response_packet",
        "trace_ref",
        "receipt_ref",
        "proof_refs",
        "qirc_hint_refs",
    ):
        if key in result:
            packets_present.append(key)

    return {
        "artifact_kind": "odin_operational_spine_report",
        "report_id": report_id,
        "work_id": work_id,
        "spine_id": spine_id,
        "generated_at_utc": generated_at_utc,
        "status": status,
        "packets_present": packets_present,
        "packets_count": len(packets_present),
        "candidate_only": candidate_only,
        "local_only": True,
        "app_owned_apply": True,
        "claim_boundary": claim_boundary,
        "not_proven": list(not_proven),
        "result_summary": {
            "work_id": work_id,
            "spine_id": spine_id,
            "status": status,
            "candidate_only": candidate_only,
            "claim_boundary": claim_boundary,
        },
    }


def save_report(report: dict, path) -> None:
    """Save a report dict as JSON to the given path.

    path may be a str or pathlib.Path.
    Creates parent directories if needed.
    """
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, sort_keys=True)
