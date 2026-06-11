from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "v7_1_1" / "build_operational_coverage_gap_report.py"
SCHEMA = ROOT / "schemas" / "v7_1_1_operational_coverage_gap_report.schema.json"
TARGET_REG = ROOT / "registries" / "v7_1_1_operational_target_registry.json"
LADDER = ROOT / "registries" / "v7_1_1_road_to_100_ladder.json"
REPORT_ID = "odin.v7_1_1_operational_coverage_gap_report"
NON_CLAIMS = {
    "no production readiness claim",
    "no release certification claim",
    "no security certification claim",
    "no target-host proof claim",
    "no live model inference proof claim",
    "no model quality proof claim",
    "no QIRC server runtime proof claim",
}

IGNORED_PATTERNS = {
    ".odin_runtime/",
    "odin_agent_shell.egg-info/",
    "__pycache__/",
    ".pytest_cache/",
    ".mypy_cache/",
    ".ruff_cache/",
    ".coverage",
    "dist/",
    "build/",
    "*.pyc",
    "*.pyo",
    "*.egg-info/",
}

IGNORED_SUBSTRINGS = [
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
]

ALLOWED_IGNORED_LOCATIONS = {
    ("ignored_evidence_paths",),
    ("senior_reviewer_notes",),
    ("senior_code_reviewer_notes",),
}


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _run_compiler(out: Path, repo_root: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT if repo_root == ROOT else repo_root / "tools" / "v7_1_1" / "build_operational_coverage_gap_report.py"),
            "--repo-root",
            str(repo_root),
            "--out",
            str(out),
            "--generated-at-utc",
            "2026-01-01T00:00:00Z",
        ],
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def test_compiler_script_exists():
    assert SCRIPT.exists()


def test_report_schema_exists_and_has_required_fields():
    assert SCHEMA.exists()
    schema = _json(SCHEMA)
    assert schema["properties"]["report_id"]["const"] == REPORT_ID
    assert "target_area_coverage" in schema["required"]
    assert "road_to_100_slice_coverage" in schema["required"]


def test_compiler_runs_successfully_and_timestamp_is_deterministic(tmp_path: Path):
    out = tmp_path / "report.json"
    result = _run_compiler(out)
    assert result.returncode == 0, result.stderr
    data = _json(out)
    assert data["generated_at_utc"] == "2026-01-01T00:00:00Z"


def test_report_top_level_shape_identity_and_claim_boundary(tmp_path: Path):
    out = tmp_path / "report.json"
    assert _run_compiler(out).returncode == 0
    data = _json(out)
    required = {
        "report_id",
        "version",
        "status",
        "generated_at_utc",
        "claim_boundary",
        "source_refs",
        "evidence_rules",
        "ignored_evidence_paths",
        "target_area_summary",
        "road_to_100_summary",
        "target_area_coverage",
        "road_to_100_slice_coverage",
        "gap_summary",
        "critical_gaps",
        "next_pr_recommendations",
        "unsupported_claims",
        "non_claims",
        "senior_reviewer_notes",
        "senior_code_reviewer_notes",
    }
    assert required <= set(data)
    assert data["report_id"] == REPORT_ID
    assert data["status"] == "local_coverage_gap_report_not_runtime_proof"
    assert "not_runtime_completion" in data["claim_boundary"]
    assert data["evidence_rules"]


def test_every_target_area_appears_once_and_slice_refs_are_valid(tmp_path: Path):
    out = tmp_path / "report.json"
    assert _run_compiler(out).returncode == 0
    data = _json(out)
    target_ids = [a["id"] for a in _json(TARGET_REG)["target_areas"]]
    valid_slice_ids = {s["id"] for s in _json(LADDER)["slices"]}
    entries = data["target_area_coverage"]
    assert [e["target_area_id"] for e in entries] == target_ids
    assert len(entries) == len(set(e["target_area_id"] for e in entries))
    for entry in entries:
        assert entry["non_claims"]
        assert set(entry["covered_by_road_to_100_slices"]) <= valid_slice_ids
        assert entry["computed_coverage_status"] != entry["declared_status"] or entry["computed_coverage_status"]


def test_every_road_to_100_slice_appears_once_and_target_refs_are_valid(tmp_path: Path):
    out = tmp_path / "report.json"
    assert _run_compiler(out).returncode == 0
    data = _json(out)
    slice_ids = [s["id"] for s in _json(LADDER)["slices"]]
    valid_target_ids = {a["id"] for a in _json(TARGET_REG)["target_areas"]}
    entries = data["road_to_100_slice_coverage"]
    assert [e["slice_id"] for e in entries] == slice_ids
    assert len(entries) == len(set(e["slice_id"] for e in entries))
    for entry in entries:
        assert entry["non_claims"]
        assert set(entry["target_area_ids"]) <= valid_target_ids


def test_future_pr_recommendations_have_target_areas_and_slices(tmp_path: Path):
    out = tmp_path / "report.json"
    assert _run_compiler(out).returncode == 0
    data = _json(out)
    assert data["next_pr_recommendations"]
    for rec in data["next_pr_recommendations"]:
        assert rec["target_area_ids"], rec
        assert rec["slice_ids"], rec
        assert rec["claim_boundary"] == "recommendation_not_implementation_proof"


def test_unsupported_claims_and_required_non_claims_present(tmp_path: Path):
    out = tmp_path / "report.json"
    assert _run_compiler(out).returncode == 0
    data = _json(out)
    assert isinstance(data["unsupported_claims"], list)
    assert NON_CLAIMS <= set(data["non_claims"])


def test_report_does_not_contain_forbidden_positive_claims_outside_context(tmp_path: Path):
    out = tmp_path / "report.json"
    assert _run_compiler(out).returncode == 0
    data = _json(out)
    text = json.dumps(data).lower()
    forbidden = [
        " is production-ready",
        " is release-ready",
        " is security-certified",
        " is target-host proven",
        " is live model proven",
        " is model quality proven",
        " qirc server implemented",
        " measured small-model improvement is proven",
    ]
    for phrase in forbidden:
        assert phrase not in text


def test_ignored_evidence_paths_are_reported(tmp_path: Path):
    out = tmp_path / "report.json"
    assert _run_compiler(out).returncode == 0
    data = _json(out)
    patterns = {entry["pattern"] for entry in data["ignored_evidence_paths"]}
    assert IGNORED_PATTERNS <= patterns


def _walk_strings(value, path=()):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from _walk_strings(item, path + (str(key),))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _walk_strings(item, path + (str(index),))
    elif isinstance(value, str):
        yield path, value.replace("\\", "/")


def _allowed_ignored_path_location(path: tuple[str, ...]) -> bool:
    return bool(path and (path[:1] in ALLOWED_IGNORED_LOCATIONS))


def test_ignored_paths_are_recursively_sanitized_outside_ignore_sections(tmp_path: Path):
    out = tmp_path / "report.json"
    assert _run_compiler(out).returncode == 0
    data = _json(out)
    violations = []
    for path, text in _walk_strings(data):
        if _allowed_ignored_path_location(path):
            continue
        for token in IGNORED_SUBSTRINGS:
            if token in text:
                violations.append((path, token, text[:160]))
    assert violations == []


def test_file_manifest_excludes_local_runtime_cache_and_build_artifacts():
    data = _json(ROOT / "FILE_MANIFEST.json")
    assert "ignored_generated_artifact_exception" not in data
    paths = [entry["path"].replace("\\", "/") for entry in data.get("files", [])]
    violations = []
    for path in paths:
        for token in IGNORED_SUBSTRINGS:
            if token in path:
                violations.append((path, token))
    assert violations == []


def test_file_manifest_preserves_pr_25_artifacts():
    data = _json(ROOT / "FILE_MANIFEST.json")
    paths = {entry["path"] for entry in data.get("files", [])}
    required = {
        "tools/v7_1_1/build_operational_coverage_gap_report.py",
        "schemas/v7_1_1_operational_coverage_gap_report.schema.json",
        "reports/v7_1_1_operational_coverage_gap_report.json",
        "docs/codex/reports/PR_25_V7_1_1_OPERATIONAL_COVERAGE_GAP_COMPILER_RETURN_REPORT.md",
        "tests/test_v7_1_1_operational_coverage_gap_compiler.py",
    }
    assert required <= paths


def test_file_manifest_count_matches_entries():
    data = _json(ROOT / "FILE_MANIFEST.json")
    assert data["file_count_excluding_manifest"] == len(data.get("files", []))


def test_file_manifest_presence_alone_does_not_create_implemented_code_candidate(tmp_path: Path):
    out = tmp_path / "report.json"
    assert _run_compiler(out).returncode == 0
    data = _json(out)
    for section in ["target_area_coverage", "road_to_100_slice_coverage"]:
        for record in data[section]:
            for ref in record["evidence_refs"]:
                if ref["path"] == "FILE_MANIFEST.json":
                    assert ref["evidence_class"] == "registry_only"
                    assert record["computed_coverage_status"] != "implemented_code_candidate"


def test_compiler_fails_closed_when_required_registry_missing(tmp_path: Path):
    repo_copy = tmp_path / "repo"
    ignore = shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__")
    shutil.copytree(ROOT, repo_copy, ignore=ignore)
    missing = repo_copy / "registries" / "v7_1_1_operational_target_registry.json"
    missing.unlink()
    out = repo_copy / "reports" / "should_not_exist.json"
    result = _run_compiler(out, repo_root=repo_copy)
    assert result.returncode != 0
    assert "required input missing" in result.stderr
    assert not out.exists()


def test_compiler_does_not_write_outside_requested_out_path(tmp_path: Path):
    before = {p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*")}
    out = tmp_path / "nested" / "report.json"
    result = _run_compiler(out)
    assert result.returncode == 0, result.stderr
    after = {p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*")}
    assert after - before == {"nested", "nested/report.json"}
    payload = out.read_text(encoding="utf-8")
    assert str(ROOT) not in payload
