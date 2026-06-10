from __future__ import annotations

DETERMINISTIC_KINDS = {"classify", "validate", "route", "summarize_metadata", "lint", "format", "echo", "noop"}


def evaluate_model_work_avoidance(work: dict) -> dict:
    intent = work.get("work_intent", {}) or {}
    policy = work.get("model_policy", {}) or {}
    requires_model = bool(intent.get("requires_model", policy.get("requires_model", True)))
    kind = str(intent.get("kind", "")).lower()
    goal = str(intent.get("goal", "")).lower()
    deterministic_sufficient = (not requires_model) or kind in DETERMINISTIC_KINDS or "deterministic" in goal or "no model" in goal
    return {
        "artifact_kind": "odin_model_work_avoidance_decision",
        "protocol_version": "7.1",
        "deterministic_sufficient": deterministic_sufficient,
        "requires_model": False if deterministic_sufficient else requires_model,
        "reason": "deterministic_or_declared_no_model_sufficient" if deterministic_sufficient else "model_projection_requested_after_pre_llm_checks",
        "candidate_only": True,
        "claim_boundary": "model_work_avoidance_is_route_discipline_not_quality_or_benchmark_claim",
    }
