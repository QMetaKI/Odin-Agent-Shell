from __future__ import annotations

def build_model_work_avoidance_shadow(work: dict) -> dict:
    work_id = work.get("work_id", "WORK-SHADOW")
    trace_id = work.get("trace_id", "TRACE-SHADOW")
    if work.get("request_direct_apply") or "direct_apply" in work.get("forbidden", []):
        return {"ok": False, "decision": "block", "work_id": work_id, "trace_id": trace_id, "reason": "direct_apply_forbidden", "authority": "candidate_only"}
    return {
        "ok": True,
        "work_id": work_id,
        "trace_id": trace_id,
        "decision": "avoid_or_minimize_model_work",
        "authority": "odin_internal_candidate_only",
        "candidate_only": True,
        "steps": ['template_check', 'cache_check', 'micro_route_check'],
        "trace": {"claim_boundary": "candidate_projection_only", "app_apply": "app_owned"},
    }
