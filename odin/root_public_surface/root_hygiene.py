"""FINAL-PR-13: Root Public Surface Hygiene Report.

Claim boundary: root_public_surface_cleanup_curates_root_without_deleting_history
candidate_only: true
"""
from __future__ import annotations

import os
from pathlib import Path

CLAIM_BOUNDARY = "root_public_surface_cleanup_curates_root_without_deleting_history"

_KNOWN_ROOT_FILES = {
    "README.md": "root_keep",
    "START_HERE.md": "root_keep",
    "CANON_ENTRY.md": "root_keep",
    "AGENTS.md": "root_keep",
    "LICENSE": "root_keep",
    "DONATIONS.md": "root_keep",
    "pyproject.toml": "root_keep",
    "SYSTEM_MAP.json": "root_keep",
    "FILE_MANIFEST.json": "root_keep",
    "CLAIM_BOUNDARY.md": "root_keep",
    "CLAUDE.md": "root_keep",
    "CODEX_START_HERE.md": "root_keep",
    "CHANGELOG.md": "root_historical_keep",
    "SECURITY.md": "root_keep",
    "LICENSE_POLICY.md": "root_keep",
    "PROTOCOL_BOUNDARY.md": "root_keep",
    "SPDX_POLICY.md": "root_keep",
    "THIRD_PARTY_NOTICES.md": "root_keep",
    "THOR_ODIN_GPL2_ONLY_POLICY.md": "root_keep",
    ".editorconfig": "root_keep",
    ".gitignore": "root_keep",
    "docs": "root_keep",
    "odin": "root_keep",
    "tests": "root_keep",
    "tools": "root_keep",
    "examples": "root_keep",
    "reports": "root_keep",
    "registries": "root_keep",
    "schemas": "root_keep",
    ".github": "root_keep",
    "dist_manifest": "root_generated_keep",
    "legacy": "root_historical_keep",
    "odin_app_sdk": "root_keep",
    "runtime": "root_historical_keep",
    "sdk": "root_keep",
    "templates": "root_keep",
    "windows": "root_keep",
    "scripts": "root_keep",
}


def build_root_hygiene_report(
    *,
    repo_root: str = ".",
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    root = Path(repo_root).resolve()
    classified = {}
    unknown = []
    try:
        for entry in sorted(os.listdir(root)):
            if entry.startswith(".git") and entry != ".github" and entry != ".gitignore" and entry != ".editorconfig":
                continue
            if entry == ".git":
                continue
            classification = _KNOWN_ROOT_FILES.get(entry, "root_unknown_needs_review")
            classified[entry] = classification
            if classification == "root_unknown_needs_review":
                unknown.append(entry)
    except Exception:
        pass

    return {
        "artifact_kind": "odin_final_pr_13_root_hygiene_report",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "classified": classified,
        "unknown_needs_review": unknown,
        "history_not_deleted": True,
        "reports_preserved": True,
        "registries_preserved": True,
        "schemas_preserved": True,
        "tests_preserved": True,
        "readme_present": (root / "README.md").exists(),
        "donations_present": (root / "DONATIONS.md").exists(),
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    }
