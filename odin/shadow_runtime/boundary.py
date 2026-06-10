from __future__ import annotations

from typing import Any, Dict, List

from .constants import FORBIDDEN_ACTION_KINDS, FORBIDDEN_BUS_REQUESTS
from .types import ShadowReason, ShadowRuntimeResult


def ensure_candidate_only(work: Dict[str, Any]) -> List[ShadowReason]:
    reasons: List[ShadowReason] = []
    output_contract = work.get("output_contract", {})
    if output_contract.get("candidate_only") is not True:
        reasons.append(ShadowReason("candidate_only_required", "output_contract.candidate_only must be true"))
    if output_contract.get("requires_app_apply_gate") is not True:
        reasons.append(ShadowReason("app_apply_gate_required", "output must require app-owned apply gate"))
    return reasons


def ensure_no_forbidden_actions(work: Dict[str, Any]) -> List[ShadowReason]:
    reasons: List[ShadowReason] = []
    actions = work.get("requested_actions", []) or []
    for action in actions:
        kind = action.get("action_kind") if isinstance(action, dict) else str(action)
        if kind in FORBIDDEN_ACTION_KINDS:
            reasons.append(ShadowReason("direct_apply_forbidden", f"forbidden action requested: {kind}"))
    return reasons


def ensure_semantic_bus_boundary(work: Dict[str, Any]) -> List[ShadowReason]:
    reasons: List[ShadowReason] = []
    bus_request = work.get("semantic_bus_request", {}) or {}
    requested = set(bus_request.get("features", []) or [])
    blocked = sorted(requested & FORBIDDEN_BUS_REQUESTS)
    for feature in blocked:
        reasons.append(ShadowReason("semantic_bus_network_forbidden", f"semantic bus feature is not allowed in Odin Core: {feature}"))
    return reasons


def ensure_binding_policy(work: Dict[str, Any]) -> List[ShadowReason]:
    reasons: List[ShadowReason] = []
    if not work.get("binding_ref"):
        reasons.append(ShadowReason("binding_missing", "binding_ref is required"))
    if not work.get("caller_id"):
        reasons.append(ShadowReason("caller_missing", "caller_id is required"))
    if work.get("claim_boundary") != "candidate_projection_only":
        reasons.append(ShadowReason("claim_boundary_invalid", "claim_boundary must be candidate_projection_only"))
    return reasons


def shadow_final_gate(result: ShadowRuntimeResult) -> ShadowRuntimeResult:
    if result.candidate and not result.candidate.candidate_only:
        result.reasons.append(ShadowReason("final_gate_blocked", "candidate_only was false"))
        result.ok = False
    if result.candidate and not result.candidate.requires_app_apply_gate:
        result.reasons.append(ShadowReason("final_gate_blocked", "requires_app_apply_gate was false"))
        result.ok = False
    if any(code.startswith("direct_apply") or code.endswith("forbidden") for code in result.reason_codes()):
        result.ok = False
    return result


def validate_shadow_boundaries(work: Dict[str, Any]) -> List[ShadowReason]:
    reasons: List[ShadowReason] = []
    reasons.extend(ensure_binding_policy(work))
    reasons.extend(ensure_candidate_only(work))
    reasons.extend(ensure_no_forbidden_actions(work))
    reasons.extend(ensure_semantic_bus_boundary(work))
    return reasons
