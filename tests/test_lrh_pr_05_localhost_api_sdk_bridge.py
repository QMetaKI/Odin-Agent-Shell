"""LRH-PR-05 — Localhost API Contract Hardening and SDK Bridge v1 tests.

Tests:
- GET /v1/health positive response
- GET /v1/status positive response
- GET /v1/providers positive response
- POST /v1/universal-work candidate-only response
- GET /v1/sessions/{id}
- GET /v1/candidates/{id}
- GET /v1/events
- GET /v1/proof-gaps
- Structured error response
- Schema fixtures validate
- Localhost-only binding/default base URL
- SDK health check
- SDK status
- SDK submit universal work
- SDK read candidate
- SDK proof gaps
- SDK rejects non-localhost base_url by default
- No apply endpoint
- No external-send endpoint
- No provider credential endpoint
- No raw app state to model endpoint
- Docs contain correct claim language
- Examples validate
- validate-localhost-api-sdk-bridge passes
"""
from __future__ import annotations

import json
import threading
from http.server import HTTPServer
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def start_test_server(host="127.0.0.1", port=0):
    from odin.daemon.local_api import OdinLocalHandler
    server = HTTPServer((host, port), OdinLocalHandler)
    actual_port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, actual_port


def stop_test_server(server):
    server.shutdown()
    server.server_close()


def get(port, path):
    from urllib.request import urlopen
    from urllib.error import HTTPError
    try:
        with urlopen(f"http://127.0.0.1:{port}{path}", timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode())
    except HTTPError as exc:
        return exc.code, json.loads(exc.read().decode())


def post(port, path, payload):
    from urllib.request import Request, urlopen
    body = json.dumps(payload).encode()
    req = Request(f"http://127.0.0.1:{port}{path}", data=body, method="POST",
                  headers={"Content-Type": "application/json"})
    from urllib.error import HTTPError
    try:
        with urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode())
    except HTTPError as exc:
        return exc.code, json.loads(exc.read().decode())


# ---------------------------------------------------------------------------
# API endpoint tests
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def api_server():
    server, port = start_test_server()
    yield port
    stop_test_server(server)


def test_v1_health_positive(api_server):
    status, body = get(api_server, "/v1/health")
    assert status == 200
    assert body["artifact_kind"] == "odin_localhost_api_health"
    assert body["status"] == "ok"
    assert body["candidate_only"] is True
    assert body["app_owned_apply"] is True
    assert body["external_send_default"] is False
    assert body["network_scope"] == "localhost_only"


def test_v1_status_positive(api_server):
    status, body = get(api_server, "/v1/status")
    assert status == 200
    assert body["artifact_kind"] == "odin_localhost_api_status"
    assert body["candidate_only"] is True
    assert body["app_owned_apply"] is True
    assert isinstance(body["candidate_count"], int)
    assert isinstance(body["session_count"], int)


def test_v1_providers_positive(api_server):
    status, body = get(api_server, "/v1/providers")
    assert status == 200
    assert body["artifact_kind"] == "odin_localhost_api_providers"
    assert isinstance(body["providers"], list)
    assert body["candidate_only"] is True
    assert "provider_proof" in body["claim_boundary"]


VALID_WORK_PAYLOAD = {
    "artifact_kind": "odin_universal_work",
    "binding_ref": "BIND-SDK-TEST-001",
    "caller_id": "sdk_bridge_test",
    "claim_boundary": {"claims": ["candidate_only"]},
    "constraints": {"actions": [], "forbidden": ["apply directly", "send externally"]},
    "input_artifacts": [{"content": "test input", "kind": "text"}],
    "model_policy": {"requires_model": False, "latency_mode": "interactive",
                     "quality_target": "standard", "resource_profile": "standard_local"},
    "output_contract": {"candidate_only": True, "app_owned_apply": True,
                        "may_apply": False, "kind": "candidate_artifact_bundle"},
    "protocol_version": "7.1",
    "work_id": "WORK-SDK-TEST-001",
    "work_intent": {"goal": "classify_test", "kind": "classify", "requires_model": False},
}


def test_v1_universal_work_candidate_only(api_server):
    status, body = post(api_server, "/v1/universal-work", {"work": VALID_WORK_PAYLOAD})
    assert status == 200
    assert body.get("candidate_only") is True
    assert body.get("app_owned_apply") is True
    assert body.get("external_send_default") is False
    assert "proof_boundaries" in body
    assert "not_app_state_mutation_proof" in body["proof_boundaries"]


def test_v1_sessions_not_found(api_server):
    status, body = get(api_server, "/v1/sessions/NONEXISTENT-SESSION-ID")
    assert status == 404
    assert body.get("error") is True
    assert body.get("code") == "session_not_found"
    assert body.get("candidate_only") is True


def test_v1_candidates_not_found(api_server):
    status, body = get(api_server, "/v1/candidates/NONEXISTENT-CAND-ID")
    assert status == 404
    assert body.get("error") is True
    assert body.get("code") == "candidate_not_found"
    assert body.get("candidate_only") is True


def test_v1_events_positive(api_server):
    status, body = get(api_server, "/v1/events")
    assert status == 200
    assert body["artifact_kind"] == "odin_localhost_api_events"
    assert isinstance(body["events"], list)
    assert body["candidate_only"] is True
    assert body["local_only"] is True


def test_v1_proof_gaps_positive(api_server):
    status, body = get(api_server, "/v1/proof-gaps")
    assert status == 200
    assert body["artifact_kind"] == "odin_localhost_api_proof_gaps"
    assert isinstance(body["proof_boundaries"], list)
    assert isinstance(body["known_gaps"], list)
    assert body["candidate_only"] is True
    assert "not_production_readiness_certification" in body["proof_boundaries"]
    assert "not_live_model_inference_proof" in body["proof_boundaries"]
    assert "not_app_state_mutation_proof" in body["proof_boundaries"]
    assert "not_external_send_authority_proof" in body["proof_boundaries"]


def test_structured_error_shape(api_server):
    status, body = get(api_server, "/v1/unknown-endpoint-xyz")
    assert status == 404
    assert body.get("error") is True
    assert "code" in body
    assert "message" in body
    assert body.get("candidate_only") is True
    assert "claim_boundary" in body
    assert "traceback" not in body
    assert "secret" not in str(body).lower()


# ---------------------------------------------------------------------------
# Forbidden endpoint tests
# ---------------------------------------------------------------------------

def test_no_apply_endpoint(api_server):
    status, body = get(api_server, "/v1/apply")
    assert status == 404
    status2, body2 = post(api_server, "/v1/apply", {})
    assert status2 == 404


def test_no_external_send_endpoint(api_server):
    status, body = get(api_server, "/v1/external-send")
    assert status == 404
    status2, body2 = post(api_server, "/v1/external-send", {})
    assert status2 == 404


def test_no_provider_credentials_endpoint(api_server):
    status, body = post(api_server, "/v1/provider-credentials", {})
    assert status == 404


def test_no_raw_app_state_to_model_endpoint(api_server):
    status, body = post(api_server, "/v1/raw-app-state-to-model", {})
    assert status == 404


def test_no_network_enable_endpoint(api_server):
    status, body = post(api_server, "/v1/network-enable", {})
    assert status == 404


# ---------------------------------------------------------------------------
# Localhost-only binding tests
# ---------------------------------------------------------------------------

def test_localhost_only_default_binding():
    from odin.daemon.local_api import run_local_api
    with pytest.raises(ValueError, match="localhost"):
        run_local_api("0.0.0.0", 19999, once_smoke=True)


def test_localhost_only_blocks_wan():
    from odin.daemon.local_api import run_local_api
    with pytest.raises(ValueError):
        run_local_api("192.168.1.1", 19998, once_smoke=True)


def test_local_api_accepts_127_0_0_1():
    from odin.daemon.local_api import run_local_api
    result = run_local_api("127.0.0.1", 0, once_smoke=True)
    assert result["status"] == "ok"


# ---------------------------------------------------------------------------
# SDK client tests
# ---------------------------------------------------------------------------

def test_sdk_rejects_non_localhost_base_url():
    from odin_app_sdk.client import OdinClient, OdinSDKBoundaryError
    with pytest.raises(OdinSDKBoundaryError):
        OdinClient("http://192.168.1.100:8877")


def test_sdk_rejects_public_base_url():
    from odin_app_sdk.client import OdinClient, OdinSDKBoundaryError
    with pytest.raises(OdinSDKBoundaryError):
        OdinClient("http://example.com:8877")


def test_sdk_allows_localhost_127():
    from odin_app_sdk.client import OdinClient
    client = OdinClient("http://127.0.0.1:8877")
    assert "127.0.0.1" in client.base_url


def test_sdk_allows_localhost_name():
    from odin_app_sdk.client import OdinClient
    client = OdinClient("http://localhost:8877")
    assert "localhost" in client.base_url


def test_sdk_health_check(api_server):
    from odin_app_sdk.client import OdinClient
    client = OdinClient(f"http://127.0.0.1:{api_server}")
    result = client.health()
    assert result["status"] == "ok"
    assert result["candidate_only"] is True


def test_sdk_status(api_server):
    from odin_app_sdk.client import OdinClient
    client = OdinClient(f"http://127.0.0.1:{api_server}")
    result = client.status()
    assert result["artifact_kind"] == "odin_localhost_api_status"
    assert result["candidate_only"] is True


def test_sdk_providers(api_server):
    from odin_app_sdk.client import OdinClient
    client = OdinClient(f"http://127.0.0.1:{api_server}")
    result = client.providers()
    assert isinstance(result["providers"], list)


def test_sdk_submit_universal_work(api_server):
    from odin_app_sdk.client import OdinClient
    client = OdinClient(f"http://127.0.0.1:{api_server}")
    result = client.submit_universal_work(VALID_WORK_PAYLOAD)
    assert result.get("candidate_only") is True
    assert result.get("app_owned_apply") is True


def test_sdk_get_candidate_not_found(api_server):
    from odin_app_sdk.client import OdinClient, OdinClientError
    client = OdinClient(f"http://127.0.0.1:{api_server}")
    with pytest.raises(OdinClientError):
        client.get_candidate("NONEXISTENT-CAND-ID-SDK")


def test_sdk_proof_gaps(api_server):
    from odin_app_sdk.client import OdinClient
    client = OdinClient(f"http://127.0.0.1:{api_server}")
    result = client.proof_gaps()
    assert "proof_boundaries" in result
    assert "not_production_readiness_certification" in result["proof_boundaries"]
    assert "not_live_model_inference_proof" in result["proof_boundaries"]


def test_sdk_events(api_server):
    from odin_app_sdk.client import OdinClient
    client = OdinClient(f"http://127.0.0.1:{api_server}")
    result = client.events()
    assert isinstance(result["events"], list)


def test_sdk_no_apply_method():
    from odin_app_sdk.client import OdinClient
    client = OdinClient.__new__(OdinClient)
    assert not hasattr(client, "apply")


def test_sdk_no_external_send_method():
    from odin_app_sdk.client import OdinClient
    client = OdinClient.__new__(OdinClient)
    assert not hasattr(client, "external_send")


# ---------------------------------------------------------------------------
# Python SDK bridge module tests
# ---------------------------------------------------------------------------

def test_sdk_bridge_rejects_non_localhost():
    from sdk.python.odin_client import OdinSDKClient, OdinSDKBoundaryError
    with pytest.raises(OdinSDKBoundaryError):
        OdinSDKClient("http://192.168.1.1:8877")


def test_sdk_bridge_allows_localhost():
    from sdk.python.odin_client import OdinSDKClient
    client = OdinSDKClient("http://127.0.0.1:8877")
    assert "127.0.0.1" in client.base_url


def test_sdk_bridge_proof_boundaries():
    from sdk.python.odin_client import SDK_BRIDGE_PROOF_BOUNDARIES
    assert "not_production_readiness_certification" in SDK_BRIDGE_PROOF_BOUNDARIES
    assert "not_live_model_inference_proof" in SDK_BRIDGE_PROOF_BOUNDARIES
    assert "not_app_state_mutation_proof" in SDK_BRIDGE_PROOF_BOUNDARIES
    assert "not_external_send_authority_proof" in SDK_BRIDGE_PROOF_BOUNDARIES


def test_sdk_bridge_no_apply_method():
    from sdk.python.odin_client import OdinSDKClient
    assert not hasattr(OdinSDKClient, "apply")


def test_sdk_bridge_no_external_send_method():
    from sdk.python.odin_client import OdinSDKClient
    assert not hasattr(OdinSDKClient, "external_send")


def test_sdk_bridge_health(api_server):
    from sdk.python.odin_client import OdinSDKClient
    client = OdinSDKClient(f"http://127.0.0.1:{api_server}")
    result = client.health()
    assert result["status"] == "ok"


def test_sdk_bridge_submit_work(api_server):
    from sdk.python.odin_client import OdinSDKClient
    client = OdinSDKClient(f"http://127.0.0.1:{api_server}")
    result = client.submit_universal_work(VALID_WORK_PAYLOAD)
    assert result.get("candidate_only") is True


def test_sdk_bridge_proof_gaps_endpoint(api_server):
    from sdk.python.odin_client import OdinSDKClient
    client = OdinSDKClient(f"http://127.0.0.1:{api_server}")
    result = client.proof_gaps()
    assert "proof_boundaries" in result
    assert "known_gaps" in result


# ---------------------------------------------------------------------------
# Schema fixture validation
# ---------------------------------------------------------------------------

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_health_schema_parses():
    schema = load_json(ROOT / "schemas/v7_1/localhost_api_health.schema.json")
    assert schema["title"] == "Odin Localhost API Health Response"


def test_status_schema_parses():
    schema = load_json(ROOT / "schemas/v7_1/localhost_api_status.schema.json")
    assert "candidate_only" in schema["properties"]


def test_providers_schema_parses():
    schema = load_json(ROOT / "schemas/v7_1/localhost_api_providers.schema.json")
    assert "providers" in schema["properties"]


def test_universal_work_request_schema_parses():
    schema = load_json(ROOT / "schemas/v7_1/localhost_api_universal_work_request.schema.json")
    assert "work" in schema["required"]


def test_universal_work_response_schema_parses():
    schema = load_json(ROOT / "schemas/v7_1/localhost_api_universal_work_response.schema.json")
    assert "candidate_only" in schema["required"]
    assert "app_owned_apply" in schema["required"]


def test_session_schema_parses():
    schema = load_json(ROOT / "schemas/v7_1/localhost_api_session.schema.json")
    assert "candidate_only" in schema["required"]


def test_candidate_schema_parses():
    schema = load_json(ROOT / "schemas/v7_1/localhost_api_candidate.schema.json")
    assert "app_owned_apply" in schema["required"]


def test_events_schema_parses():
    schema = load_json(ROOT / "schemas/v7_1/localhost_api_events.schema.json")
    assert "local_only" in schema["required"]


def test_proof_gaps_schema_parses():
    schema = load_json(ROOT / "schemas/v7_1/localhost_api_proof_gaps.schema.json")
    assert "proof_boundaries" in schema["required"]
    assert "known_gaps" in schema["required"]


def test_error_schema_parses():
    schema = load_json(ROOT / "schemas/v7_1/localhost_api_error.schema.json")
    assert schema["properties"]["error"]["const"] is True
    assert "code" in schema["required"]
    assert "message" in schema["required"]


# ---------------------------------------------------------------------------
# Example fixture validation
# ---------------------------------------------------------------------------

def test_health_fixture_valid():
    fixture = load_json(ROOT / "examples/sdk_bridge/health_response.valid.json")
    assert fixture["artifact_kind"] == "odin_localhost_api_health"
    assert fixture["candidate_only"] is True
    assert fixture["app_owned_apply"] is True
    assert fixture["external_send_default"] is False


def test_status_fixture_valid():
    fixture = load_json(ROOT / "examples/sdk_bridge/status_response.valid.json")
    assert fixture["candidate_only"] is True
    assert fixture["app_owned_apply"] is True


def test_providers_fixture_valid():
    fixture = load_json(ROOT / "examples/sdk_bridge/providers_response.valid.json")
    assert isinstance(fixture["providers"], list)
    assert fixture["candidate_only"] is True


def test_universal_work_request_fixture_valid():
    fixture = load_json(ROOT / "examples/sdk_bridge/universal_work_request.valid.json")
    assert "work" in fixture
    assert fixture["work"]["output_contract"]["candidate_only"] is True
    assert fixture["work"]["output_contract"]["app_owned_apply"] is True
    assert fixture["work"]["output_contract"]["may_apply"] is False


def test_universal_work_response_fixture_valid():
    fixture = load_json(ROOT / "examples/sdk_bridge/universal_work_response.valid.json")
    assert fixture["candidate_only"] is True
    assert fixture["app_owned_apply"] is True
    assert fixture["external_send_default"] is False
    assert "proof_boundaries" in fixture


def test_session_fixture_valid():
    fixture = load_json(ROOT / "examples/sdk_bridge/session_response.valid.json")
    assert fixture["candidate_only"] is True


def test_candidate_fixture_valid():
    fixture = load_json(ROOT / "examples/sdk_bridge/candidate_response.valid.json")
    assert fixture["candidate_only"] is True
    assert fixture["app_owned_apply"] is True


def test_events_fixture_valid():
    fixture = load_json(ROOT / "examples/sdk_bridge/events_response.valid.json")
    assert fixture["candidate_only"] is True
    assert fixture["local_only"] is True


def test_proof_gaps_fixture_valid():
    fixture = load_json(ROOT / "examples/sdk_bridge/proof_gaps_response.valid.json")
    assert "not_production_readiness_certification" in fixture["proof_boundaries"]
    assert "not_live_model_inference_proof" in fixture["proof_boundaries"]
    assert fixture["candidate_only"] is True


def test_error_fixture_valid():
    fixture = load_json(ROOT / "examples/sdk_bridge/error_response.valid.json")
    assert fixture["error"] is True
    assert "code" in fixture
    assert "message" in fixture
    assert fixture["candidate_only"] is True


# ---------------------------------------------------------------------------
# Documentation claim boundary tests
# ---------------------------------------------------------------------------

def test_localhost_api_contract_doc_exists():
    doc = ROOT / "docs/LOCALHOST_API_CONTRACT_V1.md"
    assert doc.exists(), "docs/LOCALHOST_API_CONTRACT_V1.md must exist"


def test_localhost_api_contract_no_public_network_claim():
    doc = (ROOT / "docs/LOCALHOST_API_CONTRACT_V1.md").read_text(encoding="utf-8")
    assert "not a public network API" in doc.lower() or "This is not a public network API" in doc


def test_localhost_api_contract_no_apply_claim():
    doc = (ROOT / "docs/LOCALHOST_API_CONTRACT_V1.md").read_text(encoding="utf-8")
    assert "no apply endpoint" in doc.lower() or "does not grant app apply authority" in doc.lower()


def test_sdk_bridge_doc_exists():
    doc = ROOT / "docs/SDK_BRIDGE_V1.md"
    assert doc.exists(), "docs/SDK_BRIDGE_V1.md must exist"


def test_sdk_bridge_doc_no_public_network_claim():
    doc = (ROOT / "docs/SDK_BRIDGE_V1.md").read_text(encoding="utf-8")
    assert "not a public network" in doc.lower() or "This is not a public network API" in doc


def test_sdk_bridge_doc_no_apply_claim():
    doc = (ROOT / "docs/SDK_BRIDGE_V1.md").read_text(encoding="utf-8")
    assert "no apply" in doc.lower() or "does not grant app apply authority" in doc.lower()


def test_sdk_bridge_doc_no_external_send_claim():
    doc = (ROOT / "docs/SDK_BRIDGE_V1.md").read_text(encoding="utf-8")
    assert "does not send externally" in doc.lower() or "no external send" in doc.lower()


def test_sdk_bridge_doc_proof_boundaries():
    doc = (ROOT / "docs/SDK_BRIDGE_V1.md").read_text(encoding="utf-8")
    assert "not_production_readiness" in doc or "production readiness" in doc.lower()
    assert "not_live_model_inference_proof" in doc or "live model inference" in doc.lower()


# ---------------------------------------------------------------------------
# v1 API claim boundary checks in responses
# ---------------------------------------------------------------------------

def test_v1_responses_have_claim_boundary(api_server):
    for path in ["/v1/health", "/v1/status", "/v1/providers", "/v1/events", "/v1/proof-gaps"]:
        status, body = get(api_server, path)
        assert status == 200, f"Expected 200 for {path}, got {status}"
        assert "claim_boundary" in body, f"claim_boundary missing from {path} response"


def test_v1_universal_work_response_has_proof_boundaries(api_server):
    status, body = post(api_server, "/v1/universal-work", {"work": VALID_WORK_PAYLOAD})
    assert status == 200
    assert "proof_boundaries" in body
    for boundary in [
        "not_production_readiness_certification",
        "not_live_model_inference_proof",
        "not_app_state_mutation_proof",
        "not_external_send_authority_proof",
    ]:
        assert boundary in body["proof_boundaries"], f"Missing proof boundary: {boundary}"
