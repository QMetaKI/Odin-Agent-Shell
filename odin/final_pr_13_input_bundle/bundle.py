"""FINAL-PR-13 Input Bundle — Bundle Builder.

Claim boundary: final_pr_13_input_bundle_prepares_release_closure_not_release_closure
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "final_pr_13_input_bundle_prepares_release_closure_not_release_closure"

_FORBIDDEN_CLAIMS = [
    "production_readiness",
    "security_certification",
    "release_certification",
    "general_live_model_inference",
    "real_model_benchmark",
    "model_superiority",
    "provider_execution_by_default",
    "app_apply",
    "app_state_mutation",
    "external_send",
    "public_network",
    "final_pr_13_release_closure_in_pr12",
]

_ALLOWED_STRUCTURAL_CLAIMS = [
    "candidate_only_architecture",
    "app_owned_apply_boundary",
    "release_readiness_matrix_exists",
    "risk_register_exists",
    "evidence_closure_dry_run_exists",
    "packaging_boundary_inventory_exists",
    "command_surface_indexed",
    "docs_readiness_indexed",
    "final_pr_13_input_bundle_exists",
    "claim_policy_defined",
    "semantic_kernel_ir_defined",
    "v711_coverage_mapped",
    "agent_operator_modes_defined",
    "all_prior_pr_validators_pass",
]

_HOST_SCOPED_CLAIMS = [
    "local_provider_receipt_when_enabled_by_host",
    "host_scoped_inference_when_host_enables",
]

_EXTERNAL_RECEIPT_REQUIRED_CLAIMS = [
    "production_readiness",
    "security_certification",
    "release_certification",
    "model_performance_benchmark",
    "external_distribution_proof",
]

_VALIDATION_COMMANDS = [
    "python -m odin.cli validate-final-pr-12-release-readiness-hardening",
    "python -m odin.cli validate-release-readiness-hardening",
    "python -m odin.cli validate-evidence-closure-dry-run",
    "python -m odin.cli validate-packaging-boundary-prep",
    "python -m odin.cli validate-command-surface-closure",
    "python -m odin.cli validate-docs-readiness",
    "python -m odin.cli validate-final-pr-13-input-bundle",
    "python -m odin.cli validate-final-pr-11-5-semantic-kernel-coverage",
    "python -m odin.cli validate-final-pr-11-provider-critic-thor",
    "python -m odin.cli validate-final-release-preflight",
    "python -m odin.cli validate-operational-spine",
    "python -m odin.cli validate-all",
    "PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_final_pr_12_release_readiness_hardening.py -p no:cacheprovider",
    "PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider",
]


def build_final_pr_13_input_bundle(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_final_pr_13_input_bundle",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "final_pr_13_remains_deferred": True,
        "this_is_pr13_input_only": True,
        "does_not_implement_pr13": True,
        "does_not_close_release": True,
        "repo_cognition_inputs": {
            "base_pr": "FINAL-PR-11.5 (PR #53)",
            "pr12_branch": "claude/final-pr-12-release-readiness-444jw1",
            "new_modules": [
                "odin/release_readiness_hardening/",
                "odin/evidence_closure_dry_run/",
                "odin/packaging_boundary_prep/",
                "odin/command_surface_closure/",
                "odin/docs_readiness/",
                "odin/final_pr_13_input_bundle/",
            ],
            "validators_passing": [
                "validate-all",
                "validate-final-pr-11-5-semantic-kernel-coverage",
                "validate-final-pr-11-provider-critic-thor",
                "validate-final-release-preflight",
                "validate-operational-spine",
                "validate-final-pr-12-release-readiness-hardening",
            ],
        },
        "release_readiness_matrix": {
            "status": "built",
            "module": "odin/release_readiness_hardening/readiness_matrix.py",
            "ready_structural_count": 8,
            "ready_host_scoped_count": 1,
            "external_receipt_required_count": 3,
            "deferred_to_final_pr_13_count": 3,
        },
        "evidence_closure_dry_run": {
            "status": "complete",
            "module": "odin/evidence_closure_dry_run/dry_run.py",
            "dry_run_is_not_release_closure": True,
            "closure_ready_structural_count": 5,
            "external_receipt_required_count": 4,
            "forbidden_count": 1,
        },
        "packaging_boundary_inventory": {
            "status": "complete",
            "module": "odin/packaging_boundary_prep/inventory.py",
            "include_in_release_candidate_count": 10,
            "exclude_count": 2,
            "requires_external_receipt_count": 1,
        },
        "command_surface_index": {
            "status": "complete",
            "module": "odin/command_surface_closure/command_index.py",
            "command_count": 30,
            "validator_count": 15,
            "demo_count": 10,
            "explain_count": 10,
        },
        "docs_readiness_index": {
            "status": "complete",
            "module": "odin/docs_readiness/doc_index.py",
            "docs_count": 12,
            "needs_update_count": 0,
        },
        "claims_policy": {
            "source": "odin/claims_compiler/",
            "status": "defined",
        },
        "forbidden_claims": _FORBIDDEN_CLAIMS,
        "allowed_structural_claims": _ALLOWED_STRUCTURAL_CLAIMS,
        "host_scoped_claims": _HOST_SCOPED_CLAIMS,
        "external_receipt_required_claims": _EXTERNAL_RECEIPT_REQUIRED_CLAIMS,
        "recommended_final_pr_13_title": "FINAL-PR-13: Release Closure",
        "recommended_final_pr_13_non_claims": [
            "no_production_readiness_claim",
            "no_security_certification_claim",
            "no_release_certification_claim_without_external_receipt",
            "no_model_superiority_claim",
            "no_real_model_benchmark",
            "no_provider_execution_by_default",
            "no_app_apply",
            "no_external_send",
            "no_public_network",
        ],
        "recommended_final_pr_13_validation_commands": _VALIDATION_COMMANDS,
        "not_proven": [
            "production_readiness",
            "security_certification",
            "release_certification",
            "general_live_model_inference",
            "real_model_benchmark",
            "model_superiority",
            "final_pr_13_release_closure",
        ],
    }
