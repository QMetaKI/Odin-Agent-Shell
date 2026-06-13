"""Command Surface Closure — Coverage Analysis.

Claim boundary: command_surface_closure_indexes_cli_surface_not_runtime_completion
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "command_surface_closure_indexes_cli_surface_not_runtime_completion"

_SUBSYSTEM_COVERAGE = [
    {"subsystem": "release_readiness_hardening", "has_validate": True, "has_demo": True, "has_explain": True, "status": "covered"},
    {"subsystem": "evidence_closure_dry_run", "has_validate": True, "has_demo": True, "has_explain": True, "status": "covered"},
    {"subsystem": "packaging_boundary_prep", "has_validate": True, "has_demo": True, "has_explain": True, "status": "covered"},
    {"subsystem": "command_surface_closure", "has_validate": True, "has_demo": True, "has_explain": True, "status": "covered"},
    {"subsystem": "docs_readiness", "has_validate": True, "has_demo": True, "has_explain": True, "status": "covered"},
    {"subsystem": "final_pr_13_input_bundle", "has_validate": True, "has_demo": True, "has_explain": True, "status": "covered"},
    {"subsystem": "operational_spine", "has_validate": True, "has_demo": True, "has_explain": False, "status": "partially_covered", "notes": "explain not applicable"},
    {"subsystem": "release_boundaries", "has_validate": True, "has_demo": False, "has_explain": True, "status": "partially_covered", "notes": "demo not applicable for boundary maps"},
    {"subsystem": "semantic_kernel_closure", "has_validate": True, "has_demo": True, "has_explain": True, "status": "covered"},
    {"subsystem": "claims_compiler", "has_validate": True, "has_demo": True, "has_explain": True, "status": "covered"},
    {"subsystem": "agent_operator_modes", "has_validate": True, "has_demo": True, "has_explain": True, "status": "covered"},
    {"subsystem": "local_provider_receipts", "has_validate": True, "has_demo": False, "has_explain": True, "status": "partially_covered", "notes": "demo requires host provider flag"},
    {"subsystem": "critic_runtime", "has_validate": True, "has_demo": True, "has_explain": True, "status": "covered"},
    {"subsystem": "thor_handoff_compiler", "has_validate": True, "has_demo": True, "has_explain": True, "status": "covered"},
]


def build_command_surface_coverage(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    covered = [s for s in _SUBSYSTEM_COVERAGE if s["status"] == "covered"]
    partial = [s for s in _SUBSYSTEM_COVERAGE if s["status"] == "partially_covered"]
    missing_validate = [s for s in _SUBSYSTEM_COVERAGE if not s["has_validate"]]
    return {
        "artifact_kind": "odin_command_surface_coverage",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "subsystem_coverage": _SUBSYSTEM_COVERAGE,
        "fully_covered_count": len(covered),
        "partially_covered_count": len(partial),
        "missing_validate_count": len(missing_validate),
        "missing_validate_subsystems": [s["subsystem"] for s in missing_validate],
        "not_proven": ["runtime_completion", "production_readiness"],
    }
