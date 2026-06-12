"""FINAL-PR-02 proof packet builder.

Claim boundary: demo_universal_work_proof_candidate_only_no_model_provider_app_apply
"""
from __future__ import annotations

PROOF_CLAIM_BOUNDARY = (
    "demo_universal_work_proof_candidate_only_no_model_provider_app_apply"
)

NOT_PROVEN = [
    "model_inference",
    "provider_execution",
    "real_app_bridge_runtime",
    "external_app_connection",
    "app_apply",
    "external_send",
    "qirc_core_runtime",
    "production_readiness",
    "security_certification",
    "windows_service_installer",
]


def build_final_pr_02_proof_packet() -> dict:
    """Emit the FINAL-PR-02 Demo Universal Work proof packet."""
    return {
        "artifact_kind": "odin_final_pr_02_demo_universal_work_proof_packet",
        "status": "ok_with_known_gaps",
        "candidate_only": True,
        "local_only": True,
        "model_picker_visible": True,
        "connected_apps_visible": True,
        "demo_universal_work_visible": True,
        "response_packet_visible": True,
        "candidate_artifact_visible": True,
        "handoff_context_visible": True,
        "universal_work_packet_visible": True,
        "provider_execution": False,
        "model_inference": False,
        "model_execution": False,
        "app_apply": False,
        "external_send": False,
        "qirc_core_runtime": False,
        "api_key_in_use": False,
        "not_proven": NOT_PROVEN,
        "claim_boundary": PROOF_CLAIM_BOUNDARY,
    }
