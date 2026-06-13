"""FINAL-PR-13: Release Artifact Boundary Reports.

Claim boundary: release_artifact_boundary_lists_manual_release_actions_not_external_release
candidate_only: true
"""
from __future__ import annotations

from .artifact_boundary import build_release_artifact_boundary
from .manual_release_actions import build_manual_release_actions

CLAIM_BOUNDARY = "release_artifact_boundary_lists_manual_release_actions_not_external_release"


def build_release_artifact_boundary_report(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    boundary = build_release_artifact_boundary(generated_at_utc=generated_at_utc)
    actions = build_manual_release_actions(generated_at_utc=generated_at_utc)
    return {
        "artifact_kind": "odin_final_pr_13_release_artifact_boundary_report",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "status": "ok",
        "external_release_claimed": False,
        "manual_actions_count": len(actions.get("manual_actions", [])),
        "boundary": boundary,
        "manual_actions": actions,
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    }
