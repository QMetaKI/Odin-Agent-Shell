"""Tests for LRH-PR-11: Universal Work Playground.

Claim boundary: test_lrh_pr_11_candidate_only_no_app_apply_no_external_send_no_shell_no_provider
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT / "odin" / "hub" / "static"
UWP_JS = STATIC_DIR / "universal_work_playground.js"
INDEX_HTML = STATIC_DIR / "index.html"
DOC_MD = ROOT / "docs" / "UNIVERSAL_WORK_PLAYGROUND_V1.md"
EXAMPLES_DIR = ROOT / "examples" / "universal_work_playground"
WORK_PACKET_FIXTURE = EXAMPLES_DIR / "safe_demo_work_packet.valid.json"
CANDIDATE_FIXTURE = EXAMPLES_DIR / "safe_demo_candidate_result.valid.json"


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

def test_universal_work_playground_js_exists():
    assert UWP_JS.exists(), "universal_work_playground.js must exist"


def test_index_html_loads_universal_work_playground_js():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert "universal_work_playground.js" in html, "index.html must load universal_work_playground.js"


def test_universal_work_playground_doc_exists():
    assert DOC_MD.exists(), "docs/UNIVERSAL_WORK_PLAYGROUND_V1.md must exist"


def test_universal_work_playground_test_file_exists():
    assert (ROOT / "tests" / "test_lrh_pr_11_universal_work_playground.py").exists()


def test_safe_demo_work_packet_fixture_exists():
    assert WORK_PACKET_FIXTURE.exists(), "safe_demo_work_packet.valid.json must exist"


def test_safe_demo_candidate_result_fixture_exists():
    assert CANDIDATE_FIXTURE.exists(), "safe_demo_candidate_result.valid.json must exist"


# ---------------------------------------------------------------------------
# JS API references
# ---------------------------------------------------------------------------

def test_viewer_references_v1_universal_work():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "/v1/universal-work" in js, "universal_work_playground.js must reference /v1/universal-work"


def test_viewer_references_v1_proof_gaps():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "/v1/proof-gaps" in js, "universal_work_playground.js must reference /v1/proof-gaps"


# ---------------------------------------------------------------------------
# Required boundary tokens in JS
# ---------------------------------------------------------------------------

def test_viewer_has_candidate_only_token():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "candidate_only" in js


def test_viewer_has_claim_boundary_token():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "claim_boundary" in js


def test_viewer_has_local_only_token():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "local_only" in js


def test_viewer_has_read_only_token():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "read_only" in js


def test_viewer_has_no_app_apply_token():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "no_app_apply" in js


def test_viewer_has_no_external_send_token():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "no_external_send" in js


def test_viewer_has_no_arbitrary_shell_execution_token():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "no_arbitrary_shell_execution" in js


def test_viewer_has_no_provider_execution_token():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "no_provider_execution" in js


def test_viewer_has_no_credentials_token():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "no_credentials" in js


def test_viewer_has_safe_demo_only_token():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "safe_demo_only" in js


def test_viewer_has_playground_only_token():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "playground_only" in js


def test_viewer_has_not_applied_truth_token():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "not_applied_truth" in js


def test_viewer_has_proof_boundaries_token():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "proof_boundaries" in js


def test_viewer_has_known_non_proofs_token():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "known_non_proofs" in js


def test_viewer_has_metadata_first_token():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "metadata_first" in js


def test_viewer_has_provider_as_worker_token():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "provider_as_worker_not_authority" in js


def test_viewer_has_disabled_by_default_token():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "disabled_by_default" in js


def test_viewer_has_localhost_reference():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "127.0.0.1" in js or "ODIN_API_BASE" in js, \
        "universal_work_playground.js must reference localhost or ODIN_API_BASE"


# ---------------------------------------------------------------------------
# Index.html surfaces
# ---------------------------------------------------------------------------

def test_index_html_has_uwp_work_form_surface():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert "uwp-work-form-content" in html, "index.html must have uwp-work-form-content"


def test_index_html_has_uwp_candidate_result_surface():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert "uwp-candidate-result-content" in html, "index.html must have uwp-candidate-result-content"


def test_index_html_has_uwp_proof_boundary_surface():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert "uwp-proof-boundary-content" in html, "index.html must have uwp-proof-boundary-content"


def test_index_html_has_uwp_validation_status_surface():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert "uwp-validation-status-content" in html, "index.html must have uwp-validation-status-content"


def test_index_html_has_uwp_provider_worker_context_surface():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert "uwp-provider-worker-context-content" in html, \
        "index.html must have uwp-provider-worker-context-content"


# ---------------------------------------------------------------------------
# Index.html boundary phrases
# ---------------------------------------------------------------------------

def test_index_html_has_candidate_only_phrase():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "candidate-only" in html or "candidate_only" in html


def test_index_html_has_not_applied_truth_phrase():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "not applied truth" in html or "not-applied-truth" in html


def test_index_html_has_no_app_apply_phrase():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "no app apply" in html


def test_index_html_has_no_external_send_phrase():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "no external send" in html


def test_index_html_has_no_shell_execution_phrase():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "no arbitrary shell execution" in html


def test_index_html_has_no_provider_execution_phrase():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "no provider execution" in html


def test_index_html_has_no_credentials_phrase():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "no credentials by default" in html


def test_index_html_has_safe_demo_only_phrase():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "safe demo only" in html or "safe-demo-only" in html


def test_index_html_has_candidate_result_not_applied_truth_phrase():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "candidate result is not applied truth" in html


# ---------------------------------------------------------------------------
# No forbidden interactive controls in JS
# ---------------------------------------------------------------------------

def test_viewer_has_no_app_apply_function():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "function applyCandidate(" not in js
    assert "function apply(" not in js


def test_viewer_has_no_external_send_function():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "function externalSend(" not in js
    assert "function sendExternally(" not in js


def test_viewer_has_no_shell_execution_function():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "function runShell(" not in js
    assert "function executeShell(" not in js
    assert "function runCommand(" not in js
    assert "function executeCommand(" not in js
    assert "function runScript(" not in js
    assert "function executeScript(" not in js


def test_viewer_has_no_provider_execution_function():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "function runProvider(" not in js
    assert "function executeProvider(" not in js
    assert "function callModel(" not in js
    assert "function runModel(" not in js
    assert "function testInference(" not in js


def test_viewer_has_no_credential_function():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "function saveCredential(" not in js
    assert "function setApiKey(" not in js


def test_viewer_has_no_apply_btn_id():
    js = UWP_JS.read_text(encoding="utf-8")
    assert 'id="apply-btn' not in js


def test_viewer_has_no_external_send_id():
    js = UWP_JS.read_text(encoding="utf-8")
    assert 'id="external-send' not in js


def test_viewer_has_no_provider_credential_bare_string():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "providerCredential" not in js


def test_viewer_has_no_api_key_bare_string():
    js = UWP_JS.read_text(encoding="utf-8")
    assert "apiKey" not in js


# ---------------------------------------------------------------------------
# No forbidden interactive controls in index.html
# ---------------------------------------------------------------------------

def test_index_html_has_no_apply_btn():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert 'id="apply-btn' not in html


def test_index_html_has_no_external_send_btn():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert 'id="external-send' not in html


def test_index_html_has_no_shell_command_field():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert 'name="shell_command"' not in html
    assert 'name="command"' not in html
    assert 'name="script"' not in html
    assert 'name="exec"' not in html


def test_index_html_has_no_credential_fields():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert 'name="provider_credential"' not in html
    assert 'name="api_key"' not in html
    assert 'name="token"' not in html
    assert 'name="secret"' not in html
    assert 'type="password"' not in html


def test_index_html_has_no_remote_url_fields():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert 'name="remote_url"' not in html
    assert 'name="callback_url"' not in html
    assert 'name="webhook_url"' not in html


# ---------------------------------------------------------------------------
# Safe demo work packet fixture validation
# ---------------------------------------------------------------------------

def test_safe_demo_work_packet_is_valid_json():
    data = json.loads(WORK_PACKET_FIXTURE.read_text(encoding="utf-8"))
    assert isinstance(data, dict)


def test_safe_demo_work_packet_has_candidate_only_true():
    data = json.loads(WORK_PACKET_FIXTURE.read_text(encoding="utf-8"))
    assert data.get("candidate_only") is True


def test_safe_demo_work_packet_has_local_only_true():
    data = json.loads(WORK_PACKET_FIXTURE.read_text(encoding="utf-8"))
    assert data.get("local_only") is True


def test_safe_demo_work_packet_has_app_apply_false():
    data = json.loads(WORK_PACKET_FIXTURE.read_text(encoding="utf-8"))
    assert data.get("app_apply") is False


def test_safe_demo_work_packet_has_external_send_false():
    data = json.loads(WORK_PACKET_FIXTURE.read_text(encoding="utf-8"))
    assert data.get("external_send") is False


def test_safe_demo_work_packet_has_arbitrary_shell_execution_false():
    data = json.loads(WORK_PACKET_FIXTURE.read_text(encoding="utf-8"))
    assert data.get("arbitrary_shell_execution") is False


def test_safe_demo_work_packet_has_provider_execution_false():
    data = json.loads(WORK_PACKET_FIXTURE.read_text(encoding="utf-8"))
    assert data.get("provider_execution") is False


def test_safe_demo_work_packet_has_credential_required_false():
    data = json.loads(WORK_PACKET_FIXTURE.read_text(encoding="utf-8"))
    assert data.get("credential_required") is False


def test_safe_demo_work_packet_has_claim_boundary():
    data = json.loads(WORK_PACKET_FIXTURE.read_text(encoding="utf-8"))
    assert "claim_boundary" in data and data["claim_boundary"]


def test_safe_demo_work_packet_has_proof_boundaries():
    data = json.loads(WORK_PACKET_FIXTURE.read_text(encoding="utf-8"))
    assert "proof_boundaries" in data
    assert isinstance(data["proof_boundaries"], list)
    assert len(data["proof_boundaries"]) > 0


def test_safe_demo_work_packet_has_known_non_proofs():
    data = json.loads(WORK_PACKET_FIXTURE.read_text(encoding="utf-8"))
    assert "known_non_proofs" in data
    assert isinstance(data["known_non_proofs"], list)
    assert len(data["known_non_proofs"]) > 0


def test_safe_demo_work_packet_has_no_shell_fields():
    text = WORK_PACKET_FIXTURE.read_text(encoding="utf-8").lower()
    assert "shell_command" not in text
    assert '"secret"' not in text
    assert '"token"' not in text
    assert '"password"' not in text
    assert "webhook" not in text


# ---------------------------------------------------------------------------
# Safe demo candidate result fixture validation
# ---------------------------------------------------------------------------

def test_safe_demo_candidate_result_is_valid_json():
    data = json.loads(CANDIDATE_FIXTURE.read_text(encoding="utf-8"))
    assert isinstance(data, dict)


def test_safe_demo_candidate_result_has_candidate_only_true():
    data = json.loads(CANDIDATE_FIXTURE.read_text(encoding="utf-8"))
    assert data.get("candidate_only") is True


def test_safe_demo_candidate_result_has_applied_truth_false():
    data = json.loads(CANDIDATE_FIXTURE.read_text(encoding="utf-8"))
    assert data.get("applied_truth") is False


def test_safe_demo_candidate_result_has_app_state_mutated_false():
    data = json.loads(CANDIDATE_FIXTURE.read_text(encoding="utf-8"))
    assert data.get("app_state_mutated") is False


def test_safe_demo_candidate_result_has_external_send_false():
    data = json.loads(CANDIDATE_FIXTURE.read_text(encoding="utf-8"))
    assert data.get("external_send") is False


def test_safe_demo_candidate_result_has_claim_boundary():
    data = json.loads(CANDIDATE_FIXTURE.read_text(encoding="utf-8"))
    assert "claim_boundary" in data and data["claim_boundary"]


def test_safe_demo_candidate_result_has_proof_boundaries():
    data = json.loads(CANDIDATE_FIXTURE.read_text(encoding="utf-8"))
    assert "proof_boundaries" in data
    assert isinstance(data["proof_boundaries"], list)
    assert "candidate_result_not_applied_truth" in data["proof_boundaries"]


# ---------------------------------------------------------------------------
# Docs claim boundaries
# ---------------------------------------------------------------------------

def test_doc_contains_no_app_apply_claim():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "this does not apply candidate artifacts" in doc


def test_doc_contains_no_external_send_claim():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "this does not send externally" in doc


def test_doc_contains_no_shell_execution_claim():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "this does not execute arbitrary shell commands" in doc


def test_doc_contains_no_app_state_mutation_claim():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "this does not mutate app state" in doc


def test_doc_contains_proof_boundaries():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "proof boundaries" in doc
    assert "not_production_readiness_certification" in doc


def test_doc_contains_candidate_result_not_applied_truth():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "candidate result is not applied truth" in doc


# ---------------------------------------------------------------------------
# Validator integration
# ---------------------------------------------------------------------------

def test_validate_universal_work_playground_passes():
    from odin.hub.shell import validate_universal_work_playground
    errors = validate_universal_work_playground()
    assert errors == [], f"validate_universal_work_playground returned errors: {errors}"


def test_prove_browser_hub_playground_returns_packet():
    from odin.hub.shell import build_browser_hub_proof_packet
    result = build_browser_hub_proof_packet(playground=True)
    assert result.get("artifact_kind") == "hub_universal_work_playground_proof_packet"
    assert result.get("candidate_only") is True
    assert result.get("local_only") is True
    assert result.get("playground_only") is True
    assert result.get("safe_demo_only") is True
    assert result.get("status") in {"ok", "partial"}
    assert "not_proven" in result
    assert "production_readiness" in result["not_proven"]


def test_prove_browser_hub_playground_has_proof_boundaries():
    from odin.hub.shell import build_browser_hub_proof_packet
    result = build_browser_hub_proof_packet(playground=True)
    assert "proof_boundaries" in result
    assert "candidate_result_not_applied_truth" in result["proof_boundaries"]


# ---------------------------------------------------------------------------
# Agent handoff / operator mode
# ---------------------------------------------------------------------------

def test_agent_handoff_lrh_pr_11_writes_valid_packet(tmp_path):
    import subprocess
    import sys
    out = tmp_path / "packet.json"
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "11", "--out", str(out)],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"agent-handoff failed: {result.stderr}"
    assert out.exists(), "packet file was not written"
    packet = json.loads(out.read_text(encoding="utf-8"))
    assert packet.get("candidate_only") is True
    assert packet.get("app_owned_apply") is True
    assert packet.get("lrh_pr_id") == "LRH-PR-11"


def test_agent_guard_passes_on_lrh_pr_11_packet(tmp_path):
    import subprocess
    import sys
    out = tmp_path / "packet.json"
    subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "11", "--out", str(out)],
        capture_output=True, text=True
    )
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-guard", "--packet", str(out)],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"agent-guard failed: {result.stderr}"
    guard_result = json.loads(result.stdout)
    assert guard_result.get("status") == "ok"
    assert guard_result.get("violations") == []


def test_agent_check_passes_on_lrh_pr_11_packet(tmp_path):
    import subprocess
    import sys
    out = tmp_path / "packet.json"
    subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "11", "--out", str(out)],
        capture_output=True, text=True
    )
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-check", "--packet", str(out)],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"agent-check failed: {result.stderr}"
    check_result = json.loads(result.stdout)
    assert check_result.get("status") == "ok"
