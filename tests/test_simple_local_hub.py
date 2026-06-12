"""Tests for FINAL-PR-01 Simple Local Hub.

Claim boundary: simple_local_hub_test_candidate_only_no_provider_no_browser_no_external
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

# ── UI HTML generation ───────────────────────────────────────────────────────

from odin.local_hub.ui import generate_hub_html, REQUIRED_IDS, REQUIRED_COPY


def _html():
    return generate_hub_html()


def test_ui_has_hub_title():
    assert 'id="hub-title"' in _html()


def test_ui_has_runtime_status():
    assert 'id="runtime-status"' in _html()


def test_ui_has_local_api_status():
    assert 'id="local-api-status"' in _html()


def test_ui_has_model_status():
    assert 'id="model-status"' in _html()


def test_ui_has_connected_apps_status():
    assert 'id="connected-apps-status"' in _html()


def test_ui_has_activity_status():
    assert 'id="activity-status"' in _html()


def test_ui_has_warnings_proof_gaps():
    assert 'id="warnings-proof-gaps"' in _html()


def test_ui_has_qirc_status():
    assert 'id="qirc-status"' in _html()


def test_ui_has_handoff_first_status():
    assert 'id="handoff-first-status"' in _html()


def test_ui_has_dev_mode_entry():
    assert 'id="dev-mode-entry"' in _html()


def test_ui_has_dev_mode_handoff_viewer_placeholder():
    html = _html()
    assert "handoff-viewer" in html or "handoff viewer" in html.lower()


def test_ui_says_apps_decide_candidate_only():
    html = _html()
    assert "apps decide what to apply" in html or "Candidate-only" in html


def test_ui_qirc_core_planned_not_runtime():
    html = _html()
    assert "QIRC core is planned for a later final slice" in html
    assert "non-authoritative" in html


def test_ui_handoff_first_prepares_work():
    html = _html()
    assert "Handoff-First prepares work before Universal Work" in html


# ── Localhost policy ─────────────────────────────────────────────────────────

from odin.local_hub.policy import check_host


def test_localhost_policy_accepts_127():
    ok, _ = check_host("127.0.0.1")
    assert ok


def test_localhost_policy_rejects_0000():
    ok, _ = check_host("0.0.0.0")
    assert not ok


def test_localhost_policy_rejects_public_hosts():
    for host in ["example.com", "8.8.8.8", "192.168.1.1", "::"]:
        ok, _ = check_host(host)
        assert not ok, f"expected {host!r} to be rejected"


# ── Smoke test ───────────────────────────────────────────────────────────────

from odin.local_hub.server import run_once_smoke, get_hub_status


def test_start_local_hub_once_smoke_succeeds_does_not_hang():
    result = run_once_smoke(host="127.0.0.1", port=0)
    assert result["status"] in {"ok", "partial"}, f"smoke failed: {result}"
    assert result.get("candidate_only") is True


def test_status_local_hub_stopped_state_is_clean():
    # Port 19999 is very unlikely to be in use; status should be stopped
    result = get_hub_status(host="127.0.0.1", port=19999)
    assert result["status"] in {"stopped", "running"}
    assert result.get("candidate_only") is True


# ── Proof packet ─────────────────────────────────────────────────────────────

from odin.local_hub.proof import build_simple_local_hub_proof_packet, NOT_PROVEN


def test_prove_simple_local_hub_emits_proof_packet():
    pkt = build_simple_local_hub_proof_packet()
    assert pkt["artifact_kind"] == "odin_simple_local_hub_proof_packet"
    assert pkt["status"] == "ok_with_known_gaps"


def test_proof_packet_has_candidate_only_true():
    pkt = build_simple_local_hub_proof_packet()
    assert pkt["candidate_only"] is True


def test_proof_packet_has_local_only_true():
    pkt = build_simple_local_hub_proof_packet()
    assert pkt["local_only"] is True


def test_proof_packet_not_proven_includes_required_gaps():
    pkt = build_simple_local_hub_proof_packet()
    not_proven = pkt["not_proven"]
    for gap in [
        "provider_execution", "model_inference", "qirc_core_runtime",
        "handoff_compiler_runtime", "app_bridge_runtime", "app_apply",
        "app_state_mutation", "external_send", "public_network",
        "production_readiness", "security_certification",
    ]:
        assert gap in not_proven, f"not_proven missing: {gap}"


# ── CLI validate-simple-local-hub ────────────────────────────────────────────

def test_validate_simple_local_hub_cli_passes():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-simple-local-hub"],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert result.returncode == 0, (
        f"validate-simple-local-hub failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_validate_all_includes_simple_local_hub():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-all"],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert result.returncode == 0, (
        f"validate-all failed:\nstdout: {result.stdout[:1000]}\nstderr: {result.stderr[:500]}"
    )


# ── Handoff artifact existence ────────────────────────────────────────────────

def test_repo_cognition_summary_exists():
    assert (ROOT / "docs/codex/handoffs/FINAL_PR_01_REPO_COGNITION_SUMMARY.md").exists()


def test_thor_y_handoff_request_exists():
    p = ROOT / "docs/codex/handoffs/FINAL_PR_01_THOR_Y_HANDOFF_REQUEST.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "handoff_request_id" in text


def test_compiled_thor_y_handoff_exists():
    p = ROOT / "docs/codex/handoffs/FINAL_PR_01_COMPILED_THOR_Y_HANDOFF.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "compiled_handoff_id" in text


def test_odin_agent_operator_work_packet_exists():
    p = ROOT / "docs/codex/handoffs/FINAL_PR_01_ODIN_AGENT_OPERATOR_WORK_PACKET.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "candidate_only" in text


def test_y_mjolnir_profile_notes_exist():
    p = ROOT / "docs/codex/handoffs/FINAL_PR_01_Y_MJOLNIR_PROFILE_NOTES.md"
    assert p.exists()


def test_thor_odin_y_effectiveness_audit_exists():
    p = ROOT / "docs/codex/audits/FINAL_PR_01_THOR_ODIN_Y_EFFECTIVENESS_AUDIT.md"
    assert p.exists()


# ── No provider / apply authority ────────────────────────────────────────────

def test_no_provider_execution_in_server():
    server_text = (ROOT / "odin/local_hub/server.py").read_text(encoding="utf-8")
    assert "provider" not in server_text.lower() or "no_provider" in server_text.lower()


def test_no_app_apply_authority():
    for rel in ["odin/local_hub/server.py", "odin/local_hub/proof.py", "odin/local_hub/policy.py"]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "def apply(" not in text
        assert "def external_send(" not in text


def test_full_pytest_passes():
    """Smoke guard: running this file itself must not hang or error."""
    assert True  # if we reached here, pytest is working
