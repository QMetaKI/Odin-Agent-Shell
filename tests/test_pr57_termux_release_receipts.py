import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_lrh_pr_09_uses_portable_tmp_path_and_keeps_intent():
    legacy = text("tests/test_lrh_pr_09_trace_viewer.py")
    assert "/tmp/lrh_pr_09_packet.json" not in legacy
    assert "tmp_path" in legacy
    for token in ["agent-handoff", "agent-guard", "agent-check", "LRH-PR-09", "candidate_only", "app_owned_apply"]:
        assert token in legacy


def test_release_receipt_doc_exists_and_does_not_overclaim():
    doc = text("docs/release/V1_0_0_EXTERNAL_RELEASE_RECEIPTS.md")
    assert "v1.0.0" in doc
    assert "GitHub Release" in doc
    assert "PyPI publication | not claimed" in doc
    assert "Release assets | not claimed" in doc
    low = doc.lower()
    for phrase in ["production_ready", "security certified", "model benchmark verified", "published to pypi", "release assets uploaded"]:
        assert phrase not in low


def test_pr57_validator_returns_ok(tmp_path):
    out = tmp_path / "pr57.json"
    result = subprocess.run(
        [sys.executable, "tools/rebaseline/check_pr57_termux_release_receipts.py", "--repo-root", ".", "--out", str(out), "--generated-at-utc", "2026-01-01T00:00:00Z"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    report = json.loads(out.read_text(encoding="utf-8"))
    assert report["status"] == "ok"


def test_cli_validate_pr57_returns_ok():
    result = subprocess.run([sys.executable, "-m", "odin.cli", "validate-pr57-termux-release-receipts"], cwd=ROOT, text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr + result.stdout
    assert "OK" in result.stdout


def test_validate_all_includes_pr57_validator():
    cli = text("odin/cli.py")
    assert "validate_pr57_termux_release_receipts" in cli
    assert "errors.extend(validate_pr57_termux_release_receipts())" in cli


def test_system_map_and_manifest_contain_pr57_entries():
    assert "pr57_termux_release_receipts" in text("SYSTEM_MAP.json")
    manifest = text("FILE_MANIFEST.json")
    for path in [
        "tests/test_lrh_pr_09_trace_viewer.py",
        "docs/release/V1_0_0_EXTERNAL_RELEASE_RECEIPTS.md",
        "reports/pr57_termux_and_release_receipts_report.json",
        "tools/rebaseline/check_pr57_termux_release_receipts.py",
        "tests/test_pr57_termux_release_receipts.py",
    ]:
        assert path in manifest
