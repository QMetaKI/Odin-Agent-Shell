"""Documentation Readiness — Start Here Update Plan.

Claim boundary: docs_readiness_prepares_user_docs_not_release_certification
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "docs_readiness_prepares_user_docs_not_release_certification"


def build_start_here_update_plan(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_start_here_update_plan",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "update_approach": "minimal_corrections_preserve_canonical_structure",
        "broad_rewrite": False,
        "recommended_additions": [
            {
                "section": "Current Release Status",
                "content": "Add pointer to FINAL-PR-12 release readiness hardening. Note FINAL-PR-13 remains deferred.",
                "priority": "medium",
            },
            {
                "section": "Validation Commands",
                "content": "Add validate-release-readiness-hardening and validate-final-pr-12-release-readiness-hardening",
                "priority": "medium",
            },
        ],
        "forbidden_additions": [
            "production_readiness_claim",
            "release_certification_claim",
            "model_superiority_claim",
        ],
        "not_proven": ["user_documentation_complete", "release_certification"],
    }
