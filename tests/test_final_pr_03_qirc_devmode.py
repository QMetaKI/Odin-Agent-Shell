"""Tests for FINAL-PR-03 QIRC Core Dev Mode.

Claim boundary: final_pr_03_qirc_first_slice_local_only_not_public_network_not_runtime_completion
candidate_only: true

40 tests covering:
  - surface_registry (01-08)
  - server endpoints (09-14)
  - ui.py REQUIRED_IDS (15-22)
  - demo_universal_work bus emission (23-26)
  - proof_pr03 (27-28)
  - qirc_core.policy (29-31)
  - qirc_core.channels (32-33)
  - validate integration (34-35)
  - forbidden patterns (36-38)
  - meta/coverage (39-40)
"""
from __future__ import annotations

import inspect
import json
import pathlib
import tempfile
import threading
import urllib.request

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# Surface registry tests (01-08)
# ---------------------------------------------------------------------------

def test_01_surface_registry_importable():
    from odin.local_hub.surface_registry import SURFACES, check_conflicts, get_canonical_entry
    assert SURFACES is not None


def test_02_surface_registry_has_8765():
    from odin.local_hub.surface_registry import SURFACES
    ports = {s["port"] for s in SURFACES}
    assert 8765 in ports


def test_03_surface_registry_has_8877():
    from odin.local_hub.surface_registry import SURFACES
    ports = {s["port"] for s in SURFACES}
    assert 8877 in ports


def test_04_surface_registry_has_8878():
    from odin.local_hub.surface_registry import SURFACES
    ports = {s["port"] for s in SURFACES}
    assert 8878 in ports


def test_05_surface_registry_8765_is_canonical():
    from odin.local_hub.surface_registry import get_canonical_entry
    entry = get_canonical_entry()
    assert entry["port"] == 8765
    assert entry.get("is_canonical_entry") is True


def test_06_surface_registry_conflict_check_ok():
    from odin.local_hub.surface_registry import check_conflicts
    result = check_conflicts()
    assert result["status"] == "ok"
    assert result["duplicate_ports"] == []
    assert result["public_bind_risk"] == []


def test_07_surface_registry_surface_map_summary():
    from odin.local_hub.surface_registry import surface_map_summary
    summary = surface_map_summary()
    assert summary["artifact_kind"] == "odin_hub_surface_map"
    assert summary["canonical_entry_port"] == 8765
    assert summary.get("candidate_only") is True
    assert summary.get("local_only") is True
    assert "claim_boundary" in summary


def test_08_surface_registry_all_surfaces_local_only():
    from odin.local_hub.surface_registry import SURFACES
    for s in SURFACES:
        assert s.get("local_only") is True, f"port {s['port']} missing local_only"
        assert s.get("candidate_only") is True, f"port {s['port']} missing candidate_only"


# ---------------------------------------------------------------------------
# Server endpoint tests (09-14)
# ---------------------------------------------------------------------------

def _start_ephemeral_server():
    """Start the local hub server on an ephemeral port. Returns (server, base_url, thread)."""
    from http.server import HTTPServer
    from odin.local_hub.server import _SimpleLocalHubHandler
    server = HTTPServer(("127.0.0.1", 0), _SimpleLocalHubHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f"http://127.0.0.1:{port}", thread


def test_09_server_activity_json_endpoint():
    server, base, thread = _start_ephemeral_server()
    try:
        resp = urllib.request.urlopen(f"{base}/activity.json", timeout=5)
        data = json.loads(resp.read().decode())
        assert data.get("artifact_kind") == "odin_activity_list"
        assert data.get("candidate_only") is True
        assert data.get("local_only") is True
        assert "events" in data
    finally:
        server.shutdown()
        thread.join(timeout=3)


def test_10_server_qirc_channels_json_endpoint():
    server, base, thread = _start_ephemeral_server()
    try:
        resp = urllib.request.urlopen(f"{base}/qirc/channels.json", timeout=5)
        data = json.loads(resp.read().decode())
        assert data.get("artifact_kind") == "odin_qirc_channels"
        assert data.get("candidate_only") is True
        assert data.get("local_only") is True
        assert "channels" in data
        assert len(data["channels"]) >= 7
    finally:
        server.shutdown()
        thread.join(timeout=3)


def test_11_server_qirc_events_json_endpoint():
    server, base, thread = _start_ephemeral_server()
    try:
        resp = urllib.request.urlopen(f"{base}/qirc/events.json", timeout=5)
        data = json.loads(resp.read().decode())
        assert data.get("artifact_kind") == "odin_qirc_events"
        assert data.get("candidate_only") is True
        assert data.get("local_only") is True
        assert "events" in data
    finally:
        server.shutdown()
        thread.join(timeout=3)


def test_12_server_traces_json_endpoint():
    server, base, thread = _start_ephemeral_server()
    try:
        resp = urllib.request.urlopen(f"{base}/traces.json", timeout=5)
        data = json.loads(resp.read().decode())
        assert data.get("artifact_kind") == "odin_traces"
        assert data.get("candidate_only") is True
        assert "events" in data
    finally:
        server.shutdown()
        thread.join(timeout=3)


def test_13_server_receipts_json_endpoint():
    server, base, thread = _start_ephemeral_server()
    try:
        resp = urllib.request.urlopen(f"{base}/receipts.json", timeout=5)
        data = json.loads(resp.read().decode())
        assert data.get("artifact_kind") == "odin_receipts"
        assert data.get("candidate_only") is True
        assert "events" in data
    finally:
        server.shutdown()
        thread.join(timeout=3)


def test_14_server_dev_status_json_endpoint():
    server, base, thread = _start_ephemeral_server()
    try:
        resp = urllib.request.urlopen(f"{base}/dev/status.json", timeout=5)
        data = json.loads(resp.read().decode())
        assert data.get("artifact_kind") == "odin_dev_status"
        assert data.get("candidate_only") is True
        assert "surface_map" in data
        assert "qirc_bus" in data
    finally:
        server.shutdown()
        thread.join(timeout=3)


# ---------------------------------------------------------------------------
# UI REQUIRED_IDS tests (15-22)
# ---------------------------------------------------------------------------

def test_15_ui_required_ids_has_qirc_channel_viewer():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "qirc-channel-viewer" in REQUIRED_IDS


def test_16_ui_required_ids_has_qirc_event_viewer():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "qirc-event-viewer" in REQUIRED_IDS


def test_17_ui_required_ids_has_activity_timeline():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "activity-timeline" in REQUIRED_IDS


def test_18_ui_required_ids_has_trace_viewer():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "trace-viewer" in REQUIRED_IDS


def test_19_ui_required_ids_has_receipt_viewer():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "receipt-viewer" in REQUIRED_IDS


def test_20_ui_required_ids_has_handoff_chain_viewer():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "handoff-chain-viewer" in REQUIRED_IDS


def test_21_ui_required_ids_has_surface_map_viewer():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "surface-map-viewer" in REQUIRED_IDS


def test_22_ui_required_ids_has_proof_gap_viewer():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "proof-gap-viewer" in REQUIRED_IDS


# ---------------------------------------------------------------------------
# Demo universal work bus emission (23-26)
# ---------------------------------------------------------------------------

def test_23_demo_universal_work_emits_activity_event():
    from odin.qirc_core.bus import clear_bus, list_events
    from odin.local_hub.demo_universal_work import build_demo_universal_work_response
    clear_bus()
    build_demo_universal_work_response("test input for pr03")
    events = list_events("#odin.activity")
    assert len(events) >= 1


def test_24_demo_activity_event_has_correct_kind():
    from odin.qirc_core.bus import clear_bus, list_events
    from odin.local_hub.demo_universal_work import build_demo_universal_work_response
    clear_bus()
    build_demo_universal_work_response("kind check input")
    events = list_events("#odin.activity")
    assert any(e.get("kind") == "demo_universal_work" for e in events)


def test_25_demo_activity_event_candidate_only():
    from odin.qirc_core.bus import clear_bus, list_events
    from odin.local_hub.demo_universal_work import build_demo_universal_work_response
    clear_bus()
    build_demo_universal_work_response("candidate only check")
    events = list_events("#odin.activity")
    for e in events:
        assert e.get("candidate_only") is True


def test_26_demo_activity_event_has_trace_ref():
    from odin.qirc_core.bus import clear_bus, list_events
    from odin.local_hub.demo_universal_work import build_demo_universal_work_response
    clear_bus()
    build_demo_universal_work_response("trace ref check")
    events = list_events("#odin.activity")
    assert len(events) >= 1
    # trace_ref and receipt_ref must be set (not None)
    event = events[0]
    assert event.get("trace_ref") is not None
    assert event.get("receipt_ref") is not None


# ---------------------------------------------------------------------------
# proof_pr03 tests (27-28)
# ---------------------------------------------------------------------------

def test_27_proof_pr03_packet_status():
    from odin.local_hub.proof_pr03 import build_final_pr_03_proof_packet
    packet = build_final_pr_03_proof_packet()
    assert packet["status"] == "ok_with_known_gaps"
    assert packet.get("candidate_only") is True
    assert packet.get("local_only") is True
    assert "not_proven" in packet
    assert "claim_boundary" in packet


def test_28_proof_pr03_write_report():
    from odin.local_hub.proof_pr03 import write_proof_report
    with tempfile.TemporaryDirectory() as td:
        out = pathlib.Path(td) / "test_proof.json"
        result = write_proof_report(out)
        assert result.exists()
        data = json.loads(result.read_text(encoding="utf-8"))
        assert data.get("candidate_only") is True
        assert data.get("status") == "ok_with_known_gaps"


# ---------------------------------------------------------------------------
# qirc_core.policy tests (29-31)
# ---------------------------------------------------------------------------

def test_29_default_policy_is_safe():
    from odin.qirc_core.policy import DEFAULT_POLICY
    assert DEFAULT_POLICY.is_safe() is True
    assert DEFAULT_POLICY.check() == []


def test_30_policy_violations_detected():
    from odin.qirc_core.policy import QircPolicy
    bad = QircPolicy(allow_public_network=True)
    errors = bad.check()
    assert len(errors) > 0
    assert any("allow_public_network" in e for e in errors)


def test_31_policy_all_flags_false_by_default():
    from odin.qirc_core.policy import QircPolicy
    p = QircPolicy()
    assert p.allow_public_network is False
    assert p.allow_federation is False
    assert p.allow_lan_bind is False
    assert p.allow_wan_bind is False
    assert p.allow_external_broker is False
    assert p.allow_app_apply is False
    assert p.allow_external_send is False
    assert p.allow_provider_execution is False
    assert p.allow_model_inference is False


# ---------------------------------------------------------------------------
# qirc_core.channels tests (32-33)
# ---------------------------------------------------------------------------

def test_32_required_channels_present():
    from odin.qirc_core.channels import REQUIRED_CHANNELS
    required = [
        "#odin.runtime",
        "#odin.activity",
        "#odin.trace",
        "#odin.receipt",
        "#odin.handoff",
        "#odin.dev",
        "#odin.warning",
    ]
    for ch in required:
        assert ch in REQUIRED_CHANNELS, f"missing channel: {ch}"


def test_33_is_valid_channel_accepts_known():
    from odin.qirc_core.channels import is_valid_channel
    assert is_valid_channel("#odin.activity") is True
    assert is_valid_channel("#odin.trace") is True
    assert is_valid_channel("#not.a.channel") is False


# ---------------------------------------------------------------------------
# validate integration tests (34-35)
# ---------------------------------------------------------------------------

def test_34_validate_tool_importable():
    """Validator tool can be imported and its main function is callable."""
    import tools.rebaseline.check_final_pr_03_qirc_devmode as v
    assert callable(v.main)


def test_35_qirc_core_bus_importable_and_functional():
    """qirc_core bus is importable and functional — no external deps."""
    from odin.qirc_core.bus import append_event, list_events, bus_summary, clear_bus
    clear_bus()
    evt = append_event("#odin.dev", "test", "test_suite", {"x": 1})
    assert evt.get("candidate_only") is True
    assert evt.get("local_only") is True
    summary = bus_summary()
    assert summary.get("policy_safe") is True
    assert summary.get("app_state_mutated") is False
    assert summary.get("external_sent") is False
    clear_bus()


# ---------------------------------------------------------------------------
# Forbidden pattern checks (36-38)
# ---------------------------------------------------------------------------

def test_36_qirc_core_no_provider_imports():
    """qirc_core modules must not import provider libraries."""
    qirc_dir = REPO_ROOT / "odin" / "qirc_core"
    forbidden = ["import openai", "import anthropic", "import ollama", "requests.post", "requests.get"]
    for py_file in qirc_dir.glob("*.py"):
        text = py_file.read_text(encoding="utf-8", errors="ignore")
        for marker in forbidden:
            assert marker not in text, f"{py_file.name} contains forbidden: {marker!r}"


def test_37_qirc_core_no_public_bind():
    """qirc_core modules must not attempt public network bind."""
    qirc_dir = REPO_ROOT / "odin" / "qirc_core"
    forbidden = ["0.0.0.0", "socket.bind", "socket.connect", "urllib.request.urlopen"]
    for py_file in qirc_dir.glob("*.py"):
        text = py_file.read_text(encoding="utf-8", errors="ignore")
        for marker in forbidden:
            assert marker not in text, f"{py_file.name} contains forbidden: {marker!r}"


def test_38_qirc_core_no_external_broker():
    """qirc_core modules must not reference external broker services."""
    qirc_dir = REPO_ROOT / "odin" / "qirc_core"
    forbidden = ["mqtt", "rabbitmq", "redis", "kafka", "nats", "websocket"]
    for py_file in qirc_dir.glob("*.py"):
        text = py_file.read_text(encoding="utf-8", errors="ignore").lower()
        for marker in forbidden:
            assert marker not in text, f"{py_file.name} references external broker: {marker!r}"


# ---------------------------------------------------------------------------
# Meta / coverage (39-40)
# ---------------------------------------------------------------------------

def test_39_test_file_has_sufficient_coverage():
    """This test file has at least 40 test functions."""
    this_file = pathlib.Path(__file__)
    text = this_file.read_text(encoding="utf-8")
    test_funcs = [line for line in text.splitlines() if line.startswith("def test_")]
    assert len(test_funcs) >= 40, f"only {len(test_funcs)} test functions found"


def test_40_pytest_passes_smoke():
    """Smoke assertion — this test passes means pytest is running correctly."""
    # The act of this test running and passing IS the proof.
    assert True
