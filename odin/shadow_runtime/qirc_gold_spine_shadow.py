from __future__ import annotations

def run_qirc_gold_spine_shadow(work: dict) -> dict:
    if work.get("request_direct_apply"):
        return {"ok": False, "decision": "block", "reason": "direct_apply_forbidden"}
    work_id = work.get("work_id", "WORK-SHADOW")
    trace_id = work.get("trace_id", "TRACE-SHADOW")
    return {"ok": True, "work_id": work_id, "trace_id": trace_id, "events": ["work_received", "hot_window_created", "seed_activation_completed", "admissibility_decided", "candidate_composed"], "final": "candidate_only"}
