from __future__ import annotations

def build_centerline_packet(work: dict, admissibility: dict | None = None) -> dict:
    contract = work.get("output_contract", {})
    intent = work.get("work_intent", {})
    center = intent.get("goal") or intent.get("verb") or "bounded_candidate_work"
    decision = (admissibility or {}).get("decision", "continue")
    return {
        "artifact_kind": "odin_centerline_packet",
        "protocol_version": "7.1",
        "packet_id": f"CENTER-{work.get('work_id','WORK')}",
        "work_id": work.get("work_id", "WORK"),
        "caller_id": work.get("caller_id", "unknown"),
        "active_center": center,
        "admissibility_decision": decision,
        "authority_boundary": "odin_llm_work_only_app_retains_state_apply_external_send",
        "active_ring_path": ["R0","R1","R2","R3","R4","R5","R6","R7","R8"],
        "active_maria_michael_profile": "mama_qooo_refined_80_20",
        "allowed_routes": ["deterministic", "3b_micro", "3b_7b_8b_hybrid"],
        "blocked_routes": [],
        "forbidden_claims": ["runtime_verified", "tests_passed", "app_mutation", "external_send"],
        "final_gate_required": True,
        "candidate_only": contract.get("candidate_only") is True,
    }
