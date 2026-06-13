import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_DESCRIPTION = "Odin Agent Shell v7.1 repo prep full shadow runtime coverage and validation scaffold"
NEW_DESCRIPTION = "Local-first candidate-work kernel for bounded AI coordination, receipt discipline, and app-owned apply workflows"


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_pyproject_version_and_description():
    pyproject = text("pyproject.toml")
    assert 'version = "1.0.0"' in pyproject
    assert OLD_DESCRIPTION not in pyproject
    assert NEW_DESCRIPTION in pyproject


def test_readme_release_truth_and_boundaries():
    readme = text("README.md")
    low = readme.lower()
    assert "v1.0.0 prepared_not_released" in readme
    assert "tag exists" not in low
    assert "github release exists" not in low
    assert "published to pypi" not in low
    assert "available on pypi" not in low
    assert "release assets uploaded" not in low
    assert "DONATIONS.md" in readme
    assert "## Danke / Thank You" in readme
    assert "model output is projection, not truth" in low


def test_donations_and_release_docs_exist():
    for path in [
        "DONATIONS.md",
        "docs/release/V1_0_0_EXTERNAL_RELEASE_PREP.md",
        "docs/release/V1_0_0_MANUAL_RELEASE_CHECKLIST.md",
        "docs/release/V1_0_0_RELEASE_NOTES_DRAFT.md",
    ]:
        assert (ROOT / path).exists()


def test_manual_release_checklist_external_actions_are_manual_and_unclaimed():
    checklist = text("docs/release/V1_0_0_MANUAL_RELEASE_CHECKLIST.md")
    for token in ["tag", "GitHub Release", "PyPI", "assets"]:
        assert token in checklist
    assert "manual_only: true" in checklist
    assert "claimed_by_pr56: false" in checklist


def test_validator_returns_ok(tmp_path):
    out = tmp_path / "report.json"
    result = subprocess.run(
        [sys.executable, "tools/rebaseline/check_pr56_v1_0_0_version_sync.py", "--repo-root", ".", "--out", str(out), "--generated-at-utc", "2026-01-01T00:00:00Z"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    report = json.loads(out.read_text(encoding="utf-8"))
    assert report["status"] == "ok"
    assert report["package_version"] == "1.0.0"
    assert report["release_posture"] == "v1.0.0 prepared_not_released"
    assert report["external_release_claimed"] is False


def test_cli_validate_and_demo_report_return_ok_json():
    validate = subprocess.run([sys.executable, "-m", "odin.cli", "validate-pr56-v1-version-sync"], cwd=ROOT, text=True, capture_output=True, check=False)
    assert validate.returncode == 0, validate.stderr + validate.stdout
    demo = subprocess.run([sys.executable, "-m", "odin.cli", "build-pr56-v1-version-sync-report", "--demo"], cwd=ROOT, text=True, capture_output=True, check=False)
    assert demo.returncode == 0, demo.stderr + demo.stdout
    parsed = json.loads(demo.stdout)
    assert parsed["status"] == "ok"


def test_validate_all_includes_pr56_validator():
    cli = text("odin/cli.py")
    assert "validate_pr56_v1_version_sync" in cli
    assert "errors.extend(validate_pr56_v1_version_sync())" in cli


def test_system_map_and_file_manifest_contain_pr56_entries():
    system_map = text("SYSTEM_MAP.json")
    file_manifest = text("FILE_MANIFEST.json")
    assert "pr56_v1_0_0_version_sync" in system_map
    for path in [
        "pyproject.toml",
        "README.md",
        "docs/release/V1_0_0_EXTERNAL_RELEASE_PREP.md",
        "docs/release/V1_0_0_MANUAL_RELEASE_CHECKLIST.md",
        "docs/release/V1_0_0_RELEASE_NOTES_DRAFT.md",
        "tools/rebaseline/check_pr56_v1_0_0_version_sync.py",
        "reports/pr56_v1_0_0_version_sync_report.json",
        "tests/test_pr56_v1_0_0_version_sync.py",
    ]:
        assert path in file_manifest
