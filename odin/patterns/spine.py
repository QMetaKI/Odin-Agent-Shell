from __future__ import annotations
from odin.runtime.ids import stable_id


def build_pattern_spine(patterns: list[dict], flow_packs: list[dict] | None = None) -> dict:
    flow_packs = flow_packs or []
    tags = sorted({tag for p in patterns for tag in p.get("tags", [])})
    operators = sorted({op for p in patterns for op in p.get("operators", [])})
    return {
        "artifact_kind": "odin_pattern_spine",
        "protocol_version": "7.1",
        "spine_id": stable_id("SPINE", {"patterns": patterns, "flows": flow_packs}, 12),
        "pattern_count": len(patterns),
        "flow_pack_count": len(flow_packs),
        "tags": tags,
        "operators": operators,
        "candidate_templates": [p.get("candidate_template", p.get("id")) for p in patterns if p.get("candidate_template") or p.get("id")],
        "claim_boundary": "pattern_spine_is_pattern_prior_not_truth_authority",
    }
