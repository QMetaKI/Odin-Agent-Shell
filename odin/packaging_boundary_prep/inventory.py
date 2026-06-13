"""Packaging Boundary Prep — Inventory.

Claim boundary: packaging_boundary_prep_inventories_distribution_boundaries_not_packaged_release
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "packaging_boundary_prep_inventories_distribution_boundaries_not_packaged_release"

_ITEMS = [
    {
        "category": "source_tree",
        "repo_evidence": "odin/ — full Python package tree",
        "include_in_release_candidate": True,
        "exclude_reason": None,
        "requires_external_receipt": False,
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": ["signed_distribution", "installer_proof"],
    },
    {
        "category": "python_package_metadata",
        "repo_evidence": "setup.py / pyproject.toml / setup.cfg",
        "include_in_release_candidate": True,
        "exclude_reason": None,
        "requires_external_receipt": False,
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": ["pypi_distribution", "signed_package"],
    },
    {
        "category": "cli_surface",
        "repo_evidence": "odin/cli.py — main CLI entry point",
        "include_in_release_candidate": True,
        "exclude_reason": None,
        "requires_external_receipt": False,
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": ["runtime_completion", "production_deployment"],
    },
    {
        "category": "local_hub_surface",
        "repo_evidence": "odin/local_hub/ — server, ui, policy",
        "include_in_release_candidate": True,
        "exclude_reason": None,
        "requires_external_receipt": False,
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": ["public_deployment", "production_readiness"],
    },
    {
        "category": "docs_surface",
        "repo_evidence": "docs/ — architecture, release, rebaseline, codex docs",
        "include_in_release_candidate": True,
        "exclude_reason": None,
        "requires_external_receipt": False,
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": ["user_documentation_complete"],
    },
    {
        "category": "reports_surface",
        "repo_evidence": "reports/ — proof packets, release reports, coverage reports",
        "include_in_release_candidate": True,
        "exclude_reason": None,
        "requires_external_receipt": False,
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": ["production_readiness", "release_certification"],
    },
    {
        "category": "registries_surface",
        "repo_evidence": "registries/ — operational target, slice absorption, PR12 registries",
        "include_in_release_candidate": True,
        "exclude_reason": None,
        "requires_external_receipt": False,
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": ["production_readiness"],
    },
    {
        "category": "schemas_surface",
        "repo_evidence": "schemas/ — JSON schemas for packet types",
        "include_in_release_candidate": True,
        "exclude_reason": None,
        "requires_external_receipt": False,
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": ["schema_certification"],
    },
    {
        "category": "examples_surface",
        "repo_evidence": "examples/ — fixture and example JSON files",
        "include_in_release_candidate": True,
        "exclude_reason": None,
        "requires_external_receipt": False,
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": ["production_readiness"],
    },
    {
        "category": "tests_surface",
        "repo_evidence": "tests/ — pytest test suite",
        "include_in_release_candidate": True,
        "exclude_reason": None,
        "requires_external_receipt": False,
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": ["production_readiness", "security_certification"],
    },
    {
        "category": "release_notes_candidate",
        "repo_evidence": "None — release notes require FINAL-PR-13 release closure",
        "include_in_release_candidate": False,
        "exclude_reason": "requires_final_pr_13_release_closure",
        "requires_external_receipt": False,
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": ["release_certification", "production_readiness"],
    },
    {
        "category": "external_distribution_required",
        "repo_evidence": "None — PyPI / installer distribution requires external action",
        "include_in_release_candidate": False,
        "exclude_reason": "requires_external_distribution_receipt",
        "requires_external_receipt": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": ["pypi_distribution", "installer_proof", "signed_distribution", "distribution_proof"],
    },
]


def build_packaging_inventory(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_packaging_boundary_prep_inventory",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "items": _ITEMS,
        "not_proven": ["signed_distribution", "installer_proof", "distribution_proof", "production_readiness", "release_certification"],
    }
