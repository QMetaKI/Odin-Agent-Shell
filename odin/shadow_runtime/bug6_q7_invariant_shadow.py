from __future__ import annotations
FORBIDDEN_MARKERS = {"app_mutation", "external_send", "hidden_apply", "final_reality_claim"}
def check_bug6_q7_invariants(work: dict) -> dict:
    markers = set(work.get("markers", []))
    violations = sorted(markers & FORBIDDEN_MARKERS)
    too_large = work.get("context_tokens", 0) > work.get("max_context_tokens", 1600)
    if too_large:
        violations.append("worker_load_limit")
    decision = "allow" if not violations else ("split_work" if violations == ["worker_load_limit"] else "block")
    return {"artifact_kind":"odin_bug6_q7_shadow_decision","children_first_preserved":"worker_load_limit" not in violations,"authority_separation_preserved":not any(v in violations for v in ["app_mutation","external_send","hidden_apply"]),"candidate_only_preserved":"final_reality_claim" not in violations,"q7_route_cleanliness_score":0.9 if not violations else 0.25,"violations":violations,"decision":decision}
