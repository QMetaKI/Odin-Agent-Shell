"""Evidence Closure Dry Run — Reports.

Claim boundary: evidence_closure_dry_run_classifies_receipts_not_release_closure
candidate_only: true
"""
from __future__ import annotations

from .evidence_plan import build_evidence_closure_plan
from .dry_run import run_evidence_closure_dry_run

CLAIM_BOUNDARY = "evidence_closure_dry_run_classifies_receipts_not_release_closure"


def build_evidence_closure_dry_run_report(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    plan = build_evidence_closure_plan(generated_at_utc=generated_at_utc)
    dry_run = run_evidence_closure_dry_run(generated_at_utc=generated_at_utc)
    return {
        "artifact_kind": "odin_evidence_closure_dry_run_report",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "dry_run_is_not_release_closure": True,
        "final_pr_13_remains_deferred": True,
        "evidence_plan": plan,
        "dry_run_result": dry_run,
        "summary": "Evidence closure dry run complete. External receipts required for certification claims. FINAL-PR-13 remains deferred.",
        "not_proven": ["release_closure", "production_readiness", "security_certification", "release_certification", "final_pr_13_release_closure"],
    }
