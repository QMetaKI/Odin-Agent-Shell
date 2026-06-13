"""FINAL-PR-13: Root Public Surface Reports.

Claim boundary: root_public_surface_cleanup_curates_root_without_deleting_history
candidate_only: true
"""
from __future__ import annotations

from .root_inventory import build_root_inventory
from .root_hygiene import build_root_hygiene_report
from .root_index import build_root_index

CLAIM_BOUNDARY = "root_public_surface_cleanup_curates_root_without_deleting_history"


def build_root_public_surface_report(
    *,
    repo_root: str = ".",
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    inventory = build_root_inventory(repo_root=repo_root, generated_at_utc=generated_at_utc)
    hygiene = build_root_hygiene_report(repo_root=repo_root, generated_at_utc=generated_at_utc)
    index = build_root_index(repo_root=repo_root, generated_at_utc=generated_at_utc)
    return {
        "artifact_kind": "odin_final_pr_13_root_public_surface_report",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "status": "ok",
        "readme_present": inventory.get("readme_present", False),
        "donations_present": inventory.get("donations_present", False),
        "history_preserved": hygiene.get("history_not_deleted", True),
        "inventory_summary": {
            "present_count": len(inventory.get("present", [])),
            "missing_count": len(inventory.get("missing", [])),
        },
        "hygiene_summary": {
            "unknown_count": len(hygiene.get("unknown_needs_review", [])),
        },
        "index": index,
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    }
