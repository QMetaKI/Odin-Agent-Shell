"""Tests for FINAL-PR-10++ Boundary-Gated Release Operationalization.

All tests are deterministic. No network. No model/provider calls. No app apply.

Claim boundary: final_pr_10_boundary_gated_release_operationalization_not_release_certification
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# 1-11: Boundary Matrix tests
# ---------------------------------------------------------------------------

def test_release_boundaries_imports():
    import odin.release_boundaries  # noqa: F401


def test_build_boundary_matrix_exists():
    from odin.release_boundaries import build_boundary_matrix
    assert callable(build_boundary_matrix)


def test_boundary_matrix_returns_dict():
    from odin.release_boundaries import build_boundary_matrix
    result = build_boundary_matrix()
    assert isinstance(result, dict)


def test_boundary_matrix_candidate_only():
    from odin.release_boundaries import build_boundary_matrix
    result = build_boundary_matrix()
    assert result.get("candidate_only") is True


def test_boundary_matrix_contains_candidate_only():
    from odin.release_boundaries import build_boundary_matrix
    result = build_boundary_matrix()
    assert "candidate_only" in result.get("boundaries", {})


def test_boundary_matrix_contains_app_owned_apply():
    from odin.release_boundaries import build_boundary_matrix
    result = build_boundary_matrix()
    assert "app_owned_apply" in result.get("boundaries", {})


def test_boundary_matrix_contains_no_external_send():
    from odin.release_boundaries import build_boundary_matrix
    result = build_boundary_matrix()
    assert "no_external_send" in result.get("boundaries", {})


def test_boundary_matrix_contains_provider_not_authority():
    from odin.release_boundaries import build_boundary_matrix
    result = build_boundary_matrix()
    assert "provider_not_authority" in result.get("boundaries", {})


def test_boundary_matrix_contains_qirc_not_app_authority():
    from odin.release_boundaries import build_boundary_matrix
    result = build_boundary_matrix()
    assert "qirc_not_app_authority" in result.get("boundaries", {})


def test_boundary_matrix_contains_local_provider_execution_disabled():
    from odin.release_boundaries import build_boundary_matrix
    result = build_boundary_matrix()
    assert "local_provider_execution_disabled_by_default" in result.get("boundaries", {})


def test_boundary_matrix_contains_release_closure_deferred():
    from odin.release_boundaries import build_boundary_matrix
    result = build_boundary_matrix()
    assert "release_closure_deferred_to_final_pr_11" in result.get("boundaries", {})


# ---------------------------------------------------------------------------
# 12-20: Ring Authority Map tests
# ---------------------------------------------------------------------------

def test_ring_authority_map_returns_dict():
    from odin.release_boundaries import build_ring_authority_map
    result = build_ring_authority_map()
    assert isinstance(result, dict)


def test_ring_authority_map_contains_ring_0():
    from odin.release_boundaries import build_ring_authority_map
    result = build_ring_authority_map()
    assert "ring_0" in result.get("rings", {})


def test_ring_authority_map_contains_odin_candidate_kernel():
    from odin.release_boundaries import build_ring_authority_map
    result = build_ring_authority_map()
    rings = result.get("rings", {})
    names = [r.get("name", "") for r in rings.values()]
    assert any("Candidate Kernel" in n for n in names)


def test_ring_authority_map_contains_qirc():
    from odin.release_boundaries import build_ring_authority_map
    result = build_ring_authority_map()
    rings = result.get("rings", {})
    names = [r.get("name", "") for r in rings.values()]
    assert any("QIRC" in n for n in names)


def test_ring_authority_map_contains_provider():
    from odin.release_boundaries import build_ring_authority_map
    result = build_ring_authority_map()
    rings = result.get("rings", {})
    names = [r.get("name", "") for r in rings.values()]
    assert any("Provider" in n for n in names)


def test_ring_authority_map_contains_release_governance():
    from odin.release_boundaries import build_ring_authority_map
    result = build_ring_authority_map()
    rings = result.get("rings", {})
    names = [r.get("name", "") for r in rings.values()]
    assert any("Release" in n for n in names)


def test_ring_0_owns_apply():
    from odin.release_boundaries import build_ring_authority_map
    result = build_ring_authority_map()
    ring_0 = result.get("rings", {}).get("ring_0", {})
    assert "app_state_apply" in ring_0.get("owns", [])


def test_qirc_ring_does_not_own_app_state():
    from odin.release_boundaries import build_ring_authority_map
    result = build_ring_authority_map()
    rings = result.get("rings", {})
    qirc_ring = next((r for r in rings.values() if "QIRC" in r.get("name", "")), None)
    assert qirc_ring is not None
    assert "app_state" in qirc_ring.get("does_not_own", [])


def test_provider_ring_does_not_own_truth():
    from odin.release_boundaries import build_ring_authority_map
    result = build_ring_authority_map()
    rings = result.get("rings", {})
    provider_ring = next((r for r in rings.values() if "Provider" in r.get("name", "") and "Worker" in r.get("name", "")), None)
    assert provider_ring is not None
    assert "truth_authority" in provider_ring.get("does_not_own", [])


# ---------------------------------------------------------------------------
# 21-23: Bug6/Q7 Map tests
# ---------------------------------------------------------------------------

def test_bug6_q7_map_returns_dict():
    from odin.release_boundaries import build_bug6_q7_operational_map
    result = build_bug6_q7_operational_map()
    assert isinstance(result, dict)


def test_bug6_q7_map_uses_neutral_terms():
    from odin.release_boundaries import build_bug6_q7_operational_map
    result = build_bug6_q7_operational_map()
    scanners = result.get("scanner_definitions", {})
    # Bug6 maps to authority_drift_scanner
    assert "Bug6" in scanners
    assert "authority_drift_scanner" in scanners.get("Bug6", "")


def test_bug6_q7_map_does_not_create_agent_authority():
    from odin.release_boundaries import build_bug6_q7_operational_map
    result = build_bug6_q7_operational_map()
    # Bug6 and Q7 are lenses only — no claim of being independent agents with authority
    axioms = result.get("axioms", [])
    assert any("lens" in a.lower() for a in axioms), "Bug6/Q7 must be described as lenses only"
    # Scanner definitions must use neutral terms
    scanners = result.get("scanner_definitions", {})
    assert "Bug6" in scanners and "Q7" in scanners


# ---------------------------------------------------------------------------
# 24-28: Q-Shabang Release Gate Map tests
# ---------------------------------------------------------------------------

def test_qshabang_release_gate_map_returns_dict():
    from odin.release_boundaries import build_qshabang_release_gate_map
    result = build_qshabang_release_gate_map()
    assert isinstance(result, dict)


def test_qshabang_map_contains_deterministic_precompute():
    from odin.release_boundaries import build_qshabang_release_gate_map
    result = build_qshabang_release_gate_map()
    assert "deterministic_precompute" in result.get("components", {})


def test_qshabang_map_contains_claim_evidence_reality_gates():
    from odin.release_boundaries import build_qshabang_release_gate_map
    result = build_qshabang_release_gate_map()
    assert "claim_evidence_reality_gates" in result.get("components", {})


def test_qshabang_map_contains_critic_cascade():
    from odin.release_boundaries import build_qshabang_release_gate_map
    result = build_qshabang_release_gate_map()
    assert "critic_cascade" in result.get("components", {})


def test_qshabang_map_contains_qirc_coordination():
    from odin.release_boundaries import build_qshabang_release_gate_map
    result = build_qshabang_release_gate_map()
    assert "qirc_coordination" in result.get("components", {})


# ---------------------------------------------------------------------------
# 29-36: Model Role Authority Matrix tests
# ---------------------------------------------------------------------------

def test_model_role_authority_matrix_returns_dict():
    from odin.release_boundaries import build_model_role_authority_matrix
    result = build_model_role_authority_matrix()
    assert isinstance(result, dict)


def test_model_role_matrix_contains_3b_roles():
    from odin.release_boundaries import build_model_role_authority_matrix
    result = build_model_role_authority_matrix()
    roles = result.get("roles", {})
    three_b_roles = [rid for rid in roles if rid.startswith("3b_")]
    assert len(three_b_roles) >= 5


def test_model_role_matrix_contains_7b_roles():
    from odin.release_boundaries import build_model_role_authority_matrix
    result = build_model_role_authority_matrix()
    roles = result.get("roles", {})
    seven_b_roles = [rid for rid in roles if rid.startswith("7b_")]
    assert len(seven_b_roles) >= 5


def test_model_role_matrix_contains_hybrid_roles():
    from odin.release_boundaries import build_model_role_authority_matrix
    result = build_model_role_authority_matrix()
    roles = result.get("roles", {})
    hybrid_roles = [rid for rid in roles if rid.startswith("hybrid_")]
    assert len(hybrid_roles) >= 3


def test_model_role_matrix_contains_local_provider_candidate():
    from odin.release_boundaries import build_model_role_authority_matrix
    result = build_model_role_authority_matrix()
    assert "local_provider_candidate" in result.get("roles", {})


def test_every_model_role_forbids_app_apply():
    from odin.release_boundaries import build_model_role_authority_matrix
    result = build_model_role_authority_matrix()
    for rid, role in result.get("roles", {}).items():
        assert "app_apply" in role.get("forbidden_actions", []), f"Role {rid} must forbid app_apply"


def test_every_model_role_forbids_external_send():
    from odin.release_boundaries import build_model_role_authority_matrix
    result = build_model_role_authority_matrix()
    for rid, role in result.get("roles", {}).items():
        assert "external_send" in role.get("forbidden_actions", []), f"Role {rid} must forbid external_send"


def test_every_model_role_forbids_truth_authority():
    from odin.release_boundaries import build_model_role_authority_matrix
    result = build_model_role_authority_matrix()
    for rid, role in result.get("roles", {}).items():
        assert "truth_authority" in role.get("forbidden_actions", []), f"Role {rid} must forbid truth_authority"


# ---------------------------------------------------------------------------
# 37-43: Artifact Currency tests
# ---------------------------------------------------------------------------

def test_artifact_currency_index_returns_dict():
    from odin.release_boundaries import build_artifact_currency_index
    result = build_artifact_currency_index()
    assert isinstance(result, dict)


def test_artifact_currency_includes_current_runtime():
    from odin.release_boundaries import build_artifact_currency_index
    result = build_artifact_currency_index()
    assert "current_runtime" in result.get("currency_classes", [])


def test_artifact_currency_includes_current_release_evidence():
    from odin.release_boundaries import build_artifact_currency_index
    result = build_artifact_currency_index()
    assert "current_release_evidence" in result.get("currency_classes", [])


def test_artifact_currency_includes_historical_supporting():
    from odin.release_boundaries import build_artifact_currency_index
    result = build_artifact_currency_index()
    assert "historical_supporting" in result.get("currency_classes", [])


def test_artifact_currency_includes_target_only():
    from odin.release_boundaries import build_artifact_currency_index
    result = build_artifact_currency_index()
    assert "target_only" in result.get("currency_classes", [])


def test_artifact_currency_includes_external_receipt_required():
    from odin.release_boundaries import build_artifact_currency_index
    result = build_artifact_currency_index()
    assert "external_receipt_required" in result.get("currency_classes", [])


def test_target_only_artifact_cannot_be_runtime_proof():
    from odin.release_boundaries import build_artifact_currency_index
    result = build_artifact_currency_index()
    artifacts = result.get("artifacts", {})
    for path, artifact in artifacts.items():
        if artifact.get("currency_class") == "target_only":
            allowed = artifact.get("allowed_release_use", "")
            assert "runtime_proof" not in allowed, f"target_only artifact {path} must not allow runtime_proof"


# ---------------------------------------------------------------------------
# 44-48: Evidence Closure tests
# ---------------------------------------------------------------------------

def test_evidence_closure_index_returns_dict():
    from odin.release_boundaries import build_release_evidence_closure_index
    result = build_release_evidence_closure_index()
    assert isinstance(result, dict)


def test_evidence_closure_includes_operational_spine():
    from odin.release_boundaries import build_release_evidence_closure_index
    result = build_release_evidence_closure_index()
    assert "Operational Spine" in result.get("subsystems", {})


def test_evidence_closure_includes_provider_seam():
    from odin.release_boundaries import build_release_evidence_closure_index
    result = build_release_evidence_closure_index()
    assert "Provider Seam" in result.get("subsystems", {})


def test_evidence_closure_includes_modelworkpacket():
    from odin.release_boundaries import build_release_evidence_closure_index
    result = build_release_evidence_closure_index()
    assert "ModelWorkPacket" in result.get("subsystems", {})


def test_evidence_closure_includes_final_preflight():
    from odin.release_boundaries import build_release_evidence_closure_index
    result = build_release_evidence_closure_index()
    assert "Final Preflight" in result.get("subsystems", {})


# ---------------------------------------------------------------------------
# 49-56: Final Preflight tests
# ---------------------------------------------------------------------------

def test_final_preflight_returns_dict():
    from odin.release_boundaries import run_final_release_preflight
    result = run_final_release_preflight()
    assert isinstance(result, dict)


def test_final_preflight_status_is_valid():
    from odin.release_boundaries import run_final_release_preflight
    result = run_final_release_preflight()
    assert result.get("release_preflight_status") in ("green", "yellow", "red")


def test_final_preflight_has_final_pr_11_deferred():
    from odin.release_boundaries import run_final_release_preflight
    result = run_final_release_preflight()
    assert result.get("final_pr_11_remains_deferred") is True


def test_final_preflight_forbids_production_readiness():
    from odin.release_boundaries import run_final_release_preflight
    result = run_final_release_preflight()
    assert "production_readiness" in result.get("forbidden_release_claims", [])


def test_final_preflight_forbids_security_certification():
    from odin.release_boundaries import run_final_release_preflight
    result = run_final_release_preflight()
    assert "security_certification" in result.get("forbidden_release_claims", [])


def test_final_preflight_forbids_release_certification():
    from odin.release_boundaries import run_final_release_preflight
    result = run_final_release_preflight()
    assert "release_certification" in result.get("forbidden_release_claims", [])


def test_final_preflight_forbids_live_model_inference():
    from odin.release_boundaries import run_final_release_preflight
    result = run_final_release_preflight()
    assert "live_model_inference" in result.get("forbidden_release_claims", [])


def test_final_preflight_forbids_provider_execution():
    from odin.release_boundaries import run_final_release_preflight
    result = run_final_release_preflight()
    assert "provider_execution" in result.get("forbidden_release_claims", [])


# ---------------------------------------------------------------------------
# 57-69: CLI tests
# ---------------------------------------------------------------------------

def _run_cli(*args):
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", *args],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    return result


def test_cli_validate_boundary_matrix():
    r = _run_cli("validate-boundary-matrix")
    assert r.returncode == 0


def test_cli_validate_ring_authority_map():
    r = _run_cli("validate-ring-authority-map")
    assert r.returncode == 0


def test_cli_validate_bug6_q7_operational_map():
    r = _run_cli("validate-bug6-q7-operational-map")
    assert r.returncode == 0


def test_cli_validate_qshabang_release_gate_map():
    r = _run_cli("validate-qshabang-release-gate-map")
    assert r.returncode == 0


def test_cli_validate_model_role_authority():
    r = _run_cli("validate-model-role-authority")
    assert r.returncode == 0


def test_cli_validate_release_evidence_closure():
    r = _run_cli("validate-release-evidence-closure")
    assert r.returncode == 0


def test_cli_validate_artifact_currency():
    r = _run_cli("validate-artifact-currency")
    assert r.returncode == 0


def test_cli_validate_final_release_preflight():
    r = _run_cli("validate-final-release-preflight")
    assert r.returncode == 0


def test_cli_release_preflight_returns_valid_json():
    r = _run_cli("release-preflight")
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data.get("candidate_only") is True


def test_cli_explain_boundaries_returns_valid_json():
    r = _run_cli("explain-boundaries")
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert isinstance(data, dict)


def test_cli_explain_release_claims_returns_valid_json():
    r = _run_cli("explain-release-claims")
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert isinstance(data, dict)


def test_cli_explain_model_role_authority_returns_valid_json():
    r = _run_cli("explain-model-role-authority")
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert isinstance(data, dict)


def test_cli_explain_qshabang_release_gates_returns_valid_json():
    r = _run_cli("explain-qshabang-release-gates")
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert isinstance(data, dict)


# ---------------------------------------------------------------------------
# 70: Local Hub endpoint smoke
# ---------------------------------------------------------------------------

def test_local_hub_release_preflight_payload():
    from odin.release_boundaries.final_preflight import run_final_release_preflight
    result = run_final_release_preflight()
    payload_json = json.dumps(result)
    data = json.loads(payload_json)
    assert data.get("candidate_only") is True
    assert data.get("final_pr_11_remains_deferred") is True


# ---------------------------------------------------------------------------
# 71-74: Safety checks
# ---------------------------------------------------------------------------

def test_required_ids_contains_release_boundary_gates_section():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "release-boundary-gates-section" in REQUIRED_IDS


def test_no_eval_exec_subprocess_in_release_boundaries():
    rb_dir = ROOT / "odin" / "release_boundaries"
    for py_file in rb_dir.glob("*.py"):
        if py_file.name == "__init__.py":
            continue
        text = py_file.read_text(encoding="utf-8", errors="ignore")
        assert "eval(" not in text, f"{py_file.name}: must not use eval()"
        assert "exec(" not in text, f"{py_file.name}: must not use exec()"
        assert "subprocess" not in text, f"{py_file.name}: must not use subprocess"


def test_no_uuid4_random_live_time_in_deterministic_modules():
    rb_dir = ROOT / "odin" / "release_boundaries"
    for py_file in rb_dir.glob("*.py"):
        text = py_file.read_text(encoding="utf-8", errors="ignore")
        assert "uuid.uuid4()" not in text, f"{py_file.name}: must not use uuid4()"
        assert "random.random" not in text, f"{py_file.name}: must not use random"
        assert "datetime.now()" not in text, f"{py_file.name}: must not use datetime.now()"
        assert "time.time()" not in text, f"{py_file.name}: must not use time.time()"


def test_no_public_network_calls_in_release_boundaries():
    rb_dir = ROOT / "odin" / "release_boundaries"
    for py_file in rb_dir.glob("*.py"):
        text = py_file.read_text(encoding="utf-8", errors="ignore")
        assert "urllib.request" not in text, f"{py_file.name}: must not use urllib.request"
        assert "requests.get" not in text, f"{py_file.name}: must not use requests"
        assert "socket.connect" not in text, f"{py_file.name}: must not use socket.connect"


# ---------------------------------------------------------------------------
# 75-76: No provider execution, no live model
# ---------------------------------------------------------------------------

def test_no_provider_execution_in_release_boundaries():
    from odin.release_boundaries import build_model_role_authority_matrix
    result = build_model_role_authority_matrix()
    lpc = result.get("roles", {}).get("local_provider_candidate", {})
    assert lpc.get("disabled_by_default") is True
    assert "provider_execution_without_receipt" in lpc.get("forbidden_actions", [])


def test_no_live_model_inference_claim():
    from odin.release_boundaries import run_final_release_preflight
    result = run_final_release_preflight()
    assert "live_model_inference" in result.get("forbidden_release_claims", [])
    assert "live_model_inference" not in result.get("allowed_release_claims", [])


# ---------------------------------------------------------------------------
# 77-80: Validator and metadata tests
# ---------------------------------------------------------------------------

def test_validator_returns_ok():
    import importlib.util
    validator_path = ROOT / "tools" / "rebaseline" / "check_final_pr_10_boundary_release.py"
    assert validator_path.exists(), "Validator must exist"
    spec = importlib.util.spec_from_file_location("check_final_pr_10", validator_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = str(Path(td) / "check.json")
        code = module.main(["--repo-root", str(ROOT), "--out", out, "--generated-at-utc", "2026-01-01T00:00:00Z"])
        assert code == 0, f"Validator failed with code {code}"


def test_validate_all_includes_pr10_validator():
    cli_path = ROOT / "odin" / "cli.py"
    text = cli_path.read_text(encoding="utf-8", errors="ignore")
    assert "validate_final_pr_10_boundary_release()" in text


def test_file_manifest_contains_pr10_files():
    fm_path = ROOT / "FILE_MANIFEST.json"
    if not fm_path.exists():
        pytest.skip("FILE_MANIFEST.json not present")
    fm_text = fm_path.read_text(encoding="utf-8", errors="ignore")
    required = [
        "odin/release_boundaries/__init__.py",
        "odin/release_boundaries/boundary_matrix.py",
        "odin/release_boundaries/final_preflight.py",
    ]
    for rel in required:
        assert rel in fm_text, f"FILE_MANIFEST missing: {rel}"


def test_system_map_contains_pr10_boundary_release():
    smap_path = ROOT / "SYSTEM_MAP.json"
    if not smap_path.exists():
        pytest.skip("SYSTEM_MAP.json not present")
    smap_text = smap_path.read_text(encoding="utf-8", errors="ignore")
    assert "final_pr_10_boundary_release" in smap_text


# ---------------------------------------------------------------------------
# 81-86: Baseline regression tests
# ---------------------------------------------------------------------------

def test_pr09_operational_spine_tests_pass():
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "tests/test_final_pr_09_operational_spine.py"],
        capture_output=True, text=True, cwd=str(ROOT),
        env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert r.returncode == 0, f"PR09 tests failed:\n{r.stdout}\n{r.stderr}"


def test_pr49_prep_tests_pass():
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "tests/test_final_pr_09_10_qshabang_smallmodel_prep.py"],
        capture_output=True, text=True, cwd=str(ROOT),
        env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert r.returncode == 0, f"PR49 prep tests failed:\n{r.stdout}\n{r.stderr}"


def test_pr08_tests_pass():
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "tests/test_final_pr_08_projection_candidate_spine.py"],
        capture_output=True, text=True, cwd=str(ROOT),
        env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert r.returncode == 0, f"PR08 tests failed:\n{r.stdout}\n{r.stderr}"


def test_pr07_tests_pass():
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "tests/test_final_pr_07_field_selection_spine.py"],
        capture_output=True, text=True, cwd=str(ROOT),
        env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert r.returncode == 0, f"PR07 tests failed:\n{r.stdout}\n{r.stderr}"


def test_pr06_tests_pass():
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "tests/test_final_pr_06_operational_seed_spine.py"],
        capture_output=True, text=True, cwd=str(ROOT),
        env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert r.returncode == 0, f"PR06 tests failed:\n{r.stdout}\n{r.stderr}"


def test_full_suite_result_documented():
    """Return report must be self-contained with full suite result."""
    report_path = ROOT / "docs/codex/reports/FINAL_PR_10_BOUNDARY_RELEASE_RETURN_REPORT.md"
    if not report_path.exists():
        pytest.skip("Return report not yet written")
    text = report_path.read_text(encoding="utf-8", errors="ignore")
    assert "pytest" in text.lower()
    assert "passed" in text.lower() or "ok" in text.lower()
