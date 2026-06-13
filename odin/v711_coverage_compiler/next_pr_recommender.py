"""v7.1.1 Next PR Recommender — recommends next PRs from gap index.

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

_RECOMMENDATIONS = [
    {
        "pr_id": "FINAL-PR-12",
        "pr_name": "Semantic Kernel Closure + Claims Compiler + Coverage Compiler",
        "addresses_gaps": [
            "claims_compiler",
            "y_pattern_operationalization",
            "semantic_bus",
            "trace_receipt_proof",
        ],
        "priority": "high",
    },
    {
        "pr_id": "FINAL-PR-13",
        "pr_name": "Release Closure v1 — PR13 is deferred",
        "addresses_gaps": [
            "provider_runtime",
            "candidate_tournament",
            "sdk_api_app_bridge",
            "release_boundary_gates",
        ],
        "priority": "high",
    },
]


def recommend_next_prs_from_v711_gaps(
    gap_index: dict,
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Recommend next PRs from gap index."""
    return {
        "artifact_kind": "odin_v711_next_pr_recommendations",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "gap_count_input": gap_index.get("gap_count", 0),
        "recommendations": _RECOMMENDATIONS,
        "final_pr_13_is_release_closure": True,
        "final_pr_13_remains_deferred": True,
        "not_proven": NOT_PROVEN,
    }
