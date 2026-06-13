"""FINAL-PR-13: README v1 module.

Claim boundary: readme_v1_public_surface_documents_candidate_release_without_overclaiming
candidate_only: true
"""
from .readme_plan import build_readme_v1_plan
from .thanks_block_source import verify_thor_thanks_block_source
from .reports import build_readme_v1_report

__all__ = [
    "build_readme_v1_plan",
    "verify_thor_thanks_block_source",
    "build_readme_v1_report",
]
