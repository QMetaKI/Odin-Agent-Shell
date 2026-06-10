from __future__ import annotations

def score_routes(work: dict, seed_packet: dict, resource_profile: str = "standard_local") -> dict:
    route = "3b_7b_8b_hybrid" if resource_profile not in {"low_memory_strict"} else "3b_micro"
    components = {"expected_quality_gain":0.74,"stability_gain":0.78,"boundary_fit":0.95,"context_fit":0.72,"token_cost":0.18,"latency_cost":0.22,"complexity_cost":0.20,"privacy_risk":0.05,"claim_risk":0.08,"uncertainty_cost":0.12}
    score = components["expected_quality_gain"] + components["stability_gain"] + components["boundary_fit"] + components["context_fit"] - sum(components[k] for k in ["token_cost","latency_cost","complexity_cost","privacy_risk","claim_risk","uncertainty_cost"])
    return {"artifact_kind":"odin_route_score","protocol_version":"7.1","score_id":"QSCORE-"+work.get("work_id","WORK"),"work_id":work.get("work_id","WORK"),"selected_route":route,"score":round(score,3),"components":components,"blocked_routes":[{"route":"heavy_local","reason":"quality_gain_not_worth_latency_for_interactive_work"}]}
