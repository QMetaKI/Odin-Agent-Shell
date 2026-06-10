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
FORBIDDEN_ROUTES = {
    "/v7/apply", "/v7/app-apply", "/v7/external-send", "/v7/app/state",
    "/v1/apply", "/v1/app-apply", "/v1/external-send", "/v1/app/state",
    "/v1/network-enable", "/v1/provider-credentials", "/v1/raw-app-state-to-model",
}

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


def structured_error(status: str, message: str, *, code: str = "local_api_error") -> dict:
    return {
        "error": True,
        "artifact_kind": "odin_local_api_error",
        "protocol_version": "7.1",
        "status": status,
        "code": code,
        "error_code": code,  # backward-compat alias
        "message": message,
        "details": {},
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

    def _route_v1_get(self, path: str):
        if path == '/v1/health':
            self._send(200, {
                "artifact_kind": "odin_localhost_api_health",
                "protocol_version": "7.1",
                "status": "ok",
                "runtime": "candidate",
                "network_scope": "localhost_only",
                "version": "0.8.7",
                "candidate_only": True,
                "app_owned_apply": True,
                "external_send_default": False,
            })
        elif path == '/v1/status':
            store_status = self.runtime.store.status()
            store_status.update({
                "artifact_kind": "odin_localhost_api_status",
                "candidate_only": True,
                "app_owned_apply": True,
                "external_send_default": False,
            })
            self._send(200, store_status)
        elif path == '/v1/providers':
            self._send(200, {
                "artifact_kind": "odin_localhost_api_providers",
                "protocol_version": "7.1",
                "providers": list_provider_cards(),
                "candidate_only": True,
                "claim_boundary": "provider_cards_not_live_provider_proof",
            })
        elif path.startswith('/v1/sessions/'):
            session_id = path[len('/v1/sessions/'):]
            if not session_id:
                self._send(400, structured_error("blocked", "session_id required", code="missing_session_id"))
                return
            record = self.runtime.store.read_session(session_id)
            if record.get("status") == "missing":
                self._send(404, structured_error("not_found", f"session {session_id!r} not found", code="session_not_found"))
                return
            record.update({
                "artifact_kind": "odin_localhost_api_session",
                "candidate_only": True,
            })
            self._send(200, record)
        elif path.startswith('/v1/candidates/'):
            candidate_id = path[len('/v1/candidates/'):]
            if not candidate_id:
                self._send(400, structured_error("blocked", "candidate_id required", code="missing_candidate_id"))
                return
            record = self.runtime.store.read_candidate(candidate_id)
            if record.get("status") == "missing":
                self._send(404, structured_error("not_found", f"candidate {candidate_id!r} not found", code="candidate_not_found"))
                return
            record.update({
                "artifact_kind": "odin_localhost_api_candidate",
                "candidate_only": True,
                "app_owned_apply": True,
            })
            self._send(200, record)
        elif path == '/v1/events':
            self._send(200, {
                "artifact_kind": "odin_localhost_api_events",
                "protocol_version": "7.1",
                "events": self.runtime.store.list_bus_events(),
                "candidate_only": True,
                "local_only": True,
            })
        elif path == '/v1/proof-gaps':
            self._send(200, {
                "artifact_kind": "odin_localhost_api_proof_gaps",
                "protocol_version": "7.1",
                "proof_boundaries": SDK_BRIDGE_PROOF_BOUNDARIES,
                "known_gaps": [
                    "no_live_model_inference_proof",
                    "no_production_readiness_proof",
                    "no_public_network_api_proof",
                    "no_app_state_mutation_proof",
                    "no_external_send_authority_proof",
                    "no_provider_credential_proof",
                    "no_windows_host_proof",
                    "no_security_certification",
                ],
                "candidate_only": True,
                "note": (
                    "This endpoint exposes known proof gaps. "
                    "It does not claim production readiness, live model inference, "
                    "public network access, or app-state mutation authority."
                ),
            })
        else:
            self._send(404, structured_error("blocked", "unsupported v1 route", code="not_found"))

    def do_GET(self):
        if self.path in FORBIDDEN_ROUTES:
            self._send(404, structured_error("blocked", "route not exposed by Odin local API", code="route_not_exposed"))
            return
        if self.path.startswith('/v1/'):
            self._route_v1_get(self.path)
            return
        # v7 routes (backward compatibility)
        if self.path == '/v7/health':
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
            if self.path == '/v1/universal-work':
                work = payload.get('work', payload)
                result = self.runtime.run_universal_work(
                    work,
                    caller_manifest=payload.get('caller_manifest'),
                    seed_pack=payload.get('seed_pack'),
                    pattern_mine=payload.get('pattern_mine'),
                )
                result.setdefault("candidate_only", True)
                result.setdefault("app_owned_apply", True)
                result.setdefault("external_send_default", False)
                result.setdefault("proof_boundaries", SDK_BRIDGE_PROOF_BOUNDARIES)
                self._send(200, result)
            elif self.path == '/v7/universal-work/run':
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
