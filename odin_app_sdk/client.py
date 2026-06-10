from __future__ import annotations
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

_LOCALHOST_ADDRS = {"127.0.0.1", "localhost", "::1"}

class OdinClientError(RuntimeError):
    pass

class OdinSDKBoundaryError(ValueError):
    pass


def _check_localhost_url(base_url: str) -> None:
    from urllib.parse import urlparse
    parsed = urlparse(base_url)
    hostname = (parsed.hostname or "").lower().strip("[]")
    if hostname not in _LOCALHOST_ADDRS:
        raise OdinSDKBoundaryError(
            f"OdinClient base_url must be localhost (got {hostname!r}). "
            "Odin SDK Bridge is localhost-only by default."
        )


class OdinClient:
    """SDK Bridge v1 client for Odin localhost API.

    candidate_only: True — This client reads candidates and submits work.
    No apply(), no external_send(), no provider credentials.
    """

    def __init__(self, base_url: str = "http://127.0.0.1:8877", *, allow_non_localhost: bool = False):
        self.base_url = base_url.rstrip("/")
        if not allow_non_localhost:
            _check_localhost_url(self.base_url)

    def health(self) -> dict:
        return self._request("GET", "/v1/health")

    def status(self) -> dict:
        return self._request("GET", "/v1/status")

    def providers(self) -> dict:
        return self._request("GET", "/v1/providers")

    def submit_universal_work(
        self,
        work: dict,
        *,
        caller_manifest: dict | None = None,
        seed_pack: dict | None = None,
        pattern_mine: dict | None = None,
    ) -> dict:
        payload: dict = {"work": work}
        if caller_manifest is not None:
            payload["caller_manifest"] = caller_manifest
        if seed_pack is not None:
            payload["seed_pack"] = seed_pack
        if pattern_mine is not None:
            payload["pattern_mine"] = pattern_mine
        return self._request("POST", "/v1/universal-work", payload)

    def get_session(self, session_id: str) -> dict:
        return self._request("GET", f"/v1/sessions/{session_id}")

    def get_candidate(self, candidate_id: str) -> dict:
        return self._request("GET", f"/v1/candidates/{candidate_id}")

    def events(self) -> dict:
        return self._request("GET", "/v1/events")

    def proof_gaps(self) -> dict:
        return self._request("GET", "/v1/proof-gaps")

    # Backward-compatibility aliases (v7 routes)
    def run_work(self, work: dict, *, caller_manifest: dict, seed_pack: dict | None = None, pattern_mine: dict | None = None) -> dict:
        payload = {"work": work, "caller_manifest": caller_manifest}
        if seed_pack is not None:
            payload["seed_pack"] = seed_pack
        if pattern_mine is not None:
            payload["pattern_mine"] = pattern_mine
        return self._request("POST", "/v7/universal-work/run", payload)

    def _request(self, method: str, path: str, payload: dict | None = None) -> dict:
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        req = Request(self.base_url + path, data=body, method=method, headers={"Content-Type": "application/json"})
        try:
            with urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError) as exc:
            raise OdinClientError(str(exc)) from exc
