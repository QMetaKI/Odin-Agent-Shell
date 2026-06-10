from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List

FORBIDDEN_ACTION_MARKERS = {
    "apply", "apply_changes", "mutate", "mutate_project", "send", "external_send",
    "patch_applied", "tests_passed", "runtime_verified", "security_verified",
}

@dataclass
class ShadowPolicyDecision:
    ok: bool
    work_id: str
    decision_id: str
    allowed_route_classes: List[str]
    blocked_markers: List[str] = field(default_factory=list)
    required_gates: List[str] = field(default_factory=list)
    app_authority: str = "app_retains_state_apply_and_external_actions"
    odin_authority: str = "candidate_generation_and_local_processing_only"
    boundary: str = "policy_decision_shadow_no_authority_transfer"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def evaluate_shadow_policy(work: Dict[str, Any], *, remote_allowed: bool = False) -> ShadowPolicyDecision:
    """Near-final policy evaluator for Codex conversion.

    Pure function. Does not call models, providers, sockets, app APIs or filesystem writes.
    """
    work_id = work.get("work_id", "WORK-MISSING")
    intent = work.get("work_intent") or {}
    constraints = work.get("constraints") or {}
    explicit_action_text = " ".join([
        str(intent.get("verb", "")),
        str(intent.get("mode", "")),
        str(intent.get("goal", "")),
        " ".join(str(x) for x in constraints.get("allowed", []) or []),
        " ".join(str(x) for x in work.get("requested_actions", []) or []),
    ]).lower()
    blocked = sorted(marker for marker in FORBIDDEN_ACTION_MARKERS if marker in explicit_action_text)
    model_policy = work.get("model_policy") or {}
    route = str(model_policy.get("route", "")).lower()
    if (route == "remote" or model_policy.get("allow_remote") is True) and not remote_allowed:
        blocked.append("remote_without_explicit_permission")
    output_contract = work.get("output_contract") or {}
    if output_contract.get("candidate_only") is not True:
        blocked.append("output_contract_not_candidate_only")
    if output_contract.get("requires_app_apply_gate") is not True:
        blocked.append("app_apply_gate_missing")
    allowed_route_classes = [
        "deterministic",
        "1b_2b_micro",
        "3b_micro",
        "7b_8b_quality",
        "3b_7b_8b_hybrid",
        "quality_local_if_policy_allows",
        "heavy_batch_if_policy_allows",
    ]
    if remote_allowed:
        allowed_route_classes.append("remote_optional_explicit")
    return ShadowPolicyDecision(
        ok=not blocked,
        work_id=work_id,
        decision_id=f"POL-{work_id}",
        allowed_route_classes=allowed_route_classes,
        blocked_markers=blocked,
        required_gates=[
            "binding_gate",
            "universal_work_gate",
            "candidate_only_gate",
            "claim_boundary_gate",
            "semantic_bus_local_only_gate",
            "app_owned_apply_gate",
        ],
    )
