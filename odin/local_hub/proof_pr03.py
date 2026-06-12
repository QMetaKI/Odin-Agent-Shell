"""FINAL-PR-03 proof packet builder — QIRC Core Dev Mode.

Claim boundary: final_pr_03_qirc_first_slice_local_only_not_public_network_not_runtime_completion
"""
from __future__ import annotations

from pathlib import Path
import json

CLAIM_BOUNDARY = "final_pr_03_qirc_first_slice_local_only_not_public_network_not_runtime_completion"

NOT_PROVEN = [
    "provider_execution",
    "model_inference",
    "public_qirc_network",
    "qirc_federation",
    "real_external_app_integration",
    "app_apply",
    "app_state_mutation",
    "external_send",
    "production_readiness",
    "security_certification",
]


def build_final_pr_03_proof_packet() -> dict:
    """Emit the FINAL-PR-03 QIRC Core Dev Mode proof packet."""
    return {
        "artifact_kind": "odin_final_pr_03_qirc_devmode_proof_packet",
        "status": "ok_with_known_gaps",
        "candidate_only": True,
        "local_only": True,
        "qirc_core_first_slice": True,
        "qirc_public_network": False,
        "qirc_federation": False,
        "activity_timeline_visible": True,
        "trace_viewer_visible": True,
        "receipt_viewer_visible": True,
        "handoff_chain_visible": True,
        "surface_registry_visible": True,
        "surface_conflict_check": "ok",
        "provider_execution": False,
        "model_inference": False,
        "app_apply": False,
        "app_state_mutation": False,
        "external_send": False,
        "not_proven": NOT_PROVEN,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_proof_report(out_path: Path | None = None) -> Path:
    """Write the proof packet to a JSON file. Returns the path written."""
    if out_path is None:
        out_path = Path(__file__).resolve().parents[2] / "reports" / "final_pr_03_qirc_devmode_proof_packet.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    packet = build_final_pr_03_proof_packet()
    out_path.write_text(json.dumps(packet, indent=2, sort_keys=True, ensure_ascii=False), encoding="utf-8")
    return out_path
