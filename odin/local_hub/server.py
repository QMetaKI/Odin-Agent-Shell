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
  GET /demo/projection-candidate.json  — Projection Candidate Spine demo (FINAL-PR-08)
  GET /operational-spine/status.json        — Operational spine status (FINAL-PR-09++)
  GET /operational-spine/demo.json          — Full operational spine demo (FINAL-PR-09++)
  POST /operational-spine/run               — Run operational spine on input (FINAL-PR-09++)
  GET /operational-spine/evidence-index.json  — Evidence index (FINAL-PR-09++)
  GET /operational-spine/provider-readiness.json — Provider seam readiness (FINAL-PR-09++)
  GET /operational-spine/small-model-route.json  — Small-model route plan (FINAL-PR-09++)
  GET /operational-spine/qshabang-map.json       — Q-Shabang operational map (FINAL-PR-09++)
  GET /operational-spine/modelworkpacket.example.json — ModelWorkPacket example (FINAL-PR-09++)
  GET /release/boundary-matrix.json    — Release boundary matrix (FINAL-PR-10++)
  GET /release/ring-authority-map.json — Ring authority map (FINAL-PR-10++)
  GET /release/bug6-q7-map.json        — Bug6/Q7 operational map (FINAL-PR-10++)
  GET /release/model-role-authority.json — Model role authority matrix (FINAL-PR-10++)
  GET /release/qshabang-gates.json     — Q-Shabang release gate map (FINAL-PR-10++)
  GET /release/evidence-closure.json   — Release evidence closure index (FINAL-PR-10++)
  GET /release/preflight.json          — Final release preflight (FINAL-PR-10++)
  GET /release/artifact-currency.json  — Artifact currency index (FINAL-PR-10++)
  GET /provider-receipts/status.json   — Provider receipt harness status (FINAL-PR-11)
  GET /provider-receipts/demo.json     — Provider receipt demo (FINAL-PR-11)
  POST /provider-receipts/run          — Run local provider receipt (FINAL-PR-11)
  GET /provider-receipts/claims.json   — Provider receipt claims (FINAL-PR-11)
  GET /critic-runtime/status.json      — Critic runtime binding status (FINAL-PR-11)
  GET /critic-runtime/demo.json        — Critic runtime demo (FINAL-PR-11)
  GET /route-evaluation/status.json    — Route evaluation receipt status (FINAL-PR-11)
  GET /route-evaluation/demo.json      — Route evaluation demo (FINAL-PR-11)
  GET /thor-handoff-compiler/status.json — Thor handoff compiler status (FINAL-PR-11)
  GET /thor-handoff-compiler/demo.json — Thor handoff compiler demo (FINAL-PR-11)
  GET /release/sequence-transition.json — Release sequence transition (FINAL-PR-11)
  GET /release/preflight-after-pr11.json — Preflight after PR11 (FINAL-PR-11)
  GET /v711-coverage/matrix.json        — v7.1.1 Coverage Matrix (FINAL-PR-11.5)
  GET /v711-coverage/gap-index.json     — v7.1.1 Gap Index (FINAL-PR-11.5)
  GET /semantic-kernel/closure.json     — Semantic Kernel Closure report (FINAL-PR-11.5)
  GET /semantic-kernel/ir.json          — Semantic Kernel IR objects (FINAL-PR-11.5)
  GET /semantic-kernel/pipeline.json    — Semantic Kernel Pipeline stages (FINAL-PR-11.5)
  GET /y-pattern/index.json             — Y Pattern Operationalization Index (FINAL-PR-11.5)
  GET /claims/policy.json               — Release Claims Policy (FINAL-PR-11.5)
  GET /agent-operator-modes/matrix.json — Agent Operator Mode Matrix (FINAL-PR-11.5)
  GET /release-readiness/status.json   — Release readiness status (FINAL-PR-12)
  GET /release-readiness/matrix.json   — Release readiness matrix (FINAL-PR-12)
  GET /release-readiness/risk-register.json — Release risk register (FINAL-PR-12)
  GET /evidence-closure/dry-run.json   — Evidence closure dry run (FINAL-PR-12)
  GET /packaging-boundary/inventory.json — Packaging boundary inventory (FINAL-PR-12)
  GET /command-surface/index.json      — Command surface index (FINAL-PR-12)
  GET /docs-readiness/index.json       — Docs readiness index (FINAL-PR-12)
  GET /final-pr-13/input-bundle.json   — FINAL-PR-13 input bundle (FINAL-PR-12)
  GET /release/sequence-after-pr12.json — Release sequence after PR12 (FINAL-PR-12)
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


def build_projection_candidate_payload() -> dict:
    """Build a demo Projection Candidate Spine payload for GET /demo/projection-candidate.json."""
    from odin.operational_seed_spine.selector import select_seed_route
    from odin.field_selection_spine.selector import select_field_route_from_seed_route
    from odin.projection_candidate_spine.projection_set import build_projection_set_from_field_selection
    from odin.projection_candidate_spine.candidate_graph import build_candidate_graph
    from odin.projection_candidate_spine.expression_packet import build_expression_packet
    seed = select_seed_route({"trigger_shape": "repo", "work_type": "repo"})
    fs = select_field_route_from_seed_route(seed)
    ps = build_projection_set_from_field_selection(fs)
    graph = build_candidate_graph(ps.candidate_nodes)
    ep = build_expression_packet(ps.candidate_nodes[0])
    return {
        "status": "ok",
        "candidate_only": True,
        "claim_boundary": "projection_candidate_spine_prepares_candidates_not_runtime_execution",
        "projection_set": ps.to_dict(),
        "candidate_graph": graph.to_dict(),
        "expression_packet": ep.to_dict(),
        "not_proven": [
            "hidden_runtime", "model_inference", "provider_execution", "app_apply",
            "app_state_mutation", "external_send", "generated_code_correctness",
            "production_readiness", "security_certification",
        ],
    }


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
        elif self.path == "/demo/projection-candidate.json":
            payload = build_projection_candidate_payload()
            body = json.dumps(payload, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/operational-spine/status.json":
            from odin.operational_spine.status import get_operational_spine_status
            body = json.dumps(get_operational_spine_status(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/operational-spine/demo.json":
            from odin.operational_spine.orchestrator import run_operational_spine
            body = json.dumps(run_operational_spine("demo operational spine input"), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/operational-spine/evidence-index.json":
            payload = {
                "artifact_kind": "odin_final_pr_09_operational_spine_evidence_index",
                "candidate_only": True, "local_only": True, "app_owned_apply": True,
                "claim_boundary": "final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply",
                "registry": "registries/final_pr_09_operational_spine_registry.json",
                "proof_packet": "reports/final_pr_09_operational_spine_proof_packet.json",
                "not_proven": ["live_model_inference", "production_readiness", "security_certification"],
            }
            body = json.dumps(payload, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/operational-spine/provider-readiness.json":
            from odin.operational_spine.provider_seam import build_provider_seam_packet
            body = json.dumps(build_provider_seam_packet(None), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/operational-spine/small-model-route.json":
            from odin.operational_spine.small_model_route_plan import build_small_model_route_plan
            body = json.dumps(build_small_model_route_plan(work_id="hub_demo_work"), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/operational-spine/qshabang-map.json":
            from odin.operational_spine.qshabang_runtime_map import build_qshabang_operational_map
            body = json.dumps(build_qshabang_operational_map(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/operational-spine/modelworkpacket.example.json":
            import json as _json
            from pathlib import Path as _Path
            p = _Path(__file__).resolve().parents[2] / "examples/final_pr_09/modelworkpacket.example.json"
            if p.exists():
                body = p.read_bytes()
            else:
                body = _json.dumps({"status": "not_found", "candidate_only": True}).encode("utf-8")
            self._respond(200, "application/json", body)
        # FINAL-PR-10++: Release Boundary Gates endpoints
        elif self.path == "/release/boundary-matrix.json":
            from odin.release_boundaries.boundary_matrix import build_boundary_matrix
            body = json.dumps(build_boundary_matrix(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/release/ring-authority-map.json":
            from odin.release_boundaries.ring_authority_map import build_ring_authority_map
            body = json.dumps(build_ring_authority_map(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/release/bug6-q7-map.json":
            from odin.release_boundaries.bug6_q7_operational_map import build_bug6_q7_operational_map
            body = json.dumps(build_bug6_q7_operational_map(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/release/model-role-authority.json":
            from odin.release_boundaries.model_role_authority import build_model_role_authority_matrix
            body = json.dumps(build_model_role_authority_matrix(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/release/qshabang-gates.json":
            from odin.release_boundaries.qshabang_release_gate_map import build_qshabang_release_gate_map
            body = json.dumps(build_qshabang_release_gate_map(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/release/evidence-closure.json":
            from odin.release_boundaries.evidence_closure import build_release_evidence_closure_index
            body = json.dumps(build_release_evidence_closure_index(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/release/preflight.json":
            from odin.release_boundaries.final_preflight import run_final_release_preflight
            body = json.dumps(run_final_release_preflight(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/release/artifact-currency.json":
            from odin.release_boundaries.artifact_currency import build_artifact_currency_index
            body = json.dumps(build_artifact_currency_index(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        # FINAL-PR-11: Local Provider Receipt Harness + Critic Runtime Binding + Thor Handoff Compiler v0
        elif self.path == "/provider-receipts/status.json":
            from odin.local_provider_receipts.reports import build_provider_receipt_harness_report
            body = json.dumps(build_provider_receipt_harness_report(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/provider-receipts/demo.json":
            from odin.local_provider_receipts.receipt import run_local_provider_receipt
            result = run_local_provider_receipt("deterministic_no_provider", "demo prompt", allow_local_provider_execution=False)
            body = json.dumps(result, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/provider-receipts/claims.json":
            payload = {
                "artifact_kind": "odin_provider_receipt_claims",
                "candidate_only": True,
                "final_pr_12_remains_deferred": True,
                "evidence_class": "structural_evidence",
                "claim_boundary": "local_provider_receipt_harness_scoped_local_receipts_not_quality_benchmark",
                "not_proven": ["production_readiness", "security_certification", "release_certification", "real_model_benchmark", "model_quality_superiority"],
            }
            body = json.dumps(payload, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/critic-runtime/status.json":
            from odin.critic_runtime.reports import build_critic_runtime_report
            body = json.dumps(build_critic_runtime_report(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/critic-runtime/demo.json":
            from odin.critic_runtime.cascade import run_critic_cascade
            demo_candidate = {
                "artifact_kind": "odin_demo_candidate",
                "candidate_only": True,
                "claim_boundary": "demo_candidate_boundary",
                "not_proven": ["production_readiness"],
                "app_apply": False,
                "external_send": False,
            }
            body = json.dumps(run_critic_cascade(demo_candidate), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/route-evaluation/status.json":
            from odin.route_evaluation.reports import build_route_evaluation_report
            body = json.dumps(build_route_evaluation_report(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/route-evaluation/demo.json":
            from odin.route_evaluation.receipt import run_route_evaluation_receipt
            body = json.dumps(run_route_evaluation_receipt(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/thor-handoff-compiler/status.json":
            from odin.thor_handoff_compiler.reports import build_thor_compiler_report
            body = json.dumps(build_thor_compiler_report(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/thor-handoff-compiler/demo.json":
            from odin.thor_handoff_compiler.input_contract import build_handoff_input_contract
            from odin.thor_handoff_compiler.compiler import compile_thor_handoff_bundle
            ic = build_handoff_input_contract(
                objective="Demo handoff compile",
                repo_evidence=["odin/operational_spine/"],
                allowed_edits=["odin/local_provider_receipts/"],
                forbidden_edits=["odin/operational_spine/"],
                acceptance_gates=["validate-all OK"],
                claim_boundary="demo_thor_handoff",
            )
            body = json.dumps(compile_thor_handoff_bundle(ic), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/release/sequence-transition.json":
            from pathlib import Path as _Path
            import json as _json
            p = _Path(__file__).resolve().parents[2] / "reports/final_pr_11_release_sequence_transition_report.json"
            if p.exists():
                body = p.read_bytes()
            else:
                body = _json.dumps({
                    "status": "not_found",
                    "candidate_only": True,
                    "recommended_next_pr": "FINAL-PR-12",
                    "final_pr_12_remains_deferred": True,
                }).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/release/preflight-after-pr11.json":
            from pathlib import Path as _Path
            import json as _json
            p = _Path(__file__).resolve().parents[2] / "reports/final_pr_11_preflight_after_pr11_report.json"
            if p.exists():
                body = p.read_bytes()
            else:
                body = _json.dumps({
                    "status": "yellow",
                    "candidate_only": True,
                    "recommended_next_pr": "FINAL-PR-12",
                    "final_pr_12_remains_deferred": True,
                }).encode("utf-8")
            self._respond(200, "application/json", body)
        # FINAL-PR-11.5: Semantic Kernel Coverage Compiler + Claims Compiler + Y Pattern
        elif self.path == "/v711-coverage/matrix.json":
            from odin.v711_coverage_compiler.coverage_matrix import build_v711_coverage_matrix
            body = json.dumps(build_v711_coverage_matrix(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/v711-coverage/gap-index.json":
            from odin.v711_coverage_compiler.gap_index import build_v711_gap_index
            body = json.dumps(build_v711_gap_index(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/semantic-kernel/closure.json":
            from odin.semantic_kernel_closure.reports import build_semantic_kernel_closure_report
            body = json.dumps(build_semantic_kernel_closure_report(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/semantic-kernel/ir.json":
            from odin.semantic_kernel_closure.ir import build_odin_work_ir
            body = json.dumps(build_odin_work_ir(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/semantic-kernel/pipeline.json":
            from odin.semantic_kernel_closure.pipeline import build_semantic_kernel_pipeline
            body = json.dumps(build_semantic_kernel_pipeline(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/y-pattern/index.json":
            from odin.y_pattern_operationalization_index.index_builder import build_y_pattern_operationalization_index
            body = json.dumps(build_y_pattern_operationalization_index(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/claims/policy.json":
            from odin.claims_compiler.reports import build_release_claims_policy
            body = json.dumps(build_release_claims_policy(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/agent-operator-modes/matrix.json":
            from odin.agent_operator_modes.reports import build_agent_operator_mode_matrix
            body = json.dumps(build_agent_operator_mode_matrix(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        # FINAL-PR-12: Release Readiness Hardening + Evidence Closure Dry Run + Packaging Boundary Prep
        elif self.path == "/release-readiness/status.json":
            from odin.release_readiness_hardening.readiness_matrix import build_release_readiness_matrix
            result = build_release_readiness_matrix()
            result["candidate_only"] = True
            result["final_pr_13_remains_deferred"] = True
            body = json.dumps(result, indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/release-readiness/matrix.json":
            from odin.release_readiness_hardening.readiness_matrix import build_release_readiness_matrix
            body = json.dumps(build_release_readiness_matrix(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/release-readiness/risk-register.json":
            from odin.release_readiness_hardening.risk_register import build_release_risk_register
            body = json.dumps(build_release_risk_register(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/evidence-closure/dry-run.json":
            from odin.evidence_closure_dry_run.dry_run import run_evidence_closure_dry_run
            body = json.dumps(run_evidence_closure_dry_run(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/packaging-boundary/inventory.json":
            from odin.packaging_boundary_prep.inventory import build_packaging_inventory
            body = json.dumps(build_packaging_inventory(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/command-surface/index.json":
            from odin.command_surface_closure.command_index import build_command_surface_index
            body = json.dumps(build_command_surface_index(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/docs-readiness/index.json":
            from odin.docs_readiness.doc_index import build_docs_readiness_index
            body = json.dumps(build_docs_readiness_index(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/final-pr-13/input-bundle.json":
            from odin.final_pr_13_input_bundle.bundle import build_final_pr_13_input_bundle
            body = json.dumps(build_final_pr_13_input_bundle(), indent=2).encode("utf-8")
            self._respond(200, "application/json", body)
        elif self.path == "/release/sequence-after-pr12.json":
            body = json.dumps({
                "candidate_only": True,
                "claim_boundary": "final_pr_12_release_readiness_hardening_not_release_closure",
                "current_pr": "FINAL-PR-12",
                "next_pr": "FINAL-PR-13",
                "final_pr_13_remains_deferred": True,
                "sequence": ["FINAL-PR-12 merged", "FINAL-PR-13 Release Closure — deferred"],
                "not_proven": ["production_readiness", "release_certification"],
            }, indent=2).encode("utf-8")
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
        elif self.path == "/operational-spine/run":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                payload = json.loads(raw_body.decode("utf-8"))
            except Exception:
                payload = {}
            input_text = str(payload.get("input", "demo operational spine input"))
            from odin.operational_spine.orchestrator import run_operational_spine
            result = run_operational_spine(input_text)
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
