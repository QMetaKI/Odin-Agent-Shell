"""v7.1.1 Coverage Compiler Reports.

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


def build_v711_coverage_report(
    *,
    repo_root: str = ".",
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build combined v7.1.1 coverage report."""
    from .coverage_matrix import build_v711_coverage_matrix
    from .gap_index import build_v711_gap_index
    from .next_pr_recommender import recommend_next_prs_from_v711_gaps

    matrix = build_v711_coverage_matrix(repo_root=repo_root, generated_at_utc=generated_at_utc)
    gap_index = build_v711_gap_index(repo_root=repo_root, generated_at_utc=generated_at_utc)
    recommendations = recommend_next_prs_from_v711_gaps(gap_index, generated_at_utc=generated_at_utc)

    total = len(matrix.get("coverage", []))
    gaps = gap_index.get("gap_count", 0)
    implemented = total - gaps

    return {
        "artifact_kind": "odin_v711_coverage_report",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "summary": {
            "total_targets": total,
            "implemented": implemented,
            "gaps": gaps,
            "coverage_pct": round(100 * implemented / total, 1) if total else 0,
        },
        "coverage_matrix": matrix,
        "gap_index": gap_index,
        "next_pr_recommendations": recommendations,
        "final_pr_13_remains_deferred": True,
        "not_proven": NOT_PROVEN,
    }
