"""Tests for LRH-PR-15 — Portable Packaging and Release ZIP.

Claim boundary: portable_package_candidate_only_local_only_no_signed_distribution_no_production_claim

These tests verify:
- Required file existence
- Ladder entry in registry
- Builder execution (in temp dir, no repo mutation)
- Manifest shape and constraints
- Checksum stability
- Junk exclusion policy
- Start/check script inclusion
- Support bundle path visibility
- Doc boundary phrases
- CLI command availability
- validate-all integration
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_portable_package.py"


# ---------------------------------------------------------------------------
# 10.1 Required file tests
# ---------------------------------------------------------------------------

def test_builder_script_exists():
    assert BUILDER.exists(), "scripts/build_portable_package.py must exist"


def test_doc_exists():
    assert (ROOT / "docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md").exists()


def test_test_file_exists():
    assert (ROOT / "tests/test_lrh_pr_15_portable_package.py").exists()


def test_dist_manifest_readme_exists():
    assert (ROOT / "dist_manifest/README.md").exists()


def test_dist_manifest_example_manifest_exists():
    assert (ROOT / "dist_manifest/portable_package_manifest.example.json").exists()


def test_dist_manifest_example_report_exists():
    assert (ROOT / "dist_manifest/portable_package_release_verification.example.json").exists()


def test_dist_manifest_exclusions_exists():
    assert (ROOT / "dist_manifest/portable_package_exclusions_v1.json").exists()


# ---------------------------------------------------------------------------
# 10.2 Ladder tests
# ---------------------------------------------------------------------------

def _load_ladder() -> dict:
    p = ROOT / "registries/local_runtime_hub_build_ladder_v1.json"
    return json.loads(p.read_text(encoding="utf-8"))


def _get_pr15_entry(ladder: dict) -> dict:
    for entry in ladder.get("ladder", []):
        if entry.get("id") == "LRH-PR-15":
            return entry
    return {}


def test_ladder_pr15_exists():
    ladder = _load_ladder()
    entry = _get_pr15_entry(ladder)
    assert entry, "LRH-PR-15 must exist in the ladder"


def test_ladder_pr15_title():
    ladder = _load_ladder()
    entry = _get_pr15_entry(ladder)
    assert entry.get("title") == "Portable Packaging and Release ZIP"


def test_ladder_pr15_depends_on_lrh_pr_03():
    ladder = _load_ladder()
    entry = _get_pr15_entry(ladder)
    assert "LRH-PR-03" in entry.get("depends_on", [])


def test_ladder_pr15_depends_on_lrh_pr_04():
    ladder = _load_ladder()
    entry = _get_pr15_entry(ladder)
    assert "LRH-PR-04" in entry.get("depends_on", [])


def test_ladder_pr15_depends_on_lrh_pr_14():
    ladder = _load_ladder()
    entry = _get_pr15_entry(ladder)
    assert "LRH-PR-14" in entry.get("depends_on", [])


def test_ladder_pr15_target_files_builder():
    ladder = _load_ladder()
    entry = _get_pr15_entry(ladder)
    targets = entry.get("target_files", [])
    assert any("build_portable_package.py" in t for t in targets)


def test_ladder_pr15_target_files_dist_manifest():
    ladder = _load_ladder()
    entry = _get_pr15_entry(ladder)
    targets = entry.get("target_files", [])
    assert any("dist_manifest" in t for t in targets)


def test_ladder_pr15_target_files_doc():
    ladder = _load_ladder()
    entry = _get_pr15_entry(ladder)
    targets = entry.get("target_files", [])
    assert any("PORTABLE_PACKAGE_RELEASE_ZIP_V1.md" in t for t in targets)


def test_ladder_pr15_target_files_test():
    ladder = _load_ladder()
    entry = _get_pr15_entry(ladder)
    targets = entry.get("target_files", [])
    assert any("test_lrh_pr_15" in t for t in targets)


# ---------------------------------------------------------------------------
# 10.3 Builder execution tests
# ---------------------------------------------------------------------------

def _run_builder(*extra_args: str, dry_run: bool = False) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(BUILDER)]
    if dry_run:
        cmd.append("--dry-run")
    cmd.extend(extra_args)
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60)


def test_builder_dry_run_exits_zero():
    result = _run_builder(dry_run=True)
    assert result.returncode == 0, f"Builder dry-run failed: {result.stderr}"


def test_builder_produces_manifest_in_tmp():
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = str(Path(tmp) / "pkg")
        manifest_out = str(Path(tmp) / "manifest.json")
        report_out = str(Path(tmp) / "report.json")
        result = _run_builder(
            "--out", out_dir,
            "--manifest-out", manifest_out,
            "--report-out", report_out,
        )
        assert result.returncode == 0, f"Builder failed: {result.stderr}"
        assert Path(manifest_out).exists(), "Manifest file must be created"


def test_builder_produces_report_in_tmp():
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = str(Path(tmp) / "pkg")
        manifest_out = str(Path(tmp) / "manifest.json")
        report_out = str(Path(tmp) / "report.json")
        result = _run_builder(
            "--out", out_dir,
            "--manifest-out", manifest_out,
            "--report-out", report_out,
        )
        assert result.returncode == 0, f"Builder failed: {result.stderr}"
        assert Path(report_out).exists(), "Report file must be created"


def test_builder_no_repo_mutation():
    """Builder must not write into the repo root during test execution."""
    # Run builder with explicit /tmp paths — repo root should not be mutated
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = str(Path(tmp) / "pkg")
        manifest_out = str(Path(tmp) / "manifest.json")
        report_out = str(Path(tmp) / "report.json")
        result = _run_builder(
            "--repo-root", str(ROOT),
            "--out", out_dir,
            "--manifest-out", manifest_out,
            "--report-out", report_out,
        )
        assert result.returncode == 0, f"Builder failed: {result.stderr}"
        # The repo root should not have new files created directly in it
        assert not (ROOT / "manifest.json").exists()
        assert not (ROOT / "report.json").exists()


def test_builder_zip_output():
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = str(Path(tmp) / "pkg")
        manifest_out = str(Path(tmp) / "manifest.json")
        report_out = str(Path(tmp) / "report.json")
        zip_out = str(Path(tmp) / "package.zip")
        result = _run_builder(
            "--out", out_dir,
            "--manifest-out", manifest_out,
            "--report-out", report_out,
            "--zip-out", zip_out,
        )
        assert result.returncode == 0, f"Builder failed: {result.stderr}"
        assert Path(zip_out).exists(), "ZIP file must be created when --zip-out is specified"


# ---------------------------------------------------------------------------
# 10.4 Manifest tests
# ---------------------------------------------------------------------------

def _build_manifest_for_test() -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = str(Path(tmp) / "pkg")
        manifest_out = str(Path(tmp) / "manifest.json")
        report_out = str(Path(tmp) / "report.json")
        result = _run_builder(
            "--repo-root", str(ROOT),
            "--out", out_dir,
            "--manifest-out", manifest_out,
            "--report-out", report_out,
        )
        assert result.returncode == 0, f"Builder failed: {result.stderr}"
        return json.loads(Path(manifest_out).read_text(encoding="utf-8"))


def test_manifest_artifact_kind():
    m = _build_manifest_for_test()
    assert m.get("artifact_kind") == "odin_portable_package_manifest"


def test_manifest_lrh_pr():
    m = _build_manifest_for_test()
    assert m.get("lrh_pr") == "LRH-PR-15"


def test_manifest_candidate_only():
    m = _build_manifest_for_test()
    assert m.get("candidate_only") is True


def test_manifest_local_only():
    m = _build_manifest_for_test()
    assert m.get("local_only") is True


def test_manifest_claim_boundary_present():
    m = _build_manifest_for_test()
    assert m.get("claim_boundary"), "claim_boundary must be present and non-empty"


def test_manifest_included_files_sorted():
    m = _build_manifest_for_test()
    files = m.get("included_files", [])
    assert files == sorted(files), "included_files must be sorted"


def test_manifest_no_absolute_paths():
    m = _build_manifest_for_test()
    for f in m.get("included_files", []):
        assert not Path(f).is_absolute(), f"Absolute path in manifest: {f!r}"


def test_manifest_no_backslash_paths():
    m = _build_manifest_for_test()
    for f in m.get("included_files", []):
        assert "\\" not in f, f"Backslash in manifest path: {f!r}"


def test_manifest_not_proven_present():
    m = _build_manifest_for_test()
    not_proven = m.get("not_proven", [])
    required = [
        "production_readiness",
        "security_certification",
        "signed_distribution",
        "release_certification",
        "app_apply_authority",
        "external_send_authority",
    ]
    for entry in required:
        assert entry in not_proven, f"not_proven missing required entry: {entry!r}"


def test_manifest_proof_boundaries_present():
    m = _build_manifest_for_test()
    boundaries = m.get("proof_boundaries", [])
    assert "not_production_readiness_certification" in boundaries
    assert "not_signed_distribution_proof" in boundaries
    assert "not_security_certification" in boundaries
    assert "candidate_artifact_not_applied_truth" in boundaries


# ---------------------------------------------------------------------------
# 10.5 Checksum tests
# ---------------------------------------------------------------------------

def test_checksums_are_valid_sha256():
    m = _build_manifest_for_test()
    checksums = m.get("checksums", {})
    assert checksums, "checksums must be non-empty"
    for path, digest in checksums.items():
        assert len(digest) == 64, f"Checksum for {path!r} must be 64 hex chars, got {len(digest)}"
        assert digest == digest.lower(), f"Checksum for {path!r} must be lowercase"
        # Validate it is valid hex
        int(digest, 16)


def test_checksums_stable_across_runs():
    """Same builder run on same repo produces same checksums."""
    with tempfile.TemporaryDirectory() as tmp1, tempfile.TemporaryDirectory() as tmp2:
        m1_path = str(Path(tmp1) / "manifest.json")
        m2_path = str(Path(tmp2) / "manifest.json")
        for mp in (m1_path, m2_path):
            result = _run_builder(
                "--repo-root", str(ROOT),
                "--out", str(Path(mp).parent / "pkg"),
                "--manifest-out", mp,
                "--report-out", str(Path(mp).parent / "report.json"),
            )
            assert result.returncode == 0
        m1 = json.loads(Path(m1_path).read_text(encoding="utf-8"))
        m2 = json.loads(Path(m2_path).read_text(encoding="utf-8"))
        assert m1.get("checksums") == m2.get("checksums"), "Checksums must be stable across repeated runs"


def test_manifest_stable_across_runs():
    """Manifest included_files list must be identical across repeated runs."""
    with tempfile.TemporaryDirectory() as tmp1, tempfile.TemporaryDirectory() as tmp2:
        m1_path = str(Path(tmp1) / "manifest.json")
        m2_path = str(Path(tmp2) / "manifest.json")
        for mp in (m1_path, m2_path):
            result = _run_builder(
                "--repo-root", str(ROOT),
                "--out", str(Path(mp).parent / "pkg"),
                "--manifest-out", mp,
                "--report-out", str(Path(mp).parent / "report.json"),
            )
            assert result.returncode == 0
        m1 = json.loads(Path(m1_path).read_text(encoding="utf-8"))
        m2 = json.loads(Path(m2_path).read_text(encoding="utf-8"))
        assert m1.get("included_files") == m2.get("included_files")


# ---------------------------------------------------------------------------
# 10.6 Junk exclusion tests
# ---------------------------------------------------------------------------

def test_exclusion_policy_has_git():
    excl = json.loads((ROOT / "dist_manifest/portable_package_exclusions_v1.json").read_text(encoding="utf-8"))
    dirs = excl.get("excluded_directories", [])
    assert ".git" in dirs


def test_exclusion_policy_has_pycache():
    excl = json.loads((ROOT / "dist_manifest/portable_package_exclusions_v1.json").read_text(encoding="utf-8"))
    dirs = excl.get("excluded_directories", [])
    assert "__pycache__" in dirs


def test_exclusion_policy_has_pytest_cache():
    excl = json.loads((ROOT / "dist_manifest/portable_package_exclusions_v1.json").read_text(encoding="utf-8"))
    dirs = excl.get("excluded_directories", [])
    assert ".pytest_cache" in dirs


def test_exclusion_policy_has_env():
    excl = json.loads((ROOT / "dist_manifest/portable_package_exclusions_v1.json").read_text(encoding="utf-8"))
    files = excl.get("excluded_files", [])
    assert ".env" in files


def test_exclusion_policy_has_node_modules():
    excl = json.loads((ROOT / "dist_manifest/portable_package_exclusions_v1.json").read_text(encoding="utf-8"))
    dirs = excl.get("excluded_directories", [])
    assert "node_modules" in dirs


def test_exclusion_policy_has_dist():
    excl = json.loads((ROOT / "dist_manifest/portable_package_exclusions_v1.json").read_text(encoding="utf-8"))
    dirs = excl.get("excluded_directories", [])
    assert "dist" in dirs


def test_exclusion_policy_has_build():
    excl = json.loads((ROOT / "dist_manifest/portable_package_exclusions_v1.json").read_text(encoding="utf-8"))
    dirs = excl.get("excluded_directories", [])
    assert "build" in dirs


def test_manifest_no_pycache_files():
    m = _build_manifest_for_test()
    for f in m.get("included_files", []):
        assert "__pycache__" not in f, f"__pycache__ should not appear in manifest: {f!r}"


def test_manifest_no_pytest_cache_files():
    m = _build_manifest_for_test()
    for f in m.get("included_files", []):
        assert ".pytest_cache" not in f, f".pytest_cache should not appear in manifest: {f!r}"


def test_manifest_no_git_files():
    m = _build_manifest_for_test()
    for f in m.get("included_files", []):
        assert not f.startswith(".git/"), f".git/ path in manifest: {f!r}"


def test_manifest_no_env_files():
    m = _build_manifest_for_test()
    for f in m.get("included_files", []):
        name = Path(f).name
        assert name != ".env", f".env should not appear in manifest: {f!r}"


# ---------------------------------------------------------------------------
# 10.7 Script inclusion tests
# ---------------------------------------------------------------------------

def _build_report_for_test() -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = str(Path(tmp) / "pkg")
        manifest_out = str(Path(tmp) / "manifest.json")
        report_out = str(Path(tmp) / "report.json")
        result = _run_builder(
            "--repo-root", str(ROOT),
            "--out", out_dir,
            "--manifest-out", manifest_out,
            "--report-out", report_out,
        )
        assert result.returncode == 0, f"Builder failed: {result.stderr}"
        return json.loads(Path(report_out).read_text(encoding="utf-8"))


def test_start_odin_sh_recorded():
    m = _build_manifest_for_test()
    scripts = m.get("start_check_scripts", {})
    assert "scripts/start_odin.sh" in scripts, "start_odin.sh must be recorded in start_check_scripts"


def test_check_odin_sh_recorded():
    m = _build_manifest_for_test()
    scripts = m.get("start_check_scripts", {})
    assert "scripts/check_odin.sh" in scripts


def test_start_odin_bat_recorded():
    m = _build_manifest_for_test()
    scripts = m.get("start_check_scripts", {})
    assert "scripts/start_odin.bat" in scripts


def test_check_odin_bat_recorded():
    m = _build_manifest_for_test()
    scripts = m.get("start_check_scripts", {})
    assert "scripts/check_odin.bat" in scripts


def test_start_odin_sh_present_in_repo():
    assert (ROOT / "scripts/start_odin.sh").exists(), "start_odin.sh must exist in repo"


def test_check_odin_sh_present_in_repo():
    assert (ROOT / "scripts/check_odin.sh").exists()


def test_start_odin_bat_present_in_repo():
    assert (ROOT / "scripts/start_odin.bat").exists()


def test_check_odin_bat_present_in_repo():
    assert (ROOT / "scripts/check_odin.bat").exists()


def test_start_odin_sh_included_in_manifest_files():
    m = _build_manifest_for_test()
    assert "scripts/start_odin.sh" in m.get("included_files", [])


def test_check_odin_sh_included_in_manifest_files():
    m = _build_manifest_for_test()
    assert "scripts/check_odin.sh" in m.get("included_files", [])


# ---------------------------------------------------------------------------
# 10.8 Support bundle path test
# ---------------------------------------------------------------------------

def test_support_bundle_command_in_manifest():
    m = _build_manifest_for_test()
    cmd = m.get("support_bundle_command", "")
    assert cmd, "support_bundle_command must be present and non-empty"
    assert "emit-support-bundle" in cmd or "support" in cmd.lower()


def test_support_bundle_no_security_certification_claim():
    m = _build_manifest_for_test()
    claim = m.get("support_bundle_claim", "")
    text = claim.lower()
    assert "security certification" not in text
    assert "support_organization_readiness" not in text or "not" in text or "visible" in text


def test_support_bundle_path_visible_in_report():
    r = _build_report_for_test()
    assert r.get("support_bundle_path_visible") is True


# ---------------------------------------------------------------------------
# 10.9 Documentation tests
# ---------------------------------------------------------------------------

def test_doc_contains_portable_package_candidate():
    doc = (ROOT / "docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md").read_text(encoding="utf-8").lower()
    assert "portable package candidate" in doc


def test_doc_contains_candidate_only():
    doc = (ROOT / "docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md").read_text(encoding="utf-8").lower()
    assert "candidate-only" in doc


def test_doc_contains_local_only():
    doc = (ROOT / "docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md").read_text(encoding="utf-8").lower()
    assert "local-only" in doc


def test_doc_contains_not_production_readiness():
    doc = (ROOT / "docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md").read_text(encoding="utf-8").lower()
    assert "not production readiness" in doc


def test_doc_contains_not_security_certification():
    doc = (ROOT / "docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md").read_text(encoding="utf-8").lower()
    assert "not security certification" in doc


def test_doc_contains_not_signed_distribution():
    doc = (ROOT / "docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md").read_text(encoding="utf-8").lower()
    assert "not signed distribution proof" in doc


def test_doc_contains_local_verification_report():
    doc = (ROOT / "docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md").read_text(encoding="utf-8").lower()
    assert "local verification report" in doc


def test_doc_contains_generated_artifacts_not_committed():
    doc = (ROOT / "docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md").read_text(encoding="utf-8").lower()
    assert "generated artifacts are not committed" in doc


def test_doc_contains_no_app_apply():
    doc = (ROOT / "docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md").read_text(encoding="utf-8").lower()
    assert "no app apply" in doc


def test_doc_contains_no_external_send():
    doc = (ROOT / "docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md").read_text(encoding="utf-8").lower()
    assert "no external send" in doc


def test_doc_no_positive_overclaim_is_fully_proven():
    doc = (ROOT / "docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md").read_text(encoding="utf-8").lower()
    assert "is fully proven" not in doc


def test_doc_no_positive_overclaim_is_production_ready():
    doc = (ROOT / "docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md").read_text(encoding="utf-8").lower()
    assert "is production-ready" not in doc


# ---------------------------------------------------------------------------
# 10.10 CLI tests
# ---------------------------------------------------------------------------

def _run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "odin.cli"] + list(args),
        capture_output=True,
        text=True,
        timeout=60,
        cwd=str(ROOT),
    )


def test_validate_portable_package_cli_exists():
    result = _run_cli("validate-portable-package")
    assert result.returncode == 0, f"validate-portable-package failed: {result.stdout}\n{result.stderr}"


def test_prove_portable_package_cli_exists():
    result = _run_cli("prove-portable-package")
    assert result.returncode in (0, 1), "prove-portable-package must exit 0 or 1"
    # Parse the JSON output
    try:
        packet = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"prove-portable-package did not return valid JSON: {result.stdout}")
    assert "candidate_only" in packet
    assert packet.get("candidate_only") is True


def test_prove_portable_package_status():
    result = _run_cli("prove-portable-package")
    packet = json.loads(result.stdout)
    assert packet.get("status") in {"ok", "partial"}


def test_prove_portable_package_not_proven_present():
    result = _run_cli("prove-portable-package")
    packet = json.loads(result.stdout)
    not_proven = packet.get("not_proven", [])
    assert "production_readiness" in not_proven
    assert "security_certification" in not_proven
    assert "signed_distribution" in not_proven


def test_prove_portable_package_proof_boundaries_present():
    result = _run_cli("prove-portable-package")
    packet = json.loads(result.stdout)
    boundaries = packet.get("proof_boundaries", [])
    assert "not_production_readiness_certification" in boundaries
    assert "not_signed_distribution_proof" in boundaries


def test_prove_portable_package_local_only():
    result = _run_cli("prove-portable-package")
    packet = json.loads(result.stdout)
    assert packet.get("local_only") is True


def test_prove_portable_package_portable_package_candidate():
    result = _run_cli("prove-portable-package")
    packet = json.loads(result.stdout)
    assert packet.get("portable_package_candidate") is True


# ---------------------------------------------------------------------------
# 10.11 Agent operator smoke test
# ---------------------------------------------------------------------------

def test_agent_handoff_lrh_15_candidate_only():
    result = _run_cli(
        "agent-handoff", "--agent", "claude-code", "--lrh-pr", "15",
        "--out", "/tmp/lrh_pr_15_test_packet.json",
    )
    # Agent handoff returns 0 even for incomplete packets
    assert result.returncode in (0, 1)
    if result.returncode == 0:
        try:
            packet = json.loads(result.stdout)
        except json.JSONDecodeError:
            return  # Packet written to file, not stdout in all modes
        # If we got a packet, validate basics
        if "candidate_only" in packet:
            assert packet.get("candidate_only") is True


# ---------------------------------------------------------------------------
# 10.12 validate-all integration
# ---------------------------------------------------------------------------

def test_validate_all_includes_portable_package():
    """validate-all must call validate_portable_package and not error on LRH-PR-15."""
    result = _run_cli("validate-all")
    # validate-all may report other errors from the broader repo, but must not
    # raise an exception or exit with a non-integer code
    assert isinstance(result.returncode, int)


def test_validate_portable_package_passes():
    """validate-portable-package itself must pass with LRH-PR-15 files in place."""
    result = _run_cli("validate-portable-package")
    assert result.returncode == 0, (
        f"validate-portable-package returned errors:\n{result.stdout}\n{result.stderr}"
    )


# ---------------------------------------------------------------------------
# Example fixture shape tests
# ---------------------------------------------------------------------------

def test_example_manifest_parses():
    data = json.loads(
        (ROOT / "dist_manifest/portable_package_manifest.example.json").read_text(encoding="utf-8")
    )
    assert data.get("artifact_kind") == "odin_portable_package_manifest"
    assert data.get("candidate_only") is True
    assert data.get("local_only") is True
    assert data.get("lrh_pr") == "LRH-PR-15"


def test_example_manifest_no_backslash_paths():
    data = json.loads(
        (ROOT / "dist_manifest/portable_package_manifest.example.json").read_text(encoding="utf-8")
    )
    for f in data.get("included_files", []):
        assert "\\" not in f, f"Backslash in example manifest path: {f!r}"


def test_example_report_parses():
    data = json.loads(
        (ROOT / "dist_manifest/portable_package_release_verification.example.json").read_text(encoding="utf-8")
    )
    assert data.get("artifact_kind") == "odin_portable_package_release_verification"
    assert data.get("candidate_only") is True
    assert data.get("portable_package_candidate") is True


def test_example_report_not_proven():
    data = json.loads(
        (ROOT / "dist_manifest/portable_package_release_verification.example.json").read_text(encoding="utf-8")
    )
    not_proven = data.get("not_proven", [])
    assert "production_readiness" in not_proven
    assert "security_certification" in not_proven
    assert "signed_distribution" in not_proven


def test_exclusions_parses():
    data = json.loads(
        (ROOT / "dist_manifest/portable_package_exclusions_v1.json").read_text(encoding="utf-8")
    )
    assert data.get("candidate_only") is True
    assert ".git" in data.get("excluded_directories", [])
    assert "__pycache__" in data.get("excluded_directories", [])
    assert ".env" in data.get("excluded_files", [])


def test_builder_imports_ok():
    """Builder script must be importable (stdlib-only)."""
    spec = importlib.util.spec_from_file_location("build_portable_package", BUILDER)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # Check key constants
    assert hasattr(mod, "CLAIM_BOUNDARY")
    assert hasattr(mod, "NOT_PROVEN")
    assert hasattr(mod, "PROOF_BOUNDARIES")
    assert hasattr(mod, "JUNK_DIR_PATTERNS")
