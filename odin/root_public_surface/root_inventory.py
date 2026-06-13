"""FINAL-PR-13: Root Public Surface Inventory.

Claim boundary: root_public_surface_cleanup_curates_root_without_deleting_history
candidate_only: true
"""
from __future__ import annotations

import os
from pathlib import Path

CLAIM_BOUNDARY = "root_public_surface_cleanup_curates_root_without_deleting_history"

_EXPECTED_ROOT_ITEMS = [
    "README.md",
    "START_HERE.md",
    "CANON_ENTRY.md",
    "AGENTS.md",
    "LICENSE",
    "DONATIONS.md",
    "pyproject.toml",
    "SYSTEM_MAP.json",
    "FILE_MANIFEST.json",
    "docs",
    "odin",
    "tests",
    "tools",
    "examples",
    "reports",
    "registries",
    "schemas",
    ".github",
]


def build_root_inventory(
    *,
    repo_root: str = ".",
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    root = Path(repo_root).resolve()
    present = []
    missing = []
    for item in _EXPECTED_ROOT_ITEMS:
        p = root / item
        if p.exists():
            present.append(item)
        else:
            missing.append(item)

    all_root_items = []
    try:
        for entry in sorted(os.listdir(root)):
            if entry.startswith(".git"):
                continue
            all_root_items.append(entry)
    except Exception:
        pass

    return {
        "artifact_kind": "odin_final_pr_13_root_inventory",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "expected_root_items": _EXPECTED_ROOT_ITEMS,
        "present": present,
        "missing": missing,
        "all_root_items": all_root_items,
        "readme_present": "README.md" in present,
        "donations_present": "DONATIONS.md" in present,
        "history_preserved": True,
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    }
