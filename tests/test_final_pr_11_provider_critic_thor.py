"""Tests for FINAL-PR-11: Local Provider Receipt Harness + Critic Runtime Binding + Thor Handoff Compiler v0.

Claim boundary: final_pr_11_provider_receipt_critic_thor_compiler_not_release_closure
candidate_only: true

All tests are deterministic. No network required. No provider required.
Live provider tests are skip-if-unavailable.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# 1-4: Module imports
# ---------------------------------------------------------------------------

def test_local_provider_receipts_imports():
    import odin.local_provider_receipts
    assert hasattr(odin.local_provider_receipts, "build_provider_readiness_receipt")
    assert hasattr(odin.local_provider_receipts, "build_provider_request_packet")
    assert hasattr(odin.local_provider_receipts, "run_local_provider_receipt")


def test_critic_runtime_imports():
    import odin.critic_runtime
    assert hasattr(odin.critic_runtime, "build_critic_packet")
    assert hasattr(odin.critic_runtime, "run_deterministic_critic")
    assert hasattr(odin.critic_runtime, "run_critic_cascade")


def test_route_evaluation_imports():
    import odin.route_evaluation
    assert hasattr(odin.route_evaluation, "build_route_eval_fixtures")
    assert hasattr(odin.route_evaluation, "evaluate_route_candidate")
    assert hasattr(odin.route_evaluation, "run_route_evaluation_receipt")


def test_thor_handoff_compiler_imports():
    import odin.thor_handoff_compiler
    assert hasattr(odin.thor_handoff_compiler, "build_handoff_input_contract")
    assert hasattr(odin.thor_handoff_compiler, "compile_thor_handoff_bundle")


# ---------------------------------------------------------------------------
# 5-20: Provider readiness and receipt tests
# ---------------------------------------------------------------------------

def test_provider_readiness_receipt_returns_dict():
    from odin.local_provider_receipts.readiness import build_provider_readiness_receipt
    r = build_provider_readiness_receipt("ollama_candidate")
    assert isinstance(r, dict)


def test_provider_readiness_receipt_candidate_only_true():
    from odin.local_provider_receipts.readiness import build_provider_readiness_receipt
    r = build_provider_readiness_receipt("ollama_candidate")
    assert r["candidate_only"] is True


def test_provider_readiness_receipt_has_evidence_class():
    from odin.local_provider_receipts.readiness import build_provider_readiness_receipt
    r = build_provider_readiness_receipt("ollama_candidate")
    assert "evidence_class" in r
    assert r["evidence_class"] == "structural_evidence"


def test_provider_request_packet_clamps_max_input_length():
    from odin.local_provider_receipts.request_packet import build_provider_request_packet
    long_prompt = "x" * 10000
    req = build_provider_request_packet("ollama_candidate", long_prompt, max_input_chars=100)
    assert len(req["prompt_truncated"]) == 100
    assert req["max_input_chars"] == 100


def test_default_provider_receipt_execution_allowed_false():
    from odin.local_provider_receipts.receipt import run_local_provider_receipt
    r = run_local_provider_receipt("ollama_candidate", "hello")
    assert r["execution_allowed"] is False


def test_default_provider_receipt_execution_performed_false():
    from odin.local_provider_receipts.receipt import run_local_provider_receipt
    r = run_local_provider_receipt("ollama_candidate", "hello")
    assert r["execution_performed"] is False


def test_default_provider_receipt_model_inference_false():
    from odin.local_provider_receipts.receipt import run_local_provider_receipt
    r = run_local_provider_receipt("ollama_candidate", "hello")
    assert r["model_inference"] is False


def test_default_provider_receipt_provider_execution_false():
    from odin.local_provider_receipts.receipt import run_local_provider_receipt
    r = run_local_provider_receipt("ollama_candidate", "hello")
    assert r["provider_execution"] is False


def test_explicit_flag_without_env_does_not_execute():
    from odin.local_provider_receipts.receipt import run_local_provider_receipt
    env_key = "ODIN_ENABLE_LOCAL_PROVIDER_EXECUTION"
    old = os.environ.pop(env_key, None)
    try:
        r = run_local_provider_receipt("ollama_candidate", "hello", allow_local_provider_execution=True)
        assert r["execution_performed"] is False
    finally:
        if old is not None:
            os.environ[env_key] = old


def test_unknown_provider_returns_not_allowed_receipt():
    from odin.local_provider_receipts.receipt import run_local_provider_receipt
    r = run_local_provider_receipt("unknown_provider_xyz", "hello")
    assert r["status"] == "provider_not_allowed"
    assert r["execution_performed"] is False


def test_unavailable_provider_returns_unavailable_receipt():
    from odin.local_provider_receipts.executor import run_executor
    env_key = "ODIN_ENABLE_LOCAL_PROVIDER_EXECUTION"
    old = os.environ.get(env_key)
    os.environ[env_key] = "1"
    try:
        r = run_executor(
            "ollama_candidate",
            "test",
            allow_local_provider_execution=True,
        )
        # Either unavailable (binary not found) or scoped receipt
        assert r["status"] in ("provider_unavailable", "scoped_local_provider_receipt")
    finally:
        if old is None:
            os.environ.pop(env_key, None)
        else:
            os.environ[env_key] = old


@pytest.mark.skipif(
    not (os.environ.get("ODIN_ENABLE_LOCAL_PROVIDER_EXECUTION") == "1"),
    reason="Live provider tests require ODIN_ENABLE_LOCAL_PROVIDER_EXECUTION=1",
)
def test_scoped_live_provider_receipt_is_host_scoped():
    from odin.local_provider_receipts.executor import run_executor
    r = run_executor(
        "ollama_candidate",
        "Return one sentence: Odin local receipt smoke.",
        allow_local_provider_execution=True,
    )
    if r["status"] == "scoped_local_provider_receipt":
        assert r["evidence_class"] == "host_scoped_local_receipt"
        assert r["execution_performed"] is True
        assert "real_model_benchmark" in r["not_proven"]


def test_provider_receipt_includes_input_hash():
    from odin.local_provider_receipts.receipt import run_local_provider_receipt
    r = run_local_provider_receipt("ollama_candidate", "hello")
    assert "input_hash" in r


def test_provider_receipt_includes_not_proven():
    from odin.local_provider_receipts.receipt import run_local_provider_receipt
    r = run_local_provider_receipt("ollama_candidate", "hello")
    assert "not_proven" in r
    assert isinstance(r["not_proven"], list)
    assert "production_readiness" in r["not_proven"]


def test_provider_receipt_forbids_app_apply():
    from odin.local_provider_receipts.receipt import run_local_provider_receipt
    r = run_local_provider_receipt("ollama_candidate", "hello")
    assert r.get("app_apply") is False


def test_provider_receipt_forbids_external_send():
    from odin.local_provider_receipts.receipt import run_local_provider_receipt
    r = run_local_provider_receipt("ollama_candidate", "hello")
    assert r.get("external_send") is False


# ---------------------------------------------------------------------------
# 21-31: Critic runtime tests
# ---------------------------------------------------------------------------

def test_deterministic_critic_returns_critic_packet():
    from odin.critic_runtime.deterministic_critic import run_deterministic_critic
    candidate = {"candidate_only": True, "claim_boundary": "test", "not_proven": ["x"]}
    r = run_deterministic_critic(candidate)
    assert isinstance(r, dict)
    assert r["artifact_kind"] == "odin_critic_packet"


def test_critic_packet_candidate_only_true():
    from odin.critic_runtime.deterministic_critic import run_deterministic_critic
    r = run_deterministic_critic({"candidate_only": True, "claim_boundary": "t", "not_proven": ["x"]})
    assert r["candidate_only"] is True


def test_critic_packet_not_authority_true():
    from odin.critic_runtime.deterministic_critic import run_deterministic_critic
    r = run_deterministic_critic({"candidate_only": True, "claim_boundary": "t", "not_proven": ["x"]})
    assert r["not_authority"] is True


def test_critic_packet_final_gate_required_true():
    from odin.critic_runtime.deterministic_critic import run_deterministic_critic
    r = run_deterministic_critic({"candidate_only": True, "claim_boundary": "t", "not_proven": ["x"]})
    assert r["final_gate_required"] is True


def test_critic_packet_has_evidence_class():
    from odin.critic_runtime.deterministic_critic import run_deterministic_critic
    r = run_deterministic_critic({"candidate_only": True, "claim_boundary": "t", "not_proven": ["x"]})
    assert "evidence_class" in r
    assert r["evidence_class"] == "structural_evidence"


def test_critic_detects_missing_not_proven():
    from odin.critic_runtime.deterministic_critic import run_deterministic_critic
    r = run_deterministic_critic({"candidate_only": True, "claim_boundary": "t"})
    assert len(r["errors"]) > 0
    assert any("not_proven" in e for e in r["errors"])


def test_critic_detects_app_apply_true():
    from odin.critic_runtime.deterministic_critic import run_deterministic_critic
    candidate = {"candidate_only": True, "claim_boundary": "t", "not_proven": ["x"], "app_apply": True}
    r = run_deterministic_critic(candidate)
    assert len(r["errors"]) > 0
    assert any("app_apply" in e for e in r["errors"])


def test_critic_detects_external_send_true():
    from odin.critic_runtime.deterministic_critic import run_deterministic_critic
    candidate = {"candidate_only": True, "claim_boundary": "t", "not_proven": ["x"], "external_send": True}
    r = run_deterministic_critic(candidate)
    assert len(r["errors"]) > 0
    assert any("external_send" in e for e in r["errors"])


def test_critic_cascade_runs_deterministic_mode():
    from odin.critic_runtime.cascade import run_critic_cascade
    candidate = {"candidate_only": True, "claim_boundary": "t", "not_proven": ["x"]}
    r = run_critic_cascade(candidate)
    stages = r["cascade_stages"]
    assert any(s["stage"] == "deterministic" for s in stages)


def test_critic_cascade_handles_provider_unavailable():
    from odin.critic_runtime.cascade import run_critic_cascade
    candidate = {"candidate_only": True, "claim_boundary": "t", "not_proven": ["x"]}
    r = run_critic_cascade(candidate, include_model_critic=True, allow_local_provider_execution=False)
    # Should still complete without error
    assert "cascade_stages" in r
    assert "overall_recommendation" in r


def test_critic_cascade_does_not_certify_quality():
    from odin.critic_runtime.cascade import run_critic_cascade
    candidate = {"candidate_only": True, "claim_boundary": "t", "not_proven": ["x"]}
    r = run_critic_cascade(candidate)
    assert r["not_authority"] is True
    assert "not_proven" in r
    assert "real_model_benchmark" in r["not_proven"]


# ---------------------------------------------------------------------------
# 32-41: Route evaluation tests
# ---------------------------------------------------------------------------

def test_route_eval_fixtures_include_deterministic_no_model():
    from odin.route_evaluation.fixtures import build_route_eval_fixtures
    fixtures = build_route_eval_fixtures()
    names = [f["route_name"] for f in fixtures]
    assert "deterministic_no_model" in names


def test_route_eval_fixtures_include_3b_primary():
    from odin.route_evaluation.fixtures import build_route_eval_fixtures
    fixtures = build_route_eval_fixtures()
    names = [f["route_name"] for f in fixtures]
    assert "3b_primary" in names


def test_route_eval_fixtures_include_7b_primary():
    from odin.route_evaluation.fixtures import build_route_eval_fixtures
    fixtures = build_route_eval_fixtures()
    names = [f["route_name"] for f in fixtures]
    assert "7b_primary" in names


def test_route_eval_fixtures_include_3b_7b_hybrid():
    from odin.route_evaluation.fixtures import build_route_eval_fixtures
    fixtures = build_route_eval_fixtures()
    names = [f["route_name"] for f in fixtures]
    assert "3b_7b_hybrid" in names


def test_route_eval_receipt_says_not_a_model_quality_benchmark_true():
    from odin.route_evaluation.receipt import run_route_evaluation_receipt
    r = run_route_evaluation_receipt()
    assert r["not_a_model_quality_benchmark"] is True


def test_route_eval_receipt_says_no_superiority_claim_true():
    from odin.route_evaluation.receipt import run_route_evaluation_receipt
    r = run_route_evaluation_receipt()
    assert r["no_superiority_claim"] is True


def test_route_eval_checks_schema_valid():
    from odin.route_evaluation.evaluator import evaluate_route_candidate
    candidate = {"candidate_only": True, "claim_boundary": "t", "not_proven": ["x"], "app_apply": False, "external_send": False}
    r = evaluate_route_candidate("test_route", candidate)
    assert "schema_valid" in r["dimensions"]


def test_route_eval_checks_slot_completeness():
    from odin.route_evaluation.evaluator import evaluate_route_candidate
    candidate = {
        "candidate_only": True,
        "claim_boundary": "t",
        "not_proven": ["x"],
        "app_apply": False,
        "external_send": False,
        "slot_contract": {"slot_class": "test"},
    }
    r = evaluate_route_candidate("test_route", candidate)
    assert r["dimensions"]["slot_completeness"] is True


def test_route_eval_checks_boundary_violations():
    from odin.route_evaluation.evaluator import evaluate_route_candidate
    candidate = {
        "candidate_only": False,  # violation
        "claim_boundary": "t",
        "not_proven": ["x"],
        "app_apply": False,
        "external_send": False,
    }
    r = evaluate_route_candidate("test_route", candidate)
    assert r["dimensions"]["boundary_violations"] > 0


def test_route_eval_receipt_has_evidence_class():
    from odin.route_evaluation.receipt import run_route_evaluation_receipt
    r = run_route_evaluation_receipt()
    assert "evidence_class" in r
    assert r["evidence_class"] == "structural_evidence"


# ---------------------------------------------------------------------------
# 42-51: Thor Handoff Compiler tests
# ---------------------------------------------------------------------------

def test_thor_input_contract_builds_deterministic_id():
    from odin.thor_handoff_compiler.input_contract import build_handoff_input_contract
    ic = build_handoff_input_contract(
        objective="test",
        repo_evidence=["f.py"],
        allowed_edits=["a/"],
        forbidden_edits=["b/"],
        acceptance_gates=["gate1"],
        claim_boundary="test_cb",
    )
    assert "contract_id" in ic
    ic2 = build_handoff_input_contract(
        objective="test",
        repo_evidence=["f.py"],
        allowed_edits=["a/"],
        forbidden_edits=["b/"],
        acceptance_gates=["gate1"],
        claim_boundary="test_cb",
    )
    assert ic["contract_id"] == ic2["contract_id"]


def test_thor_compiler_produces_agent_operator_work_packet():
    from odin.thor_handoff_compiler.input_contract import build_handoff_input_contract
    from odin.thor_handoff_compiler.compiler import compile_thor_handoff_bundle
    ic = build_handoff_input_contract(objective="t", repo_evidence=[], allowed_edits=[], forbidden_edits=[], acceptance_gates=[], claim_boundary="t")
    bundle = compile_thor_handoff_bundle(ic)
    assert "agent_operator_work_packet" in bundle


def test_thor_compiler_produces_acceptance_matrix():
    from odin.thor_handoff_compiler.input_contract import build_handoff_input_contract
    from odin.thor_handoff_compiler.compiler import compile_thor_handoff_bundle
    ic = build_handoff_input_contract(objective="t", repo_evidence=[], allowed_edits=[], forbidden_edits=[], acceptance_gates=["g1"], claim_boundary="t")
    bundle = compile_thor_handoff_bundle(ic)
    assert "acceptance_matrix" in bundle
    assert bundle["acceptance_matrix"]["rows"][0]["gate"] == "g1"


def test_thor_compiler_produces_validator_plan():
    from odin.thor_handoff_compiler.input_contract import build_handoff_input_contract
    from odin.thor_handoff_compiler.compiler import compile_thor_handoff_bundle
    ic = build_handoff_input_contract(objective="t", repo_evidence=[], allowed_edits=[], forbidden_edits=[], acceptance_gates=["g1"], claim_boundary="t")
    bundle = compile_thor_handoff_bundle(ic)
    assert "validator_plan" in bundle
    assert bundle["validator_plan"]["stdlib_only"] is True


def test_thor_compiler_produces_pr_body_skeleton():
    from odin.thor_handoff_compiler.input_contract import build_handoff_input_contract
    from odin.thor_handoff_compiler.compiler import compile_thor_handoff_bundle
    ic = build_handoff_input_contract(objective="test_obj", repo_evidence=[], allowed_edits=[], forbidden_edits=[], acceptance_gates=[], claim_boundary="t")
    bundle = compile_thor_handoff_bundle(ic)
    assert "pr_body_skeleton" in bundle
    assert "test_obj" in bundle["pr_body_skeleton"]["pr_body_text"]


def test_thor_compiler_produces_return_report_contract():
    from odin.thor_handoff_compiler.input_contract import build_handoff_input_contract
    from odin.thor_handoff_compiler.compiler import compile_thor_handoff_bundle
    ic = build_handoff_input_contract(objective="t", repo_evidence=[], allowed_edits=[], forbidden_edits=[], acceptance_gates=[], claim_boundary="t")
    bundle = compile_thor_handoff_bundle(ic)
    assert "return_report_contract" in bundle
    assert "required_sections" in bundle["return_report_contract"]


def test_thor_compiler_does_not_claim_thor_runtime_execution():
    from odin.thor_handoff_compiler.input_contract import build_handoff_input_contract
    from odin.thor_handoff_compiler.compiler import compile_thor_handoff_bundle
    ic = build_handoff_input_contract(objective="t", repo_evidence=[], allowed_edits=[], forbidden_edits=[], acceptance_gates=[], claim_boundary="t")
    bundle = compile_thor_handoff_bundle(ic)
    assert bundle["thor_runtime_execution"] is False
    assert bundle["agent_autonomy"] is False


# ---------------------------------------------------------------------------
# 49-51: Release sequence transition tests
# ---------------------------------------------------------------------------

def test_release_sequence_transition_says_final_pr_12_is_release_closure():
    p = ROOT / "reports/final_pr_11_release_sequence_transition_report.json"
    assert p.exists(), "release sequence transition report missing"
    data = json.loads(p.read_text())
    assert data["new_release_closure"] == "FINAL-PR-12"


def test_preflight_after_pr11_recommends_final_pr_12():
    p = ROOT / "reports/final_pr_11_preflight_after_pr11_report.json"
    assert p.exists(), "preflight after PR11 report missing"
    data = json.loads(p.read_text())
    assert data["recommended_next_pr"] == "FINAL-PR-12"


def test_final_pr_12_remains_deferred():
    p = ROOT / "reports/final_pr_11_release_sequence_transition_report.json"
    assert p.exists()
    data = json.loads(p.read_text())
    assert data["final_pr_12_remains_deferred"] is True


# ---------------------------------------------------------------------------
# 52-65: CLI tests
# ---------------------------------------------------------------------------

def _run_cli(*args: str, check_json: bool = False) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli"] + list(args),
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    output = result.stdout + result.stderr
    if check_json and result.returncode == 0:
        json.loads(result.stdout)
    return result.returncode, output


def test_cli_validate_local_provider_receipt_harness_returns_0():
    code, out = _run_cli("validate-local-provider-receipt-harness")
    assert code == 0, f"Expected 0, got {code}: {out}"


def test_cli_local_provider_doctor_returns_valid_json():
    code, _ = _run_cli("local-provider-doctor", check_json=True)
    assert code == 0


def test_cli_run_local_provider_receipt_demo_returns_valid_json():
    code, _ = _run_cli("run-local-provider-receipt", "--demo", check_json=True)
    assert code == 0


def test_cli_validate_critic_runtime_binding_returns_0():
    code, out = _run_cli("validate-critic-runtime-binding")
    assert code == 0, f"Expected 0, got {code}: {out}"


def test_cli_run_critic_cascade_demo_returns_valid_json():
    code, _ = _run_cli("run-critic-cascade", "--demo", check_json=True)
    assert code == 0


def test_cli_validate_route_evaluation_receipts_returns_0():
    code, out = _run_cli("validate-route-evaluation-receipts")
    assert code == 0, f"Expected 0, got {code}: {out}"


def test_cli_run_route_evaluation_demo_returns_valid_json():
    code, _ = _run_cli("run-route-evaluation", "--demo", check_json=True)
    assert code == 0


def test_cli_validate_thor_handoff_compiler_returns_0():
    code, out = _run_cli("validate-thor-handoff-compiler")
    assert code == 0, f"Expected 0, got {code}: {out}"


def test_cli_compile_thor_handoff_demo_returns_valid_json():
    code, _ = _run_cli("compile-thor-handoff", "--demo", check_json=True)
    assert code == 0


def test_cli_validate_final_pr_11_provider_critic_thor_returns_0():
    # This runs the full validator — will fail until all files exist
    code, out = _run_cli("validate-final-pr-11-provider-critic-thor")
    assert code == 0, f"Expected 0, got {code}:\n{out}"


# ---------------------------------------------------------------------------
# 62-65: Local Hub payload tests
# ---------------------------------------------------------------------------

def test_local_hub_provider_receipt_demo_payload_returns_json():
    from odin.local_provider_receipts.receipt import run_local_provider_receipt
    result = run_local_provider_receipt("deterministic_no_provider", "demo", allow_local_provider_execution=False)
    assert isinstance(result, dict)
    json.dumps(result)  # must be serializable


def test_local_hub_critic_runtime_demo_payload_returns_json():
    from odin.critic_runtime.cascade import run_critic_cascade
    candidate = {"candidate_only": True, "claim_boundary": "t", "not_proven": ["x"]}
    result = run_critic_cascade(candidate)
    assert isinstance(result, dict)
    json.dumps(result)


def test_local_hub_thor_compiler_demo_payload_returns_json():
    from odin.thor_handoff_compiler.input_contract import build_handoff_input_contract
    from odin.thor_handoff_compiler.compiler import compile_thor_handoff_bundle
    ic = build_handoff_input_contract(objective="demo", repo_evidence=[], allowed_edits=[], forbidden_edits=[], acceptance_gates=[], claim_boundary="demo")
    result = compile_thor_handoff_bundle(ic)
    json.dumps(result)


def test_local_hub_preflight_after_pr11_payload_returns_json():
    p = ROOT / "reports/final_pr_11_preflight_after_pr11_report.json"
    data = json.loads(p.read_text())
    json.dumps(data)


# ---------------------------------------------------------------------------
# 66-69: UI section tests
# ---------------------------------------------------------------------------

def test_required_ids_contains_provider_receipt_harness_section():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "provider-receipt-harness-section" in REQUIRED_IDS


def test_required_ids_contains_critic_runtime_binding_section():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "critic-runtime-binding-section" in REQUIRED_IDS


def test_required_ids_contains_thor_handoff_compiler_section():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "thor-handoff-compiler-section" in REQUIRED_IDS


def test_required_ids_contains_release_sequence_transition_section():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "release-sequence-transition-section" in REQUIRED_IDS


# ---------------------------------------------------------------------------
# 70-73: Safety invariant tests
# ---------------------------------------------------------------------------

def test_no_eval_exec_in_new_modules():
    new_modules = [
        ROOT / "odin/local_provider_receipts",
        ROOT / "odin/critic_runtime",
        ROOT / "odin/route_evaluation",
        ROOT / "odin/thor_handoff_compiler",
    ]
    for module_dir in new_modules:
        for py_file in module_dir.glob("*.py"):
            text = py_file.read_text(encoding="utf-8")
            assert "eval(" not in text, f"eval() found in {py_file}"
            assert "exec(" not in text, f"exec() found in {py_file}"


def test_no_public_network_calls_in_new_modules():
    executor = ROOT / "odin/local_provider_receipts/executor.py"
    new_modules = [
        ROOT / "odin/local_provider_receipts",
        ROOT / "odin/critic_runtime",
        ROOT / "odin/route_evaluation",
        ROOT / "odin/thor_handoff_compiler",
    ]
    bad_patterns = ["urllib.request.urlopen", "requests.get", "requests.post"]
    for module_dir in new_modules:
        for py_file in module_dir.glob("*.py"):
            if py_file == executor:
                continue
            text = py_file.read_text(encoding="utf-8")
            for pat in bad_patterns:
                assert pat not in text, f"Public network call {pat!r} found in {py_file}"


def test_no_app_state_mutation():
    from odin.local_provider_receipts.receipt import run_local_provider_receipt
    r = run_local_provider_receipt("ollama_candidate", "test")
    assert r.get("app_apply") is False
    assert r.get("external_send") is False


def test_no_external_send():
    from odin.critic_runtime.cascade import run_critic_cascade
    candidate = {"candidate_only": True, "claim_boundary": "t", "not_proven": ["x"]}
    r = run_critic_cascade(candidate)
    assert r.get("external_send") is False
    assert r.get("public_network") is False


# ---------------------------------------------------------------------------
# 74-77: Validator and metadata tests
# ---------------------------------------------------------------------------

def test_validator_returns_ok():
    import tempfile
    validator = ROOT / "tools/rebaseline/check_final_pr_11_provider_critic_thor.py"
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "report.json"
        result = subprocess.run(
            [sys.executable, str(validator), "--repo-root", str(ROOT), "--out", str(out)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if out.exists():
            report = json.loads(out.read_text())
            assert report["status"] == "ok", f"Validator errors: {report.get('errors', [])}"
        assert result.returncode == 0, f"Validator failed:\n{result.stderr}"


def test_validate_all_includes_pr11_validator():
    cli_text = (ROOT / "odin/cli.py").read_text(encoding="utf-8")
    assert "validate_final_pr_11_provider_critic_thor" in cli_text


def test_file_manifest_contains_required_pr11_files():
    fm = ROOT / "FILE_MANIFEST.json"
    assert fm.exists()
    text = fm.read_text(encoding="utf-8")
    required = [
        "odin/local_provider_receipts/__init__.py",
        "odin/critic_runtime/__init__.py",
        "odin/route_evaluation/__init__.py",
        "odin/thor_handoff_compiler/__init__.py",
        "tests/test_final_pr_11_provider_critic_thor.py",
    ]
    for rel in required:
        assert rel in text, f"FILE_MANIFEST missing: {rel}"


def test_system_map_contains_final_pr_11():
    sm = ROOT / "SYSTEM_MAP.json"
    assert sm.exists()
    text = sm.read_text(encoding="utf-8")
    assert "final_pr_11_provider_critic_thor" in text


# ---------------------------------------------------------------------------
# 78-84: Regression tests — ensure prior PRs still pass
# ---------------------------------------------------------------------------

def test_pr10_tests_still_pass():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/test_final_pr_10_boundary_release.py", "-p", "no:cacheprovider"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"PR10 tests failed:\n{result.stdout}\n{result.stderr}"


def test_pr09_tests_still_pass():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/test_final_pr_09_operational_spine.py", "-p", "no:cacheprovider"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"PR09 tests failed:\n{result.stdout}\n{result.stderr}"


def test_pr49_prep_tests_still_pass():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/test_final_pr_09_10_qshabang_smallmodel_prep.py", "-p", "no:cacheprovider"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"PR49 tests failed:\n{result.stdout}\n{result.stderr}"


def test_pr08_tests_still_pass():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/test_final_pr_08_projection_candidate_spine.py", "-p", "no:cacheprovider"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"PR08 tests failed:\n{result.stdout}\n{result.stderr}"


def test_pr07_tests_still_pass():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/test_final_pr_07_field_selection_spine.py", "-p", "no:cacheprovider"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"PR07 tests failed:\n{result.stdout}\n{result.stderr}"


def test_pr06_tests_still_pass():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/test_final_pr_06_operational_seed_spine.py", "-p", "no:cacheprovider"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"PR06 tests failed:\n{result.stdout}\n{result.stderr}"
