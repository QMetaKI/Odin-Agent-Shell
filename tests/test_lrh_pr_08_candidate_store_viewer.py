"""Tests for LRH-PR-08: Sessions, Candidates, Store and Proof Gap Viewer.

Claim boundary: test_lrh_pr_08_candidate_store_viewer_no_apply_no_external_send_no_store_mutation_no_raw_payload

All tests are deterministic static checks — no browser automation, no npm, no external network.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT / "odin" / "hub" / "static"
CSV_JS = STATIC_DIR / "candidate_store_viewer.js"
INDEX_HTML = STATIC_DIR / "index.html"
DOC = ROOT / "docs" / "HUB_CANDIDATE_STORE_VIEWER_V1.md"
TEST_FILE = ROOT / "tests" / "test_lrh_pr_08_candidate_store_viewer.py"


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

def test_candidate_store_viewer_js_exists():
    assert CSV_JS.exists(), "candidate_store_viewer.js must exist"


def test_index_html_loads_candidate_store_viewer_js():
    html = INDEX_HTML.read_text(encoding="utf-8", errors="ignore")
    assert "candidate_store_viewer.js" in html, "index.html must load candidate_store_viewer.js"


def test_doc_exists():
    assert DOC.exists(), "HUB_CANDIDATE_STORE_VIEWER_V1.md must exist"


def test_test_file_exists():
    assert TEST_FILE.exists(), "test_lrh_pr_08_candidate_store_viewer.py must exist"


# ---------------------------------------------------------------------------
# API reference checks
# ---------------------------------------------------------------------------

def test_viewer_references_v1_candidates():
    js = CSV_JS.read_text(encoding="utf-8", errors="ignore")
    assert "/v1/candidates" in js, "candidate_store_viewer.js must reference /v1/candidates"


def test_viewer_references_v1_sessions():
    js = CSV_JS.read_text(encoding="utf-8", errors="ignore")
    assert "/v1/sessions" in js, "candidate_store_viewer.js must reference /v1/sessions"


def test_viewer_references_v1_proof_gaps():
    js = CSV_JS.read_text(encoding="utf-8", errors="ignore")
    assert "/v1/proof-gaps" in js, "candidate_store_viewer.js must reference /v1/proof-gaps"


# ---------------------------------------------------------------------------
# Boundary token checks in JS
# ---------------------------------------------------------------------------

def test_viewer_has_candidate_only_token():
    js = CSV_JS.read_text(encoding="utf-8", errors="ignore")
    assert "candidate_only" in js, "candidate_store_viewer.js must include 'candidate_only' token"


def test_viewer_has_claim_boundary_token():
    js = CSV_JS.read_text(encoding="utf-8", errors="ignore")
    assert "claim_boundary" in js, "candidate_store_viewer.js must include 'claim_boundary' token"


def test_viewer_has_not_applied_truth_token():
    js = CSV_JS.read_text(encoding="utf-8", errors="ignore")
    assert "not_applied_truth" in js or "not applied truth" in js.lower(), \
        "candidate_store_viewer.js must include 'not_applied_truth' token"


def test_viewer_has_no_apply_token():
    js = CSV_JS.read_text(encoding="utf-8", errors="ignore")
    assert "no_apply" in js or "No app apply" in js, \
        "candidate_store_viewer.js must include no-apply boundary token"


def test_viewer_localhost_default():
    js = CSV_JS.read_text(encoding="utf-8", errors="ignore")
    assert "127.0.0.1" in js or "ODIN_API_BASE" in js, \
        "candidate_store_viewer.js must reference localhost default"


# ---------------------------------------------------------------------------
# Surface ID checks in index.html
# ---------------------------------------------------------------------------

def test_index_has_sessions_surface():
    html = INDEX_HTML.read_text(encoding="utf-8", errors="ignore")
    assert "csv-sessions-content" in html, "index.html must have sessions view surface"


def test_index_has_candidate_artifact_surface():
    html = INDEX_HTML.read_text(encoding="utf-8", errors="ignore")
    assert "csv-candidate-content" in html, "index.html must have candidate artifact surface"


def test_index_has_store_metadata_surface():
    html = INDEX_HTML.read_text(encoding="utf-8", errors="ignore")
    assert "csv-store-content" in html, "index.html must have store metadata surface"


def test_index_has_proof_gap_viewer_surface():
    html = INDEX_HTML.read_text(encoding="utf-8", errors="ignore")
    assert "csv-proof-gaps-content" in html, "index.html must have proof gap viewer surface"


# ---------------------------------------------------------------------------
# Boundary banner and warning checks in index.html
# ---------------------------------------------------------------------------

def test_index_has_candidate_only_boundary_banner():
    html = INDEX_HTML.read_text(encoding="utf-8", errors="ignore")
    assert "candidate-only" in html.lower() or "Candidate-only" in html, \
        "index.html must have candidate-only boundary banner"


def test_index_has_not_applied_truth_warning():
    html = INDEX_HTML.read_text(encoding="utf-8", errors="ignore")
    assert "not-applied-truth" in html.lower() or "not applied truth" in html.lower(), \
        "index.html must have not-applied truth warning"


def test_index_has_no_app_apply_boundary():
    html = INDEX_HTML.read_text(encoding="utf-8", errors="ignore")
    assert "No app apply" in html, "index.html must include 'No app apply' boundary text"


def test_index_has_no_external_send_boundary():
    html = INDEX_HTML.read_text(encoding="utf-8", errors="ignore")
    assert "No external send" in html, "index.html must include 'No external send' boundary text"


def test_index_has_no_store_mutation_boundary():
    html = INDEX_HTML.read_text(encoding="utf-8", errors="ignore")
    assert "No store mutation" in html, "index.html must include 'No store mutation' boundary text"


def test_index_has_no_raw_payload_boundary():
    html = INDEX_HTML.read_text(encoding="utf-8", errors="ignore")
    assert "No raw sensitive payload" in html or "raw sensitive payload" in html.lower(), \
        "index.html must include raw sensitive payload protection boundary"


# ---------------------------------------------------------------------------
# No forbidden interactive controls in JS
# ---------------------------------------------------------------------------

FORBIDDEN_CONTROLS = [
    "function apply(",
    "function applyCandidate(",
    "function externalSend(",
    "function sendExternally(",
    "function storeWrite(",
    "function storeDelete(",
    "function rawPayloadReveal(",
    'onclick="apply(',
    'id="apply-btn',
    'id="external-send',
    "providerCredential",
    "enablePublicNetwork(",
    "hiddenUpload(",
    "remoteUpload(",
]


@pytest.mark.parametrize("pattern", FORBIDDEN_CONTROLS)
def test_viewer_js_has_no_forbidden_control(pattern):
    js = CSV_JS.read_text(encoding="utf-8", errors="ignore")
    assert pattern.lower() not in js.lower(), \
        f"candidate_store_viewer.js must not contain forbidden control: {pattern!r}"


# ---------------------------------------------------------------------------
# No forbidden interactive controls in index.html (candidate viewer section)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("pattern", FORBIDDEN_CONTROLS)
def test_index_html_has_no_forbidden_control(pattern):
    html = INDEX_HTML.read_text(encoding="utf-8", errors="ignore")
    assert pattern.lower() not in html.lower(), \
        f"index.html must not contain forbidden interactive control: {pattern!r}"


# ---------------------------------------------------------------------------
# Raw sensitive payload protection
# ---------------------------------------------------------------------------

def test_viewer_js_says_raw_payloads_redacted():
    js = CSV_JS.read_text(encoding="utf-8", errors="ignore")
    assert "REDACTED" in js or "redact" in js.lower(), \
        "candidate_store_viewer.js must implement raw sensitive payload redaction"


def test_viewer_js_no_raw_payload_reveal_function():
    js = CSV_JS.read_text(encoding="utf-8", errors="ignore")
    assert "rawPayloadReveal" not in js, \
        "candidate_store_viewer.js must not define rawPayloadReveal()"
    assert "unsafePayloadToggle" not in js, \
        "candidate_store_viewer.js must not define unsafePayloadToggle()"


# ---------------------------------------------------------------------------
# Docs boundary claim checks
# ---------------------------------------------------------------------------

DOC_REQUIRED_PHRASES = [
    "does not apply candidate artifacts",
    "does not show candidates as applied truth",
    "does not mutate the runtime store",
    "does not send externally",
    "does not display raw sensitive payloads by default",
    "does not close proof gaps by displaying them",
    "does not prove production readiness",
    "proof boundaries",
]


@pytest.mark.parametrize("phrase", DOC_REQUIRED_PHRASES)
def test_doc_has_required_phrase(phrase):
    doc_text = DOC.read_text(encoding="utf-8", errors="ignore").lower()
    assert phrase.lower() in doc_text, \
        f"HUB_CANDIDATE_STORE_VIEWER_V1.md must contain: {phrase!r}"


def test_doc_has_no_candidate_as_truth_claim():
    doc_text = DOC.read_text(encoding="utf-8", errors="ignore").lower()
    # Positive claims like "candidates are applied truth" or "shows as truth" are forbidden.
    # Negated uses ("not applied truth", "does not show ... as applied truth") are expected.
    assert "candidates are applied truth" not in doc_text, \
        "HUB_CANDIDATE_STORE_VIEWER_V1.md must not claim candidates are applied truth"
    assert "shown as applied truth" not in doc_text or "not shown as applied truth" in doc_text, \
        "HUB_CANDIDATE_STORE_VIEWER_V1.md must not claim candidates are shown as applied truth"


def test_doc_has_no_store_mutation_claim():
    doc_text = DOC.read_text(encoding="utf-8", errors="ignore").lower()
    # "does not mutate" is the expected phrase — bare "mutates" should not appear
    assert "mutates the runtime store" not in doc_text, \
        "HUB_CANDIDATE_STORE_VIEWER_V1.md must not claim store mutation"


# ---------------------------------------------------------------------------
# Validator integration
# ---------------------------------------------------------------------------

def test_validate_candidate_store_viewer_passes():
    from odin.hub.shell import validate_candidate_store_viewer
    errors = validate_candidate_store_viewer()
    assert errors == [], f"validate_candidate_store_viewer returned errors: {errors}"


def test_prove_browser_hub_candidates_emits_proof_packet():
    from odin.hub.shell import build_candidate_store_viewer_proof_packet
    packet = build_candidate_store_viewer_proof_packet()
    assert packet["artifact_kind"] == "hub_candidate_store_viewer_proof_packet"
    assert packet["candidate_only"] is True
    assert packet["local_only"] is True
    assert packet["read_only"] is True
    assert packet["viewer_only"] is True
    assert "not_proven" in packet
    assert "production_readiness" in packet["not_proven"]
    assert "candidate_application" in packet["not_proven"]
    assert "store_mutation" in packet["not_proven"]
    assert "proof_boundaries" in packet
    assert "claim_boundary" in packet


def test_prove_browser_hub_candidates_proof_boundaries():
    from odin.hub.shell import build_candidate_store_viewer_proof_packet
    packet = build_candidate_store_viewer_proof_packet()
    boundaries = packet["proof_boundaries"]
    required = [
        "not_production_readiness_certification",
        "not_candidate_application_proof",
        "not_candidate_as_truth_proof",
        "not_store_mutation_proof",
        "not_raw_sensitive_payload_safety_certification",
        "not_app_state_mutation_proof",
        "not_external_send_authority_proof",
    ]
    for b in required:
        assert b in boundaries, f"Proof boundary missing: {b}"


def test_agent_handoff_lrh_pr_08_writes_valid_packet(tmp_path):
    import subprocess, sys
    out_path = tmp_path / "packet.json"
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "08", "--out", str(out_path)],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"agent-handoff failed: {result.stderr}"
    assert out_path.exists(), "agent-handoff --out must write packet file"
    packet = json.loads(out_path.read_text())
    assert packet["lrh_pr"] == "08"
    assert packet["candidate_only"] is True
    assert packet["app_owned_apply"] is True


def test_agent_guard_passes_for_pr08_packet(tmp_path):
    import subprocess, sys
    out_path = tmp_path / "packet.json"
    subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "08", "--out", str(out_path)],
        capture_output=True, text=True, check=True
    )
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-guard", "--packet", str(out_path)],
        capture_output=True, text=True
    )
    guard = json.loads(result.stdout)
    assert guard["status"] == "ok", f"agent-guard must pass: {guard}"
    assert guard["violations"] == [], "agent-guard must have no violations"


def test_agent_check_passes_for_pr08_packet(tmp_path):
    import subprocess, sys
    out_path = tmp_path / "packet.json"
    subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "08", "--out", str(out_path)],
        capture_output=True, text=True, check=True
    )
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-check", "--packet", str(out_path)],
        capture_output=True, text=True
    )
    check = json.loads(result.stdout)
    assert check["status"] == "ok", f"agent-check must pass: {check}"


def test_agent_proof_gaps_classified_expected_not_blocking(tmp_path):
    import subprocess, sys
    out_path = tmp_path / "packet.json"
    subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "08", "--out", str(out_path)],
        capture_output=True, text=True, check=True
    )
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-proof", "--packet", str(out_path)],
        capture_output=True, text=True
    )
    proof = json.loads(result.stdout)
    # gaps_present is expected for PR-level packets — guard/check pass is the gate
    assert proof["status"] in {"ok", "gaps_present"}, \
        f"agent-proof must be ok or gaps_present (expected): {proof}"
    assert "declared_boundaries" in proof


def test_validate_all_passes():
    import subprocess, sys
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-all"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"validate-all must pass: {result.stdout}\n{result.stderr}"


def test_validate_candidate_store_viewer_cli():
    import subprocess, sys
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-candidate-store-viewer"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"validate-candidate-store-viewer CLI must pass: {result.stdout}\n{result.stderr}"
    assert "OK" in result.stdout
