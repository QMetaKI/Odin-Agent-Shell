"""FINAL-PR-13: Root Public Surface Cleanup module.

Claim boundary: root_public_surface_cleanup_curates_root_without_deleting_history
candidate_only: true
"""
from .root_inventory import build_root_inventory
from .root_hygiene import build_root_hygiene_report
from .root_index import build_root_index
from .reports import build_root_public_surface_report

__all__ = [
    "build_root_inventory",
    "build_root_hygiene_report",
    "build_root_index",
    "build_root_public_surface_report",
]
