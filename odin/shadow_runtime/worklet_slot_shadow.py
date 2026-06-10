from __future__ import annotations

from typing import Any, Dict, List


def build_shadow_worklet_plan(work: Dict[str, Any], route: str = "3b_7b_8b_hybrid") -> Dict[str, Any]:
    verb = (work.get("work_intent") or {}).get("verb", "generate_candidate")
    return {
        "artifact_kind": "odin_shadow_worklet_plan",
        "protocol_version": "7.1-shadow",
        "work_id": work.get("work_id"),
        "nodes": [
            {"node_id": "W1", "worklet_type": "binding_check", "route": "deterministic"},
            {"node_id": "W2", "worklet_type": "context_capsule", "route": "deterministic"},
            {"node_id": "W3", "worklet_type": f"{verb}_slot", "route": route},
            {"node_id": "W4", "worklet_type": "critic_cascade", "route": "3b_micro_critic_router"},
            {"node_id": "W5", "worklet_type": "candidate_compose", "route": "deterministic"},
        ],
        "edges": [
            ["W1", "W2"], ["W2", "W3"], ["W3", "W4"], ["W4", "W5"],
        ],
        "claim_boundary": "worklet_plan_candidate_only",
    }


def build_shadow_gaptext(work: Dict[str, Any], slot_class: str = "bounded_slot") -> Dict[str, Any]:
    intent = work.get("work_intent") or {}
    constraints = work.get("constraints") or {}
    return {
        "artifact_kind": "odin_shadow_gaptext",
        "protocol_version": "7.1-shadow",
        "work_id": work.get("work_id"),
        "slot_class": slot_class,
        "sections": {
            "task": intent.get("goal") or intent.get("verb", "bounded work"),
            "allowed": constraints.get("allowed", []),
            "forbidden": constraints.get("forbidden", []) + ["apply", "send", "verified_claim"],
            "output_shape": (work.get("output_contract") or {}).get("artifact_type", "candidate"),
            "self_check": "Return only candidate content supported by input artifacts.",
        },
        "boundary": "gaptext_only_no_prompt_runtime_claim",
    }
