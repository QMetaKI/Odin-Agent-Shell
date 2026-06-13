from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIM_BOUNDARY = "pre_release_super_audit_reports_repo_reality_not_release_certification"


def load_json(rel: str):
    path = ROOT / rel
    assert path.exists(), f"missing {rel}"
    return json.loads(path.read_text(encoding="utf-8"))


def test_01_audit_registry_exists_and_parses():
    data = load_json("registries/pre_release_super_audit_registry.json")
    assert data["registry_id"] == "pre_release_super_audit_registry"


def test_02_main_audit_report_exists_and_parses():
    data = load_json("reports/pre_release_super_audit_report.json")
    assert data["audit_id"] == "pre_release_super_audit"


def test_03_pr_lineage_report_exists_and_parses():
    data = load_json("reports/pre_release_super_audit_pr_lineage.json")
    assert data["lineage"]


def test_04_runtime_path_report_exists_and_parses():
    data = load_json("reports/pre_release_super_audit_runtime_paths.json")
    assert data["results"]


def test_05_architecture_conformance_report_exists_and_parses():
    data = load_json("reports/pre_release_super_audit_architecture_conformance.json")
    assert data["matrix"]


def test_06_model_leverage_simulation_report_exists_and_parses():
    data = load_json("reports/pre_release_super_audit_model_leverage_simulation.json")
    assert data["model_leverage_mode"] == "structured_simulation"


def test_07_recommended_prs_report_exists_and_parses():
    data = load_json("reports/pre_release_super_audit_recommended_prs.json")
    assert data["recommended_next_prs"]


def test_08_executive_brief_exists():
    assert (ROOT / "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_EXECUTIVE_BRIEF.md").exists()


def test_09_full_report_exists():
    assert (ROOT / "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_FULL_REPORT.md").exists()


def test_10_cli_audit_pre_release_super_exists():
    proc = subprocess.run([sys.executable, "-m", "odin.cli", "--help"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.returncode == 0
    assert "audit-pre-release-super" in proc.stdout


def test_11_audit_script_exists():
    assert (ROOT / "tools/audit/run_pre_release_super_audit.py").exists()


def test_12_audit_script_can_run_in_lightweight_mode():
    proc = subprocess.run([sys.executable, "tools/audit/run_pre_release_super_audit.py", "--lightweight", "--check-only"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    assert proc.returncode == 0, proc.stderr
    assert "pre_release_super_audit" in proc.stdout


def test_13_reports_include_claim_boundary():
    for rel in [
        "reports/pre_release_super_audit_report.json",
        "reports/pre_release_super_audit_pr_lineage.json",
        "reports/pre_release_super_audit_runtime_paths.json",
        "reports/pre_release_super_audit_architecture_conformance.json",
        "reports/pre_release_super_audit_model_leverage_simulation.json",
        "reports/pre_release_super_audit_recommended_prs.json",
    ]:
        assert load_json(rel)["claim_boundary"] == CLAIM_BOUNDARY


def test_14_reports_include_not_proven():
    assert "not_proven" in load_json("reports/pre_release_super_audit_report.json")
    assert "not_proven" in load_json("reports/pre_release_super_audit_model_leverage_simulation.json")


def test_15_no_release_completion_overclaim():
    text = (ROOT / "reports/pre_release_super_audit_report.json").read_text(encoding="utf-8").lower()
    assert "production" + " ready" not in text


def test_16_no_security_certification_claim():
    data = load_json("reports/pre_release_super_audit_report.json")
    assert "security_certification" in data["not_proven"]


def test_17_model_leverage_separates_measured_simulated_hypothesized():
    data = load_json("reports/pre_release_super_audit_model_leverage_simulation.json")
    assert "measured" in data
    assert "simulated" in data
    assert "hypothesized" in data


def test_18_recommended_pr_decision_exists():
    data = load_json("reports/pre_release_super_audit_recommended_prs.json")
    assert data["decision"]
    assert data["release_pr_should_move_to"]


def test_19_system_map_has_pre_release_super_audit_entry():
    data = load_json("SYSTEM_MAP.json")
    assert "pre_release_super_audit" in data
    assert data["pre_release_super_audit"]["release_position"] == "before_FINAL_PR_09"


def test_20_file_manifest_includes_audit_files():
    data = load_json("FILE_MANIFEST.json")
    paths = {entry["path"] for entry in data["files"]}
    assert "tools/audit/run_pre_release_super_audit.py" in paths
    assert "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_EXECUTIVE_BRIEF.md" in paths
    assert "reports/pre_release_super_audit_report.json" in paths
