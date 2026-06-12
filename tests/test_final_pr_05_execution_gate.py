"""FINAL-PR-05 tests: Execution Gate + Mock Provider + Proof Chain + Ladder Scaffold.

Claim boundary: final_pr_05_tests_candidate_only_no_provider_execution_no_model_inference
candidate_only: true
"""
from __future__ import annotations

import json
import threading
import urllib.request
from http.server import HTTPServer
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


# ── Execution Gate Policy ──────────────────────────────────────────────────────

def test_execution_gate_default_policy_allows_mock():
    from odin.execution_gate.policy import DEFAULT_EXECUTION_GATE_POLICY as p
    assert p.mock_execution_allowed is True


def test_execution_gate_default_policy_blocks_local_candidate():
    from odin.execution_gate.policy import DEFAULT_EXECUTION_GATE_POLICY as p
    assert p.local_candidate_execution_allowed is False


def test_execution_gate_default_policy_blocks_remote():
    from odin.execution_gate.policy import DEFAULT_EXECUTION_GATE_POLICY as p
    assert p.remote_execution_allowed is False


def test_execution_gate_default_policy_blocks_api_key_reads():
    from odin.execution_gate.policy import DEFAULT_EXECUTION_GATE_POLICY as p
    assert p.api_key_reads_allowed is False


# ── Mock Execution ─────────────────────────────────────────────────────────────

def test_mock_execution_returns_deterministic_response_packet():
    from odin.execution_gate.mock_provider import MockProvider
    mp = MockProvider()
    r1 = mp.execute(input_text="hello world")
    r2 = mp.execute(input_text="hello world")
    assert r1["candidate_text"] == r2["candidate_text"], "mock execution must be deterministic"


def test_mock_execution_has_candidate_only_true():
    from odin.execution_gate.mock_provider import build_mock_response
    result = build_mock_response("test input")
    assert result["candidate_only"] is True


def test_mock_execution_has_local_only_true():
    from odin.execution_gate.mock_provider import build_mock_response
    result = build_mock_response("test input")
    assert result["local_only"] is True


def test_mock_execution_marks_model_inference_false():
    from odin.execution_gate.mock_provider import build_mock_response
    result = build_mock_response("test input")
    assert result["model_inference"] is False


def test_mock_execution_marks_real_provider_execution_false():
    from odin.execution_gate.mock_provider import build_mock_response
    result = build_mock_response("test input")
    assert result["real_provider_execution"] is False


def test_mock_execution_has_app_apply_false():
    from odin.execution_gate.mock_provider import build_mock_response
    result = build_mock_response("test input")
    assert result["app_apply"] is False


def test_mock_execution_emits_qirc_event():
    from odin.qirc_core.bus import clear_bus, list_events
    from odin.execution_gate.gateway import execute_candidate
    clear_bus()
    execute_candidate(input_text="qirc-event-test", provider_id="mock")
    events = list_events("#odin.model")
    assert len(events) > 0, "mock execution must emit QIRC events on #odin.model"


def test_mock_execution_creates_trace_receipt_refs():
    from odin.execution_gate.mock_provider import build_mock_response
    result = build_mock_response("trace-test")
    assert result.get("trace_ref") is not None
    assert result.get("receipt_ref") is not None


# ── Local Candidate Blocked ────────────────────────────────────────────────────

def test_local_candidate_execution_attempt_blocked_by_default():
    from odin.execution_gate.gateway import execute_candidate
    for pid in ("ollama_candidate", "llama_cpp_candidate"):
        result = execute_candidate(input_text="test", provider_id=pid)
        assert result["gate_decision"] == "blocked", f"{pid} must be blocked by default"


def test_blocked_attempt_emits_qirc_warning_event():
    from odin.qirc_core.bus import clear_bus, list_events
    from odin.execution_gate.gateway import execute_candidate
    clear_bus()
    execute_candidate(input_text="test", provider_id="ollama_candidate")
    warning_events = list_events("#odin.warning")
    model_events = list_events("#odin.model")
    # Should have blocking event on either #odin.warning or #odin.model
    all_events = warning_events + model_events
    blocked_kinds = [e.get("kind") for e in all_events]
    assert any("blocked" in k for k in blocked_kinds), \
        f"expected a blocked event but got: {blocked_kinds}"


# ── Proof Chain ────────────────────────────────────────────────────────────────

def test_proof_chain_references_pr01():
    from odin.proof_chain.registry import PROOF_CHAIN_REGISTRY
    assert "final_pr_01" in PROOF_CHAIN_REGISTRY


def test_proof_chain_references_pr02():
    from odin.proof_chain.registry import PROOF_CHAIN_REGISTRY
    assert "final_pr_02" in PROOF_CHAIN_REGISTRY


def test_proof_chain_references_pr03():
    from odin.proof_chain.registry import PROOF_CHAIN_REGISTRY
    assert "final_pr_03" in PROOF_CHAIN_REGISTRY


def test_proof_chain_references_pr04():
    from odin.proof_chain.registry import PROOF_CHAIN_REGISTRY
    assert "final_pr_04" in PROOF_CHAIN_REGISTRY


def test_proof_chain_references_pr05():
    from odin.proof_chain.registry import PROOF_CHAIN_REGISTRY
    assert "final_pr_05" in PROOF_CHAIN_REGISTRY


# ── Ladder Scaffold ────────────────────────────────────────────────────────────

def test_ladder_scaffold_produces_target_pr06_worker_packet():
    from odin.final_pr_ladder.compiler import compile_worker_packet_scaffold
    scaffold = compile_worker_packet_scaffold(target_pr_id="FINAL-PR-06")
    assert scaffold["target_pr_id"] == "FINAL-PR-06"
    assert scaffold["artifact_kind"] == "odin_final_pr_worker_packet_scaffold"


def test_ladder_scaffold_is_candidate_only():
    from odin.final_pr_ladder.compiler import compile_worker_packet_scaffold
    scaffold = compile_worker_packet_scaffold(target_pr_id="FINAL-PR-06")
    assert scaffold["candidate_only"] is True


def test_ladder_scaffold_does_not_claim_full_thor_replacement():
    from odin.final_pr_ladder.compiler import compile_worker_packet_scaffold
    scaffold = compile_worker_packet_scaffold(target_pr_id="FINAL-PR-06")
    assert "thor_runtime_replacement" in scaffold["not_proven"]
    # Check claim boundary
    assert scaffold["claim_boundary"] == "final_pr_ladder_scaffold_not_full_prompt_compiler"


# ── Endpoints (HTTP) ───────────────────────────────────────────────────────────

def _start_hub() -> tuple[HTTPServer, int]:
    from odin.local_hub.server import _SimpleLocalHubHandler
    server = HTTPServer(("127.0.0.1", 0), _SimpleLocalHubHandler)
    port = server.server_address[1]
    t = threading.Thread(target=server.serve_forever)
    t.daemon = True
    t.start()
    return server, port


def test_endpoint_execution_gate_status_json_exists():
    server, port = _start_hub()
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/execution-gate/status.json") as resp:
            data = json.loads(resp.read().decode())
        assert data.get("artifact_kind") == "odin_execution_gate_policy"
    finally:
        server.shutdown()


def test_post_execution_gate_mock_returns_candidate_response():
    server, port = _start_hub()
    try:
        body = json.dumps({"input": "test mock execution"}).encode("utf-8")
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/execution-gate/mock",
            data=body,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        assert data.get("mock_execution") is True
        assert data.get("model_inference") is False
        assert data.get("candidate_only") is True
    finally:
        server.shutdown()


def test_endpoint_proof_chain_json_exists():
    server, port = _start_hub()
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/execution-gate/proof-chain.json") as resp:
            data = json.loads(resp.read().decode())
        assert data.get("artifact_kind") == "odin_final_pr_proof_chain"
        assert data.get("candidate_only") is True
    finally:
        server.shutdown()


def test_endpoint_final_pr_ladder_scaffold_json_exists():
    server, port = _start_hub()
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/final-pr-ladder/scaffold.json") as resp:
            data = json.loads(resp.read().decode())
        assert data.get("artifact_kind") == "odin_final_pr_worker_packet_scaffold"
        assert data.get("candidate_only") is True
    finally:
        server.shutdown()


# ── UI IDs ─────────────────────────────────────────────────────────────────────

def test_ui_contains_execution_gate_status():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "execution-gate-status" in REQUIRED_IDS


def test_ui_contains_mock_execution_panel():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "mock-execution-panel" in REQUIRED_IDS


def test_ui_contains_mock_execution_result():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "mock-execution-result" in REQUIRED_IDS


def test_ui_contains_local_candidate_policy_status():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "local-candidate-policy-status" in REQUIRED_IDS


def test_ui_contains_execution_boundary_status():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "execution-boundary-status" in REQUIRED_IDS


def test_ui_contains_proof_chain_status():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "proof-chain-status" in REQUIRED_IDS


def test_ui_contains_final_pr_ladder_scaffold_status():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "final-pr-ladder-scaffold-status" in REQUIRED_IDS


def test_ui_contains_model_execution_warning():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "model-execution-warning" in REQUIRED_IDS


# ── Validators ─────────────────────────────────────────────────────────────────

def test_validate_final_pr_05_execution_gate_passes():
    import tempfile
    import importlib.util
    tool_path = ROOT / "tools" / "rebaseline" / "check_final_pr_05_execution_gate.py"
    assert tool_path.exists(), "FINAL-PR-05 validator must exist"
    spec = importlib.util.spec_from_file_location("check_final_pr_05", tool_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "report.json"
        code = module.main(["--repo-root", str(ROOT), "--out", str(out), "--generated-at-utc", "2026-01-01T00:00:00Z"])
    assert code == 0, "validate-final-pr-05-execution-gate must pass with 0 errors"


def test_validate_all_passes():
    import sys
    from odin.cli import validate_all
    errors = validate_all()
    assert errors == [], f"validate-all must pass but found errors: {errors[:5]}"


# ── Previous PR compatibility ──────────────────────────────────────────────────

def test_previous_final_pr_01_test_simple_hub_exists():
    assert (ROOT / "tests" / "test_simple_local_hub.py").exists()


def test_previous_final_pr_02_test_model_apps_exists():
    assert (ROOT / "tests" / "test_final_pr_02_model_apps_demo.py").exists()


def test_previous_final_pr_03_test_qirc_devmode_exists():
    assert (ROOT / "tests" / "test_final_pr_03_qirc_devmode.py").exists()


def test_previous_final_pr_04_test_provider_probe_exists():
    assert (ROOT / "tests" / "test_final_pr_04_provider_probe_security.py").exists()


def test_full_pytest_collection_includes_all_pr_tests():
    """Smoke check: all FINAL-PR test files are present for full pytest run."""
    required = [
        "tests/test_simple_local_hub.py",
        "tests/test_final_pr_02_model_apps_demo.py",
        "tests/test_final_pr_03_qirc_devmode.py",
        "tests/test_final_pr_04_provider_probe_security.py",
        "tests/test_final_pr_05_execution_gate.py",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), f"missing test file: {rel}"
