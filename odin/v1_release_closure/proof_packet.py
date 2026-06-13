"""FINAL-PR-13: v1.0 Release Closure Proof Packet.

Claim boundary: v1_release_closure_closes_local_candidate_release_not_external_release
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "v1_release_closure_closes_local_candidate_release_not_external_release"


def build_v1_release_closure_proof_packet(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_final_pr_13_v1_release_closure_proof_packet",
        "candidate_only": True,
        "app_owned_apply": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "proven": [
            "v1_release_closure_matrix_exists",
            "v1_release_truth_exists",
            "readme_v1_public_surface_exists",
            "root_public_surface_inventory_exists",
            "root_hygiene_report_exists",
            "donations_root_file_exists",
            "thor_thanks_block_imported_exactly_into_readme",
            "release_artifact_boundary_exists",
            "manual_external_release_actions_listed",
            "external_release_not_claimed",
        ],
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
