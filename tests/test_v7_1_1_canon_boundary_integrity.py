from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/v7_1_1/check_canon_boundary_integrity.py"
CLAIM_REGISTRY = ROOT / "registries/v7_1_1_claim_boundary_registry.json"
FORBIDDEN_REGISTRY = ROOT / "registries/v7_1_1_forbidden_claim_registry.json"
SCHEMA = ROOT / "schemas/v7_1_1_canon_boundary_integrity_report.schema.json"
REPORT = ROOT / "reports/v7_1_1_canon_boundary_integrity_report.json"
PR25_TOOL = ROOT / "tools/v7_1_1/build_operational_coverage_gap_report.py"

REQUIRED_NON_CLAIMS = {
    "no runtime completion claim",
    "no production readiness claim",
    "no release certification claim",
    "no security certification claim",
    "no target-host proof claim",
    "no live model inference proof claim",
    "no model quality proof claim",
    "no QIRC server runtime proof claim",
    "no provider execution proof claim",
    "no app-owned apply/state/external-send authority claim",
    "no external app integration proof claim",
    "no measured small-model performance improvement proof claim",
}

REQUIRED_PATTERNS = {
    "production ready",
    "production-ready",
    "ready for production",
    "release ready",
    "release-ready",
    "security certified",
    "security-certified",
    "certified secure",
    "target-host proven",
    "target host proven",
    "target-host proof complete",
    "target host proof complete",
    "live model proven",
    "live model proof complete",
    "model quality proven",
    "measured small-model improvement",
    "QIRC server implemented",
    "QIRC runtime implemented",
    "provider execution implemented",
    "Windows service implemented",
    "Windows tray implemented",
    "installer proof complete",
    "external app integration proven",
    "app apply authority implemented",
    "external send implemented",
    "network/public room implemented",
}

IGNORED_SUBSTRINGS = {
    ".odin_runtime/",
    "odin_agent_shell.egg-info/",
    "__pycache__/",
    ".pytest_cache/",
    ".mypy_cache/",
    ".ruff_cache/",
    ".coverage",
    "dist/",
    "build/",
    ".pyc",
    ".pyo",
    ".egg-info/",
    ".git/",
}


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _run(out: Path, repo_root: Path = ROOT, *extra: str):
    return subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--repo-root",
            str(repo_root),
            "--out",
            str(out),
            "--generated-at-utc",
            "2026-01-01T00:00:00Z",
            *extra,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def _make_min_repo(tmp_path: Path, body: str, rel: str = "docs/claim.md") -> Path:
    repo = tmp_path / "repo"
    (repo / "registries").mkdir(parents=True)
    (repo / "docs").mkdir(parents=True)
    shutil.copy2(CLAIM_REGISTRY, repo / "registries/v7_1_1_claim_boundary_registry.json")
    shutil.copy2(FORBIDDEN_REGISTRY, repo / "registries/v7_1_1_forbidden_claim_registry.json")
    target = repo / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8")
    return repo


def test_required_artifacts_exist():
    assert CLAIM_REGISTRY.exists()
    assert FORBIDDEN_REGISTRY.exists()
    assert TOOL.exists()
    assert SCHEMA.exists()


def test_tool_runs_successfully_with_deterministic_timestamp(tmp_path: Path):
    out = tmp_path / "report.json"
    result = _run(out)
    assert result.returncode == 0, result.stderr + result.stdout
    data = _json(out)
    assert data["generated_at_utc"] == "2026-01-01T00:00:00Z"


def test_report_identity_status_and_claim_boundary(tmp_path: Path):
    out = tmp_path / "report.json"
    assert _run(out).returncode == 0
    data = _json(out)
    assert data["report_id"] == "odin.v7_1_1_canon_boundary_integrity_report"
    assert data["status"] == "local_claim_boundary_integrity_report_not_runtime_proof"
    assert "static_local_claim_scan" in data["claim_boundary"] or "not_claim_truth" in data["claim_boundary"]


def test_required_non_claims_are_present_in_registry_and_report(tmp_path: Path):
    registry = _json(CLAIM_REGISTRY)
    assert REQUIRED_NON_CLAIMS <= set(registry["required_non_claims"])
    out = tmp_path / "report.json"
    assert _run(out).returncode == 0
    data = _json(out)
    assert REQUIRED_NON_CLAIMS <= set(data["non_claims"])


def test_forbidden_patterns_and_allowed_context_markers_present():
    registry = _json(FORBIDDEN_REGISTRY)
    assert REQUIRED_PATTERNS <= set(registry["positive_claim_patterns"])
    markers = set(registry["allowed_context_markers"])
    for marker in ["non-claim", "not claimed", "future evidence", "external receipt required"]:
        assert marker in markers


def test_current_repo_report_has_zero_hard_violations(tmp_path: Path):
    out = tmp_path / "report.json"
    assert _run(out).returncode == 0
    data = _json(out)
    assert data["hard_violations"] == []
    assert data["summary"]["hard_violation_count"] == 0


def test_tool_fails_closed_when_claim_boundary_registry_is_missing(tmp_path: Path):
    repo = tmp_path / "repo"
    (repo / "registries").mkdir(parents=True)
    shutil.copy2(FORBIDDEN_REGISTRY, repo / "registries/v7_1_1_forbidden_claim_registry.json")
    out = tmp_path / "report.json"
    result = _run(out, repo)
    assert result.returncode != 0
    assert _json(out)["hard_violations"]


def test_injected_forbidden_positive_claim_is_flagged(tmp_path: Path):
    repo = _make_min_repo(tmp_path, "The runtime is production ready.\n")
    out = tmp_path / "report.json"
    result = _run(out, repo)
    assert result.returncode != 0
    data = _json(out)
    assert any(f["context_type"] == "forbidden_positive_claim" for f in data["hard_violations"])


def test_same_phrase_is_allowed_as_explicit_non_claim(tmp_path: Path):
    repo = _make_min_repo(tmp_path, "Non-claim: production ready is not claimed.\n")
    out = tmp_path / "report.json"
    assert _run(out, repo).returncode == 0
    data = _json(out)
    assert data["hard_violations"] == []
    assert data["allowed_context_findings"]


def test_same_phrase_is_allowed_as_forbidden_pattern_definition(tmp_path: Path):
    repo = _make_min_repo(tmp_path, "Forbidden pattern definition: production ready.\n")
    out = tmp_path / "report.json"
    assert _run(out, repo).returncode == 0
    data = _json(out)
    assert data["hard_violations"] == []
    assert data["allowed_context_findings"] or data["pattern_definition_findings"]


def test_same_phrase_is_allowed_as_future_evidence(tmp_path: Path):
    repo = _make_min_repo(tmp_path, "Future evidence: production ready requires external proof.\n")
    out = tmp_path / "report.json"
    assert _run(out, repo).returncode == 0
    data = _json(out)
    assert data["hard_violations"] == []
    assert data["external_receipt_required_findings"]


def test_same_phrase_is_allowed_as_external_receipt_required(tmp_path: Path):
    repo = _make_min_repo(tmp_path, "External receipt required before any production ready wording.\n")
    out = tmp_path / "report.json"
    assert _run(out, repo).returncode == 0
    data = _json(out)
    assert data["hard_violations"] == []
    assert data["external_receipt_required_findings"]


def test_forbidden_registry_patterns_are_pattern_definition_context(tmp_path: Path):
    out = tmp_path / "report.json"
    assert _run(out).returncode == 0
    data = _json(out)
    assert any(f["file_path"] == "registries/v7_1_1_forbidden_claim_registry.json" for f in data["pattern_definition_findings"])


def test_test_fixture_phrases_are_test_fixture_context(tmp_path: Path):
    out = tmp_path / "report.json"
    assert _run(out).returncode == 0
    data = _json(out)
    assert any(f["file_path"].startswith("tests/") for f in data["test_fixture_findings"])


def test_ignored_path_families_are_excluded_from_scan_scope(tmp_path: Path):
    repo = _make_min_repo(tmp_path, "Non-claim: clean file.\n")
    ignored = repo / ".odin_runtime/receipt.md"
    ignored.parent.mkdir(parents=True)
    ignored.write_text("production ready\n", encoding="utf-8")
    out = tmp_path / "report.json"
    assert _run(out, repo).returncode == 0
    data = _json(out)
    assert all(".odin_runtime" not in path for path in data["scan_scope"])


def test_generated_report_does_not_use_ignored_generated_paths_as_evidence(tmp_path: Path):
    out = tmp_path / "report.json"
    assert _run(out).returncode == 0
    data = _json(out)
    evidence_paths = [f.get("file_path", "") for key, value in data.items() if isinstance(value, list) for f in value if isinstance(f, dict)]
    assert not any(token in path for path in evidence_paths for token in IGNORED_SUBSTRINGS)


def test_boundary_report_itself_includes_non_claims():
    data = _json(REPORT)
    assert REQUIRED_NON_CLAIMS <= set(data["non_claims"])


def test_pr25_coverage_gap_report_remains_generatable(tmp_path: Path):
    out = tmp_path / "pr25_report.json"
    result = subprocess.run(
        [sys.executable, str(PR25_TOOL), "--repo-root", str(ROOT), "--out", str(out), "--generated-at-utc", "2026-01-01T00:00:00Z"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    data = _json(out)
    assert data["report_id"] == "odin.v7_1_1_operational_coverage_gap_report"


def test_tool_writes_only_to_requested_out_path(tmp_path: Path):
    repo = _make_min_repo(tmp_path, "Non-claim: clean file.\n")
    before = {p.relative_to(repo).as_posix() for p in repo.rglob("*") if p.is_file()}
    out = tmp_path / "custom/report.json"
    assert _run(out, repo).returncode == 0
    after = {p.relative_to(repo).as_posix() for p in repo.rglob("*") if p.is_file()}
    assert before == after
    assert out.exists()


def test_generated_report_does_not_leak_absolute_local_paths(tmp_path: Path):
    out = tmp_path / "report.json"
    assert _run(out).returncode == 0
    text = out.read_text(encoding="utf-8")
    assert str(ROOT) not in text
    assert "/workspace/" not in text


def test_schema_declares_required_report_contract():
    schema = _json(SCHEMA)
    assert schema["properties"]["report_id"]["const"] == "odin.v7_1_1_canon_boundary_integrity_report"
    assert "hard_violations" in schema["required"]
    assert "recommendations" in schema["required"]


def test_file_manifest_excludes_ignored_generated_artifacts():
    data = _json(ROOT / "FILE_MANIFEST.json")
    paths = [entry["path"].replace("\\", "/") for entry in data.get("files", [])]
    assert not any(token in path for path in paths for token in IGNORED_SUBSTRINGS)
