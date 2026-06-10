from __future__ import annotations

def build_ring_activation_map(work: dict, route_score: dict) -> dict:
    rings = []
    for ring, role in [("R0","boundary"),("R1","policy"),("R2","universal_work"),("R3","context"),("R4","semantic_bus"),("R5","slots"),("R6","model_route"),("R7","critics"),("R8","candidate")]:
        rings.append({"ring":ring,"role":role,"activation_level":0.8 if ring in {"R0","R1","R6"} else 0.55,"pressure":"normal","reason":"required_for_bounded_candidate_flow"})
    return {"artifact_kind":"odin_ring_activation_map","protocol_version":"7.1","map_id":"RING-"+work.get("work_id","WORK"),"work_id":work.get("work_id","WORK"),"rings":rings}
