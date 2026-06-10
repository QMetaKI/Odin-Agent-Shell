from __future__ import annotations

from odin.models.model_router import choose_route
from .admissibility import evaluate_admissibility
from .model_work_avoidance import evaluate_model_work_avoidance


def score_pre_llm_route(work: dict) -> dict:
    admissibility = evaluate_admissibility(work)
    avoidance = evaluate_model_work_avoidance(work)
    policy = work.get("model_policy", {}) or {}
    blocked = list(admissibility.get("blocked_reasons", []))
    requires_model = bool(avoidance.get("requires_model", True)) and not blocked
    route = "cannot_safely_complete" if blocked else choose_route(
        policy.get("resource_profile", "standard_local"),
        policy.get("latency_mode", "interactive"),
        policy.get("quality_target", "standard"),
        requires_model,
    )
    selected_worker = "blocked_candidate_rejection" if blocked else ("deterministic_candidate_worker" if not requires_model else "smallest_sufficient_model_projection_worker")
    provider_id = None if (blocked or not requires_model) else "mock_provider"
    proof_gaps: list[str] = []
    if blocked:
        proof_gaps.append("provider_not_dispatched_due_to_pre_llm_authority_block")
    if not requires_model:
        proof_gaps.append("model_not_executed_deterministic_route")
    else:
        proof_gaps.append("live_model_inference_not_verified")
    return {
        "artifact_kind": "odin_pre_llm_route",
        "protocol_version": "7.1",
        "route_id": f"pre_llm:{route}",
        "requires_model": requires_model,
        "selected_worker_class": selected_worker,
        "selected_provider_id": provider_id,
        "route": route,
        "reason": avoidance.get("reason") if not blocked else "blocked_before_provider_dispatch",
        "cost_profile": "no_model_local" if not requires_model else "bounded_mock_or_stub_projection",
        "risk_profile": "blocked_authority_request" if blocked else "candidate_only_no_apply",
        "blocked_reasons": blocked,
        "proof_gap": proof_gaps,
        "candidate_only": True,
        "claim_boundary": "pre_llm_route_score_no_model_quality_or_live_inference_claim",
    }
