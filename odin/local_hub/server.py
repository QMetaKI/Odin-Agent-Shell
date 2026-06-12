"""Simple Local Hub HTTP server — FINAL-PR-01/02/03/04/05/06.

Claim boundary: simple_local_hub_localhost_only_candidate_no_app_apply_no_external_send_no_provider_execution

Python stdlib only — no external dependencies.
Default: host=127.0.0.1, port=8765
Endpoints:
  GET /             — hub UI
  GET /status.json  — hub status
  GET /healthz      — health check
  GET /models.json  — model picker status (FINAL-PR-02)
  GET /apps.json    — connected apps status (FINAL-PR-02)
  GET /demo/universal-work.json — demo universal work info (FINAL-PR-02)
  POST /demo/universal-work     — deterministic demo response (FINAL-PR-02)
  GET /activity.json            — local activity events from QIRC bus (FINAL-PR-03)
  GET /qirc/channels.json       — QIRC channel list (FINAL-PR-03)
  GET /qirc/events.json         — all QIRC bus events (FINAL-PR-03)
  GET /traces.json              — trace events from QIRC bus (FINAL-PR-03)
  GET /receipts.json            — receipt events from QIRC bus (FINAL-PR-03)
  GET /dev/status.json          — dev status including surface map (FINAL-PR-03)
  POST /qirc/events             — create local demo event (FINAL-PR-03)
  GET /providers.json           — provider policy list (FINAL-PR-04)
  GET /providers/probe.json     — provider probe readiness status (FINAL-PR-04)
  POST /providers/probe         — safe local provider probe, candidate-only (FINAL-PR-04)
  GET /security/runtime-smoke.json — runtime security smoke result (FINAL-PR-04)
  GET /execution-gate/status.json  — execution gate policy status (FINAL-PR-05)
  POST /execution-gate/mock        — deterministic mock execution (FINAL-PR-05)
  GET /execution-gate/proof-chain.json — proof chain cross-references (FINAL-PR-05)
  GET /final-pr-ladder/scaffold.json   — FINAL-PR ladder scaffold (FINAL-PR-05)
  GET /demo/y-route.json               — Y Pattern Spine route hint demo (Y-PATTERN-SPINE)
  GET /demo/seed-route.json            — Operational Seed Spine demo (FINAL-PR-06)
  GET /demo/field-selection.json       — Field Selection Spine demo (FINAL-PR-07)
"""
from __future__ import annotations

import json
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

from odin.local_hub.policy import check_host, CLAIM_BOUNDARY
from odin.local_hub.ui import generate_hub_html, generate_status_json, REQUIRED_IDS
from odin.local_hub.model_picker import build_models_json
from odin.local_hub.connected_apps import build_apps_json
from odin.local_hub.demo_universal_work import build_demo_universal_work_response, get_demo_universal_work_json

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765


class _SimpleLocalHubHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            body = b'{"status":"ok","hub":"simple_local_hub","version":"final_pr_02"}'
            self._respond(200, "application/json", body)
        elif self.path == "/status.json":
            body = generate_status_json().encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path in ("/", "/index.html"):
            body = generate_hub_html().encode("utf-8")
            self._respond(200, "text/html; charset=utf-8", body)
        elif self.path == "/models.json":
            body = json.dumps(build_models_json(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/apps.json":
            body = json.dumps(build_apps_json(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/demo/universal-work.json":
            body = json.dumps(get_demo_universal_work_json(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/activity.json":
            from odin.qirc_core.bus import list_events
            events = list_events("#odin.activity")
            body = json.dumps({"artifact_kind": "odin_activity_list", "candidate_only": True, "local_only": True, "events": events, "claim_boundary": "final_pr_03_qirc_first_slice_local_only"}, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/qirc/channels.json":
            from odin.qirc_core.channels import list_channels
            body = json.dumps({"artifact_kind": "odin_qirc_channels", "candidate_only": True, "local_only": True, "channels": list_channels(), "claim_boundary": "final_pr_03_qirc_first_slice_local_only"}, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/qirc/events.json":
            from odin.qirc_core.bus import list_events
            body = json.dumps({"artifact_kind": "odin_qirc_events", "candidate_only": True, "local_only": True, "events": list_events(), "claim_boundary": "final_pr_03_qirc_first_slice_local_only"}, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/traces.json":
            from odin.qirc_core.bus import list_events
            events = list_events("#odin.trace")
            body = json.dumps({"artifact_kind": "odin_traces", "candidate_only": True, "local_only": True, "events": events, "claim_boundary": "final_pr_03_qirc_first_slice_local_only"}, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/receipts.json":
            from odin.qirc_core.bus import list_events
            events = list_events("#odin.receipt")
            body = json.dumps({"artifact_kind": "odin_receipts", "candidate_only": True, "local_only": True, "events": events, "claim_boundary": "final_pr_03_qirc_first_slice_local_only"}, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/dev/status.json":
            from odin.local_hub.surface_registry import surface_map_summary
            from odin.qirc_core.bus import bus_summary
            body = json.dumps({"artifact_kind": "odin_dev_status", "candidate_only": True, "local_only": True, "surface_map": surface_map_summary(), "qirc_bus": bus_summary(), "claim_boundary": "final_pr_03_qirc_first_slice_local_only"}, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/providers.json":
            from odin.providers.policy import list_policies
            body = json.dumps({"artifact_kind": "odin_provider_policy_list", "candidate_only": True, "local_only": True, "provider_execution": False, "model_inference": False, "providers": list_policies(), "claim_boundary": "provider_probe_candidate_only_no_model_execution_no_api_key_no_external_network"}, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/providers/probe.json":
            from odin.providers.probe import build_provider_status_packet
            from odin.qirc_core.bus import append_event
            packet = build_provider_status_packet()
            for p in packet.get("providers", []):
                append_event(channel="#odin.model", kind="provider_probe_status", source="local_hub", payload={k: p.get(k) for k in ("provider_id", "status", "probe_allowed", "execution_allowed", "candidate_only", "local_only", "model_inference", "provider_execution")})
            body = json.dumps(packet, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/security/runtime-smoke.json":
            from odin.runtime_security.smoke import run_runtime_security_smoke
            from pathlib import Path
            result = run_runtime_security_smoke(Path(__file__).resolve().parents[2])
            body = json.dumps(result.as_dict(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/execution-gate/status.json":
            from odin.execution_gate.policy import DEFAULT_EXECUTION_GATE_POLICY
            body = json.dumps(DEFAULT_EXECUTION_GATE_POLICY.as_dict(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/execution-gate/proof-chain.json":
            from odin.proof_chain.builder import build_proof_chain
            body = json.dumps(build_proof_chain(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/final-pr-ladder/scaffold.json":
            from odin.final_pr_ladder.compiler import compile_worker_packet_scaffold
            scaffold = compile_worker_packet_scaffold(
                target_pr_id="FINAL-PR-06",
                prior_return_report_path="reports/final_pr_05_execution_gate_report.json",
                profile="claude-code",
            )
            body = json.dumps(scaffold, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/demo/y-route.json":
            from odin.y_pattern_spine.profiles import build_route_hint_demo
            body = json.dumps(build_route_hint_demo(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/demo/field-selection.json":
            from odin.field_selection_spine.selector import select_field_route
            selection = select_field_route({"trigger_shape": "repo", "work_type": "repo", "repo_evidence": "SYSTEM_MAP.json"})
            payload = {
                "status": "ok",
                "candidate_only": True,
                "claim_boundary": "field_selection_scores_routes_not_truth",
                "field_selection": selection.to_dict(),
                "not_proven": selection.why_trace.not_proven,
            }
            body = json.dumps(payload, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/demo/seed-route.json":
            from odin.operational_seed_spine.selector import select_seed_route
            from odin.operational_seed_spine.work_capsule import compile_work_capsule
            route = select_seed_route({"trigger_shape": "repo", "work_type": "repo"})
            capsule = compile_work_capsule(route)
            payload = {
                "status": "ok",
                "candidate_only": True,
                "claim_boundary": "operational_seed_spine_routes_work_not_authority",
                "seed_route": route.to_dict(),
                "work_capsule": capsule.to_dict(),
                "not_proven": capsule.not_proven,
            }
            body = json.dumps(payload, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        else:
            body = b'{"status":"not_found"}'
            self._respond(404, "application/json", body)

    def do_POST(self):
        if self.path == "/demo/universal-work":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                payload = json.loads(raw_body.decode("utf-8"))
            except Exception:
                payload = {}
            input_text = payload.get("input", "demo input")
            result = build_demo_universal_work_response(input_text=str(input_text))
            body = json.dumps(result, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/qirc/events":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                payload = json.loads(raw_body.decode("utf-8"))
            except Exception:
                payload = {}
            from odin.qirc_core.bus import append_event
            channel = str(payload.get("channel", "#odin.dev"))
            kind = str(payload.get("kind", "demo"))
            source = str(payload.get("source", "local_hub"))
            event_payload = payload.get("payload", {})
            if not isinstance(event_payload, dict):
                event_payload = {}
            event = append_event(channel=channel, kind=kind, source=source, payload=event_payload)
            body = json.dumps({"status": "ok", "event": event, "candidate_only": True, "local_only": True, "claim_boundary": "final_pr_03_qirc_first_slice_local_only"}, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/providers/probe":
            from odin.providers.probe import build_provider_status_packet
            from odin.qirc_core.bus import append_event
            packet = build_provider_status_packet()
            for p in packet.get("providers", []):
                append_event(channel="#odin.model", kind="provider_probe_status", source="local_hub_post", payload={k: p.get(k) for k in ("provider_id", "status", "probe_allowed", "execution_allowed", "candidate_only", "local_only", "model_inference", "provider_execution")})
            body = json.dumps(packet, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/execution-gate/mock":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                payload = json.loads(raw_body.decode("utf-8"))
            except Exception:
                payload = {}
            input_text = str(payload.get("input", "demo mock input"))
            from odin.execution_gate.gateway import execute_candidate
            result = execute_candidate(input_text=input_text, provider_id="mock")
            body = json.dumps(result, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
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
