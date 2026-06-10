from __future__ import annotations

def build_why_trace(work: dict, centerline: dict, seed_packet: dict, role_packet: dict, route_score: dict, ring_map: dict) -> dict:
    return {"artifact_kind":"odin_why_trace","protocol_version":"7.1","why_trace_id":"WHY-"+work.get("work_id","WORK"),"work_id":work.get("work_id","WORK"),"selected_center":centerline.get("active_center"),"selected_route":route_score.get("selected_route"),"active_seeds":[s["seed_id"] for s in seed_packet.get("active_seeds",[])],"active_archetype_roles":role_packet.get("active_roles",[]),"blocked_routes":route_score.get("blocked_routes",[]),"summary":"Selected route preserves candidate-only boundary and smallest sufficient worker discipline.","redaction_level":"app_safe"}
