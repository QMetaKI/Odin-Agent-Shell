"""Simple Local Hub proof packet builder — FINAL-PR-01.

Claim boundary: simple_local_hub_local_receipt_not_runtime_completion_not_production
"""
from __future__ import annotations

PROOF_CLAIM_BOUNDARY = "simple_local_hub_local_receipt_not_runtime_completion_not_production"

NOT_PROVEN = [
    "provider_execution",
    "model_inference",
    "qirc_core_runtime",
    "handoff_compiler_runtime",
    "app_bridge_runtime",
    "app_apply",
    "app_state_mutation",
    "external_send",
    "public_network",
    "production_readiness",
    "security_certification",
]


def build_simple_local_hub_proof_packet(host: str = "127.0.0.1") -> dict:
    """Emit the FINAL-PR-01 Simple Local Hub proof packet."""
    return {
        "artifact_kind": "odin_simple_local_hub_proof_packet",
        "status": "ok_with_known_gaps",
        "candidate_only": True,
        "local_only": True,
        "host": host,
        "browser_hub_visible": True,
        "normal_user_status_visible": True,
        "model_picker_placeholder_visible": True,
        "connected_apps_placeholder_visible": True,
        "activity_placeholder_visible": True,
        "qirc_status_placeholder_visible": True,
        "handoff_first_placeholder_visible": True,
        "dev_mode_placeholder_visible": True,
        "not_proven": NOT_PROVEN,
        "claim_boundary": PROOF_CLAIM_BOUNDARY,
    }
