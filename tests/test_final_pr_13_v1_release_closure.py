"""FINAL-PR-13: v1.0 Candidate Release Closure Tests.

Claim boundary: final_pr_13_v1_candidate_release_closure_not_external_release
candidate_only: true
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# Module imports
# ---------------------------------------------------------------------------

def test_v1_release_closure_imports():
    import odin.v1_release_closure
    assert odin.v1_release_closure is not None


def test_root_public_surface_imports():
    import odin.root_public_surface
    assert odin.root_public_surface is not None


def test_readme_v1_imports():
    import odin.readme_v1
    assert odin.readme_v1 is not None


def test_donation_surface_imports():
    import odin.donation_surface
    assert odin.donation_surface is not None


def test_release_artifact_boundary_imports():
    import odin.release_artifact_boundary
    assert odin.release_artifact_boundary is not None


# ---------------------------------------------------------------------------
# v1 release closure matrix
# ---------------------------------------------------------------------------

def test_v1_release_closure_matrix_returns_dict():
    from odin.v1_release_closure.closure_matrix import build_v1_release_closure_matrix
    result = build_v1_release_closure_matrix()
    assert isinstance(result, dict)


def test_v1_release_closure_matrix_candidate_only():
    from odin.v1_release_closure.closure_matrix import build_v1_release_closure_matrix
    result = build_v1_release_closure_matrix()
    assert result.get("candidate_only") is True


# ---------------------------------------------------------------------------
# v1 release truth
# ---------------------------------------------------------------------------

def test_v1_release_truth_returns_dict():
    from odin.v1_release_closure.release_truth import build_v1_release_truth
    result = build_v1_release_truth()
    assert isinstance(result, dict)


def test_v1_release_truth_external_release_claimed_false():
    from odin.v1_release_closure.release_truth import build_v1_release_truth
    result = build_v1_release_truth()
    assert result.get("external_release_claimed") is False


def test_v1_release_truth_tag_creation_claimed_false():
    from odin.v1_release_closure.release_truth import build_v1_release_truth
    result = build_v1_release_truth()
    assert result.get("tag_creation_claimed") is False


def test_v1_release_truth_github_release_claimed_false():
    from odin.v1_release_closure.release_truth import build_v1_release_truth
    result = build_v1_release_truth()
    assert result.get("github_release_claimed") is False


def test_v1_release_truth_pypi_publication_claimed_false():
    from odin.v1_release_closure.release_truth import build_v1_release_truth
    result = build_v1_release_truth()
    assert result.get("pypi_publication_claimed") is False


# ---------------------------------------------------------------------------
# Root inventory
# ---------------------------------------------------------------------------

def test_root_inventory_returns_dict():
    from odin.root_public_surface.root_inventory import build_root_inventory
    result = build_root_inventory(repo_root=str(ROOT))
    assert isinstance(result, dict)


def test_root_inventory_contains_readme():
    from odin.root_public_surface.root_inventory import build_root_inventory
    result = build_root_inventory(repo_root=str(ROOT))
    assert "README.md" in result.get("present", [])


def test_root_inventory_contains_donations():
    from odin.root_public_surface.root_inventory import build_root_inventory
    result = build_root_inventory(repo_root=str(ROOT))
    assert "DONATIONS.md" in result.get("present", [])


# ---------------------------------------------------------------------------
# Root hygiene report
# ---------------------------------------------------------------------------

def test_root_hygiene_report_returns_dict():
    from odin.root_public_surface.root_hygiene import build_root_hygiene_report
    result = build_root_hygiene_report(repo_root=str(ROOT))
    assert isinstance(result, dict)


def test_root_hygiene_report_does_not_delete_history():
    from odin.root_public_surface.root_hygiene import build_root_hygiene_report
    result = build_root_hygiene_report(repo_root=str(ROOT))
    assert result.get("history_not_deleted") is True


# ---------------------------------------------------------------------------
# README.md checks
# ---------------------------------------------------------------------------

def test_readme_exists():
    assert (ROOT / "README.md").exists()


def test_readme_has_odin_heading():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "# Odin Agent Shell" in text


def test_readme_has_current_status():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Current Status" in text


def test_readme_has_what_odin_is():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## What Odin Is" in text


def test_readme_has_what_odin_is_not():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## What Odin Is Not" in text


def test_readme_has_quick_start():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Quick Start" in text


def test_readme_has_documentation_map():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Documentation Map" in text


def test_readme_has_v1_release_truth():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## v1.0 Candidate Release Truth" in text


def test_readme_has_safety_claim_boundaries():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Safety / Claim Boundaries" in text


def test_readme_has_support_donations_license():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Support, Donations, and License" in text


def test_readme_has_danke_thank_you_heading():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Danke / Thank You" in text


def test_readme_includes_exact_thor_thanks_block():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Danke an Q Germany" in text
    assert "Danke an Q USA" in text
    assert "Danke an Q Worldwide" in text
    assert "Ohne euch wäre das alles unmöglich gewesen" in text
    assert "Gewidmet, dem goldenen Herzen" in text
    assert "Thank you to Q Germany" in text
    assert "Thank you to Q USA" in text
    assert "Thank you to Q Worldwide" in text
    assert "Without you, all of this would have been impossible" in text
    assert "Dedicated to the golden heart of a unique woman and loving mother" in text


def test_readme_links_donations():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "DONATIONS.md" in text


def test_readme_does_not_claim_pypi():
    text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    assert "available on pypi" not in text
    assert "published to pypi" not in text
    assert "released on pypi" not in text


def test_readme_does_not_claim_github_release():
    text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    assert "github release exists" not in text


def test_readme_does_not_claim_production_readiness():
    text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    assert "is production_ready" not in text
    assert "production ready" not in text


def test_readme_does_not_claim_security_certification():
    text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    assert "security certified" not in text
    assert "is security_verified" not in text


def test_readme_does_not_claim_model_superiority():
    text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    assert "model superiority" not in text
    assert "superior model" not in text


# ---------------------------------------------------------------------------
# DONATIONS.md checks
# ---------------------------------------------------------------------------

def test_donations_exists():
    assert (ROOT / "DONATIONS.md").exists()


def test_donations_references_odin():
    text = (ROOT / "DONATIONS.md").read_text(encoding="utf-8")
    assert "Odin" in text


def test_donations_includes_paypal():
    text = (ROOT / "DONATIONS.md").read_text(encoding="utf-8")
    assert "QMetaKI@gmail.com" in text


def test_donations_says_optional():
    text = (ROOT / "DONATIONS.md").read_text(encoding="utf-8").lower()
    assert "optional" in text


def test_donations_no_support_obligation():
    text = (ROOT / "DONATIONS.md").read_text(encoding="utf-8").lower()
    assert "support obligation" in text


def test_donations_no_licensing_rights():
    text = (ROOT / "DONATIONS.md").read_text(encoding="utf-8").lower()
    assert "licensing" in text


def test_donations_no_governance_rights():
    text = (ROOT / "DONATIONS.md").read_text(encoding="utf-8").lower()
    assert "governance" in text


def test_donations_no_paid_support():
    text = (ROOT / "DONATIONS.md").read_text(encoding="utf-8").lower()
    assert "paid support" in text


# ---------------------------------------------------------------------------
# Release artifact boundary
# ---------------------------------------------------------------------------

def test_release_artifact_boundary_returns_dict():
    from odin.release_artifact_boundary.artifact_boundary import build_release_artifact_boundary
    result = build_release_artifact_boundary()
    assert isinstance(result, dict)


def test_release_artifact_boundary_lists_tag_action():
    from odin.release_artifact_boundary.manual_release_actions import build_manual_release_actions
    result = build_manual_release_actions()
    action_names = [a.get("action") for a in result.get("manual_actions", [])]
    assert "create git tag" in action_names


def test_release_artifact_boundary_lists_github_release():
    from odin.release_artifact_boundary.manual_release_actions import build_manual_release_actions
    result = build_manual_release_actions()
    action_names = [a.get("action") for a in result.get("manual_actions", [])]
    assert "create GitHub Release" in action_names


def test_release_artifact_boundary_lists_pypi():
    from odin.release_artifact_boundary.manual_release_actions import build_manual_release_actions
    result = build_manual_release_actions()
    action_names = [a.get("action") for a in result.get("manual_actions", [])]
    assert "publish to PyPI" in action_names


def test_release_artifact_boundary_lists_asset_upload():
    from odin.release_artifact_boundary.manual_release_actions import build_manual_release_actions
    result = build_manual_release_actions()
    action_names = [a.get("action") for a in result.get("manual_actions", [])]
    assert "upload release assets" in action_names


def test_release_artifact_boundary_does_not_claim_actions():
    from odin.release_artifact_boundary.manual_release_actions import build_manual_release_actions
    result = build_manual_release_actions()
    for action in result.get("manual_actions", []):
        assert action.get("claimed_by_pr13") is False, \
            f"Action '{action.get('action')}' claimed_by_pr13 must be False"


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------

def _run_cli(*args):
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli"] + list(args),
        capture_output=True, text=True, cwd=str(ROOT),
        env={"PYTHONPATH": str(ROOT), "PATH": "/usr/bin:/bin", "HOME": "/root"}
    )
    return result


def test_cli_validate_v1_release_closure_returns_0():
    r = _run_cli("validate-v1-release-closure")
    assert r.returncode == 0, f"stderr: {r.stderr}"


def test_cli_build_v1_release_closure_matrix_demo_returns_json():
    r = _run_cli("build-v1-release-closure-matrix", "--demo")
    assert r.returncode == 0, f"stderr: {r.stderr}"
    data = json.loads(r.stdout)
    assert data.get("candidate_only") is True


def test_cli_validate_root_public_surface_returns_0():
    r = _run_cli("validate-root-public-surface")
    assert r.returncode == 0, f"stderr: {r.stderr}"


def test_cli_build_root_inventory_demo_returns_json():
    r = _run_cli("build-root-inventory", "--demo")
    assert r.returncode == 0, f"stderr: {r.stderr}"
    data = json.loads(r.stdout)
    assert data.get("candidate_only") is True


def test_cli_validate_readme_v1_returns_0():
    r = _run_cli("validate-readme-v1")
    assert r.returncode == 0, f"stderr: {r.stderr}"


def test_cli_build_readme_v1_plan_demo_returns_json():
    r = _run_cli("build-readme-v1-plan", "--demo")
    assert r.returncode == 0, f"stderr: {r.stderr}"
    data = json.loads(r.stdout)
    assert data.get("candidate_only") is True


def test_cli_validate_donation_surface_returns_0():
    r = _run_cli("validate-donation-surface")
    assert r.returncode == 0, f"stderr: {r.stderr}"


def test_cli_build_donations_plan_demo_returns_json():
    r = _run_cli("build-donations-plan", "--demo")
    assert r.returncode == 0, f"stderr: {r.stderr}"
    data = json.loads(r.stdout)
    assert data.get("candidate_only") is True


def test_cli_validate_release_artifact_boundary_returns_0():
    r = _run_cli("validate-release-artifact-boundary")
    assert r.returncode == 0, f"stderr: {r.stderr}"


def test_cli_build_release_artifact_boundary_demo_returns_json():
    r = _run_cli("build-release-artifact-boundary", "--demo")
    assert r.returncode == 0, f"stderr: {r.stderr}"
    data = json.loads(r.stdout)
    assert data.get("candidate_only") is True


def test_cli_validate_final_pr_13_returns_0():
    r = _run_cli("validate-final-pr-13-v1-release-closure")
    assert r.returncode == 0, f"stderr: {r.stderr}\nstdout: {r.stdout}"


# ---------------------------------------------------------------------------
# Local Hub tests
# ---------------------------------------------------------------------------

def test_local_hub_v1_release_closure_payload():
    from odin.v1_release_closure.reports import build_v1_release_closure_report
    result = build_v1_release_closure_report()
    assert isinstance(result, dict)
    assert result.get("candidate_only") is True


def test_local_hub_root_public_surface_payload():
    from odin.root_public_surface.reports import build_root_public_surface_report
    result = build_root_public_surface_report()
    assert isinstance(result, dict)
    assert result.get("candidate_only") is True


def test_local_hub_readme_v1_payload():
    from odin.readme_v1.readme_plan import build_readme_v1_plan
    result = build_readme_v1_plan()
    assert isinstance(result, dict)
    assert result.get("candidate_only") is True


def test_local_hub_donation_surface_payload():
    from odin.donation_surface.donations_plan import build_donations_plan
    result = build_donations_plan()
    assert isinstance(result, dict)
    assert result.get("candidate_only") is True


def test_local_hub_release_artifact_boundary_payload():
    from odin.release_artifact_boundary.artifact_boundary import build_release_artifact_boundary
    result = build_release_artifact_boundary()
    assert isinstance(result, dict)
    assert result.get("candidate_only") is True


# ---------------------------------------------------------------------------
# REQUIRED_IDS tests
# ---------------------------------------------------------------------------

def test_required_ids_contains_v1_release_closure():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "v1-release-closure-section" in REQUIRED_IDS


def test_required_ids_contains_root_public_surface():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "root-public-surface-section" in REQUIRED_IDS


def test_required_ids_contains_readme_v1():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "readme-v1-section" in REQUIRED_IDS


def test_required_ids_contains_donation_surface():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "donation-surface-section" in REQUIRED_IDS


def test_required_ids_contains_release_artifact_boundary():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "release-artifact-boundary-section" in REQUIRED_IDS


def test_required_ids_contains_final_pr_13_closure():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "final-pr-13-closure-section" in REQUIRED_IDS


# ---------------------------------------------------------------------------
# Code safety checks
# ---------------------------------------------------------------------------

def test_no_eval_exec_in_new_modules():
    new_modules = [
        ROOT / "odin" / "v1_release_closure",
        ROOT / "odin" / "root_public_surface",
        ROOT / "odin" / "readme_v1",
        ROOT / "odin" / "donation_surface",
        ROOT / "odin" / "release_artifact_boundary",
    ]
    for module_dir in new_modules:
        for py_file in module_dir.glob("*.py"):
            text = py_file.read_text(encoding="utf-8")
            assert "eval(" not in text, f"eval() found in {py_file}"
            assert "exec(" not in text, f"exec() found in {py_file}"
            assert "subprocess" not in text, f"subprocess found in {py_file}"


def test_no_public_network_calls():
    new_modules = [
        ROOT / "odin" / "v1_release_closure",
        ROOT / "odin" / "root_public_surface",
        ROOT / "odin" / "readme_v1",
        ROOT / "odin" / "donation_surface",
        ROOT / "odin" / "release_artifact_boundary",
    ]
    for module_dir in new_modules:
        for py_file in module_dir.glob("*.py"):
            text = py_file.read_text(encoding="utf-8")
            assert "urllib.request.urlopen" not in text, f"network call in {py_file}"
            assert "requests.get" not in text, f"network call in {py_file}"


def test_no_app_state_mutation():
    new_modules = [
        ROOT / "odin" / "v1_release_closure",
        ROOT / "odin" / "root_public_surface",
        ROOT / "odin" / "readme_v1",
        ROOT / "odin" / "donation_surface",
        ROOT / "odin" / "release_artifact_boundary",
    ]
    for module_dir in new_modules:
        for py_file in module_dir.glob("*.py"):
            text = py_file.read_text(encoding="utf-8")
            assert "app_state_mutation = True" not in text, f"app state mutation in {py_file}"


def test_no_external_send():
    new_modules = [
        ROOT / "odin" / "v1_release_closure",
        ROOT / "odin" / "root_public_surface",
        ROOT / "odin" / "readme_v1",
        ROOT / "odin" / "donation_surface",
        ROOT / "odin" / "release_artifact_boundary",
    ]
    for module_dir in new_modules:
        for py_file in module_dir.glob("*.py"):
            text = py_file.read_text(encoding="utf-8")
            assert "external_send = True" not in text, f"external send in {py_file}"


# ---------------------------------------------------------------------------
# Validator test
# ---------------------------------------------------------------------------

def test_validator_returns_ok():
    import importlib.util
    import tempfile
    tool_path = ROOT / "tools" / "rebaseline" / "check_final_pr_13_v1_release_closure.py"
    assert tool_path.exists(), "Validator tool missing"
    spec = importlib.util.spec_from_file_location("odin_final_pr_13_validator", tool_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "report.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
    assert code == 0, f"Validator returned non-zero: {code}"


# ---------------------------------------------------------------------------
# validate-all includes PR13
# ---------------------------------------------------------------------------

def test_validate_all_includes_pr13_validator():
    cli_text = (ROOT / "odin" / "cli.py").read_text(encoding="utf-8")
    assert "validate_final_pr_13_v1_release_closure()" in cli_text


# ---------------------------------------------------------------------------
# FILE_MANIFEST and SYSTEM_MAP
# ---------------------------------------------------------------------------

def test_file_manifest_parseable():
    fm_path = ROOT / "FILE_MANIFEST.json"
    assert fm_path.exists()
    data = json.loads(fm_path.read_text(encoding="utf-8"))
    assert isinstance(data, (dict, list))


def test_system_map_parseable():
    sm_path = ROOT / "SYSTEM_MAP.json"
    assert sm_path.exists()
    data = json.loads(sm_path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)


# ---------------------------------------------------------------------------
# Prior PR regression tests
# ---------------------------------------------------------------------------

def test_pr12_module_still_importable():
    import odin.release_readiness_hardening
    assert odin.release_readiness_hardening is not None


def test_pr11_5_module_still_importable():
    import odin.semantic_kernel_closure
    assert odin.semantic_kernel_closure is not None


def test_pr11_module_still_importable():
    import odin.local_provider_receipts
    assert odin.local_provider_receipts is not None


def test_pr10_module_still_importable():
    import odin.release_boundaries
    assert odin.release_boundaries is not None


def test_pr09_module_still_importable():
    import odin.operational_spine
    assert odin.operational_spine is not None
