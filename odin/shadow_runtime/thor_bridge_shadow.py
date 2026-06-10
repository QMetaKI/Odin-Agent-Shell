from __future__ import annotations

from typing import Any, Dict


def build_shadow_thor_bridge_plan(work: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "artifact_kind": "odin_shadow_thor_bridge_plan",
        "protocol_version": "7.1-shadow",
        "work_id": work.get("work_id"),
        "thor_mode": "lite" if (work.get("work_intent") or {}).get("verb") != "plan" else "review",
        "handoff_fields": ["task", "guard", "expected_output", "return_contract", "claim_boundary"],
        "return_contract": {
            "candidate_only": True,
            "requires_review": True,
            "no_apply": True,
        },
        "boundary": "thor_bridge_candidate_handoff_only_no_agent_authority",
    }
