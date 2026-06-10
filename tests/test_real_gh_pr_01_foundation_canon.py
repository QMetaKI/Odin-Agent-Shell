from __future__ import annotations

import json
from pathlib import Path

from odin.cli import ROOT, validate_current_public_canon


ROOT_DOCS = [
    "README.md",
    "START_HERE.md",
    "CANON_ENTRY.md",
    "CODEX_START_HERE.md",
    "CLAIM_BOUNDARY.md",
    "PROTOCOL_BOUNDARY.md",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_real_gh_pr_01_current_public_canon_validator_passes() -> None:
    assert validate_current_public_canon() == []


def test_root_docs_point_to_v087_handoff_and_v086_runtime_base() -> None:
    for rel in ROOT_DOCS:
        text = read(rel)
        assert "v0.8.7 CODEX_REAL_PR_HANDOFF_LADDER_LOCK" in text
        assert "v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK" in text
        assert "REAL-GH-PR-01..08" in text
        assert "PR-00..PR-123" in text
        assert "REAL-PR-01..28" in text


def test_root_docs_do_not_present_older_locks_as_current() -> None:
    for rel in ROOT_DOCS:
        for line in read(rel).splitlines():
            normalized = " ".join(line.lower().split())
            has_old_version = any(marker in normalized for marker in ["v0.3", "v0.4", "v0.5", "v0.6", "v0.7"])
            if "current" in normalized and has_old_version:
                assert any(scope in normalized for scope in ["historical", "history", "changelog", "not the current", "not current"]), line
            assert "is the current canonical prep state" not in normalized
            assert "current actual github execution sequence: `real-pr-" not in normalized


def test_actual_and_internal_ladders_remain_distinct() -> None:
    handoff = json.loads((ROOT / "registries" / "codex_real_pr_handoff_registry.json").read_text(encoding="utf-8"))
    execution_ids = [pr["id"] for pr in handoff["execution_prs"]]
    assert execution_ids == [f"REAL-GH-PR-{index:02d}" for index in range(1, 9)]
    assert handoff["current_handoff"] == "v0.8.7_CODEX_REAL_PR_HANDOFF_LADDER_LOCK"
    assert handoff["current_base"] == "v0.8.6_DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK"
    assert handoff["internal_traceability_ladders"] == ["PR-00..PR-123", "REAL-PR-01..28"]


def test_universal_work_candidate_boundary_language_is_preserved() -> None:
    combined = "\n".join(read(rel) for rel in ROOT_DOCS).lower()
    for phrase in [
        "candidate-only",
        "caller/app-owned apply",
        "apps own state",
        "external sends",
        "providers are",
        "qirc",
        "not app-state authority",
        "model output is projection, not truth",
    ]:
        assert phrase in combined


def test_overclaim_language_is_negated_or_proof_gap_scoped() -> None:
    allowed_scopes = ["not " + "production" + " ready", "does not claim", "not claim", "without receipt"]
    for rel in ROOT_DOCS:
        for line in read(rel).splitlines():
            normalized = " ".join(line.lower().split())
            if "production" + " ready" in normalized:
                assert any(scope in normalized for scope in allowed_scopes), line
