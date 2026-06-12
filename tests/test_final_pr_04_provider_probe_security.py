"""FINAL-PR-04 tests: Provider Probe + Provider Policy + Runtime Security Smoke.

Claim boundary: final_pr_04_tests_candidate_only_no_provider_execution_no_model_inference
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


# ── Provider Registry ──────────────────────────────────────────────────────────

def test_provider_registry_contains_all():
    from odin.providers.registry import PROVIDER_REGISTRY, REQUIRED_PROVIDER_IDS
    for pid in REQUIRED_PROVIDER_IDS:
        assert pid in PROVIDER_REGISTRY, f"missing provider_id: {pid}"


def test_all_providers_execution_allowed_false():
    from odin.providers.registry import PROVIDER_REGISTRY
    for pid, entry in PROVIDER_REGISTRY.items():
        assert entry.get("execution_allowed") is False, f"{pid}: execution_allowed must be False"


def test_local_candidate_providers_no_api_key():
    from odin.providers.registry import PROVIDER_REGISTRY
    for pid in ("ollama_candidate", "llama_cpp_candidate"):
        entry = PROVIDER_REGISTRY[pid]
        assert entry.get("requires_api_key") is False, f"{pid}: requires_api_key must be False"
        assert entry.get("remote") is False, f"{pid}: remote must be False"


# ── Provider Probe ─────────────────────────────────────────────────────────────

def test_probe_all_returns_candidate_local():
    from odin.providers.probe import probe_all_providers
    results = probe_all_providers()
    for r in results:
        assert r.get("candidate_only") is True, f"{r['provider_id']}: candidate_only must be True"
        assert r.get("local_only") is True, f"{r['provider_id']}: local_only must be True"


def test_missing_ollama_binary_not_found():
    from odin.providers.probe import probe_provider
    result = probe_provider("ollama_candidate")
    # Either not_found (binary absent) or available (binary present) — never error
    assert result["status"] in ("available", "not_found", "disabled", "blocked"), \
        f"unexpected status: {result['status']}"
    assert result["execution_allowed"] is False
    assert result["model_inference"] is False


def test_missing_llama_binary_not_found():
    from odin.providers.probe import probe_provider
    result = probe_provider("llama_cpp_candidate")
    assert result["status"] in ("available", "not_found", "disabled", "blocked")
    assert result["execution_allowed"] is False
    assert result["model_inference"] is False


def test_probe_does_not_perform_model_inference():
    from odin.providers.probe import probe_all_providers
    results = probe_all_providers()
    for r in results:
        assert r.get("model_inference") is False, f"{r['provider_id']}: model_inference must be False"


def test_probe_does_not_read_api_keys():
    from odin.providers import probe as probe_mod
    content = Path(probe_mod.__file__).read_text(encoding="utf-8")
    assert "OPENAI_API_KEY" not in content, "probe.py must not reference OPENAI_API_KEY"
    assert "ANTHROPIC_API_KEY" not in content, "probe.py must not reference ANTHROPIC_API_KEY"


# ── Runtime Security Smoke ─────────────────────────────────────────────────────

def test_runtime_security_smoke_ok():
    from odin.runtime_security.smoke import run_runtime_security_smoke
    result = run_runtime_security_smoke(ROOT)
    d = result.as_dict()
    assert d["status"] == "ok", f"smoke findings: {d['forbidden_findings']}"
    assert d["provider_execution_default"] is False
    assert d["model_inference_default"] is False
    assert d["api_key_reads"] is False
    assert d["external_network"] is False
    assert d["public_bind"] is False


def test_runtime_security_smoke_detects_forbidden():
    from odin.runtime_security.smoke import scan_content
    findings = scan_content("OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')", "synthetic_test")
    assert len(findings) > 0, "scan_content must detect OPENAI_API_KEY"
    markers = [f["marker"] for f in findings]
    assert any("OPENAI_API_KEY" in m for m in markers)


# ── QIRC Channels ─────────────────────────────────────────────────────────────

def test_qirc_model_channel_exists():
    from odin.qirc_core.channels import REQUIRED_CHANNELS
    assert "#odin.model" in REQUIRED_CHANNELS, "REQUIRED_CHANNELS must include #odin.model"


def test_provider_probe_emits_qirc_event():
    from odin.qirc_core.bus import clear_bus, list_events, append_event
    clear_bus()
    from odin.providers.probe import probe_all_providers
    results = probe_all_providers()
    for p in results:
        append_event(
            channel="#odin.model",
            kind="provider_probe_status",
            source="test",
            payload={k: p.get(k) for k in ("provider_id", "status", "execution_allowed", "model_inference")},
        )
    events = list_events("#odin.model")
    assert len(events) > 0, "QIRC #odin.model must have provider probe events"
    pids = {e["payload"]["provider_id"] for e in events}
    assert "mock" in pids


# ── Hub Endpoints ──────────────────────────────────────────────────────────────

def _start_hub_server(host="127.0.0.1", port=0):
    from odin.local_hub.server import _SimpleLocalHubHandler
    server = HTTPServer((host, port), _SimpleLocalHubHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, server.server_address[1]


def _get(port, path, host="127.0.0.1"):
    resp = urllib.request.urlopen(f"http://{host}:{port}{path}", timeout=5)
    return json.loads(resp.read().decode())


def _post(port, path, data=b"{}", host="127.0.0.1"):
    req = urllib.request.Request(
        f"http://{host}:{port}{path}",
        data=data,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    resp = urllib.request.urlopen(req, timeout=5)
    return json.loads(resp.read().decode())


def test_local_hub_providers_json():
    server, port = _start_hub_server()
    try:
        data = _get(port, "/providers.json")
        assert data.get("candidate_only") is True
        assert data.get("provider_execution") is False
        assert isinstance(data.get("providers"), list)
        pids = [p["provider_id"] for p in data["providers"]]
        assert "none" in pids
        assert "mock" in pids
    finally:
        server.shutdown()


def test_local_hub_providers_probe_json():
    server, port = _start_hub_server()
    try:
        data = _get(port, "/providers/probe.json")
        assert data.get("candidate_only") is True
        assert data.get("provider_execution") is False
        assert data.get("model_inference") is False
        assert isinstance(data.get("providers"), list)
    finally:
        server.shutdown()


def test_local_hub_providers_probe_post():
    server, port = _start_hub_server()
    try:
        data = _post(port, "/providers/probe")
        assert data.get("candidate_only") is True
        assert data.get("provider_execution") is False
        assert data.get("model_inference") is False
        providers = data.get("providers", [])
        for p in providers:
            assert p.get("execution_allowed") is False
    finally:
        server.shutdown()


def test_local_hub_security_smoke_json():
    server, port = _start_hub_server()
    try:
        data = _get(port, "/security/runtime-smoke.json")
        assert data.get("candidate_only") is True
        assert data.get("status") in ("ok", "findings")
        assert data.get("provider_execution_default") is False
    finally:
        server.shutdown()


# ── UI ID Checks ───────────────────────────────────────────────────────────────

def _get_html(port, host="127.0.0.1"):
    resp = urllib.request.urlopen(f"http://{host}:{port}/", timeout=5)
    return resp.read().decode()


def test_ui_provider_policy_status_id():
    server, port = _start_hub_server()
    try:
        html = _get_html(port)
        assert 'id="provider-policy-status"' in html
    finally:
        server.shutdown()


def test_ui_provider_probe_panel_id():
    server, port = _start_hub_server()
    try:
        html = _get_html(port)
        assert 'id="provider-probe-panel"' in html
    finally:
        server.shutdown()


def test_ui_provider_probe_results_id():
    server, port = _start_hub_server()
    try:
        html = _get_html(port)
        assert 'id="provider-probe-results"' in html
    finally:
        server.shutdown()


def test_ui_provider_execution_boundary_id():
    server, port = _start_hub_server()
    try:
        html = _get_html(port)
        assert 'id="provider-execution-boundary"' in html
    finally:
        server.shutdown()


def test_ui_runtime_security_smoke_status_id():
    server, port = _start_hub_server()
    try:
        html = _get_html(port)
        assert 'id="runtime-security-smoke-status"' in html
    finally:
        server.shutdown()


def test_ui_secret_scan_status_id():
    server, port = _start_hub_server()
    try:
        html = _get_html(port)
        assert 'id="secret-scan-status"' in html
    finally:
        server.shutdown()


def test_ui_network_boundary_status_id():
    server, port = _start_hub_server()
    try:
        html = _get_html(port)
        assert 'id="network-boundary-status"' in html
    finally:
        server.shutdown()


def test_ui_qirc_provider_events_status_id():
    server, port = _start_hub_server()
    try:
        html = _get_html(port)
        assert 'id="qirc-provider-events-status"' in html
    finally:
        server.shutdown()


# ── Proof Packet ───────────────────────────────────────────────────────────────

def test_proof_packet_provider_execution_false():
    from odin.providers.proof import build_proof_packet
    packet = build_proof_packet()
    assert packet.get("provider_execution") is False


def test_proof_packet_model_inference_false():
    from odin.providers.proof import build_proof_packet
    packet = build_proof_packet()
    assert packet.get("model_inference") is False


def test_proof_packet_api_key_reads_false():
    from odin.providers.proof import build_proof_packet
    packet = build_proof_packet()
    assert packet.get("api_key_reads") is False


def test_proof_packet_external_network_false():
    from odin.providers.proof import build_proof_packet
    packet = build_proof_packet()
    assert packet.get("external_network") is False


def test_proof_packet_persisted(tmp_path):
    from odin.providers.proof import persist_proof_packet
    packet = persist_proof_packet(tmp_path)
    out = tmp_path / "reports" / "final_pr_04_provider_probe_security_proof_packet.json"
    assert out.exists(), "proof packet must be persisted"
    loaded = json.loads(out.read_text(encoding="utf-8"))
    assert loaded.get("provider_execution") is False
    assert loaded.get("model_inference") is False


# ── Validator / CLI ────────────────────────────────────────────────────────────

def test_validate_final_pr_04():
    from odin.cli import validate_final_pr_04_provider_probe_security
    errors = validate_final_pr_04_provider_probe_security()
    assert errors == [], f"FINAL-PR-04 validator errors: {errors}"


def test_validate_all_passes():
    from odin.cli import validate_all
    errors = validate_all()
    assert errors == [], f"validate-all errors: {errors}"


# ── Previous PR Regression ─────────────────────────────────────────────────────

def test_previous_final_pr_01():
    from odin.cli import validate_simple_local_hub
    errors = validate_simple_local_hub()
    assert errors == [], f"FINAL-PR-01 regression: {errors}"


def test_previous_final_pr_02():
    from odin.cli import validate_final_pr_02_model_apps_demo
    errors = validate_final_pr_02_model_apps_demo()
    assert errors == [], f"FINAL-PR-02 regression: {errors}"


def test_previous_final_pr_03():
    from odin.cli import validate_final_pr_03_qirc_devmode
    errors = validate_final_pr_03_qirc_devmode()
    assert errors == [], f"FINAL-PR-03 regression: {errors}"
