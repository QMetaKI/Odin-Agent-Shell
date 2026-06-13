"""Agent Operator Modes — list and get mode presets.

Claim boundary: agent_operator_modes_define_bounded_worker_presets_not_agent_autonomy
candidate_only: true
"""
from __future__ import annotations

from .presets import AGENT_OPERATOR_MODES


def list_agent_operator_modes() -> list[dict]:
    """Return list of mode summary dicts."""
    return [
        {
            "mode_id": m["mode_id"],
            "tool_target": m["tool_target"],
            "best_for": m["best_for"],
            "claim_boundary": m["claim_boundary"],
            "candidate_only": m["candidate_only"],
            "agent_autonomy": m["agent_autonomy"],
        }
        for m in AGENT_OPERATOR_MODES
    ]


def get_agent_operator_mode(mode_id: str) -> dict:
    """Return full mode dict or raise KeyError if not found."""
    for m in AGENT_OPERATOR_MODES:
        if m["mode_id"] == mode_id:
            return m
    raise KeyError(f"Agent operator mode not found: {mode_id!r}")
