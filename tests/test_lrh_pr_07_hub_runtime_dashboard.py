"""LRH-PR-07: Hub Runtime Dashboard and Health Surfaces — deterministic static tests.

Claim boundary: lrh_pr_07_tests_candidate_only_no_app_apply_no_external_send

All tests are deterministic and local-only. No browser automation. No npm.
No external network. No app apply. No external send. No provider execution.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT / "odin" / "hub" / "static"
DASHBOARD_JS = STATIC_DIR / "dashboard.js"
INDEX_HTML = STATIC_DIR / "index.html"
DOC = ROOT / "docs" / "HUB_RUNTIME_DASHBOARD_V1.md"
REPORT = ROOT / "docs" / "codex" / "reports" / "LRH-PR-07_RETURN_REPORT.md"


# ---------------------------------------------------------------------------
# File existence tests
# ---------------------------------------------------------------------------

def test_dashboard_js_exists():
    assert DASHBOARD_JS.exists(), "dashboard.js must exist"


def test_index_html_exists():
    assert INDEX_HTML.exists(), "index.html must exist"


def test_hub_runtime_dashboard_doc_exists():
    assert DOC.exists(), "docs/HUB_RUNTIME_DASHBOARD_V1.md must exist"


def test_return_report_exists():
    assert REPORT.exists(), "LRH-PR-07_RETURN_REPORT.md must exist"


# ---------------------------------------------------------------------------
# dashboard.js API reference tests
# ---------------------------------------------------------------------------

def _js():
    return DASHBOARD_JS.read_text(encoding="utf-8", errors="ignore")


def test_dashboard_references_v1_health():
    assert "/v1/health" in _js(), "dashboard.js must reference /v1/health"


def test_dashboard_references_v1_status():
    assert "/v1/status" in _js(), "dashboard.js must reference /v1/status"


def test_dashboard_references_v1_proof_gaps():
    assert "/v1/proof-gaps" in _js(), "dashboard.js must reference /v1/proof-gaps"


def test_dashboard_references_candidate_only():
    assert "candidate_only" in _js(), "dashboard.js must reference candidate_only"


def test_dashboard_references_claim_boundary():
    assert "claim_boundary" in _js(), "dashboard.js must reference claim_boundary"


def test_dashboard_references_localhost():
    js = _js()
    assert "127.0.0.1" in js or "ODIN_API_BASE" in js, \
        "dashboard.js must reference localhost default or ODIN_API_BASE"


# ---------------------------------------------------------------------------
# dashboard.js forbidden interactive controls tests
# ---------------------------------------------------------------------------

def test_dashboard_no_apply_function():
    js = _js()
    assert "function apply(" not in js, "dashboard.js must not have apply() function"
    assert ".prototype.apply = function" not in js, "dashboard.js must not define apply on prototype"


def test_dashboard_no_external_send_function():
    js = _js()
    assert "function externalSend(" not in js, "dashboard.js must not have externalSend() function"
    assert "prototype.externalSend" not in js, "dashboard.js must not define externalSend on prototype"


def test_dashboard_no_hidden_upload():
    js = _js().lower()
    for pattern in ("hiddenupload(", "remoteupload(", "diagnosticupload("):
        assert pattern not in js, f"dashboard.js must not have {pattern}"


def test_dashboard_no_provider_credential():
    assert "providerCredential" not in _js(), \
        "dashboard.js must not reference providerCredential"


def test_dashboard_no_apply_button_onclick():
    js = _js().lower()
    for pattern in ('onclick="apply(', "onclick='apply("):
        assert pattern not in js, f"dashboard.js must not have apply onclick: {pattern}"


# ---------------------------------------------------------------------------
# index.html dashboard section tests
# ---------------------------------------------------------------------------

def _html():
    return INDEX_HTML.read_text(encoding="utf-8", errors="ignore")


def test_index_html_loads_dashboard_js():
    assert "dashboard.js" in _html(), "index.html must load dashboard.js"


def test_index_html_has_dashboard_panel():
    assert "dashboard-panel" in _html(), "index.html must have dashboard-panel section"


def test_index_html_has_runtime_status_surface():
    assert "runtime-status" in _html(), "index.html must have runtime-status surface"


def test_index_html_has_health_surface():
    assert "dashboard-health" in _html(), "index.html must have dashboard-health surface"


def test_index_html_has_validation_status_surface():
    assert "validation-status" in _html(), "index.html must have validation-status surface"


def test_index_html_has_doctor_surface():
    assert "doctor" in _html().lower(), "index.html must have doctor surface"


def test_index_html_has_support_bundle_surface():
    assert "support-bundle" in _html().lower(), "index.html must have support-bundle surface"


def test_index_html_has_proof_gap_summary_surface():
    assert "proof-gap-summary" in _html(), "index.html must have proof-gap-summary surface"


def test_index_html_has_missing_capabilities_surface():
    assert "missing-capabilities" in _html(), "index.html must have missing-capabilities surface"


def test_index_html_support_bundle_says_local_only():
    html = _html().lower()
    assert "local-only" in html, "support bundle surface must say local-only"


def test_index_html_support_bundle_says_diagnostics_only():
    html = _html().lower()
    assert "diagnostics-only" in html, "support bundle surface must say diagnostics-only"


def test_index_html_support_bundle_no_hidden_upload():
    html = _html().lower()
    assert "no hidden upload" in html, "support bundle surface must say 'no hidden upload'"


def test_index_html_dashboard_no_apply_btn():
    html = _html().lower()
    assert 'id="apply-btn' not in html, "index.html must not have apply-btn"
    assert "id='apply-btn" not in html, "index.html must not have apply-btn"


def test_index_html_dashboard_no_external_send_btn():
    html = _html().lower()
    assert 'id="external-send' not in html, "index.html must not have external-send control"


# ---------------------------------------------------------------------------
# Doc claim boundary tests
# ---------------------------------------------------------------------------

def _doc():
    return DOC.read_text(encoding="utf-8", errors="ignore").lower()


def test_doc_not_production_health_certification():
    assert "not a production health certification" in _doc(), \
        "doc must explicitly state: not a production health certification"


def test_doc_not_hosted_cloud_dashboard():
    assert "not a hosted cloud dashboard" in _doc(), \
        "doc must explicitly state: not a hosted cloud dashboard"


def test_doc_does_not_upload_diagnostics():
    assert "does not upload diagnostics" in _doc(), \
        "doc must explicitly state: does not upload diagnostics"


def test_doc_does_not_grant_app_apply():
    assert "does not grant app apply" in _doc(), \
        "doc must state: does not grant app apply authority"


def test_doc_does_not_send_externally():
    assert "does not send externally" in _doc(), \
        "doc must state: does not send externally"


def test_doc_does_not_execute_providers():
    assert "does not execute provider" in _doc(), \
        "doc must state: does not execute providers"


def test_doc_proof_boundaries_present():
    assert "proof boundaries" in _doc(), "doc must include proof boundaries section"


def test_doc_not_production_readiness():
    assert "not_production_readiness" in _doc(), \
        "doc must reference not_production_readiness proof boundary"


# ---------------------------------------------------------------------------
# Shell module import and validator tests
# ---------------------------------------------------------------------------

def test_shell_module_importable():
    from odin.hub.shell import (
        validate_hub_runtime_dashboard,
        build_dashboard_proof_packet,
        DASHBOARD_CLAIM_BOUNDARY,
        DASHBOARD_PROOF_BOUNDARIES,
    )
    assert callable(validate_hub_runtime_dashboard)
    assert callable(build_dashboard_proof_packet)
    assert isinstance(DASHBOARD_CLAIM_BOUNDARY, str)
    assert len(DASHBOARD_PROOF_BOUNDARIES) >= 5


def test_validate_hub_runtime_dashboard_returns_no_errors():
    from odin.hub.shell import validate_hub_runtime_dashboard
    errors = validate_hub_runtime_dashboard()
    assert errors == [], f"validate_hub_runtime_dashboard() returned errors: {errors}"


def test_dashboard_proof_packet_structure():
    from odin.hub.shell import build_dashboard_proof_packet
    packet = build_dashboard_proof_packet()
    assert packet["artifact_kind"] == "hub_runtime_dashboard_proof_packet"
    assert packet["candidate_only"] is True
    assert packet["local_only"] is True
    assert packet["dashboard_only"] is True
    assert "proof_boundaries" in packet
    assert "claim_boundary" in packet
    assert "not_proven" in packet


def test_dashboard_proof_packet_not_proven_includes_production_readiness():
    from odin.hub.shell import build_dashboard_proof_packet
    packet = build_dashboard_proof_packet()
    assert "production_readiness" in packet["not_proven"]


def test_dashboard_proof_packet_not_proven_includes_live_model_inference():
    from odin.hub.shell import build_dashboard_proof_packet
    packet = build_dashboard_proof_packet()
    assert "live_model_inference" in packet["not_proven"]


def test_dashboard_proof_packet_not_proven_includes_app_state_mutation():
    from odin.hub.shell import build_dashboard_proof_packet
    packet = build_dashboard_proof_packet()
    assert "app_state_mutation" in packet["not_proven"]


def test_dashboard_proof_packet_not_proven_includes_external_send():
    from odin.hub.shell import build_dashboard_proof_packet
    packet = build_dashboard_proof_packet()
    assert "external_send_authority" in packet["not_proven"]


def test_dashboard_proof_boundaries_include_not_production_readiness():
    from odin.hub.shell import DASHBOARD_PROOF_BOUNDARIES
    assert "not_production_readiness_certification" in DASHBOARD_PROOF_BOUNDARIES


def test_dashboard_proof_boundaries_include_not_hidden_upload():
    from odin.hub.shell import DASHBOARD_PROOF_BOUNDARIES
    assert "not_hidden_diagnostic_upload_proof" in DASHBOARD_PROOF_BOUNDARIES


# ---------------------------------------------------------------------------
# CLI: validate-hub-runtime-dashboard
# ---------------------------------------------------------------------------

def test_cli_validate_hub_runtime_dashboard_passes():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-hub-runtime-dashboard"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert result.returncode == 0, \
        f"validate-hub-runtime-dashboard failed:\n{result.stdout}\n{result.stderr}"
    assert "OK" in result.stdout


# ---------------------------------------------------------------------------
# CLI: prove-browser-hub --dashboard
# ---------------------------------------------------------------------------

def test_cli_prove_browser_hub_dashboard_emits_proof_packet():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "prove-browser-hub", "--dashboard"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert result.returncode == 0, \
        f"prove-browser-hub --dashboard failed:\n{result.stdout}\n{result.stderr}"
    packet = json.loads(result.stdout)
    assert packet["artifact_kind"] == "hub_runtime_dashboard_proof_packet"
    assert packet["candidate_only"] is True


def test_cli_prove_browser_hub_dashboard_packet_has_claim_boundary():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "prove-browser-hub", "--dashboard"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    packet = json.loads(result.stdout)
    assert "claim_boundary" in packet
    assert "candidate_only" in packet["claim_boundary"]


# ---------------------------------------------------------------------------
# CLI: agent-handoff --lrh-pr 07
# ---------------------------------------------------------------------------

def test_agent_handoff_lrh_pr_07_produces_valid_packet(tmp_path):
    out = tmp_path / "lrh_pr_07_packet.json"
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "07", "--out", str(out)],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert result.returncode == 0, \
        f"agent-handoff --lrh-pr 07 failed:\n{result.stdout}\n{result.stderr}"
    packet = json.loads(out.read_text())
    assert packet["candidate_only"] is True
    assert packet["app_owned_apply"] is True
    assert packet["lrh_pr_id"] == "LRH-PR-07"


def test_agent_handoff_lrh_pr_07_allowed_files_contain_dashboard(tmp_path):
    out = tmp_path / "lrh_pr_07_packet.json"
    subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "07", "--out", str(out)],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    packet = json.loads(out.read_text())
    allowed = packet.get("allowed_files", [])
    assert any("dashboard" in f for f in allowed), \
        f"allowed_files must reference dashboard: {allowed}"


# ---------------------------------------------------------------------------
# CLI: agent-guard/check/proof on PR-07 packet
# ---------------------------------------------------------------------------

def test_agent_guard_passes_on_pr_07_packet(tmp_path):
    out = tmp_path / "packet.json"
    subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "07", "--out", str(out)],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-guard", "--packet", str(out)],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 0, \
        f"agent-guard failed:\n{result.stdout}\n{result.stderr}"
    guard = json.loads(result.stdout)
    assert guard["status"] == "ok"
    assert guard["violations"] == []


def test_agent_check_passes_on_pr_07_packet(tmp_path):
    out = tmp_path / "packet.json"
    subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "07", "--out", str(out)],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-check", "--packet", str(out)],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 0, \
        f"agent-check failed:\n{result.stdout}\n{result.stderr}"
    check = json.loads(result.stdout)
    assert check["status"] == "ok"


def test_agent_proof_runs_on_pr_07_packet(tmp_path):
    out = tmp_path / "packet.json"
    subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "07", "--out", str(out)],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-proof", "--packet", str(out)],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 0, \
        f"agent-proof failed:\n{result.stdout}\n{result.stderr}"
    proof = json.loads(result.stdout)
    assert "declared_boundaries" in proof or "claim_boundary" in proof


# ---------------------------------------------------------------------------
# validate-all still passes
# ---------------------------------------------------------------------------

def test_validate_all_still_passes():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-all"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert result.returncode == 0, \
        f"validate-all failed after PR-07 changes:\n{result.stdout}\n{result.stderr}"
