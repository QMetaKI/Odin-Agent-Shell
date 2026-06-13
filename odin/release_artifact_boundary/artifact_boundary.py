"""FINAL-PR-13: Release Artifact Boundary.

Claim boundary: release_artifact_boundary_lists_manual_release_actions_not_external_release
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "release_artifact_boundary_lists_manual_release_actions_not_external_release"


def build_release_artifact_boundary(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_final_pr_13_release_artifact_boundary",
        "candidate_only": True,
        "app_owned_apply": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "local_candidate_release_closure_claimed": True,
        "external_release_claimed": False,
        "tag_creation_claimed": False,
        "github_release_creation_claimed": False,
        "pypi_publication_claimed": False,
        "release_asset_upload_claimed": False,
        "signed_distribution_claimed": False,
        "pr13_may_close_local_candidate_release_readiness": True,
        "pr13_may_prepare_release_notes_candidates": True,
        "pr13_may_not_perform_external_release_actions": True,
        "pr13_may_not_claim_external_actions_occurred": True,
        "not_proven": [
            "production_readiness",
            "security_certification",
            "external_release_certification",
            "general_live_model_inference",
            "real_model_benchmark",
            "model_superiority",
            "tag_creation",
            "github_release_creation",
            "pypi_publication",
            "release_asset_upload",
            "signed_distribution",
        ],
    }
