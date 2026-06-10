from __future__ import annotations

def decide_qirc_admissibility(centerline_clear: bool, scope: str, remote_allowed: bool = False) -> dict:
    if not centerline_clear:
        return {"decision": "hold", "reason": ["centerline_unclear"], "next": "ask_context"}
    if scope == "too_broad":
        return {"decision": "split_work", "reason": ["scope_too_broad"], "next": "worklet_graph"}
    blocked = []
    if not remote_allowed:
        blocked.append({"route": "remote", "reason": "remote_not_allowed"})
    return {"artifact_kind": "odin_qirc_admissibility_gate", "protocol_version": "7.1", "decision": "go", "reason": ["centerline_clear", "candidate_only_preserved"], "blocked_routes": blocked, "next": "slot_forge"}
