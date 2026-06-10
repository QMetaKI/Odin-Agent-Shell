from __future__ import annotations

from typing import Any, Dict


def build_low_memory_shadow_plan(work: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "artifact_kind": "odin_shadow_low_memory_plan",
        "protocol_version": "7.1-shadow",
        "work_id": work.get("work_id"),
        "resource_profile": "low_memory_strict",
        "enabled_features": [
            "deterministic_rules", "semantic_bus_light", "context_capsule", "3b_micro_slots", "short_trace_retention"
        ],
        "disabled_features": [
            "heavy_tournament", "normal_7b_route", "large_context", "remote_default", "developer_labs_heavy"
        ],
        "route_ladder": ["static_template", "decision_table", "context_capsule", "1b_2b_micro", "3b_q4_micro", "ask_context"],
        "boundary": "low_memory_plan_only_no_quality_overclaim",
    }
