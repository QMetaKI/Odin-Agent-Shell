from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer

from odin.bus.bus import LocalSemanticBus
from odin.daemon.local_api import OdinLocalHandler
from odin.runtime.engine import run_universal_work_file
from odin.runtime.store import RuntimeStore
from odin.work_atoms.runtime import WorkAtomRuntime, execute_work_atoms, plan_work_atoms_from_types
from odin.worklets.compiler import compile_worklet_graph_to_atom_plan
from odin.worklets.graph import build_worklet_graph, validate_worklet_graph


def test_semantic_bus_event_publish_is_local_candidate_only(tmp_path):
    store = RuntimeStore(tmp_path)
    bus = LocalSemanticBus(store=store)
    event = bus.publish("app.apply", work_id="WORK-1", session_id="SESSION-1", trace_id="TRACE-1", payload={"content": "redacted"})
    assert event["event_id"].startswith("BUS-")
    assert event["event_type"] == "runtime.boundary_rejected"
    assert event["candidate_only"] is True
    assert event["local_only"] is True
    assert "payload_digest" in event
    assert store.read_bus_event(event["event_id"])["event_id"] == event["event_id"]


def test_worklet_graph_compiles_bounded_atoms():
    work = {"work_id": "WORK-WORKLET", "work_intent": {"work_atoms": ["context_compress_atom", "boundary_scan_atom"]}}
    graph = build_worklet_graph(work)
    assert validate_worklet_graph(graph) == []
    plan = compile_worklet_graph_to_atom_plan(graph)
    assert plan["status"] == "ok"
    assert [a["atom_type"] for a in plan["atoms"]] == ["context_compress_atom", "boundary_scan_atom"]
    assert all(a["worklet_id"] == "WORKLET-00-main" for a in plan["atoms"])


def test_cycle_and_unknown_atom_fail_closed():
    graph = {
        "artifact_kind": "odin_worklet_graph",
        "protocol_version": "7.1",
        "graph_id": "WORKLETGRAPH-cycle",
        "work_id": "WORK-CYCLE",
        "worklets": [
            {"worklet_id": "A", "depends_on": ["B"], "atoms": ["context_compress_atom"]},
            {"worklet_id": "B", "depends_on": ["A"], "atoms": ["unknown_atom"]},
        ],
        "candidate_only": True,
        "claim_boundary": "test_fixture",
    }
    plan = compile_worklet_graph_to_atom_plan(graph)
    assert plan["status"] == "blocked"
    assert any("cycle_detected" in error for error in plan["errors"])
    assert "unknown_atom:unknown_atom" in plan["errors"]
    result = execute_work_atoms(plan, {})
    assert result["status"] == "blocked"
    assert result["side_effects"] == []


def test_atom_budget_overflow_and_model_required_without_proof_fail_closed():
    over_budget = plan_work_atoms_from_types(
        "WORK-BUDGET",
        [{"atom_type": "context_compress_atom", "worklet_id": "W"} for _ in range(WorkAtomRuntime().max_total_atoms + 1)],
    )
    result = execute_work_atoms(over_budget, {})
    assert result["status"] == "blocked"
    assert any(error.startswith("atom_budget_exceeded") for error in result["errors"])

    model_required = plan_work_atoms_from_types(
        "WORK-MODEL",
        [{"atom_type": "candidate_variant_atom", "worklet_id": "W", "model_required": True}],
    )
    model_result = execute_work_atoms(model_required, {})
    assert model_result["status"] == "blocked"
    assert any(error.startswith("model_required_without_provider_execution_proof") for error in model_result["errors"])


def test_runtime_store_writes_and_reads_candidates_sessions_events(tmp_path):
    store = RuntimeStore(tmp_path)
    candidate = {"candidate_id": "CAND-1", "content": {"ok": True}}
    session = {"response_id": "RESP-1", "candidates": [candidate]}
    event = {"event_id": "BUS-1", "event_type": "runtime.test", "work_id": "W", "session_id": "S", "trace_id": "T", "payload_digest": "abc"}
    store.write_session(session)
    store.write_bus_event(event)
    assert store.read_candidate("CAND-1")["candidate_id"] == "CAND-1"
    assert store.read_session("RESP-1")["response_id"] == "RESP-1"
    assert store.read_bus_event("BUS-1")["event_type"] == "runtime.test"
    status = store.status()
    assert status["candidate_count"] == 1
    assert status["session_count"] == 1
    assert status["bus_event_count"] == 1
    assert "not_host_proof" in status["claim_boundary"]


def _post_raw(server: HTTPServer, path: str, body: bytes):
    url = f"http://127.0.0.1:{server.server_port}{path}"
    req = urllib.request.Request(url, data=body, method="POST", headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))


def test_local_api_rejects_malformed_json_and_no_app_apply_route(tmp_path):
    handler = type("TestOdinLocalHandler", (OdinLocalHandler,), {"runtime": __import__("odin.runtime.engine", fromlist=["OdinRuntime"]).OdinRuntime(store=RuntimeStore(tmp_path))})
    server = HTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        status, payload = _post_raw(server, "/v7/universal-work/run", b"{")
        assert status == 400
        assert payload["artifact_kind"] == "odin_local_api_error"
        assert payload["error_code"] == "malformed_json"
        status, payload = _post_raw(server, "/v7/app-apply", b"{}")
        assert status == 404
        assert payload["error_code"] == "route_not_exposed"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_run_golden_flow_still_produces_candidate():
    result = run_universal_work_file(
        "examples/runtime/universal_work_full.valid.json",
        seed_pack_path="examples/runtime/app_seed_pack_full.valid.json",
        pattern_mine_path="examples/runtime/pattern_mine_full.valid.json",
        caller_manifest_path="examples/runtime/app_caller_manifest.valid.json",
    )
    assert result["runtime_status"] == "candidate_generated"
    assert result["candidates"]
    assert result["bus_digest"]["event_count"] >= 4
    assert result["candidates"][0]["content"]["work_atom_execution"]["status"] == "ok"
