"""Operational Spine status reporting.

Claim boundary: final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply"

_SUBSYSTEMS = [
    "model_roles",
    "small_model_route_plan",
    "modelworkpacket_builder",
    "qshabang_runtime_map",
    "deferred_system_lift",
    "provider_seam",
    "receipts",
    "reports",
    "orchestrator",
]

_NOT_PROVEN = [
    "production_readiness",
    "live_model_inference",
    "app_state_mutation",
    "external_send_authority",
]


def get_operational_spine_status() -> dict:
    """Return status of the operational spine package."""
    return {
        "artifact_kind": "odin_operational_spine_status",
        "status": "candidate_schema_only",
        "subsystems_present": list(_SUBSYSTEMS),
        "subsystems_count": len(_SUBSYSTEMS),
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(_NOT_PROVEN),
    }


def get_operational_spine_doctor() -> dict:
    """Return doctor/health dict for operational spine."""
    checks = []
    for subsystem in _SUBSYSTEMS:
        checks.append({
            "subsystem": subsystem,
            "status": "schema_present",
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return {
        "artifact_kind": "odin_operational_spine_doctor",
        "overall": "schema_only_no_live_execution",
        "checks": checks,
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(_NOT_PROVEN),
    }
