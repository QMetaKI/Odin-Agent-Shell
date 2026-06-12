"""Simple Local Hub HTTP server — FINAL-PR-01.

Claim boundary: simple_local_hub_localhost_only_candidate_no_app_apply_no_external_send_no_provider_execution

Python stdlib only — no external dependencies.
Default: host=127.0.0.1, port=8765
Endpoints: GET /, GET /status.json, GET /healthz
"""
from __future__ import annotations

import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

from odin.local_hub.policy import check_host, CLAIM_BOUNDARY
from odin.local_hub.ui import generate_hub_html, generate_status_json, REQUIRED_IDS

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765


class _SimpleLocalHubHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            body = b'{"status":"ok","hub":"simple_local_hub"}'
            self._respond(200, "application/json", body)
        elif self.path == "/status.json":
            body = generate_status_json().encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path in ("/", "/index.html"):
            body = generate_hub_html().encode("utf-8")
            self._respond(200, "text/html; charset=utf-8", body)
        else:
            body = b'{"status":"not_found"}'
            self._respond(404, "application/json", body)

    def _respond(self, code: int, content_type: str, body: bytes) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass  # suppress request logs in tests/smoke


def run_once_smoke(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> dict:
    """Start server, smoke-test /healthz and /, shut down cleanly. Does not hang.

    Uses port=0 for ephemeral OS-assigned port when port argument is 0.
    """
    ok, reason = check_host(host)
    if not ok:
        return {
            "status": "blocked",
            "error": reason,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    steps: list[dict] = []
    server = HTTPServer((host, port), _SimpleLocalHubHandler)
    actual_port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    base = f"http://{host}:{actual_port}"
    try:
        # Smoke /healthz
        try:
            resp = urllib.request.urlopen(f"{base}/healthz", timeout=5)
            healthz_body = resp.read().decode()
            healthz_ok = '"status"' in healthz_body
            steps.append({
                "step": "healthz",
                "status": "ok" if healthz_ok else "failed",
                "body_preview": healthz_body[:100],
            })
        except Exception as exc:
            steps.append({"step": "healthz", "status": "error", "error": str(exc)})

        # Smoke / and verify UI markers
        try:
            resp = urllib.request.urlopen(f"{base}/", timeout=5)
            html_body = resp.read().decode()
            missing = [id_ for id_ in REQUIRED_IDS if f'id="{id_}"' not in html_body]
            ui_ok = not missing
            steps.append({
                "step": "ui_markers",
                "status": "ok" if ui_ok else "failed",
                "missing_ids": missing,
            })
        except Exception as exc:
            steps.append({"step": "ui_markers", "status": "error", "error": str(exc)})
    finally:
        server.shutdown()
        thread.join(timeout=3)

    all_ok = all(s.get("status") == "ok" for s in steps)
    return {
        "status": "ok" if all_ok else "partial",
        "host": host,
        "port": actual_port,
        "candidate_only": True,
        "local_only": True,
        "smoke_steps": steps,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def get_hub_status(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> dict:
    """Check if the simple local hub is reachable. Returns stopped state if not."""
    ok, reason = check_host(host)
    if not ok:
        return {"status": "blocked", "error": reason, "claim_boundary": CLAIM_BOUNDARY}

    base = f"http://{host}:{port}"
    try:
        urllib.request.urlopen(f"{base}/healthz", timeout=2)
        return {
            "status": "running",
            "host": host,
            "port": port,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    except Exception:
        return {
            "status": "stopped",
            "host": host,
            "port": port,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }
