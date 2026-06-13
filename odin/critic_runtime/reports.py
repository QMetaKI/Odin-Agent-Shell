"""Critic runtime report builder — FINAL-PR-11."""
from __future__ import annotations

from odin.critic_runtime.critic_packet import CLAIM_BOUNDARY, _NOT_PROVEN


def build_critic_runtime_report(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build a structural report on the critic runtime binding."""
    return {
        "artifact_kind": "odin_critic_runtime_report",
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "app_apply": False,
        "external_send": False,
        "public_network": False,
        "evidence_class": "structural_evidence",
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(_NOT_PROVEN),
        "critic_modes": ["deterministic", "model_critic_optional"],
        "critic_is_advisory": True,
        "critic_not_authority": True,
        "final_gate_required": True,
        "cascade_stages": ["deterministic", "model_critic (optional, gated)"],
        "generated_at_utc": generated_at_utc,
    }
