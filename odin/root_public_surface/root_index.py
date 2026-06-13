"""FINAL-PR-13: Root Public Surface Index.

Claim boundary: root_public_surface_cleanup_curates_root_without_deleting_history
candidate_only: true
"""
from __future__ import annotations

from pathlib import Path

CLAIM_BOUNDARY = "root_public_surface_cleanup_curates_root_without_deleting_history"


def build_root_index(
    *,
    repo_root: str = ".",
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    root = Path(repo_root).resolve()
    return {
        "artifact_kind": "odin_final_pr_13_root_index",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "primary_entry_points": [
            {"file": "README.md", "purpose": "v1.0 public surface — start here"},
            {"file": "START_HERE.md", "purpose": "First-use pointer"},
            {"file": "CANON_ENTRY.md", "purpose": "Current public canon entry"},
            {"file": "AGENTS.md", "purpose": "Agent operator boundary definitions"},
            {"file": "CODEX_START_HERE.md", "purpose": "Codex workflow entry"},
            {"file": "DONATIONS.md", "purpose": "Optional donations information"},
        ],
        "primary_directories": [
            {"dir": "odin/", "purpose": "Core Odin Python package"},
            {"dir": "docs/", "purpose": "Documentation, specs, audits, reports"},
            {"dir": "tests/", "purpose": "Test suite"},
            {"dir": "tools/", "purpose": "Validator and rebaseline tools"},
            {"dir": "examples/", "purpose": "Example artifacts and fixtures"},
            {"dir": "reports/", "purpose": "Generated proof and evidence reports"},
            {"dir": "registries/", "purpose": "Machine-readable registries"},
            {"dir": "schemas/", "purpose": "JSON schemas"},
            {"dir": ".github/", "purpose": "GitHub workflows and configuration"},
        ],
        "quick_validation": [
            "python -m odin.cli validate-all",
            "python -m odin.cli run-operational-spine --demo",
            "python -m odin.cli build-v1-release-truth --demo",
            "PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider",
        ],
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    }
