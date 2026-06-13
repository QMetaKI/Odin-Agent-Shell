"""FINAL-PR-13: README v1 Reports.

Claim boundary: readme_v1_public_surface_documents_candidate_release_without_overclaiming
candidate_only: true
"""
from __future__ import annotations

from pathlib import Path

from .readme_plan import build_readme_v1_plan, _REQUIRED_SECTIONS
from .thanks_block_source import verify_thor_thanks_block_source, THOR_THANKS_BLOCK_HEADING

CLAIM_BOUNDARY = "readme_v1_public_surface_documents_candidate_release_without_overclaiming"


def build_readme_v1_report(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    plan = build_readme_v1_plan(generated_at_utc=generated_at_utc)
    root = Path(__file__).resolve().parents[2]
    readme_path = root / "README.md"
    readme_exists = readme_path.exists()
    sections_present = []
    sections_missing = []
    thanks_block_present = False
    donations_link_present = False
    if readme_exists:
        text = readme_path.read_text(encoding="utf-8")
        for section in _REQUIRED_SECTIONS:
            if section in text:
                sections_present.append(section)
            else:
                sections_missing.append(section)
        thanks_block_present = THOR_THANKS_BLOCK_HEADING in text
        donations_link_present = "DONATIONS.md" in text
    return {
        "artifact_kind": "odin_final_pr_13_readme_v1_report",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "status": "ok" if readme_exists and not sections_missing else "incomplete",
        "readme_exists": readme_exists,
        "sections_present_count": len(sections_present),
        "sections_missing": sections_missing,
        "thanks_block_present": thanks_block_present,
        "donations_link_present": donations_link_present,
        "plan": plan,
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    }
