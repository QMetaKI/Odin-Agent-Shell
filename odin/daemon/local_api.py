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

class OdinLocalHandler(BaseHTTPRequestHandler):
    runtime = OdinRuntime(store=RuntimeStore())

    def log_message(self, fmt, *args):
        return

    def _send(self, status: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json_body(self) -> dict:
        length = int(self.headers.get('Content-Length', '0'))
        return json.loads(self.rfile.read(length).decode('utf-8') or '{}')

    def do_GET(self):
        if self.path == '/v7/health':
            self._send(200, {"status": "ok", "runtime": "candidate", "network_scope": "localhost_only", "version": "0.8.6"})
        elif self.path == '/v7/store/status':
            self._send(200, self.runtime.store.status())
        elif self.path == '/v7/providers':
            self._send(200, {"artifact_kind": "odin_provider_cards", "providers": list_provider_cards(), "claim_boundary": "provider_cards_not_live_provider_proof"})
        elif self.path == '/v7/hub/snapshot':
            self._send(200, build_hub_snapshot(self.runtime.store.status()))
        elif self.path == '/v7/recovery/safe-mode-plan':
            self._send(200, build_safe_mode_plan("api_request"))
        else:
            self._send(404, {"error": "not_found"})

    def do_POST(self):
        try:
            payload = self._json_body()
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
                self._send(404, {"error": "not_found"})
        except Exception as exc:
            self._send(400, {"error": str(exc), "claim_boundary": "local_api_error_no_apply"})

def create_app():
    return OdinLocalHandler

def run_local_api(host: str = '127.0.0.1', port: int = 8765):
    server = HTTPServer((host, port), OdinLocalHandler)
    try:
        server.serve_forever()
    finally:
        server.server_close()
