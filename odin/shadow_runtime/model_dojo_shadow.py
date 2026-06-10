from __future__ import annotations

from typing import Any, Dict, List


def score_shadow_model_dojo(model_id: str, results: Dict[str, float] | None = None) -> Dict[str, Any]:
    results = results or {"json_fill": 0.84, "claim_scan": 0.79, "long_synthesis": 0.42, "latency": 0.88}
    best_for = [name for name, score in results.items() if score >= 0.75 and name != "latency"]
    avoid_for = [name for name, score in results.items() if score < 0.50]
    return {
        "artifact_kind": "odin_shadow_model_dojo_profile",
        "protocol_version": "7.1-shadow",
        "model_id": model_id,
        "best_for": best_for,
        "avoid_for": avoid_for,
        "scores": results,
        "profile_status": "shadow_profile_candidate",
        "boundary": "profile_candidate_only_no_benchmark_claim",
    }
