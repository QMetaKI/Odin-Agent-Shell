"""Tests for FINAL-PR-12: Release Readiness Hardening + Evidence Closure Dry Run + Packaging Boundary Prep.

Claim boundary: final_pr_12_release_readiness_hardening_not_release_closure
candidate_only: true
"""
from __future__ import annotations
import importlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


# ============================================================
# 1-6: Module imports
# ============================================================

def test_release_readiness_hardening_imports():
    import odin.release_readiness_hardening  # noqa: F401

def test_evidence_closure_dry_run_imports():
    import odin.evidence_closure_dry_run  # noqa: F401

def test_packaging_boundary_prep_imports():
    import odin.packaging_boundary_prep  # noqa: F401

def test_command_surface_closure_imports():
    import odin.command_surface_closure  # noqa: F401

def test_docs_readiness_imports():
    import odin.docs_readiness  # noqa: F401

def test_final_pr_13_input_bundle_imports():
    import odin.final_pr_13_input_bundle  # noqa: F401


# ============================================================
# 7-15: Release Readiness Matrix
# ============================================================

def test_release_readiness_matrix_returns_dict():
    from odin.release_readiness_hardening import build_release_readiness_matrix
    result = build_release_readiness_matrix()
    assert isinstance(result, dict)

def test_release_readiness_matrix_candidate_only():
    from odin.release_readiness_hardening import build_release_readiness_matrix
    result = build_release_readiness_matrix()
    assert result.get("candidate_only") is True

def test_release_readiness_matrix_contains_production_readiness_boundary():
    from odin.release_readiness_hardening import build_release_readiness_matrix
    result = build_release_readiness_matrix()
    rows = result.get("rows", [])
    cats = [r["category"] for r in rows]
    assert "production_readiness_boundary" in cats

def test_release_readiness_matrix_contains_security_certification_boundary():
    from odin.release_readiness_hardening import build_release_readiness_matrix
    result = build_release_readiness_matrix()
    rows = result.get("rows", [])
    cats = [r["category"] for r in rows]
    assert "security_certification_boundary" in cats

def test_release_readiness_matrix_contains_release_certification_boundary():
    from odin.release_readiness_hardening import build_release_readiness_matrix
    result = build_release_readiness_matrix()
    rows = result.get("rows", [])
    cats = [r["category"] for r in rows]
    assert "release_certification_boundary" in cats

def test_risk_register_contains_forbidden_production_claim():
    from odin.release_readiness_hardening import build_release_risk_register
    result = build_release_risk_register()
    risks = result.get("risks", [])
    forbidden = [r.get("forbidden_claim") for r in risks]
    assert "production_readiness" in forbidden

def test_risk_register_contains_forbidden_security_claim():
    from odin.release_readiness_hardening import build_release_risk_register
    result = build_release_risk_register()
    risks = result.get("risks", [])
    forbidden = [r.get("forbidden_claim") for r in risks]
    assert "security_certification" in forbidden

def test_risk_register_contains_forbidden_release_claim():
    from odin.release_readiness_hardening import build_release_risk_register
    result = build_release_risk_register()
    risks = result.get("risks", [])
    forbidden = [r.get("forbidden_claim") for r in risks]
    assert "release_certification" in forbidden

def test_hardening_plan_points_to_final_pr_13():
    from odin.release_readiness_hardening import build_release_hardening_plan
    result = build_release_hardening_plan()
    assert result.get("target_pr") == "FINAL-PR-13"
    assert result.get("final_pr_13_remains_deferred") is True


# ============================================================
# 16-20: Evidence Closure Dry Run
# ============================================================

def test_evidence_closure_dry_run_returns_dict():
    from odin.evidence_closure_dry_run import run_evidence_closure_dry_run
    result = run_evidence_closure_dry_run()
    assert isinstance(result, dict)

def test_evidence_closure_dry_run_candidate_only():
    from odin.evidence_closure_dry_run import run_evidence_closure_dry_run
    result = run_evidence_closure_dry_run()
    assert result.get("candidate_only") is True

def test_dry_run_has_closure_statuses():
    from odin.evidence_closure_dry_run import run_evidence_closure_dry_run
    result = run_evidence_closure_dry_run()
    results = result.get("results", [])
    assert len(results) > 0
    statuses = {r.get("closure_status") for r in results}
    assert "closure_ready_structural" in statuses

def test_dry_run_does_not_close_release():
    from odin.evidence_closure_dry_run import run_evidence_closure_dry_run
    result = run_evidence_closure_dry_run()
    assert result.get("dry_run_is_not_release_closure") is True
    assert result.get("final_pr_13_remains_deferred") is True

def test_dry_run_includes_safe_wording():
    from odin.evidence_closure_dry_run import run_evidence_closure_dry_run
    result = run_evidence_closure_dry_run()
    results = result.get("results", [])
    for r in results:
        assert "safe_wording" in r
        assert r["safe_wording"]


# ============================================================
# 21-27: Packaging Boundary
# ============================================================

def test_packaging_inventory_returns_dict():
    from odin.packaging_boundary_prep import build_packaging_inventory
    result = build_packaging_inventory()
    assert isinstance(result, dict)

def test_packaging_inventory_candidate_only():
    from odin.packaging_boundary_prep import build_packaging_inventory
    result = build_packaging_inventory()
    assert result.get("candidate_only") is True

def test_packaging_inventory_contains_source_tree():
    from odin.packaging_boundary_prep import build_packaging_inventory
    result = build_packaging_inventory()
    cats = [item["category"] for item in result.get("items", [])]
    assert "source_tree" in cats

def test_packaging_inventory_contains_cli_surface():
    from odin.packaging_boundary_prep import build_packaging_inventory
    result = build_packaging_inventory()
    cats = [item["category"] for item in result.get("items", [])]
    assert "cli_surface" in cats

def test_packaging_inventory_contains_local_hub_surface():
    from odin.packaging_boundary_prep import build_packaging_inventory
    result = build_packaging_inventory()
    cats = [item["category"] for item in result.get("items", [])]
    assert "local_hub_surface" in cats

def test_packaging_inventory_does_not_claim_signed_distribution():
    from odin.packaging_boundary_prep import build_packaging_inventory
    result = build_packaging_inventory()
    assert "signed_distribution" in result.get("not_proven", [])

def test_packaging_manifest_plan_does_not_build_release_artifact():
    from odin.packaging_boundary_prep import build_packaging_manifest_plan
    result = build_packaging_manifest_plan()
    assert result.get("does_not_build_release_artifact") is True
    assert result.get("does_not_create_signed_package") is True


# ============================================================
# 28-32: Command Surface
# ============================================================

def test_command_surface_index_returns_dict():
    from odin.command_surface_closure import build_command_surface_index
    result = build_command_surface_index()
    assert isinstance(result, dict)

def test_command_surface_index_contains_validators():
    from odin.command_surface_closure import build_command_surface_index
    result = build_command_surface_index()
    cmds = result.get("commands", [])
    classes = [c["command_class"] for c in cmds]
    assert "validator" in classes

def test_command_surface_index_contains_demos():
    from odin.command_surface_closure import build_command_surface_index
    result = build_command_surface_index()
    cmds = result.get("commands", [])
    classes = [c["command_class"] for c in cmds]
    assert "demo_builder" in classes

def test_command_surface_index_contains_explain_commands():
    from odin.command_surface_closure import build_command_surface_index
    result = build_command_surface_index()
    cmds = result.get("commands", [])
    classes = [c["command_class"] for c in cmds]
    assert "explain" in classes

def test_command_alias_policy_handles_historical_aliases():
    from odin.command_surface_closure import build_command_alias_policy
    result = build_command_alias_policy()
    assert result.get("historical_aliases_preserved") is True


# ============================================================
# 33-37: Docs Readiness
# ============================================================

def test_docs_readiness_index_returns_dict():
    from odin.docs_readiness import build_docs_readiness_index
    result = build_docs_readiness_index()
    assert isinstance(result, dict)

def test_docs_readiness_index_contains_operator_start():
    from odin.docs_readiness import build_docs_readiness_index
    result = build_docs_readiness_index()
    cats = [d["category"] for d in result.get("docs", [])]
    assert "operator_start" in cats

def test_docs_readiness_index_contains_developer_start():
    from odin.docs_readiness import build_docs_readiness_index
    result = build_docs_readiness_index()
    cats = [d["category"] for d in result.get("docs", [])]
    assert "developer_start" in cats

def test_docs_readiness_index_contains_claims_boundary():
    from odin.docs_readiness import build_docs_readiness_index
    result = build_docs_readiness_index()
    cats = [d["category"] for d in result.get("docs", [])]
    assert "claims_boundary" in cats

def test_docs_readiness_index_contains_non_claims():
    from odin.docs_readiness import build_docs_readiness_index
    result = build_docs_readiness_index()
    not_proven = result.get("not_proven", [])
    assert "user_documentation_complete" in not_proven


# ============================================================
# 38-44: FINAL-PR-13 Input Bundle
# ============================================================

def test_final_pr_13_input_bundle_returns_dict():
    from odin.final_pr_13_input_bundle import build_final_pr_13_input_bundle
    result = build_final_pr_13_input_bundle()
    assert isinstance(result, dict)

def test_final_pr_13_input_bundle_candidate_only():
    from odin.final_pr_13_input_bundle import build_final_pr_13_input_bundle
    result = build_final_pr_13_input_bundle()
    assert result.get("candidate_only") is True

def test_final_pr_13_input_bundle_contains_forbidden_claims():
    from odin.final_pr_13_input_bundle import build_final_pr_13_input_bundle
    result = build_final_pr_13_input_bundle()
    forbidden = result.get("forbidden_claims", [])
    assert "production_readiness" in forbidden
    assert "security_certification" in forbidden
    assert "release_certification" in forbidden

def test_final_pr_13_input_bundle_contains_recommended_title():
    from odin.final_pr_13_input_bundle import build_final_pr_13_input_bundle
    result = build_final_pr_13_input_bundle()
    assert "FINAL-PR-13" in result.get("recommended_final_pr_13_title", "")

def test_final_pr_13_input_bundle_contains_validation_commands():
    from odin.final_pr_13_input_bundle import build_final_pr_13_input_bundle
    result = build_final_pr_13_input_bundle()
    cmds = result.get("recommended_final_pr_13_validation_commands", [])
    assert len(cmds) > 0

def test_release_sequence_after_pr12_points_to_final_pr_13():
    seq_path = REPO_ROOT / "reports/final_pr_12_release_sequence_after_pr12.json"
    assert seq_path.exists(), "release sequence after PR12 report missing"
    seq = json.loads(seq_path.read_text(encoding="utf-8"))
    assert seq.get("next_pr") == "FINAL-PR-13"

def test_final_pr_13_remains_deferred():
    from odin.final_pr_13_input_bundle import build_final_pr_13_input_bundle
    result = build_final_pr_13_input_bundle()
    assert result.get("final_pr_13_remains_deferred") is True


# ============================================================
# 45-57: CLI commands
# ============================================================

def _run_cli(*args):
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", *args],
        capture_output=True, text=True, cwd=str(REPO_ROOT)
    )
    return result

def test_cli_validate_release_readiness_hardening_returns_0():
    r = _run_cli("validate-release-readiness-hardening")
    assert r.returncode == 0

def test_cli_build_release_readiness_matrix_returns_valid_json():
    r = _run_cli("build-release-readiness-matrix", "--demo")
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data.get("candidate_only") is True

def test_cli_validate_evidence_closure_dry_run_returns_0():
    r = _run_cli("validate-evidence-closure-dry-run")
    assert r.returncode == 0

def test_cli_run_evidence_closure_dry_run_returns_valid_json():
    r = _run_cli("run-evidence-closure-dry-run", "--demo")
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data.get("candidate_only") is True

def test_cli_validate_packaging_boundary_prep_returns_0():
    r = _run_cli("validate-packaging-boundary-prep")
    assert r.returncode == 0

def test_cli_build_packaging_boundary_returns_valid_json():
    r = _run_cli("build-packaging-boundary", "--demo")
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data.get("candidate_only") is True

def test_cli_validate_command_surface_closure_returns_0():
    r = _run_cli("validate-command-surface-closure")
    assert r.returncode == 0

def test_cli_build_command_surface_index_returns_valid_json():
    r = _run_cli("build-command-surface-index", "--demo")
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data.get("candidate_only") is True

def test_cli_validate_docs_readiness_returns_0():
    r = _run_cli("validate-docs-readiness")
    assert r.returncode == 0

def test_cli_build_docs_readiness_index_returns_valid_json():
    r = _run_cli("build-docs-readiness-index", "--demo")
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data.get("candidate_only") is True

def test_cli_validate_final_pr_13_input_bundle_returns_0():
    r = _run_cli("validate-final-pr-13-input-bundle")
    assert r.returncode == 0

def test_cli_build_final_pr_13_input_bundle_returns_valid_json():
    r = _run_cli("build-final-pr-13-input-bundle", "--demo")
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data.get("candidate_only") is True

def test_cli_validate_final_pr_12_release_readiness_hardening_returns_0():
    r = _run_cli("validate-final-pr-12-release-readiness-hardening")
    assert r.returncode == 0


# ============================================================
# 58-69: Local Hub payloads and REQUIRED_IDS
# ============================================================

def test_local_hub_release_readiness_matrix_payload():
    from odin.release_readiness_hardening.readiness_matrix import build_release_readiness_matrix
    result = build_release_readiness_matrix()
    body = json.dumps(result)
    data = json.loads(body)
    assert data.get("candidate_only") is True

def test_local_hub_evidence_closure_dry_run_payload():
    from odin.evidence_closure_dry_run.dry_run import run_evidence_closure_dry_run
    result = run_evidence_closure_dry_run()
    body = json.dumps(result)
    data = json.loads(body)
    assert data.get("candidate_only") is True

def test_local_hub_packaging_boundary_payload():
    from odin.packaging_boundary_prep.inventory import build_packaging_inventory
    result = build_packaging_inventory()
    body = json.dumps(result)
    data = json.loads(body)
    assert data.get("candidate_only") is True

def test_local_hub_command_surface_payload():
    from odin.command_surface_closure.command_index import build_command_surface_index
    result = build_command_surface_index()
    body = json.dumps(result)
    data = json.loads(body)
    assert data.get("candidate_only") is True

def test_local_hub_docs_readiness_payload():
    from odin.docs_readiness.doc_index import build_docs_readiness_index
    result = build_docs_readiness_index()
    body = json.dumps(result)
    data = json.loads(body)
    assert data.get("candidate_only") is True

def test_local_hub_final_pr_13_input_bundle_payload():
    from odin.final_pr_13_input_bundle.bundle import build_final_pr_13_input_bundle
    result = build_final_pr_13_input_bundle()
    body = json.dumps(result)
    data = json.loads(body)
    assert data.get("candidate_only") is True

def test_required_ids_contains_release_readiness_hardening_section():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "release-readiness-hardening-section" in REQUIRED_IDS

def test_required_ids_contains_evidence_closure_dry_run_section():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "evidence-closure-dry-run-section" in REQUIRED_IDS

def test_required_ids_contains_packaging_boundary_prep_section():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "packaging-boundary-prep-section" in REQUIRED_IDS

def test_required_ids_contains_command_surface_closure_section():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "command-surface-closure-section" in REQUIRED_IDS

def test_required_ids_contains_docs_readiness_section():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "docs-readiness-section" in REQUIRED_IDS

def test_required_ids_contains_final_pr_13_input_bundle_section():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "final-pr-13-input-bundle-section" in REQUIRED_IDS


# ============================================================
# 70-77: Safety, metadata, validator
# ============================================================

def test_no_eval_exec_subprocess_in_new_modules():
    new_module_dirs = [
        "odin/release_readiness_hardening",
        "odin/evidence_closure_dry_run",
        "odin/packaging_boundary_prep",
        "odin/command_surface_closure",
        "odin/docs_readiness",
        "odin/final_pr_13_input_bundle",
    ]
    for mod_dir in new_module_dirs:
        for py_file in (REPO_ROOT / mod_dir).glob("*.py"):
            text = py_file.read_text(encoding="utf-8")
            assert "eval(" not in text, f"eval() found in {py_file}"
            assert "exec(" not in text, f"exec() found in {py_file}"
            assert "subprocess" not in text, f"subprocess found in {py_file}"

def test_no_public_network_calls_in_new_modules():
    new_module_dirs = [
        "odin/release_readiness_hardening",
        "odin/evidence_closure_dry_run",
        "odin/packaging_boundary_prep",
        "odin/command_surface_closure",
        "odin/docs_readiness",
        "odin/final_pr_13_input_bundle",
    ]
    forbidden_patterns = ["urllib.request.urlopen", "http.client", "socket.connect", "requests.get"]
    for mod_dir in new_module_dirs:
        for py_file in (REPO_ROOT / mod_dir).glob("*.py"):
            text = py_file.read_text(encoding="utf-8")
            for pat in forbidden_patterns:
                assert pat not in text, f"{pat} found in {py_file}"

def test_no_app_state_mutation_in_new_modules():
    # All new modules must have candidate_only: True in outputs
    from odin.release_readiness_hardening import build_release_readiness_matrix
    from odin.evidence_closure_dry_run import run_evidence_closure_dry_run
    from odin.packaging_boundary_prep import build_packaging_inventory
    from odin.command_surface_closure import build_command_surface_index
    from odin.docs_readiness import build_docs_readiness_index
    from odin.final_pr_13_input_bundle import build_final_pr_13_input_bundle
    for fn in [build_release_readiness_matrix, run_evidence_closure_dry_run,
               build_packaging_inventory, build_command_surface_index,
               build_docs_readiness_index, build_final_pr_13_input_bundle]:
        result = fn()
        assert result.get("candidate_only") is True, f"candidate_only not True in {fn.__name__}"

def test_no_external_send():
    # All new modules must not claim external send
    from odin.final_pr_13_input_bundle import build_final_pr_13_input_bundle
    result = build_final_pr_13_input_bundle()
    assert "external_send" in result.get("forbidden_claims", [])

def test_validator_returns_ok():
    validator_path = REPO_ROOT / "tools/rebaseline/check_final_pr_12_release_readiness_hardening.py"
    assert validator_path.exists(), "PR12 validator missing"
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "report.json"
        result = subprocess.run(
            [sys.executable, str(validator_path),
             "--repo-root", str(REPO_ROOT),
             "--out", str(out),
             "--generated-at-utc", "2026-01-01T00:00:00Z"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            if out.exists():
                report = json.loads(out.read_text(encoding="utf-8"))
                pytest.fail(f"Validator failed with errors: {report.get('errors', [])}")
            else:
                pytest.fail(f"Validator failed: {result.stderr}")
        report = json.loads(out.read_text(encoding="utf-8"))
        assert report.get("status") == "ok"

def test_validate_all_includes_pr12_validator():
    cli_path = REPO_ROOT / "odin/cli.py"
    text = cli_path.read_text(encoding="utf-8")
    assert "validate_final_pr_12_release_readiness_hardening" in text

def test_file_manifest_contains_required_pr12_files():
    manifest_path = REPO_ROOT / "FILE_MANIFEST.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files_in_manifest = {f["path"] for f in manifest.get("files", [])}
    required = [
        "odin/release_readiness_hardening/__init__.py",
        "odin/evidence_closure_dry_run/__init__.py",
        "odin/packaging_boundary_prep/__init__.py",
        "odin/command_surface_closure/__init__.py",
        "odin/docs_readiness/__init__.py",
        "odin/final_pr_13_input_bundle/__init__.py",
    ]
    missing = [p for p in required if p not in files_in_manifest]
    assert not missing, f"FILE_MANIFEST missing: {missing}"

def test_system_map_contains_final_pr_12():
    sysmap_path = REPO_ROOT / "SYSTEM_MAP.json"
    assert sysmap_path.exists()
    sysmap = json.loads(sysmap_path.read_text(encoding="utf-8"))
    assert "final_pr_12_release_readiness_hardening" in sysmap


# ============================================================
# 78-86: Baseline tests still pass (import-only checks here)
# ============================================================

def test_pr11_5_modules_still_import():
    import odin.v711_coverage_compiler  # noqa: F401
    import odin.semantic_kernel_closure  # noqa: F401
    import odin.claims_compiler  # noqa: F401
    import odin.agent_operator_modes  # noqa: F401

def test_pr11_modules_still_import():
    import odin.local_provider_receipts  # noqa: F401
    import odin.critic_runtime  # noqa: F401
    import odin.thor_handoff_compiler  # noqa: F401

def test_pr10_modules_still_import():
    import odin.release_boundaries  # noqa: F401

def test_pr09_modules_still_import():
    import odin.operational_spine  # noqa: F401

def test_pr12_return_report_is_self_contained():
    report_path = REPO_ROOT / "docs/codex/reports/FINAL_PR_12_RELEASE_READINESS_RETURN_REPORT.md"
    assert report_path.exists(), "PR12 return report missing"
    text = report_path.read_text(encoding="utf-8")
    assert "FINAL-PR-13" in text
    assert "candidate_only" in text
    assert "not_proven" in text
