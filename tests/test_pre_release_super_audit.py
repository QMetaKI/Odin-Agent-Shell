from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIM_BOUNDARY = "pre_release_super_audit_reports_repo_reality_not_release_certification"
AUDIT_DIR = ROOT / "docs" / "codex" / "audits" / "pre_release_super_audit"
REPORTS = [
    "reports/pre_release_super_audit_report.json",
    "reports/pre_release_super_audit_pr_lineage.json",
    "reports/pre_release_super_audit_system_cohesion.json",
    "reports/pre_release_super_audit_architecture_conformance.json",
    "reports/pre_release_super_audit_runtime_paths.json",
    "reports/pre_release_super_audit_q_shabang_operationalization.json",
    "reports/pre_release_super_audit_bug6_q7_rings_boundaries.json",
    "reports/pre_release_super_audit_model_leverage_simulation.json",
    "reports/pre_release_super_audit_thor_odin_effectiveness.json",
    "reports/pre_release_super_audit_recommended_prs.json",
]
DOCS = [
    "00_EXECUTIVE_BRIEF.md",
    "01_FULL_SYSTEM_REPORT.md",
    "02_PR_LINEAGE.md",
    "03_SYSTEM_COHESION.md",
    "04_ARCHITECTURE_CONFORMANCE.md",
    "05_RUNTIME_PATHS_AND_SMOKE.md",
    "06_Q_SHABANG_OPERATIONALIZATION.md",
    "07_BUG6_Q7_RINGS_BOUNDARIES.md",
    "08_MODEL_LEVERAGE_SIMULATION.md",
    "09_THOR_ODIN_EFFECTIVENESS.md",
    "10_RELEASE_READINESS_DECISION.md",
    "11_REMEDIATION_PR_PLAN.md",
    "12_CHATGPT_REVIEW_HANDOFF.md",
    "13_SENIOR_REVIEW.md",
    "14_CODE_REVIEW.md",
]


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
    assert data["model_leverage_mode"] == "structured_simulation_not_empirical_benchmark"


def test_07_recommended_prs_report_exists_and_parses():
    data = load_json("reports/pre_release_super_audit_recommended_prs.json")
    assert data["recommended_next_prs"]


def test_08_executive_brief_exists():
    assert (AUDIT_DIR / "00_EXECUTIVE_BRIEF.md").exists()


def test_09_full_report_exists():
    assert (AUDIT_DIR / "01_FULL_SYSTEM_REPORT.md").exists()


def test_10_chatgpt_review_handoff_exists():
    assert (AUDIT_DIR / "12_CHATGPT_REVIEW_HANDOFF.md").exists()


def test_11_cli_audit_pre_release_super_exists():
    proc = subprocess.run([sys.executable, "-m", "odin.cli", "--help"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.returncode == 0
    assert "audit-pre-release-super" in proc.stdout


def test_12_cli_validate_pre_release_super_audit_exists():
    proc = subprocess.run([sys.executable, "-m", "odin.cli", "--help"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.returncode == 0
    assert "validate-pre-release-super-audit" in proc.stdout


def test_13_audit_script_exists():
    assert (ROOT / "tools/audit/run_pre_release_super_audit.py").exists()


def test_14_audit_script_lightweight_mode_runs():
    proc = subprocess.run([sys.executable, "tools/audit/run_pre_release_super_audit.py", "--repo-root", ".", "--out", "reports/pre_release_super_audit_report.json", "--lightweight", "--check-only"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    assert proc.returncode == 0, proc.stderr
    assert "pre_release_super_audit" in proc.stdout


def test_15_reports_include_candidate_only_true():
    for rel in REPORTS:
        assert load_json(rel)["candidate_only"] is True


def test_16_reports_include_claim_boundary():
    for rel in REPORTS:
        assert load_json(rel)["claim_boundary"] == CLAIM_BOUNDARY


def test_17_reports_include_not_proven():
    for rel in ["reports/pre_release_super_audit_report.json", "reports/pre_release_super_audit_model_leverage_simulation.json"]:
        assert "not_proven" in load_json(rel)


def test_18_no_release_completion_certification_claim():
    text = (ROOT / "reports/pre_release_super_audit_report.json").read_text(encoding="utf-8").lower()
    assert "production" + " ready" not in text


def test_19_no_security_certification_claim():
    data = load_json("reports/pre_release_super_audit_report.json")
    assert "security_certification" in data["not_proven"]


def test_20_model_leverage_report_separates_measured_simulated_hypothesized():
    data = load_json("reports/pre_release_super_audit_model_leverage_simulation.json")
    assert data["measured"] is False
    assert data["simulated"] is True
    assert data["hypothesized"] is True
    for row in data["scenarios"]:
        assert {"measured", "simulated", "hypothesized"}.issubset(row)


def test_21_recommended_pr_decision_exists():
    data = load_json("reports/pre_release_super_audit_recommended_prs.json")
    assert data["decision"]
    assert data["release_pr_should_move_to"]


def test_22_pr_lineage_includes_final_pr_06_07_08():
    data = load_json("reports/pre_release_super_audit_pr_lineage.json")
    titles = "\n".join(entry["title"] for entry in data["lineage"])
    assert "FINAL-PR-06" in titles
    assert "FINAL-PR-07" in titles
    assert "FINAL-PR-08" in titles


def test_23_runtime_paths_include_validate_all():
    data = load_json("reports/pre_release_super_audit_runtime_paths.json")
    commands = [row["command_or_endpoint"] for row in data["results"]]
    assert any("validate-all" in cmd for cmd in commands)


def test_24_system_map_has_pre_release_super_audit_entry():
    data = load_json("SYSTEM_MAP.json")
    assert "pre_release_super_audit" in data
    entry = data["pre_release_super_audit"]
    assert entry["release_position"] == "before_FINAL_PR_09"
    assert "validate-pre-release-super-audit" in entry["cli_commands"]


def test_25_file_manifest_includes_all_audit_files():
    data = load_json("FILE_MANIFEST.json")
    paths = {entry["path"] for entry in data["files"]}
    for name in DOCS:
        assert f"docs/codex/audits/pre_release_super_audit/{name}" in paths
    for rel in REPORTS:
        assert rel in paths
    assert "tools/audit/run_pre_release_super_audit.py" in paths
    assert "tests/test_pre_release_super_audit.py" in paths
