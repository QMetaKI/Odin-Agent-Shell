from __future__ import annotations

from typing import Any, Dict, List

from .boundary import validate_shadow_boundaries
from .types import ShadowContextCapsule, ShadowReason, ShadowSlotContract, ShadowWorkletGraph, ShadowWorkletNode


def validate_shadow_universal_work(work: Dict[str, Any]) -> List[ShadowReason]:
    reasons = validate_shadow_boundaries(work)
    if not work.get("work_id"):
        reasons.append(ShadowReason("work_id_missing", "work_id is required"))
    if not work.get("input_artifacts"):
        reasons.append(ShadowReason("input_artifacts_missing", "at least one input artifact is required"))
    intent = work.get("work_intent", {})
    if not intent.get("verb"):
        reasons.append(ShadowReason("verb_missing", "work_intent.verb is required"))
    return reasons


def make_shadow_context_capsule(work: Dict[str, Any]) -> ShadowContextCapsule:
    intent = work.get("work_intent", {})
    constraints = work.get("constraints", {})
    return ShadowContextCapsule(
        capsule_id=f"CAP-{work['work_id']}",
        work_id=work["work_id"],
        task_center=intent.get("goal") or intent.get("verb", "bounded work"),
        must_use=list(constraints.get("allowed", []) or []),
        must_not_use=list(constraints.get("forbidden", []) or []),
        style=work.get("style", "clear, bounded, candidate-only"),
    )


def make_shadow_worklet_graph(work: Dict[str, Any], route: str) -> ShadowWorkletGraph:
    verb = work.get("work_intent", {}).get("verb", "generate_candidate")
    nodes = [
        ShadowWorkletNode("W1", "validate_context", "deterministic", "context_capsule_candidate"),
        ShadowWorkletNode("W2", f"{verb}_slot", route, "candidate_projection"),
        ShadowWorkletNode("W3", "critic_minicheck", "3b_micro_critic_router", "critic_report_candidate"),
        ShadowWorkletNode("W4", "compose_response", "deterministic", "response_packet_candidate"),
    ]
    return ShadowWorkletGraph(graph_id=f"WG-{work['work_id']}", work_id=work["work_id"], nodes=nodes)


def make_shadow_slot_contract(work: Dict[str, Any], route: str) -> ShadowSlotContract:
    output_contract = work.get("output_contract", {})
    max_tokens = int(output_contract.get("max_tokens", 600))
    return ShadowSlotContract(
        slot_id=f"SLOT-{work['work_id']}",
        slot_class=f"{work.get('work_intent', {}).get('verb', 'generate')}.slot",
        model_route=route,
        max_input_tokens=min(1800, max(400, max_tokens * 3)),
        max_output_tokens=max_tokens,
        forbidden_claims=list(work.get("constraints", {}).get("forbidden", []) or []) + ["applied", "verified", "sent"],
    )
