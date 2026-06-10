from __future__ import annotations

def decide_admissibility(work: dict) -> dict:
    contract = work.get("output_contract", {})
    forbidden = set(work.get("constraints", {}).get("forbidden", []))
    reasons = []
    if contract.get("candidate_only") is not True:
        reasons.append("output_contract_not_candidate_only")
    if contract.get("requires_app_apply_gate") is not True:
        reasons.append("app_apply_gate_missing")
    if "apply_directly" in forbidden or "direct_apply" in forbidden:
        reasons.append("direct_apply_forbidden")
    if reasons:
        return {"artifact_kind":"odin_admissibility_decision","protocol_version":"7.1","decision_id":"ADM-"+work.get("work_id","WORK"),"work_id":work.get("work_id","WORK"),"decision":"block","reasons":reasons}
    return {"artifact_kind":"odin_admissibility_decision","protocol_version":"7.1","decision_id":"ADM-"+work.get("work_id","WORK"),"work_id":work.get("work_id","WORK"),"decision":"continue","reasons":["center_and_candidate_boundary_ok"]}
