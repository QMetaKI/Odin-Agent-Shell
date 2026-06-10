"""Odin SDK Bridge v1 — Python client.

candidate_only: True
app_owned_apply: True
external_send_default: False
localhost_only: True

This SDK bridge allows host apps to:
- Health-check Odin
- Read status and providers
- Submit Universal Work (candidate-only result)
- Read Candidate Artifacts
- Read Sessions
- Read local events
- Read proof gaps

It does NOT provide:
- apply() method
- external_send() method
- provider credential defaults
- WAN/LAN network access
- live model inference
- app-state mutation
"""
from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

_LOCALHOST_ADDRS = frozenset({"127.0.0.1", "localhost", "::1"})

SDK_BRIDGE_CLAIM_BOUNDARY = (
    "sdk_bridge_v1_candidate_only_no_app_apply_no_external_send_"
    "no_wan_lan_no_provider_credentials_no_live_model_proof"
)

SDK_BRIDGE_PROOF_BOUNDARIES = [
    "not_production_readiness_certification",
    "not_windows_service_tray_installer_proof",
    "not_signed_installer_proof",
    "not_live_model_inference_proof",
    "not_model_quality_proof",
    "not_security_certification",
    "not_public_network_api_proof",
    "not_app_state_mutation_proof",
    "not_external_send_authority_proof",
    "not_provider_credential_proof",
]


class OdinSDKError(RuntimeError):
    """Structured error from Odin SDK Bridge."""

    def __init__(self, message: str, *, code: str = "sdk_error", details: dict | None = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}
        self.candidate_only = True
        self.claim_boundary = SDK_BRIDGE_CLAIM_BOUNDARY


class OdinSDKBoundaryError(OdinSDKError):
    """Raised when a request violates Odin boundary rules (e.g., non-localhost URL)."""


def _check_localhost_url(base_url: str) -> None:
    parsed = urlparse(base_url)
    hostname = (parsed.hostname or "").lower().strip("[]")
    if hostname not in _LOCALHOST_ADDRS:
        raise OdinSDKBoundaryError(
            f"OdinSDKClient base_url must resolve to localhost (got {hostname!r}). "
            "The SDK Bridge is localhost-only by default.",
            code="non_localhost_url_blocked",
        )


class OdinSDKClient:
    """Odin SDK Bridge v1 client.

    candidate_only: True
    app_owned_apply: True
    no apply() method
    no external_send() method
    no provider credentials
    localhost-only by default
    """

    def __init__(self, base_url: str = "http://127.0.0.1:8877", *, allow_non_localhost: bool = False, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        if not allow_non_localhost:
            _check_localhost_url(self.base_url)

    def health(self) -> dict:
        """GET /v1/health — returns runtime health status (candidate-only)."""
        return self._request("GET", "/v1/health")

    def status(self) -> dict:
        """GET /v1/status — returns runtime store status (candidate-only)."""
        return self._request("GET", "/v1/status")

    def providers(self) -> dict:
        """GET /v1/providers — returns provider card list (candidate-only, not live inference proof)."""
        return self._request("GET", "/v1/providers")

    def submit_universal_work(
        self,
        work: dict,
        *,
        caller_manifest: dict | None = None,
        seed_pack: dict | None = None,
        pattern_mine: dict | None = None,
    ) -> dict:
        """POST /v1/universal-work — submit work, receive candidate-only result.

        Returns a candidate artifact. Does NOT apply app state.
        Does NOT send externally. App owns apply/state/external-send.
        """
        payload: dict = {"work": work}
        if caller_manifest is not None:
            payload["caller_manifest"] = caller_manifest
        if seed_pack is not None:
            payload["seed_pack"] = seed_pack
        if pattern_mine is not None:
            payload["pattern_mine"] = pattern_mine
        return self._request("POST", "/v1/universal-work", payload)

    def get_session(self, session_id: str) -> dict:
        """GET /v1/sessions/{id} — read session record (candidate-only)."""
        return self._request("GET", f"/v1/sessions/{session_id}")

    def get_candidate(self, candidate_id: str) -> dict:
        """GET /v1/candidates/{id} — read candidate artifact (candidate-only, app owns apply)."""
        return self._request("GET", f"/v1/candidates/{candidate_id}")

    def events(self) -> dict:
        """GET /v1/events — read local bus events (candidate-only, local-only)."""
        return self._request("GET", "/v1/events")

    def proof_gaps(self) -> dict:
        """GET /v1/proof-gaps — read known proof gaps summary."""
        return self._request("GET", "/v1/proof-gaps")

    def _request(self, method: str, path: str, payload: dict | None = None) -> dict:
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        req = Request(self.base_url + path, data=body, method=method, headers=headers)
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data
        except HTTPError as exc:
            try:
                error_body = json.loads(exc.read().decode("utf-8"))
                raise OdinSDKError(
                    error_body.get("message", str(exc)),
                    code=error_body.get("code", "http_error"),
                    details=error_body,
                ) from exc
            except (json.JSONDecodeError, AttributeError):
                raise OdinSDKError(str(exc), code="http_error") from exc
        except (URLError, TimeoutError) as exc:
            raise OdinSDKError(str(exc), code="connection_error") from exc
