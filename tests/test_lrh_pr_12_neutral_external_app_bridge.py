"""Tests for LRH-PR-12 — Neutral External App Bridge Pack.

Claim boundary: neutral_external_app_bridge_pack_candidate_only_no_app_apply_no_external_send_no_credentials

These tests are deterministic, static validators. They do not:
- make live network requests
- use browser automation
- require npm
- apply candidate artifacts
- send externally
- use credentials
- perform concrete external app integration
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
_BRIDGE_EXAMPLES = _ROOT / "examples" / "external_app_bridge"
_BRIDGE_DOC = _ROOT / "docs" / "NEUTRAL_EXTERNAL_APP_BRIDGE_PACK_V1.md"


# ---------------------------------------------------------------------------
# Required file presence
# ---------------------------------------------------------------------------

REQUIRED_FILES = [
    "docs/NEUTRAL_EXTERNAL_APP_BRIDGE_PACK_V1.md",
    "examples/external_app_bridge/neutral_host_health_check.py",
    "examples/external_app_bridge/neutral_host_submit_universal_work.py",
    "examples/external_app_bridge/neutral_host_read_candidate.py",
    "examples/external_app_bridge/neutral_host_read_proof_gaps.py",
    "examples/external_app_bridge/neutral_bridge_config.example.json",
    "examples/external_app_bridge/neutral_universal_work_request.valid.json",
    "examples/external_app_bridge/neutral_candidate_artifact_response.valid.json",
    "tests/test_lrh_pr_12_neutral_external_app_bridge.py",
]


@pytest.mark.parametrize("rel", REQUIRED_FILES)
def test_required_file_exists(rel):
    assert (_ROOT / rel).exists(), f"Required file missing: {rel}"


# ---------------------------------------------------------------------------
# Bridge config fixture
# ---------------------------------------------------------------------------

def _load_bridge_config():
    return json.loads((_BRIDGE_EXAMPLES / "neutral_bridge_config.example.json").read_text(encoding="utf-8"))


def test_bridge_config_odin_base_url():
    cfg = _load_bridge_config()
    assert cfg.get("odin_base_url") == "http://127.0.0.1:8877", "odin_base_url must be http://127.0.0.1:8877"


def test_bridge_config_localhost_only_true():
    cfg = _load_bridge_config()
    assert cfg.get("localhost_only") is True, "localhost_only must be true"


def test_bridge_config_host_app_owns_apply():
    cfg = _load_bridge_config()
    assert cfg.get("host_app_owns_apply") is True, "host_app_owns_apply must be true"


def test_bridge_config_host_app_owns_state():
    cfg = _load_bridge_config()
    assert cfg.get("host_app_owns_state") is True, "host_app_owns_state must be true"


def test_bridge_config_host_app_owns_external_send():
    cfg = _load_bridge_config()
    assert cfg.get("host_app_owns_external_send") is True, "host_app_owns_external_send must be true"


def test_bridge_config_odin_app_apply_false():
    cfg = _load_bridge_config()
    assert cfg.get("odin_app_apply") is False, "odin_app_apply must be false"


def test_bridge_config_odin_external_send_false():
    cfg = _load_bridge_config()
    assert cfg.get("odin_external_send") is False, "odin_external_send must be false"


def test_bridge_config_credential_required_false():
    cfg = _load_bridge_config()
    assert cfg.get("credential_required") is False, "credential_required must be false"


FORBIDDEN_CONFIG_KEYS = [
    "token", "secret", "api_key", "password", "credential", "webhook_url", "callback_url", "remote_url",
]


@pytest.mark.parametrize("key", FORBIDDEN_CONFIG_KEYS)
def test_bridge_config_no_forbidden_keys(key):
    cfg = _load_bridge_config()
    assert key not in cfg, f"bridge config must not contain forbidden key: {key!r}"


# ---------------------------------------------------------------------------
# Universal Work request fixture
# ---------------------------------------------------------------------------

def _load_work_request():
    return json.loads((_BRIDGE_EXAMPLES / "neutral_universal_work_request.valid.json").read_text(encoding="utf-8"))


def test_work_request_candidate_only_true():
    wr = _load_work_request()
    assert wr.get("candidate_only") is True


def test_work_request_local_only_true():
    wr = _load_work_request()
    assert wr.get("local_only") is True


def test_work_request_app_apply_false():
    wr = _load_work_request()
    assert wr.get("app_apply") is False


def test_work_request_external_send_false():
    wr = _load_work_request()
    assert wr.get("external_send") is False


def test_work_request_host_app_owns_apply():
    wr = _load_work_request()
    assert wr.get("host_app_owns_apply") is True


def test_work_request_host_app_owns_state():
    wr = _load_work_request()
    assert wr.get("host_app_owns_state") is True


def test_work_request_host_app_owns_external_send():
    wr = _load_work_request()
    assert wr.get("host_app_owns_external_send") is True


def test_work_request_has_claim_boundary():
    wr = _load_work_request()
    assert "claim_boundary" in wr


def test_work_request_has_proof_boundaries():
    wr = _load_work_request()
    assert "proof_boundaries" in wr


def test_work_request_has_known_non_proofs():
    wr = _load_work_request()
    assert "known_non_proofs" in wr


# ---------------------------------------------------------------------------
# Candidate artifact fixture
# ---------------------------------------------------------------------------

def _load_candidate_artifact():
    return json.loads((_BRIDGE_EXAMPLES / "neutral_candidate_artifact_response.valid.json").read_text(encoding="utf-8"))


def test_candidate_artifact_candidate_only_true():
    ca = _load_candidate_artifact()
    assert ca.get("candidate_only") is True


def test_candidate_artifact_applied_truth_false():
    ca = _load_candidate_artifact()
    assert ca.get("applied_truth") is False, "applied_truth must be false — candidate is not applied truth"


def test_candidate_artifact_app_state_mutated_false():
    ca = _load_candidate_artifact()
    assert ca.get("app_state_mutated") is False


def test_candidate_artifact_external_send_false():
    ca = _load_candidate_artifact()
    assert ca.get("external_send") is False


def test_candidate_artifact_has_claim_boundary():
    ca = _load_candidate_artifact()
    assert "claim_boundary" in ca


def test_candidate_artifact_has_proof_boundaries():
    ca = _load_candidate_artifact()
    assert "proof_boundaries" in ca


# ---------------------------------------------------------------------------
# Example file content checks
# ---------------------------------------------------------------------------

def _read_example(name: str) -> str:
    return (_BRIDGE_EXAMPLES / name).read_text(encoding="utf-8", errors="ignore")


def test_health_check_has_localhost_guard():
    src = _read_example("neutral_host_health_check.py")
    assert "127.0.0.1" in src or "localhost" in src, "health check must reference localhost"


def test_health_check_does_not_send_externally():
    src = _read_example("neutral_host_health_check.py")
    assert "send_external" not in src and "externalSend" not in src
    assert "upload" not in src.lower() or "urlopen" in src


def test_health_check_has_candidate_only_boundary():
    src = _read_example("neutral_host_health_check.py")
    assert "candidate_only" in src


def test_health_check_has_host_app_owns_apply():
    src = _read_example("neutral_host_health_check.py")
    assert "host_app_owns_apply" in src


def test_submit_work_does_not_apply_candidate():
    src = _read_example("neutral_host_submit_universal_work.py")
    assert "apply_candidate" not in src
    assert "applyCandidate" not in src
    assert "host_app_owns_apply" in src


def test_submit_work_applied_truth_is_false():
    src = _read_example("neutral_host_submit_universal_work.py")
    assert "applied_truth" in src and "False" in src


def test_submit_work_has_localhost_guard():
    src = _read_example("neutral_host_submit_universal_work.py")
    assert "127.0.0.1" in src or "localhost" in src


def test_read_candidate_does_not_mutate_host_state():
    src = _read_example("neutral_host_read_candidate.py")
    assert "mutate" not in src.lower() or "does not mutate" in src.lower()
    assert "host_app_owns_apply" in src


def test_read_candidate_applied_truth_false():
    src = _read_example("neutral_host_read_candidate.py")
    assert "applied_truth" in src and "False" in src


def test_read_proof_gaps_does_not_close_gaps():
    src = _read_example("neutral_host_read_proof_gaps.py")
    assert "gaps_closed_by_this_read" in src or "does not close" in src.lower()
    assert "False" in src


def test_read_proof_gaps_has_known_non_proofs():
    src = _read_example("neutral_host_read_proof_gaps.py")
    assert "KNOWN_NON_PROOFS" in src or "known_non_proofs" in src


# ---------------------------------------------------------------------------
# SDK helper forbidden name checks
# ---------------------------------------------------------------------------

SDK_FILES = [
    _ROOT / "sdk" / "python" / "odin_client.py",
    _ROOT / "odin_app_sdk" / "client.py",
]

FORBIDDEN_HELPER_NAMES = [
    "apply_candidate",
    "mutate_app_state",
    "send_external",
    "upload_result",
    "publish_result",
    "store_credential",
    "save_credential",
    "set_api_key",
    "set_token",
    "run_provider",
    "execute_provider",
    "call_model",
    "run_model",
]


@pytest.mark.parametrize("sdk_file,helper", [
    (sdk, h) for sdk in SDK_FILES for h in FORBIDDEN_HELPER_NAMES
])
def test_sdk_no_forbidden_helper(sdk_file, helper):
    if not sdk_file.exists():
        pytest.skip(f"{sdk_file.name} not found")
    src = sdk_file.read_text(encoding="utf-8", errors="ignore")
    assert f"def {helper}(" not in src, f"{sdk_file.name}: must not define forbidden helper def {helper}()"


# ---------------------------------------------------------------------------
# Doc content checks
# ---------------------------------------------------------------------------

def _doc_text():
    return _BRIDGE_DOC.read_text(encoding="utf-8", errors="ignore").lower()


REQUIRED_DOC_PHRASES = [
    "host app owns apply",
    "host app owns state",
    "host app owns external send",
    "odin does not apply",
    "odin does not send externally",
    "candidate artifact",
    "not applied truth",
    "localhost",
    "not_production_readiness_certification",
    "not a hosted bridge",
]


@pytest.mark.parametrize("phrase", REQUIRED_DOC_PHRASES)
def test_doc_has_required_phrase(phrase):
    doc = _doc_text()
    assert phrase.lower() in doc, f"Doc missing required phrase: {phrase!r}"


FORBIDDEN_DOC_CLAIMS = [
    "production bridge complete",
    "security certified",
    "production-ready bridge",
]


@pytest.mark.parametrize("claim", FORBIDDEN_DOC_CLAIMS)
def test_doc_no_forbidden_overclaim(claim):
    doc = _doc_text()
    assert claim.lower() not in doc, f"Doc contains forbidden overclaim: {claim!r}"


def test_doc_no_concrete_third_party_names():
    doc = _BRIDGE_DOC.read_text(encoding="utf-8", errors="ignore")
    forbidden_names = ["Slack", "Notion", "Salesforce", "HubSpot", "Zapier", "Make.com", "IFTTT"]
    for name in forbidden_names:
        assert name not in doc, f"Doc must not reference concrete third-party app: {name!r}"


def test_doc_no_hosted_bridge_claim():
    doc = _doc_text()
    assert "hosted bridge" not in doc or "not a hosted bridge" in doc


def test_doc_no_public_gateway_claim():
    doc = _doc_text()
    assert "public gateway" not in doc or "not a public" in doc


# ---------------------------------------------------------------------------
# CLI validator integration
# ---------------------------------------------------------------------------

def test_validate_neutral_external_app_bridge_passes():
    from odin.hub.shell import validate_neutral_external_app_bridge
    errors = validate_neutral_external_app_bridge()
    assert errors == [], f"validate_neutral_external_app_bridge() returned errors: {errors}"


def test_prove_neutral_external_app_bridge_emits_proof_packet():
    from odin.hub.shell import build_neutral_external_app_bridge_proof_packet
    packet = build_neutral_external_app_bridge_proof_packet()
    assert packet.get("candidate_only") is True
    assert packet.get("artifact_kind") == "neutral_external_app_bridge_pack_proof_packet"
    assert packet.get("status") in {"ok", "partial"}
    assert "not_proven" in packet
    assert "production_readiness" in packet["not_proven"]
    assert "proof_boundaries" in packet
    assert "claim_boundary" in packet


def test_prove_packet_not_proven_includes_required():
    from odin.hub.shell import build_neutral_external_app_bridge_proof_packet
    packet = build_neutral_external_app_bridge_proof_packet()
    required_not_proven = [
        "production_readiness",
        "security_certification",
        "hosted_bridge",
        "public_gateway",
        "real_external_app_integration",
        "app_apply_authority",
        "external_send_authority",
    ]
    for item in required_not_proven:
        assert item in packet["not_proven"], f"not_proven must include: {item!r}"


# ---------------------------------------------------------------------------
# Agent-handoff packet
# ---------------------------------------------------------------------------

def test_agent_handoff_lrh_pr_12_packet_exists():
    packet_path = Path("/tmp/lrh_pr_12_packet.json")
    if not packet_path.exists():
        pytest.skip("agent-handoff packet not generated yet (/tmp/lrh_pr_12_packet.json)")
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    assert packet.get("candidate_only") is True
    assert packet.get("lrh_pr_id") == "LRH-PR-12"


def test_agent_guard_check_pass():
    from odin.agent_operator.guards import check_forbidden_actions
    packet_path = Path("/tmp/lrh_pr_12_packet.json")
    if not packet_path.exists():
        pytest.skip("agent-handoff packet not generated yet")
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    result = check_forbidden_actions(packet)
    assert result.get("status") == "ok", f"agent-guard forbidden action check failed: {result}"


# ---------------------------------------------------------------------------
# validate-all integration (smoke test)
# ---------------------------------------------------------------------------

def test_validate_all_includes_neutral_bridge():
    """validate_all() must call validate_neutral_external_app_bridge() without error."""
    from odin.cli import validate_all
    errors = validate_all()
    neutral_errors = [e for e in errors if "neutral external app bridge" in e.lower()]
    assert neutral_errors == [], f"validate_all() has neutral bridge errors: {neutral_errors}"
