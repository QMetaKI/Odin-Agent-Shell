"""Release Readiness Hardening — Combined Report.

Claim boundary: release_readiness_hardening_prepares_release_closure_not_certification
candidate_only: true
app_owned_apply: true

Combines readiness matrix, risk register, and hardening plan into a single
release readiness hardening report for FINAL-PR-12.
FINAL-PR-13 remains deferred.
"""
from __future__ import annotations

CLAIM_BOUNDARY = "release_readiness_hardening_prepares_release_closure_not_certification"

NOT_PROVEN = [
    "production_readiness",
    "security_certification",
    "release_certification",
    "general_live_model_inference",
    "real_model_benchmark",
    "model_superiority",
    "final_pr_13_release_closure",
]


def build_release_readiness_hardening_report(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build the combined release readiness hardening report for FINAL-PR-12.

    Combines readiness matrix, risk register, and hardening plan.
    This is not release certification. FINAL-PR-13 remains deferred.
    """
    from .readiness_matrix import build_release_readiness_matrix
    from .risk_register import build_release_risk_register
    from .hardening_plan import build_release_hardening_plan

    matrix = build_release_readiness_matrix(generated_at_utc=generated_at_utc)
    risk_register = build_release_risk_register(generated_at_utc=generated_at_utc)
    hardening_plan = build_release_hardening_plan(generated_at_utc=generated_at_utc)

    ready_structural = [
        r["category"] for r in matrix["rows"]
        if r["readiness_status"] == "ready_structural"
    ]
    ready_host_scoped = [
        r["category"] for r in matrix["rows"]
        if r["readiness_status"] == "ready_host_scoped"
    ]
    deferred = [
        r["category"] for r in matrix["rows"]
        if r["readiness_status"] == "deferred_to_final_pr_13"
    ]
    external_required = [
        r["category"] for r in matrix["rows"]
        if r["readiness_status"] == "external_receipt_required"
    ]
    mitigated_risks = [r["risk_id"] for r in risk_register["risks"]]
    completed_steps = [
        s["step_id"] for s in hardening_plan["steps"]
        if s["status"] == "completed_in_final_pr_12"
    ]

    return {
        "artifact_kind": "odin_release_readiness_hardening_report",
        "candidate_only": True,
        "app_owned_apply": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "summary": "Release readiness hardening complete. FINAL-PR-13 remains deferred.",
        "final_pr_13_remains_deferred": True,
        "matrix_summary": {
            "total_rows": len(matrix["rows"]),
            "ready_structural": ready_structural,
            "ready_host_scoped": ready_host_scoped,
            "deferred_to_final_pr_13": deferred,
            "external_receipt_required": external_required,
        },
        "risk_register_summary": {
            "total_risks": len(risk_register["risks"]),
            "all_mitigated_by_boundary": True,
            "mitigated_risk_ids": mitigated_risks,
        },
        "hardening_plan_summary": {
            "target_pr": hardening_plan["target_pr"],
            "total_steps": len(hardening_plan["steps"]),
            "completed_steps": completed_steps,
        },
        "matrix": matrix,
        "risk_register": risk_register,
        "hardening_plan": hardening_plan,
        "not_proven": NOT_PROVEN,
    }
