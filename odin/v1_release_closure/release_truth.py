"""FINAL-PR-13: v1.0 Release Truth.

Claim boundary: v1_release_closure_closes_local_candidate_release_not_external_release
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "v1_release_closure_closes_local_candidate_release_not_external_release"


def build_v1_release_truth(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_final_pr_13_v1_release_truth",
        "candidate_only": True,
        "app_owned_apply": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "release_posture": "v1.0 candidate release closure, local candidate-only",
        "local_candidate_release_closed": True,
        "external_release_claimed": False,
        "tag_creation_claimed": False,
        "github_release_claimed": False,
        "pypi_publication_claimed": False,
        "release_asset_upload_claimed": False,
        "signed_distribution_claimed": False,
        "production_readiness_claimed": False,
        "security_certification_claimed": False,
        "model_superiority_claimed": False,
        "real_model_benchmark_claimed": False,
        "provider_execution_by_default": False,
        "app_apply": False,
        "app_state_mutation": False,
        "external_send": False,
        "public_network": False,
        "manual_external_actions_still_required": [
            "create git tag",
            "create GitHub Release",
            "publish to PyPI",
            "upload release assets",
            "verify external release state",
            "publish release notes externally",
        ],
        "current_status_wording": (
            "Current public repo posture: v1.0 candidate release closure, "
            "local candidate-only, not externally released unless a maintainer "
            "separately creates and verifies a tag, GitHub Release, PyPI publication, "
            "and release assets."
        ),
        "not_proven": [
            "production_readiness",
            "security_certification",
            "external_release_certification",
            "general_live_model_inference",
            "real_model_benchmark",
            "model_superiority",
            "provider_execution_by_default",
            "app_apply",
            "app_state_mutation",
            "external_send",
            "public_network",
            "tag_creation",
            "github_release_creation",
            "pypi_publication",
            "release_asset_upload",
            "signed_distribution",
        ],
    }
