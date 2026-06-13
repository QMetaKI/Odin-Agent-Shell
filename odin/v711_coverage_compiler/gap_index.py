"""v7.1.1 Gap Index — lists targets not yet fully implemented.

Claim boundary: v711_coverage_compiler_maps_target_to_repo_evidence_not_runtime_completion
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "v711_coverage_compiler_maps_target_to_repo_evidence_not_runtime_completion"

NOT_PROVEN = [
    "production_readiness",
    "live_model_inference",
    "app_state_mutation",
    "external_send_authority",
]

_IMPLEMENTED_STATUSES = {"implemented"}


def build_v711_gap_index(
    *,
    repo_root: str = ".",
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build gap index from coverage matrix — rows where status != 'implemented'."""
    from .coverage_matrix import build_v711_coverage_matrix

    matrix = build_v711_coverage_matrix(repo_root=repo_root, generated_at_utc=generated_at_utc)
    coverage = matrix.get("coverage", [])

    gaps = []
    for row in coverage:
        status = row.get("status", "")
        if status not in _IMPLEMENTED_STATUSES:
            gaps.append({
                "target_id": row["target_id"],
                "target_name": row["target_name"],
                "status": status,
                "evidence_class": row.get("evidence_class", ""),
                "current_gap": row.get("current_gap", ""),
                "next_action": row.get("next_action", ""),
                "priority_for_pr13": row.get("target_priority", "medium"),
            })

    return {
        "artifact_kind": "odin_v711_gap_index",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "gap_count": len(gaps),
        "gaps": gaps,
        "not_proven": NOT_PROVEN,
    }
