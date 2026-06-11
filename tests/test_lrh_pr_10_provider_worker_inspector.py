"""Tests for LRH-PR-10: Provider / Worker / Pre-LLM Inspector.

Claim boundary: test_lrh_pr_10_candidate_only_no_provider_execution_no_credentials_no_live_inference
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT / "odin" / "hub" / "static"
PWI_JS = STATIC_DIR / "provider_worker_inspector.js"
INDEX_HTML = STATIC_DIR / "index.html"
DOC_MD = ROOT / "docs" / "PROVIDER_WORKER_INSPECTOR_V1.md"


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

def test_provider_worker_inspector_js_exists():
    assert PWI_JS.exists(), "provider_worker_inspector.js must exist"


def test_index_html_loads_provider_worker_inspector_js():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert "provider_worker_inspector.js" in html, "index.html must load provider_worker_inspector.js"


def test_provider_worker_inspector_doc_exists():
    assert DOC_MD.exists(), "docs/PROVIDER_WORKER_INSPECTOR_V1.md must exist"


def test_provider_worker_inspector_test_file_exists():
    assert (ROOT / "tests" / "test_lrh_pr_10_provider_worker_inspector.py").exists()


# ---------------------------------------------------------------------------
# JS API references
# ---------------------------------------------------------------------------

def test_viewer_references_v1_providers():
    js = PWI_JS.read_text(encoding="utf-8")
    assert "/v1/providers" in js, "provider_worker_inspector.js must reference /v1/providers"


def test_viewer_references_v1_status_or_proof_gaps():
    js = PWI_JS.read_text(encoding="utf-8")
    assert "/v1/status" in js or "/v1/proof-gaps" in js, \
        "provider_worker_inspector.js must reference /v1/status or /v1/proof-gaps"


def test_viewer_references_v1_proof_gaps():
    js = PWI_JS.read_text(encoding="utf-8")
    assert "/v1/proof-gaps" in js, "provider_worker_inspector.js must reference /v1/proof-gaps"


# ---------------------------------------------------------------------------
# Required boundary tokens in JS
# ---------------------------------------------------------------------------

def test_viewer_has_candidate_only_boundary_token():
    js = PWI_JS.read_text(encoding="utf-8")
    assert "candidate_only" in js


def test_viewer_has_claim_boundary_token():
    js = PWI_JS.read_text(encoding="utf-8")
    assert "claim_boundary" in js


def test_viewer_has_local_only_boundary_token():
    js = PWI_JS.read_text(encoding="utf-8")
    assert "local_only" in js


def test_viewer_has_read_only_boundary_token():
    js = PWI_JS.read_text(encoding="utf-8")
    assert "read_only" in js


def test_viewer_has_no_provider_execution_token():
    js = PWI_JS.read_text(encoding="utf-8")
    assert "no_provider_execution" in js


def test_viewer_has_no_credentials_token():
    js = PWI_JS.read_text(encoding="utf-8")
    assert "no_credentials" in js


def test_viewer_has_metadata_first_token():
    js = PWI_JS.read_text(encoding="utf-8")
    assert "metadata_first" in js


def test_viewer_has_provider_as_worker_token():
    js = PWI_JS.read_text(encoding="utf-8")
    assert "provider_as_worker" in js


# ---------------------------------------------------------------------------
# Required surface IDs in index.html
# ---------------------------------------------------------------------------

def test_index_has_provider_card_surface():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert "pwi-provider-cards-content" in html, "index.html must have pwi-provider-cards-content"


def test_index_has_worker_permission_surface():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert "pwi-worker-permission-content" in html, "index.html must have pwi-worker-permission-content"


def test_index_has_pre_llm_route_surface():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert "pwi-pre-llm-route-content" in html, "index.html must have pwi-pre-llm-route-content"


def test_index_has_model_avoidance_surface():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert "pwi-model-avoidance-content" in html, "index.html must have pwi-model-avoidance-content"


def test_index_has_redaction_status_surface():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert "pwi-redaction-status-content" in html, "index.html must have pwi-redaction-status-content"


def test_index_has_disabled_by_default_surface():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert "pwi-disabled-by-default-content" in html, "index.html must have pwi-disabled-by-default-content"


def test_index_has_proof_gaps_surface():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert "pwi-proof-gaps-content" in html, "index.html must have pwi-proof-gaps-content"


# ---------------------------------------------------------------------------
# Boundary text in index.html
# ---------------------------------------------------------------------------

def test_index_has_provider_as_worker_not_authority_text():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "provider is worker, not authority" in html, \
        "index.html must contain 'Provider is worker, not authority' boundary text"


def test_index_has_no_live_inference_without_receipt_text():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "no live inference without receipt" in html, \
        "index.html must contain 'No live inference without receipt' boundary text"


def test_index_has_no_credentials_by_default_text():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "no credentials by default" in html, \
        "index.html must contain 'No credentials by default' boundary text"


def test_index_has_disabled_by_default_text():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "disabled by default" in html, "index.html must contain 'Disabled by default' boundary text"


def test_index_has_no_provider_execution_text():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "no provider execution" in html, "index.html must contain 'No provider execution' boundary text"


def test_index_has_no_worker_mutation_text():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "no worker mutation" in html, "index.html must contain 'No worker mutation' boundary text"


def test_index_has_no_route_mutation_text():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "no route mutation" in html, "index.html must contain 'No route mutation' boundary text"


def test_index_has_redaction_status_not_safety_certification_text():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "redaction status is not safety certification" in html or "not-certification" in html, \
        "index.html must contain redaction status not-certification boundary phrase"


# ---------------------------------------------------------------------------
# Forbidden interactive controls — JS
# ---------------------------------------------------------------------------

FORBIDDEN_JS_CONTROLS = [
    "function runProvider(",
    "function executeProvider(",
    "function callModel(",
    "function runModel(",
    "function testInference(",
    "function saveCredential(",
    "function setApiKey(",
    "function enableProvider(",
    "function disableProvider(",
    "function mutateWorker(",
    "function editPermission(",
    "function changeRoute(",
    "function mutateRoute(",
    "function bypassRedaction(",
    "function rawPayloadReveal(",
    "function externalSend(",
    "function uploadDiagnostics(",
    "function hiddenUpload(",
]


@pytest.mark.parametrize("pattern", FORBIDDEN_JS_CONTROLS)
def test_viewer_has_no_forbidden_js_control(pattern):
    js = PWI_JS.read_text(encoding="utf-8").lower()
    assert pattern.lower() not in js, \
        f"provider_worker_inspector.js must not contain forbidden control: {pattern!r}"


# ---------------------------------------------------------------------------
# Forbidden credential inputs — index.html
# ---------------------------------------------------------------------------

FORBIDDEN_HTML_INPUTS = [
    'type="password"',
    'id="api-key',
    'id="provider-credential',
    "providerCredential",
]


@pytest.mark.parametrize("pattern", FORBIDDEN_HTML_INPUTS)
def test_index_has_no_credential_input(pattern):
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert pattern.lower() not in html, \
        f"index.html must not contain credential input pattern: {pattern!r}"


# ---------------------------------------------------------------------------
# Forbidden execution controls in index.html
# ---------------------------------------------------------------------------

FORBIDDEN_HTML_CONTROLS = [
    "runProvider(",
    "executeProvider(",
    "callModel(",
    "runModel(",
    "testInference(",
    "mutateRoute(",
    "changeRoute(",
    "mutateWorker(",
    "editPermission(",
    "bypassRedaction(",
    "externalSend(",
    "hiddenUpload(",
]


@pytest.mark.parametrize("pattern", FORBIDDEN_HTML_CONTROLS)
def test_index_has_no_forbidden_html_control(pattern):
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert pattern.lower() not in html, \
        f"index.html must not contain forbidden control: {pattern!r}"


# ---------------------------------------------------------------------------
# Localhost guard in JS
# ---------------------------------------------------------------------------

def test_viewer_has_localhost_guard():
    js = PWI_JS.read_text(encoding="utf-8")
    assert "127.0.0.1" in js or "ODIN_API_BASE" in js, \
        "provider_worker_inspector.js must reference localhost default"


def test_viewer_not_referencing_wan():
    js = PWI_JS.read_text(encoding="utf-8")
    assert "0.0.0.0" not in js, "provider_worker_inspector.js must not reference 0.0.0.0"


# ---------------------------------------------------------------------------
# Doc boundary phrases
# ---------------------------------------------------------------------------

def test_doc_states_does_not_execute_providers():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "this does not execute providers" in doc


def test_doc_states_does_not_call_live_models():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "this does not call live models" in doc


def test_doc_states_does_not_store_credentials():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "this does not store or request provider credentials" in doc


def test_doc_states_does_not_treat_providers_as_authority():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "this does not treat providers as authority" in doc


def test_doc_states_does_not_mutate_worker_permissions():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "this does not mutate worker permissions" in doc


def test_doc_states_does_not_mutate_routing_policy():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "this does not mutate routing policy" in doc


def test_doc_states_does_not_bypass_redaction():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "this does not bypass redaction" in doc


def test_doc_states_does_not_prove_model_quality():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "this does not prove model quality" in doc


def test_doc_states_does_not_prove_production_readiness():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "this does not prove production readiness" in doc


def test_doc_states_does_not_prove_security_certification():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "this does not prove security certification" in doc


def test_doc_has_proof_boundaries_section():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "proof boundaries" in doc


def test_doc_has_not_production_readiness_certification():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "not_production_readiness_certification" in doc


def test_doc_has_no_provider_authority_claim():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    # Doc must not claim providers are authority — it must negate it
    assert "provider is worker, not authority" in doc or "providers are not authority" in doc or \
           "not_provider_authority_proof" in doc, \
        "doc must explicitly negate provider authority"


def test_doc_has_no_live_inference_proof_claim():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "not_live_model_inference_proof" in doc, \
        "doc must contain not_live_model_inference_proof boundary"


def test_doc_has_no_model_quality_claim():
    doc = DOC_MD.read_text(encoding="utf-8").lower()
    assert "not_model_quality_proof" in doc, \
        "doc must contain not_model_quality_proof boundary"


# ---------------------------------------------------------------------------
# Validator integration
# ---------------------------------------------------------------------------

def test_validate_provider_worker_inspector_passes():
    from odin.hub.shell import validate_provider_worker_inspector
    errors = validate_provider_worker_inspector()
    assert errors == [], f"validate_provider_worker_inspector() returned errors: {errors}"


def test_prove_browser_hub_providers_emits_proof_packet():
    from odin.hub.shell import build_provider_worker_inspector_proof_packet
    packet = build_provider_worker_inspector_proof_packet()
    assert packet["artifact_kind"] == "hub_provider_worker_inspector_proof_packet"
    assert packet["candidate_only"] is True
    assert packet["local_only"] is True
    assert packet["read_only"] is True
    assert packet["provider_worker_inspector_only"] is True
    assert "not_proven" in packet
    assert "proof_boundaries" in packet
    assert "claim_boundary" in packet


def test_prove_browser_hub_providers_status_ok():
    from odin.hub.shell import build_provider_worker_inspector_proof_packet
    packet = build_provider_worker_inspector_proof_packet()
    assert packet.get("status") == "ok", \
        f"prove-browser-hub --providers packet status not ok: {packet.get('validation_errors')}"


def test_prove_browser_hub_providers_not_proven_includes_required_gaps():
    from odin.hub.shell import build_provider_worker_inspector_proof_packet
    packet = build_provider_worker_inspector_proof_packet()
    not_proven = packet.get("not_proven", [])
    for required_gap in [
        "production_readiness",
        "live_model_inference",
        "model_quality",
        "provider_authority",
        "security_certification",
    ]:
        assert required_gap in not_proven, f"not_proven must include {required_gap!r}"


# ---------------------------------------------------------------------------
# Agent Operator Mode — LRH Ladder Compiler
# ---------------------------------------------------------------------------

def test_agent_handoff_lrh_pr_10_writes_valid_packet(tmp_path):
    out_path = str(tmp_path / "lrh_pr_10_packet.json")
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_agent_work_packet
    packet = compile_lrh_pr_to_agent_work_packet("10", "claude-code")
    assert packet.get("candidate_only") is True
    assert packet.get("app_owned_apply") is True
    assert packet.get("external_send_default") is False
    assert packet.get("hidden_tool_execution_allowed") is False
    assert "LRH-PR-10" in packet.get("lrh_pr_id", "")


def test_agent_guard_passes_on_lrh_pr_10_packet():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_agent_work_packet
    from odin.agent_operator.guards import check_forbidden_actions
    packet = compile_lrh_pr_to_agent_work_packet("10", "claude-code")
    result = check_forbidden_actions(packet)
    assert result["status"] == "ok", f"agent-guard failed: {result}"


def test_agent_check_passes_on_lrh_pr_10_packet():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_agent_work_packet
    from odin.agent_operator.packets import validate_agent_work_packet
    packet = compile_lrh_pr_to_agent_work_packet("10", "claude-code")
    result = validate_agent_work_packet(packet)
    assert result["status"] == "ok", f"agent-check failed: {result}"


def test_agent_proof_gaps_classified_expected_not_blocking():
    """agent-proof gaps_present is expected for PR-level packets when guard/check pass."""
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_agent_work_packet
    from odin.agent_operator.guards import check_forbidden_actions
    from odin.agent_operator.packets import validate_agent_work_packet
    packet = compile_lrh_pr_to_agent_work_packet("10", "claude-code")
    guard = check_forbidden_actions(packet)
    check = validate_agent_work_packet(packet)
    # Guard and check must pass — then proof gaps are expected/not-blocking per spec
    assert guard["status"] == "ok"
    assert check["status"] == "ok"


# ---------------------------------------------------------------------------
# list-providers command integration
# ---------------------------------------------------------------------------

def test_list_providers_returns_provider_cards():
    from odin.models.providers.registry import list_provider_cards
    cards = list_provider_cards()
    assert isinstance(cards, list)
    assert len(cards) > 0
    for card in cards:
        assert card.get("candidate_only") is True
        assert card.get("may_apply") is False
        assert "provider_id" in card


def test_providers_all_disabled_by_default():
    from odin.models.providers.registry import list_provider_cards
    cards = list_provider_cards()
    stub_cards = [c for c in cards if "stub" in str(c.get("provider_id", ""))]
    for card in stub_cards:
        assert card.get("enabled_by_default") is False, \
            f"stub provider {card.get('provider_id')} must be disabled by default"


def test_providers_have_no_live_inference_verified():
    from odin.models.providers.registry import list_provider_cards
    cards = list_provider_cards()
    for card in cards:
        # No provider should claim live_inference_verified=True without a receipt
        if card.get("provider_kind") in ("mock", "null", "echo"):
            assert card.get("live_inference_verified") is False, \
                f"{card.get('provider_id')} must not claim live_inference_verified=True"
