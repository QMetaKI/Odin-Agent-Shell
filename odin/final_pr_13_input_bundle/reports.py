"""FINAL-PR-13 Input Bundle — Reports.

Claim boundary: final_pr_13_input_bundle_prepares_release_closure_not_release_closure
candidate_only: true
"""
from __future__ import annotations

from .bundle import build_final_pr_13_input_bundle
from .prompt_inputs import build_final_pr_13_prompt_inputs

CLAIM_BOUNDARY = "final_pr_13_input_bundle_prepares_release_closure_not_release_closure"


def build_final_pr_13_input_bundle_report(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    bundle = build_final_pr_13_input_bundle(generated_at_utc=generated_at_utc)
    prompt_inputs = build_final_pr_13_prompt_inputs(generated_at_utc=generated_at_utc)
    return {
        "artifact_kind": "odin_final_pr_13_input_bundle_report",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "final_pr_13_remains_deferred": True,
        "bundle": bundle,
        "prompt_inputs": prompt_inputs,
        "summary": "FINAL-PR-13 input bundle complete. This is prep only. Release Closure remains FINAL-PR-13.",
        "not_proven": ["production_readiness", "security_certification", "release_certification", "final_pr_13_release_closure"],
    }
