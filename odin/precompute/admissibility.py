from __future__ import annotations

AUTHORITY_ACTIONS = {"direct_apply", "apply", "send_external", "external_send", "mutate_app_state", "write_app_state", "accept_claim", "issue_receipt"}
AUTHORITY_GOAL_MARKERS = ["apply directly", "send externally", "mutate app state", "write app state", "issue receipt"]


def evaluate_admissibility(work: dict) -> dict:
    constraints = work.get("constraints", {}) or {}
    output_contract = work.get("output_contract", {}) or {}
    work_intent = work.get("work_intent", {}) or {}
    blocked: list[str] = []
    actions = {str(a).lower() for a in constraints.get("actions", [])}
    for action in sorted(actions & AUTHORITY_ACTIONS):
        blocked.append(f"forbidden_authority_action:{action}")
    if output_contract.get("may_apply") is True:
        blocked.append("output_contract_may_apply_true")
    if output_contract.get("candidate_only") is False:
        blocked.append("output_contract_candidate_only_false")
    if output_contract.get("app_owned_apply") is False:
        blocked.append("output_contract_app_owned_apply_false")
    goal = str(work_intent.get("goal", "")).lower()
    for marker in AUTHORITY_GOAL_MARKERS:
        if marker in goal:
            blocked.append(f"forbidden_goal:{marker}")
    return {
        "artifact_kind": "odin_pre_llm_admissibility_decision",
        "protocol_version": "7.1",
        "status": "blocked" if blocked else "allowed",
        "blocked_reasons": blocked,
        "candidate_only": True,
        "claim_boundary": "pre_llm_admissibility_blocks_app_authority_before_provider_dispatch",
    }
