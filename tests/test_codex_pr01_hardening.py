import json
from pathlib import Path

import pytest

from odin.cli import (
    CURRENT_CODEX_PR_IDS,
    ROOT,
    _scan_positive_overclaims,
    validate_current_canon_hardening,
    validate_runtime_imports,
    validate_schemas_json,
)
from odin.runtime.config import load_runtime_config
from odin.runtime.errors import OdinValidationError


def test_current_canon_hardening_references_five_pr_path_and_historical_traceability():
    assert validate_current_canon_hardening() == []
    combined = "\n".join(
        (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        for rel in ["README.md", "START_HERE.md", "CANON_ENTRY.md", "CODEX_START_HERE.md", "CLAIM_BOUNDARY.md"]
    )
    for pid in CURRENT_CODEX_PR_IDS:
        assert pid in combined
    for historical in ["PR-00..PR-123", "REAL-PR-01..28", "REAL-GH-PR-01..08"]:
        assert historical in combined


def test_handoff_registry_exposes_five_pr_overlay_without_deleting_eight_pr_traceability():
    registry = json.loads((ROOT / "registries/codex_real_pr_handoff_registry.json").read_text(encoding="utf-8"))
    assert [item["id"] for item in registry["codex_pr_hardening_path"]] == CURRENT_CODEX_PR_IDS
    assert len(registry["execution_prs"]) == 8
    assert registry["historical_traceability"] == ["PR-00..PR-123", "REAL-PR-01..28", "REAL-GH-PR-01..08"]


def test_overclaim_scanner_blocks_positive_claims_but_allows_proof_gap_negation():
    assert _scan_positive_overclaims("This release is production " + "ready for users.") == ["production " + "ready"]
    allowed = "No production readiness proof; not production ready; no live model inference proof."
    assert _scan_positive_overclaims(allowed) == []


def test_schema_json_and_runtime_skeleton_import_validation_are_clean():
    assert validate_schemas_json() == []
    assert validate_runtime_imports() == []


def test_runtime_config_missing_optional_is_visible_and_strict_missing_errors(tmp_path):
    missing = tmp_path / "missing-runtime-config.json"
    cfg = load_runtime_config(missing)
    assert cfg.runtime_candidate_version == "0.8.6"
    assert cfg.config_source.startswith("defaults_missing_optional:")
    with pytest.raises(OdinValidationError, match="runtime config file not found"):
        load_runtime_config(missing, strict=True)


def test_runtime_config_malformed_present_file_errors_deterministically(tmp_path):
    path = tmp_path / "bad-runtime-config.json"
    path.write_text("{not-json", encoding="utf-8")
    with pytest.raises(OdinValidationError, match="invalid runtime config JSON"):
        load_runtime_config(path)
