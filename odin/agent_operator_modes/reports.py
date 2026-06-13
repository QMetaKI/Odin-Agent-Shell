"""Agent Operator Mode Matrix Report.

Claim boundary: agent_operator_modes_define_bounded_worker_presets_not_agent_autonomy
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "agent_operator_modes_define_bounded_worker_presets_not_agent_autonomy"

NOT_PROVEN = [
    "production_readiness",
    "live_model_inference",
    "app_state_mutation",
    "external_send_authority",
]


def build_agent_operator_mode_matrix(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build agent operator mode matrix."""
    from .presets import AGENT_OPERATOR_MODES

    return {
        "artifact_kind": "odin_agent_operator_mode_matrix",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "mode_count": len(AGENT_OPERATOR_MODES),
        "modes": AGENT_OPERATOR_MODES,
        "agent_autonomy": False,
        "app_apply": False,
        "external_send": False,
        "not_proven": NOT_PROVEN,
    }
