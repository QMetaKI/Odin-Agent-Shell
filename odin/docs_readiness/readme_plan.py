"""Documentation Readiness — README Update Plan.

Claim boundary: docs_readiness_prepares_user_docs_not_release_certification
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "docs_readiness_prepares_user_docs_not_release_certification"


def build_readme_update_plan(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_readme_update_plan",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "update_approach": "minimal_corrections_preserve_canonical_structure",
        "broad_rewrite": False,
        "recommended_additions": [
            {
                "section": "Validation",
                "content": "Add FINAL-PR-12 validate commands as current-state pointers",
                "priority": "low",
            },
        ],
        "forbidden_additions": [
            "production_readiness_claim",
            "release_certification_claim",
            "security_certification_claim",
            "model_superiority_claim",
        ],
        "preserve_canonical_structure": True,
        "not_proven": ["user_documentation_complete", "release_certification"],
    }
