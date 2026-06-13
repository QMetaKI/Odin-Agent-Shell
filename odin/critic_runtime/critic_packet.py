"""Critic packet builder — FINAL-PR-11."""
from __future__ import annotations

import hashlib
import json

CLAIM_BOUNDARY = "critic_runtime_binding_scores_candidates_not_truth_not_apply"

_NOT_PROVEN = [
    "production_readiness",
    "security_certification",
    "release_certification",
    "real_model_benchmark",
    "model_quality_superiority",
    "app_apply",
    "app_state_mutation",
    "external_send",
    "public_network",
    "final_authority",
]


def _sha256_id(prefix: str, payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    h = hashlib.sha256(raw.encode()).hexdigest()[:16]
    return f"{prefix}{h}"


def build_critic_packet(
    candidate: dict,
    *,
    critic_mode: str = "deterministic",
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build a critic packet envelope for a candidate.

    Critic is advisory. Not final authority. Cannot apply. Cannot send.
    """
    packet_id = _sha256_id(
        "critic_packet_",
        {"candidate_id": candidate.get("artifact_kind", "unknown"), "critic_mode": critic_mode, "ts": generated_at_utc},
    )
    return {
        "artifact_kind": "odin_critic_packet",
        "critic_packet_id": packet_id,
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "app_apply": False,
        "external_send": False,
        "public_network": False,
        "critic_mode": critic_mode,
        "not_authority": True,
        "final_gate_required": True,
        "evidence_class": "structural_evidence",
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(_NOT_PROVEN),
        "candidate_snapshot": {
            "artifact_kind": candidate.get("artifact_kind"),
            "candidate_only": candidate.get("candidate_only"),
            "claim_boundary": candidate.get("claim_boundary"),
        },
        "generated_at_utc": generated_at_utc,
    }
