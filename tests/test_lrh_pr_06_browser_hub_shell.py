"""Tests for LRH-PR-06 Browser Odin Hub Shell.

All tests are deterministic static checks — no browser automation, no npm, no network.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
HUB_DIR = ROOT / "odin" / "hub"
STATIC_DIR = HUB_DIR / "static"
API_CLIENT = HUB_DIR / "api_client.js"
INDEX_HTML = STATIC_DIR / "index.html"
STYLES_CSS = STATIC_DIR / "styles.css"
APP_JS = STATIC_DIR / "app.js"
DOC = ROOT / "docs" / "BROWSER_ODIN_HUB_SHELL_V1.md"


# -----------------------------------------------------------------------
# Static file existence
# -----------------------------------------------------------------------

def test_static_files_exist():
    assert INDEX_HTML.exists(), "index.html must exist"
    assert STYLES_CSS.exists(), "styles.css must exist"
    assert APP_JS.exists(), "app.js must exist"
    assert API_CLIENT.exists(), "api_client.js must exist"
    assert (HUB_DIR / "shell.py").exists(), "shell.py must exist"


def test_doc_exists():
    assert DOC.exists(), "BROWSER_ODIN_HUB_SHELL_V1.md must exist"


def test_test_file_exists():
    assert (ROOT / "tests" / "test_lrh_pr_06_browser_hub_shell.py").exists()


# -----------------------------------------------------------------------
# Boundary banner
# -----------------------------------------------------------------------

def test_index_html_includes_boundary_banner():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert "Localhost only" in html, "boundary banner must include 'Localhost only'"
    assert "Candidate-only" in html, "boundary banner must include 'Candidate-only'"
    assert "No app apply" in html, "boundary banner must include 'No app apply'"
    assert "No external send" in html, "boundary banner must include 'No external send'"
    assert "No provider execution" in html, "boundary banner must include 'No provider execution'"


def test_index_html_boundary_banner_element():
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert "boundary-banner" in html, "index.html must include boundary-banner element"


# -----------------------------------------------------------------------
# Navigation shell
# -----------------------------------------------------------------------

def test_index_html_includes_navigation_shell():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "health" in html, "navigation must include health"
    assert "status" in html, "navigation must include status"
    assert "proof-gap" in html, "navigation must include proof-gaps"


def test_index_html_includes_candidates_nav():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "candidate" in html, "navigation must include candidates"


def test_index_html_includes_events_nav():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "event" in html, "navigation must include events"


def test_index_html_includes_universal_work_placeholder():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert "universal" in html or "playground" in html, \
        "index.html must include Universal Work Playground placeholder"


# -----------------------------------------------------------------------
# No interactive apply/external-send controls
# -----------------------------------------------------------------------

def test_index_html_no_apply_button():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    # Text mentions are allowed (e.g. "No app apply" in boundary banner)
    # but interactive controls like onclick="apply(...)" or id="apply-btn" must not appear
    assert 'onclick="apply(' not in html
    assert "id=\"apply-btn" not in html
    assert "id='apply-btn" not in html
    assert "function apply()" not in html


def test_index_html_no_external_send_button():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert 'onclick="externalsend' not in html
    assert 'id="external-send-btn' not in html
    assert "function externalsend()" not in html


def test_index_html_no_provider_credential_field():
    html = INDEX_HTML.read_text(encoding="utf-8").lower()
    assert 'type="password"' not in html or "credential" not in html, \
        "index.html must not have a provider credential entry field"


# -----------------------------------------------------------------------
# API client — defaults and references
# -----------------------------------------------------------------------

def test_api_client_defaults_to_localhost():
    js = API_CLIENT.read_text(encoding="utf-8")
    assert "127.0.0.1" in js, "api_client.js must default to 127.0.0.1"
    assert "8877" in js, "api_client.js must reference default port 8877"


def test_api_client_does_not_use_remote_network_default():
    js = API_CLIENT.read_text(encoding="utf-8")
    assert "0.0.0.0" not in js, "api_client.js must not reference 0.0.0.0"


def test_api_client_references_v1_health():
    js = API_CLIENT.read_text(encoding="utf-8")
    assert "/v1/health" in js


def test_api_client_references_v1_status():
    js = API_CLIENT.read_text(encoding="utf-8")
    assert "/v1/status" in js


def test_api_client_references_v1_proof_gaps():
    js = API_CLIENT.read_text(encoding="utf-8")
    assert "/v1/proof-gaps" in js


def test_api_client_has_no_external_send_function():
    js = API_CLIENT.read_text(encoding="utf-8")
    # The string "external_send" may appear in claim boundary constants/comments
    # but must NOT appear as a callable function or method definition
    assert "function externalSend(" not in js
    assert "function external_send(" not in js
    assert ".prototype.externalSend" not in js
    assert ".prototype.external_send" not in js


def test_api_client_has_no_apply_function():
    js = API_CLIENT.read_text(encoding="utf-8")
    assert "function apply(" not in js
    # prototype method check
    assert ".apply = function" not in js


def test_api_client_localhost_guard_present():
    js = API_CLIENT.read_text(encoding="utf-8")
    assert "isLocalhost" in js or "localhost" in js.lower()


# -----------------------------------------------------------------------
# Docs claim boundaries
# -----------------------------------------------------------------------

def test_docs_no_hosted_cloud_ui():
    text = DOC.read_text(encoding="utf-8").lower()
    assert "not a hosted cloud ui" in text


def test_docs_no_public_network_api():
    text = DOC.read_text(encoding="utf-8").lower()
    assert "not a public network api" in text


def test_docs_no_app_apply():
    text = DOC.read_text(encoding="utf-8").lower()
    assert "does not grant app apply" in text


def test_docs_no_external_send():
    text = DOC.read_text(encoding="utf-8").lower()
    assert "does not send externally" in text


def test_docs_no_provider_execution():
    text = DOC.read_text(encoding="utf-8").lower()
    assert "does not execute provider" in text


def test_docs_proof_boundaries_section():
    text = DOC.read_text(encoding="utf-8").lower()
    assert "proof boundaries" in text
    assert "not_production_readiness" in text


def test_docs_universal_work_playground_is_placeholder():
    text = DOC.read_text(encoding="utf-8").lower()
    assert "placeholder" in text
    assert "lrh-pr-11" in text or "lrh-pr-06" in text


# -----------------------------------------------------------------------
# validate-browser-hub-shell integration
# -----------------------------------------------------------------------

def test_validate_browser_hub_shell_passes():
    from odin.hub.shell import validate_browser_hub_shell
    errors = validate_browser_hub_shell()
    assert errors == [], f"validate_browser_hub_shell() errors: {errors}"


# -----------------------------------------------------------------------
# prove-browser-hub --shell-only proof packet
# -----------------------------------------------------------------------

def test_prove_browser_hub_shell_only_emits_packet():
    from odin.hub.shell import build_browser_hub_proof_packet, BROWSER_HUB_PROOF_BOUNDARIES
    packet = build_browser_hub_proof_packet(shell_only=True)
    assert packet["artifact_kind"] == "browser_hub_shell_proof_packet"
    assert packet["candidate_only"] is True
    assert packet["local_only"] is True
    assert packet["shell_only"] is True
    assert isinstance(packet["not_proven"], list)
    assert "production_readiness" in packet["not_proven"]
    assert "app_state_mutation" in packet["not_proven"]
    assert "external_send_authority" in packet["not_proven"]
    for boundary in BROWSER_HUB_PROOF_BOUNDARIES:
        assert boundary in packet["proof_boundaries"], f"missing proof boundary: {boundary}"


def test_prove_browser_hub_no_apply_control_in_proof():
    from odin.hub.shell import build_browser_hub_proof_packet
    packet = build_browser_hub_proof_packet(shell_only=True)
    # Proven must include no_apply_controls
    assert "no_apply_controls" in packet.get("proven", [])
    assert "no_external_send_controls" in packet.get("proven", [])
