"""Packaging Boundary Prep — Manifest Plan.

Claim boundary: packaging_boundary_prep_inventories_distribution_boundaries_not_packaged_release
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "packaging_boundary_prep_inventories_distribution_boundaries_not_packaged_release"


def build_packaging_manifest_plan(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_packaging_manifest_plan",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "does_not_build_release_artifact": True,
        "does_not_create_signed_package": True,
        "does_not_claim_installer_proof": True,
        "does_not_claim_distribution_proof": True,
        "manifest_plan_is_inventory_only": True,
        "manifest_entries": [
            {"entry": "odin/", "type": "python_package", "status": "include"},
            {"entry": "setup.py", "type": "package_metadata", "status": "include"},
            {"entry": "docs/", "type": "documentation", "status": "include"},
            {"entry": "registries/", "type": "registries", "status": "include"},
            {"entry": "schemas/", "type": "schemas", "status": "include"},
            {"entry": "examples/", "type": "examples", "status": "include"},
            {"entry": "tests/", "type": "test_suite", "status": "include"},
            {"entry": "reports/", "type": "proof_reports", "status": "include"},
            {"entry": "tools/", "type": "validator_tools", "status": "include"},
            {"entry": "SYSTEM_MAP.json", "type": "system_metadata", "status": "include"},
            {"entry": "FILE_MANIFEST.json", "type": "file_index", "status": "include"},
            {"entry": "RELEASE_NOTES.md", "type": "release_notes", "status": "deferred_to_final_pr_13"},
        ],
        "not_proven": ["signed_distribution", "installer_proof", "distribution_proof", "release_certification"],
    }
