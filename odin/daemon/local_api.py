from __future__ import annotations
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
from odin.runtime.engine import OdinRuntime
from odin.runtime.store import RuntimeStore
from odin.seeds.compiler import compile_seed_pack
from odin.patterns.intake import compile_pattern_mine
from odin.flow_packs.compiler import compile_flow_packs
from odin.models.providers.registry import list_provider_cards
from odin.hub.static_hub import build_hub_snapshot
from odin.recovery.safe_mode import build_safe_mode_plan
from odin.work_atoms.runtime import WorkAtomRuntime

LOCAL_API_CLAIM_BOUNDARY = "local_api_candidate_only_no_app_apply_no_external_send_no_wan_lan_claim"
FORBIDDEN_ROUTES = {"/v7/apply", "/v7/app-apply", "/v7/external-send", "/v7/app/state"}


def structured_error(status: str, message: str, *, code: str = "local_api_error") -> dict:
    return {
        "artifact_kind": "odin_local_api_error",
        "protocol_version": "7.1",
        "status": status,
        "error_code": code,
        "error": message,
        "candidate_only": True,
        "claim_boundary": LOCAL_API_CLAIM_BOUNDARY,
    }


class OdinLocalHandler(BaseHTTPRequestHandler):
    runtime = OdinRuntime(store=RuntimeStore())

    def log_message(self, fmt, *args):
        return

    def _send(self, status: int, payload: dict):
        payload.setdefault("claim_boundary", LOCAL_API_CLAIM_BOUNDARY)
        body = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json_body(self) -> tuple[dict | None, dict | None]:
        try:
            length = int(self.headers.get('Content-Length', '0'))
        except ValueError:
            return None, structured_error("blocked", "invalid content length", code="invalid_content_length")
        raw = self.rfile.read(length).decode('utf-8') if length else '{}'
        try:
            payload = json.loads(raw or '{}')
        except json.JSONDecodeError as exc:
            return None, structured_error("blocked", f"malformed JSON body: {exc.msg}", code="malformed_json")
        if not isinstance(payload, dict):
            return None, structured_error("blocked", "JSON body must be an object", code="invalid_json_shape")
        return payload, None

    def do_GET(self):
        if self.path in FORBIDDEN_ROUTES:
            self._send(404, structured_error("blocked", "route not exposed by Odin local API", code="route_not_exposed"))
        elif self.path == '/v7/health':
            self._send(200, {"artifact_kind": "odin_local_api_health", "status": "ok", "runtime": "candidate", "network_scope": "localhost_only", "version": "0.8.7"})
        elif self.path == '/v7/store/status':
            self._send(200, self.runtime.store.status())
        elif self.path == '/v7/providers':
            self._send(200, {"artifact_kind": "odin_provider_cards", "providers": list_provider_cards(), "claim_boundary": "provider_cards_not_live_provider_proof"})
        elif self.path == '/v7/hub/snapshot':
            self._send(200, build_hub_snapshot(self.runtime.store.status()))
        elif self.path == '/v7/recovery/safe-mode-plan':
            self._send(200, build_safe_mode_plan("api_request"))
        elif self.path == '/v7/bus/events':
            self._send(200, {"artifact_kind": "odin_local_bus_event_list", "events": self.runtime.store.list_bus_events(), "candidate_only": True})
        elif self.path == '/v7/worklets/registry':
            self._send(200, {"artifact_kind": "odin_worklet_registry_view", "max_total_atoms": WorkAtomRuntime().max_total_atoms, "candidate_only": True})
        else:
            self._send(404, structured_error("blocked", "unsupported route", code="not_found"))

    def do_POST(self):
        if self.path in FORBIDDEN_ROUTES:
            self._send(404, structured_error("blocked", "route not exposed by Odin local API", code="route_not_exposed"))
            return
        payload, err = self._json_body()
        if err:
            self._send(400, err)
            return
        assert payload is not None
        try:
            if self.path == '/v7/universal-work/run':
                work = payload.get('work', payload)
                result = self.runtime.run_universal_work(work, caller_manifest=payload.get('caller_manifest'), seed_pack=payload.get('seed_pack'), pattern_mine=payload.get('pattern_mine'))
                self._send(200, result)
            elif self.path == '/v7/seed-packs/compile':
                self._send(200, compile_seed_pack(payload.get('seed_pack', payload), payload.get('work')))
            elif self.path == '/v7/pattern-mines/compile':
                self._send(200, compile_pattern_mine(payload.get('pattern_mine', payload)))
            elif self.path == '/v7/flow-packs/compile':
                self._send(200, {"artifact_kind": "odin_compiled_flow_pack_set", "flow_packs": compile_flow_packs(payload.get('flow_packs', [])), "candidate_only": True})
            else:
                self._send(404, structured_error("blocked", "unsupported route", code="not_found"))
        except Exception as exc:
            self._send(400, structured_error("blocked", str(exc), code="request_blocked"))


def create_app():
    return OdinLocalHandler


def run_local_api(host: str = '127.0.0.1', port: int = 8765, *, once_smoke: bool = False):
    if host not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("local API only binds localhost by default; WAN/LAN hosts are not enabled")
    server = HTTPServer((host, port), OdinLocalHandler)
    if once_smoke:
        server.server_close()
        return {"artifact_kind": "odin_local_api_smoke", "status": "ok", "host": host, "port": port, "claim_boundary": LOCAL_API_CLAIM_BOUNDARY}
    try:
        server.serve_forever()
    finally:
        server.server_close()
