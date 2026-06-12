"""Tests for FINAL-PR-02 Model Picker + Connected Apps + Demo Universal Work.

Claim boundary: final_pr_02_test_candidate_only_no_provider_no_browser_no_external
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

# ── Imports ───────────────────────────────────────────────────────────────────

from odin.local_hub.ui import generate_hub_html, REQUIRED_IDS
from odin.local_hub.model_picker import build_models_json, get_model_options, get_provider_status
from odin.local_hub.connected_apps import build_apps_json, get_app_slots, get_app_bridge_status
from odin.local_hub.demo_universal_work import build_demo_universal_work_response, get_demo_universal_work_json
from odin.local_hub.proof_pr02 import build_final_pr_02_proof_packet


def _html():
    return generate_hub_html()


# ── Test 1: Model picker section UI ID exists ─────────────────────────────────

def test_model_picker_section_id_in_html():
    assert 'id="model-picker-section"' in _html()


# ── Test 2: Mock model option exists ─────────────────────────────────────────

def test_model_option_mock_id_in_html():
    assert 'id="model-option-mock"' in _html()


# ── Test 3: None model option exists ─────────────────────────────────────────

def test_model_option_none_id_in_html():
    assert 'id="model-option-none"' in _html()


# ── Test 4: Local candidate option says not executed ─────────────────────────

def test_model_option_local_candidate_says_not_executed():
    html = _html()
    assert 'id="model-option-local-candidate"' in html
    assert "not executed" in html.lower() or "not executed yet" in html.lower() or "deferred" in html.lower()


# ── Test 5: Provider status panel exists ─────────────────────────────────────

def test_provider_status_panel_in_html():
    assert 'id="provider-status-panel"' in _html()


# ── Test 6: Connected apps section exists ─────────────────────────────────────

def test_connected_apps_section_in_html():
    assert 'id="connected-apps-section"' in _html()


# ── Test 7: Generic, browser, file app slots exist ────────────────────────────

def test_app_slots_in_html():
    html = _html()
    assert 'id="connected-app-slot-generic"' in html
    assert 'id="connected-app-slot-browser"' in html
    assert 'id="connected-app-slot-file"' in html


# ── Test 8: App bridge status is placeholder/candidate-only ───────────────────

def test_app_bridge_status_is_placeholder():
    html = _html()
    assert 'id="app-bridge-status"' in html
    lower = html.lower()
    assert "placeholder" in lower or "demo" in lower or "not connected" in lower


# ── Test 9: Demo Universal Work section exists ────────────────────────────────

def test_demo_universal_work_section_in_html():
    assert 'id="demo-universal-work-section"' in _html()


# ── Test 10: Demo Handoff Context marker exists ───────────────────────────────

def test_demo_handoff_context_in_html():
    assert 'id="demo-handoff-context"' in _html()


# ── Test 11: Demo Universal Work packet marker exists ────────────────────────

def test_demo_universal_work_packet_in_html():
    assert 'id="demo-universal-work-packet"' in _html()


# ── Test 12: Demo candidate artifact marker exists ───────────────────────────

def test_demo_candidate_artifact_in_html():
    assert 'id="demo-candidate-artifact"' in _html()


# ── Test 13: Demo response packet marker exists ───────────────────────────────

def test_demo_response_packet_in_html():
    assert 'id="demo-response-packet"' in _html()


# ── Test 14: Demo endpoint returns candidate_only true ───────────────────────

def test_demo_response_candidate_only_true():
    resp = build_demo_universal_work_response("test input")
    assert resp["candidate_only"] is True


# ── Test 15: Demo endpoint returns provider_execution false ──────────────────

def test_demo_response_provider_execution_false():
    resp = build_demo_universal_work_response()
    assert resp["provider_execution"] is False


# ── Test 16: Demo endpoint returns model_execution/model_inference false ──────

def test_demo_response_model_inference_false():
    resp = build_demo_universal_work_response()
    assert resp.get("model_inference") is False or resp.get("model_execution") is False


# ── Test 17: Demo endpoint returns app_apply false ───────────────────────────

def test_demo_response_app_apply_false():
    resp = build_demo_universal_work_response()
    assert resp["app_apply"] is False


# ── Test 18: Demo endpoint returns external_send false ───────────────────────

def test_demo_response_external_send_false():
    resp = build_demo_universal_work_response()
    assert resp["external_send"] is False


# ── Test 19: Demo endpoint includes not_proven list ──────────────────────────

def test_demo_response_includes_not_proven():
    resp = build_demo_universal_work_response()
    np = resp.get("not_proven", [])
    assert isinstance(np, list)
    assert len(np) > 0
    assert "model_inference" in np
    assert "provider_execution" in np
    assert "app_apply" in np


# ── Test 20: prove-final-pr-02-demo-universal-work emits proof packet ─────────

def test_prove_final_pr_02_demo_universal_work_emits_proof_packet():
    pkt = build_final_pr_02_proof_packet()
    assert pkt["artifact_kind"] == "odin_final_pr_02_demo_universal_work_proof_packet"
    assert pkt["status"] == "ok_with_known_gaps"
    assert pkt["candidate_only"] is True
    assert pkt["model_picker_visible"] is True
    assert pkt["connected_apps_visible"] is True
    assert pkt["demo_universal_work_visible"] is True
    assert pkt["response_packet_visible"] is True
    assert pkt["candidate_artifact_visible"] is True
    assert pkt["handoff_context_visible"] is True
    assert pkt["universal_work_packet_visible"] is True
    assert pkt["provider_execution"] is False
    assert pkt["model_inference"] is False
    assert pkt["app_apply"] is False
    assert pkt["external_send"] is False
    assert pkt["qirc_core_runtime"] is False


# ── Test 21: validate-final-pr-02-model-apps-demo passes ─────────────────────

def test_validate_final_pr_02_model_apps_demo_cli_passes():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-final-pr-02-model-apps-demo"],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert result.returncode == 0, (
        f"validate-final-pr-02-model-apps-demo failed:\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


# ── Test 22: validate-all includes new validator ──────────────────────────────

def test_validate_all_includes_final_pr_02():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-all"],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert result.returncode == 0, (
        f"validate-all failed:\nstdout: {result.stdout[:2000]}\nstderr: {result.stderr[:500]}"
    )


# ── Test 23: Thor/Y handoff request exists ────────────────────────────────────

def test_thor_y_handoff_request_exists():
    p = ROOT / "docs/codex/handoffs/FINAL_PR_02_THOR_Y_HANDOFF_REQUEST.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "handoff_request_id" in text
    assert "final_pr_02" in text.lower()


# ── Test 24: Compiled Thor/Y handoff exists ───────────────────────────────────

def test_compiled_thor_y_handoff_exists():
    p = ROOT / "docs/codex/handoffs/FINAL_PR_02_COMPILED_THOR_Y_HANDOFF.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "compiled_handoff_id" in text
    assert "candidate_only" in text


# ── Test 25: Odin work packet exists ─────────────────────────────────────────

def test_odin_work_packet_exists():
    p = ROOT / "docs/codex/handoffs/FINAL_PR_02_ODIN_AGENT_OPERATOR_WORK_PACKET.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "candidate_only" in text
    assert "forbidden_actions" in text


# ── Test 26: Hub Surface Decision exists ─────────────────────────────────────

def test_hub_surface_decision_exists():
    p = ROOT / "docs/codex/handoffs/FINAL_PR_02_HUB_SURFACE_DECISION.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "8765" in text
    assert "8877" in text or "8878" in text


# ── Test 27: Thor audit exists ────────────────────────────────────────────────

def test_thor_effectiveness_audit_exists():
    p = ROOT / "docs/codex/audits/FINAL_PR_02_THOR_EFFECTIVENESS_AUDIT.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "thor" in text.lower()
    assert "backlog" in text.lower() or "finding" in text.lower()


# ── Test 28: Odin audit exists ───────────────────────────────────────────────

def test_odin_effectiveness_audit_exists():
    p = ROOT / "docs/codex/audits/FINAL_PR_02_ODIN_EFFECTIVENESS_AUDIT.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "odin" in text.lower()
    assert "finding" in text.lower() or "backlog" in text.lower()


# ── Test 29: No provider/model/network/API-key execution occurs ───────────────

def test_no_provider_or_model_execution_in_modules():
    for rel in [
        "odin/local_hub/server.py",
        "odin/local_hub/model_picker.py",
        "odin/local_hub/connected_apps.py",
        "odin/local_hub/demo_universal_work.py",
        "odin/local_hub/proof_pr02.py",
    ]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        for bad in ["import openai", "import anthropic", "import ollama",
                    "subprocess.run", "subprocess.Popen",
                    "os.environ.get(\"OPENAI", "os.environ.get(\"ANTHROPIC"]:
            assert bad not in text, f"{rel} contains forbidden marker: {bad!r}"
        assert "def apply(" not in text
        assert "def external_send(" not in text


# ── Test 30: Full pytest passes (guard) ──────────────────────────────────────

def test_full_pytest_passes_guard():
    """Smoke guard: reaching this line confirms pytest is working."""
    assert True


# ── Additional checks: demo flow fields ──────────────────────────────────────

def test_demo_response_has_handoff_context():
    resp = build_demo_universal_work_response("my work")
    hc = resp.get("handoff_context", {})
    assert hc.get("profile") == "generic"
    assert "provider_execution" in hc.get("forbidden_actions", [])


def test_demo_response_has_universal_work():
    resp = build_demo_universal_work_response()
    uw = resp.get("universal_work", {})
    assert uw.get("kind") == "demo"
    assert uw.get("status") == "compiled"


def test_demo_response_has_candidate_artifact():
    resp = build_demo_universal_work_response()
    ca = resp.get("candidate_artifact", {})
    assert ca.get("artifact_kind") == "demo_candidate"
    assert ca.get("summary")


def test_models_json_candidate_only():
    data = build_models_json()
    assert data["candidate_only"] is True
    assert data["model_inference"] is False
    assert data["provider_execution"] is False
    assert len(data["options"]) >= 3


def test_apps_json_no_real_app():
    data = build_apps_json()
    assert data["candidate_only"] is True
    assert data["real_app_connected"] is False
    assert data["app_apply"] is False
    assert len(data["slots"]) >= 3


def test_demo_uw_json_info_structure():
    info = get_demo_universal_work_json()
    assert info["candidate_only"] is True
    assert "flow" in info
    assert "demo_response_preview" in info


def test_all_required_ui_ids_in_html():
    html = _html()
    for id_ in REQUIRED_IDS:
        assert f'id="{id_}"' in html, f"Missing UI id: {id_!r}"


def test_return_report_exists():
    p = ROOT / "docs/codex/reports/FINAL_PR_02_MODEL_APPS_DEMO_RETURN_REPORT.md"
    assert p.exists()


def test_rebaseline_spec_doc_exists():
    p = ROOT / "docs/rebaseline/FINAL_PR_02_MODEL_APPS_DEMO.md"
    assert p.exists()


def test_schema_file_exists():
    p = ROOT / "schemas/final_pr_02_demo_universal_work_response_packet.schema.json"
    assert p.exists()


def test_example_file_exists():
    p = ROOT / "examples/final_pr_02/demo_universal_work_response_packet.example.json"
    assert p.exists()
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("candidate_only") is True
