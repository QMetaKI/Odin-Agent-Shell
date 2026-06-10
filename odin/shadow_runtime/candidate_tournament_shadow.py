from __future__ import annotations

from typing import Any, Dict, List


def run_shadow_candidate_tournament(work: Dict[str, Any], candidates: List[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    candidates = candidates or [
        {"candidate_id": "CAND-A", "score": 0.72, "risk": 0.10},
        {"candidate_id": "CAND-B", "score": 0.82, "risk": 0.16},
        {"candidate_id": "CAND-C", "score": 0.67, "risk": 0.05},
    ]
    ranked = sorted(candidates, key=lambda c: (c.get("score", 0) - c.get("risk", 0)), reverse=True)
    return {
        "artifact_kind": "odin_shadow_candidate_tournament",
        "protocol_version": "7.1-shadow",
        "work_id": work.get("work_id"),
        "ranking": ranked,
        "selected_candidate_id": ranked[0]["candidate_id"] if ranked else None,
        "critic_axes": ["claim", "style", "genericness", "schema"],
        "boundary": "selection_candidate_only_no_apply",
    }
