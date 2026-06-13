"""Documentation Readiness — Reports.

Claim boundary: docs_readiness_prepares_user_docs_not_release_certification
candidate_only: true
"""
from __future__ import annotations

from .doc_index import build_docs_readiness_index
from .start_here_plan import build_start_here_update_plan
from .readme_plan import build_readme_update_plan

CLAIM_BOUNDARY = "docs_readiness_prepares_user_docs_not_release_certification"


def build_docs_readiness_report(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    index = build_docs_readiness_index(generated_at_utc=generated_at_utc)
    start_here_plan = build_start_here_update_plan(generated_at_utc=generated_at_utc)
    readme_plan = build_readme_update_plan(generated_at_utc=generated_at_utc)
    return {
        "artifact_kind": "odin_docs_readiness_report",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "doc_index": index,
        "start_here_plan": start_here_plan,
        "readme_plan": readme_plan,
        "summary": "Docs readiness index complete. Minimal update plans prepared. FINAL-PR-13 remains deferred.",
        "not_proven": ["user_documentation_complete", "release_certification", "production_readiness"],
    }
