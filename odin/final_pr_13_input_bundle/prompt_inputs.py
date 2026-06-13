"""FINAL-PR-13 Input Bundle — Prompt Inputs.

Claim boundary: final_pr_13_input_bundle_prepares_release_closure_not_release_closure
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "final_pr_13_input_bundle_prepares_release_closure_not_release_closure"


def build_final_pr_13_prompt_inputs(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_final_pr_13_prompt_inputs",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "final_pr_13_remains_deferred": True,
        "prompt_inputs": {
            "required_baseline": [
                "FINAL-PR-12 merged into main",
                "All FINAL-PR-12 validators pass",
                "All tests pass including tests/test_final_pr_12_release_readiness_hardening.py",
                "FINAL-PR-13 input bundle built and validated",
            ],
            "core_claim_boundary": "final_pr_13_release_closure_not_release_distribution",
            "forbidden_in_pr13": [
                "claim production_readiness without external receipt",
                "claim security_certification without external audit receipt",
                "claim model_superiority without benchmark receipt",
                "open provider execution by default",
                "apply app state",
                "send externally",
                "use public network",
            ],
            "key_deliverables_for_pr13": [
                "Release closure wording document",
                "Release sequence closure report",
                "Final claim policy confirmation",
                "Release readiness certification (structural only, not external cert)",
                "PR13 proof packet",
            ],
            "source_of_truth_files": [
                "reports/final_pr_12_release_readiness_matrix.json",
                "reports/final_pr_12_evidence_closure_dry_run.json",
                "reports/final_pr_12_packaging_boundary_inventory.json",
                "reports/final_pr_12_command_surface_index.json",
                "reports/final_pr_12_docs_readiness_index.json",
                "reports/final_pr_12_final_pr_13_input_bundle.json",
                "reports/final_pr_12_release_readiness_proof_packet.json",
            ],
            "do_not_in_pr13": [
                "Do not claim production readiness",
                "Do not claim security certification",
                "Do not certify external distribution",
                "Do not run model inference",
                "Do not apply app state",
                "Do not send externally",
                "Do not use public network",
                "Do not claim model superiority",
            ],
        },
        "not_proven": ["production_readiness", "security_certification", "release_certification", "final_pr_13_release_closure"],
    }
