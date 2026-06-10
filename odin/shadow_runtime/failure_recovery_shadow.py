from __future__ import annotations

from typing import Any, Dict, List

RECOVERY_BY_FAILURE = {
    "BINDING_INVALID": ["reject_before_model", "ask_app_to_repair_manifest_or_binding"],
    "PRIVACY_DENIED": ["redact_or_block", "ask_app_for_lower_privacy_digest"],
    "ARTIFACT_BLOCKED": ["block", "request_safe_artifact_digest"],
    "VERB_FORBIDDEN": ["reject", "suggest_allowed_verb"],
    "OUTPUT_CONTRACT_INVALID": ["reject", "repair_candidate_contract"],
    "CONTEXT_TOO_BROAD": ["semantic_pressure_valve", "split_work", "ask_context"],
    "MODEL_ROUTE_BLOCKED": ["lower_route", "ask_user_permission", "cannot_safely_complete"],
    "CLAIM_BOUNDARY_HIT": ["downgrade_language", "remove_claim", "request_receipt"],
    "SCHEMA_INVALID": ["3b_schema_repair", "retry_once", "block_if_unrepaired"],
    "NEEDS_CONTEXT": ["context_request_to_app"],
    "CANNOT_SAFELY_COMPLETE": ["return_conflict_candidate"],
}


def plan_shadow_failure_recovery(failure_codes: List[str]) -> Dict[str, Any]:
    actions: List[str] = []
    for code in failure_codes:
        actions.extend(RECOVERY_BY_FAILURE.get(code, ["return_conflict_candidate"]))
    deduped = []
    for action in actions:
        if action not in deduped:
            deduped.append(action)
    return {
        "artifact_kind": "odin_shadow_failure_recovery_plan",
        "protocol_version": "7.1-shadow",
        "failure_codes": failure_codes,
        "recommended_actions": deduped,
        "first_principle": "repair_before_escalate_but_block_before_overclaim",
        "boundary": "failure_recovery_candidate_only_no_hidden_apply",
    }
