from __future__ import annotations

def build_output_intelligence_composer_shadow(work: dict) -> dict:
    work_id = work.get("work_id", "WORK-SHADOW")
    trace_id = work.get("trace_id", "TRACE-SHADOW")
    if work.get("request_direct_apply") or "direct_apply" in work.get("forbidden", []):
        return {"ok": False, "decision": "block", "work_id": work_id, "trace_id": trace_id, "reason": "direct_apply_forbidden", "authority": "candidate_only"}
    return {
        "ok": True,
        "work_id": work_id,
        "trace_id": trace_id,
        "decision": "compose_candidate_bundle",
        "authority": "odin_internal_candidate_only",
        "candidate_only": True,
        "steps": ['fragments', 'actions', 'why_trace', 'candidate_dna'],
        "trace": {"claim_boundary": "candidate_projection_only", "app_apply": "app_owned"},
    }
