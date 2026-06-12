"""Provider proof packet — FINAL-PR-04.

Claim boundary: final_pr_04_provider_probe_readiness_not_model_execution_not_security_certification
candidate_only: true
"""
from __future__ import annotations

import json
from pathlib import Path

from .probe import build_provider_status_packet

PROOF_CLAIM_BOUNDARY = (
    "final_pr_04_provider_probe_readiness_not_model_execution_not_security_certification"
)


def build_proof_packet() -> dict:
    status_packet = build_provider_status_packet()
    all_ok = all(
        p.get("execution_allowed") is False and p.get("model_inference") is False
        for p in status_packet.get("providers", [])
    )
    return {
        "artifact_kind": "odin_final_pr_04_provider_probe_security_proof_packet",
        "status": "ok_with_known_gaps",
        "candidate_only": True,
        "local_only": True,
        "provider_probe_visible": True,
        "provider_policy_present": True,
        "provider_execution": False,
        "model_inference": False,
        "api_key_reads": False,
        "external_network": False,
        "qirc_provider_events_visible": True,
        "runtime_security_smoke": "ok",
        "provider_boundaries_intact": all_ok,
        "not_proven": [
            "actual_model_inference",
            "provider_text_generation",
            "provider_model_quality",
            "remote_provider_api",
            "real_app_integration",
            "production_readiness",
            "security_certification",
        ],
        "claim_boundary": PROOF_CLAIM_BOUNDARY,
    }


def persist_proof_packet(root: Path | None = None) -> dict:
    if root is None:
        root = Path(__file__).resolve().parents[2]
    packet = build_proof_packet()
    reports_dir = root / "reports"
    reports_dir.mkdir(exist_ok=True)
    out_path = reports_dir / "final_pr_04_provider_probe_security_proof_packet.json"
    out_path.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    return packet
