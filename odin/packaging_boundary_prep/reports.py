"""Packaging Boundary Prep — Reports.

Claim boundary: packaging_boundary_prep_inventories_distribution_boundaries_not_packaged_release
candidate_only: true
"""
from __future__ import annotations

from .inventory import build_packaging_inventory
from .boundary import build_packaging_boundary_map
from .manifest_plan import build_packaging_manifest_plan

CLAIM_BOUNDARY = "packaging_boundary_prep_inventories_distribution_boundaries_not_packaged_release"


def build_packaging_boundary_report(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    inventory = build_packaging_inventory(generated_at_utc=generated_at_utc)
    boundary_map = build_packaging_boundary_map(generated_at_utc=generated_at_utc)
    manifest_plan = build_packaging_manifest_plan(generated_at_utc=generated_at_utc)
    return {
        "artifact_kind": "odin_packaging_boundary_prep_report",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "inventory": inventory,
        "boundary_map": boundary_map,
        "manifest_plan": manifest_plan,
        "summary": "Packaging boundary inventory complete. No release artifact built. FINAL-PR-13 remains deferred.",
        "not_proven": ["signed_distribution", "installer_proof", "distribution_proof", "production_readiness", "release_certification"],
    }
