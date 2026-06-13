"""Release Readiness Hardening — Hardening Plan.

Claim boundary: release_readiness_hardening_prepares_release_closure_not_certification
candidate_only: true
app_owned_apply: true

This module builds the release hardening plan for FINAL-PR-12.
It identifies all preparatory steps needed before FINAL-PR-13 release closure.
FINAL-PR-13 remains deferred until FINAL-PR-12 is accepted.
"""
from __future__ import annotations

CLAIM_BOUNDARY = "release_readiness_hardening_prepares_release_closure_not_certification"

NOT_PROVEN = [
    "production_readiness",
    "security_certification",
    "release_certification",
    "final_pr_13_release_closure",
]

_STEPS = [
    {
        "step_id": "STEP-01",
        "title": "Release Readiness Matrix Review",
        "description": (
            "Build and review the release readiness matrix. Confirm all categories are "
            "correctly classified: ready_structural, ready_host_scoped, "
            "external_receipt_required, or deferred_to_final_pr_13. "
            "Matrix output is candidate_only and does not certify release."
        ),
        "status": "completed_in_final_pr_12",
        "prepares_final_pr_13": True,
    },
    {
        "step_id": "STEP-02",
        "title": "Risk Register Review",
        "description": (
            "Build and review the release risk register. Confirm all boundary risks "
            "are identified and mitigated by structural enforcement. "
            "No risk is 'resolved' by external certification claims."
        ),
        "status": "completed_in_final_pr_12",
        "prepares_final_pr_13": True,
    },
    {
        "step_id": "STEP-03",
        "title": "Evidence Closure Dry Run",
        "description": (
            "Run a dry-run evidence closure exercise. For each release claim, classify "
            "the required evidence class and determine what is available vs. missing. "
            "External/certification claims are explicitly classified as external_receipt_required. "
            "Dry run does NOT close the release."
        ),
        "status": "completed_in_final_pr_12",
        "prepares_final_pr_13": True,
    },
    {
        "step_id": "STEP-04",
        "title": "Packaging Boundary Inventory",
        "description": (
            "Inventory all packaging boundary items: source tree, metadata, CLI surface, "
            "docs surface, reports surface, schemas, examples, tests. "
            "Identify what is included vs. excluded from the release candidate. "
            "Does not build actual release artifact, sign packages, or claim distribution proof."
        ),
        "status": "completed_in_final_pr_12",
        "prepares_final_pr_13": True,
    },
    {
        "step_id": "STEP-05",
        "title": "Command Surface Closure",
        "description": (
            "Build the command surface index covering all CLI commands: validators, demo builders, "
            "explain commands, doctor, receipt, and release readiness commands. "
            "Establish alias policy and coverage analysis. "
            "Full runtime completion closure deferred to FINAL-PR-13."
        ),
        "status": "completed_in_final_pr_12",
        "prepares_final_pr_13": True,
    },
    {
        "step_id": "STEP-06",
        "title": "Docs Readiness",
        "description": (
            "Build docs readiness index identifying all key documentation files and their "
            "update needs. Produce minimal update plans for README.md and START_HERE.md. "
            "Actual documentation updates deferred to FINAL-PR-13."
        ),
        "status": "completed_in_final_pr_12",
        "prepares_final_pr_13": True,
    },
    {
        "step_id": "STEP-07",
        "title": "Claims Policy Hardening",
        "description": (
            "Confirm claims policy is correctly enforced. Verify all FINAL-PR-12 artifacts "
            "have candidate_only: true, correct not_proven lists, and correct claim_boundary "
            "values. Forbidden claims are explicitly listed and not made."
        ),
        "status": "completed_in_final_pr_12",
        "prepares_final_pr_13": True,
    },
    {
        "step_id": "STEP-08",
        "title": "FINAL-PR-13 Input Bundle Delivery",
        "description": (
            "Assemble the FINAL-PR-13 input bundle: repo cognition inputs, release readiness "
            "matrix summary, evidence closure dry run summary, packaging boundary inventory "
            "summary, command surface index summary, docs readiness summary, claims policy, "
            "and structured prompt inputs. "
            "Bundle is input-only. FINAL-PR-13 remains deferred and is not implemented."
        ),
        "status": "completed_in_final_pr_12",
        "prepares_final_pr_13": True,
    },
]


def build_release_hardening_plan(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build the release hardening plan for FINAL-PR-12.

    Returns a structured plan describing all hardening steps that prepare
    for FINAL-PR-13 release closure. FINAL-PR-13 remains deferred.
    This is not release certification.
    """
    return {
        "artifact_kind": "odin_release_readiness_hardening_plan",
        "candidate_only": True,
        "app_owned_apply": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "target_pr": "FINAL-PR-13",
        "final_pr_13_remains_deferred": True,
        "steps": _STEPS,
        "not_proven": NOT_PROVEN,
    }
