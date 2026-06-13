"""FINAL-PR-13: v1.0 Release Closure Matrix.

Claim boundary: v1_release_closure_closes_local_candidate_release_not_external_release
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "v1_release_closure_closes_local_candidate_release_not_external_release"

_MATRIX_ROWS = [
    {"item": "README v1 public surface", "status": "closed_structural"},
    {"item": "START_HERE current-state pointer", "status": "closed_structural"},
    {"item": "CANON_ENTRY current-state pointer", "status": "closed_structural"},
    {"item": "DONATIONS root file", "status": "closed_structural"},
    {"item": "Thank You block imported exactly", "status": "closed_structural"},
    {"item": "root public surface inventory", "status": "closed_structural"},
    {"item": "root hygiene report", "status": "closed_structural"},
    {"item": "candidate-only release wording", "status": "closed_candidate_only"},
    {"item": "app-owned apply wording", "status": "closed_candidate_only"},
    {"item": "local provider receipt boundary", "status": "closed_local_receipt"},
    {"item": "host-scoped receipt boundary", "status": "closed_local_receipt"},
    {"item": "claims compiler policy", "status": "closed_structural"},
    {"item": "semantic kernel coverage", "status": "closed_structural"},
    {"item": "v7.1.1 coverage matrix", "status": "closed_structural"},
    {"item": "agent operator modes", "status": "closed_structural"},
    {"item": "release readiness dry run", "status": "closed_structural"},
    {"item": "evidence closure dry run", "status": "closed_structural"},
    {"item": "packaging boundary inventory", "status": "closed_structural"},
    {"item": "command surface index", "status": "closed_structural"},
    {"item": "docs readiness index", "status": "closed_structural"},
    {"item": "manual release action boundary", "status": "manual_external_action_required"},
    {"item": "external release state boundary", "status": "external_receipt_required"},
    {"item": "security certification boundary", "status": "not_claimed"},
    {"item": "production readiness boundary", "status": "not_claimed"},
    {"item": "model performance boundary", "status": "not_claimed"},
]


def build_v1_release_closure_matrix(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_final_pr_13_v1_release_closure_matrix",
        "candidate_only": True,
        "app_owned_apply": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
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
        "matrix": _MATRIX_ROWS,
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
