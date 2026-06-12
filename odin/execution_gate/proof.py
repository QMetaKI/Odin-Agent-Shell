"""Execution gate proof packet — FINAL-PR-05.

Claim boundary: final_pr_05_execution_gate_mock_only_not_model_quality_not_production
candidate_only: true
local_only: true
"""
from __future__ import annotations

import time

CLAIM_BOUNDARY = "final_pr_05_execution_gate_mock_only_not_model_quality_not_production"

NOT_PROVEN = [
    "actual_local_model_inference",
    "real_provider_execution",
    "remote_provider_api",
    "model_quality",
    "production_readiness",
    "security_certification",
    "full_thor_replacement",
]


def build_execution_gate_proof_packet(
    mock_execution_completed: bool = True,
    qirc_events_visible: bool = True,
    proof_chain_present: bool = True,
    ladder_scaffold_present: bool = True,
) -> dict:
    return {
        "artifact_kind": "odin_final_pr_05_execution_gate_proof_packet",
        "status": "ok_with_known_gaps",
        "candidate_only": True,
        "local_only": True,
        "mock_execution_allowed": True,
        "mock_execution_completed": mock_execution_completed,
        "mock_execution_is_model_inference": False,
        "real_provider_execution": False,
        "local_candidate_execution_default": False,
        "remote_execution_allowed": False,
        "api_key_reads": False,
        "external_network": False,
        "app_apply": False,
        "app_state_mutation": False,
        "external_send": False,
        "qirc_execution_events_visible": qirc_events_visible,
        "proof_chain_present": proof_chain_present,
        "ladder_scaffold_present": ladder_scaffold_present,
        "not_proven": NOT_PROVEN,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "claim_boundary": CLAIM_BOUNDARY,
    }
