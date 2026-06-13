"""Packaging Boundary Prep — Boundary Map.

Claim boundary: packaging_boundary_prep_inventories_distribution_boundaries_not_packaged_release
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "packaging_boundary_prep_inventories_distribution_boundaries_not_packaged_release"


def build_packaging_boundary_map(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_packaging_boundary_map",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "boundaries": [
            {
                "boundary_id": "repo_to_release_candidate",
                "from_side": "repo_source_tree",
                "to_side": "release_candidate_package",
                "gate": "FINAL-PR-13_release_closure",
                "current_status": "not_crossed",
                "notes": "Crossing this boundary requires FINAL-PR-13 release closure.",
            },
            {
                "boundary_id": "release_candidate_to_distribution",
                "from_side": "release_candidate_package",
                "to_side": "external_distribution",
                "gate": "external_distribution_receipt",
                "current_status": "not_crossed",
                "notes": "Crossing this boundary requires external distribution receipt (PyPI, installer, etc.).",
            },
            {
                "boundary_id": "internal_to_production",
                "from_side": "internal_candidate",
                "to_side": "production_deployment",
                "gate": "external_production_validation_receipt",
                "current_status": "not_crossed",
                "notes": "Production deployment requires external validation receipt not available in FINAL-PR-12.",
            },
        ],
        "not_proven": ["signed_distribution", "installer_proof", "distribution_proof", "production_readiness", "release_certification"],
    }
