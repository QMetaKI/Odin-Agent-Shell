from __future__ import annotations


def compose_candidate_content(*, work: dict, route_decision: dict, provider_result: dict | None = None, deterministic_output: dict | None = None, worker_card: dict | None = None) -> dict:
    projection = provider_result if provider_result is not None else deterministic_output or {
        "artifact_kind": "odin_deterministic_no_model_output",
        "text": "deterministic candidate route selected; no provider projection executed",
        "candidate_only": True,
        "claim_boundary": "deterministic_output_not_app_truth",
    }
    return {
        "artifact_kind": "odin_output_composition",
        "protocol_version": "7.1",
        "work_id": work.get("work_id"),
        "route": route_decision,
        "worker_boundary": worker_card or {},
        "provider_boundary": provider_result or {"selected_provider_id": None, "model_inference_verified": False},
        "projection": projection,
        "route_reason": route_decision.get("reason"),
        "proof_gaps": list(route_decision.get("proof_gap", [])),
        "candidate_only": True,
        "app_owned_apply": True,
        "may_apply": False,
        "may_issue_receipt": False,
        "claim_boundary": "output_composer_buffers_projection_into_candidate_artifact_not_truth_or_receipt",
    }
