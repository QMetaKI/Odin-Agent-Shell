from __future__ import annotations
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

class OdinClientError(RuntimeError):
    pass

class OdinClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8765"):
        self.base_url = base_url.rstrip("/")

    def health(self) -> dict:
        return self._request("GET", "/v7/health")

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
