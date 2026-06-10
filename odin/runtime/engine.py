from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import json

from odin.apps.caller_manifest import validate_caller_manifest, build_default_manifest
from odin.universal_work.universal_work_validator import validate_universal_work
from odin.runtime.ids import stable_id
from odin.runtime.errors import OdinValidationError
from odin.qirc.ledger import QircLedger
from odin.seeds.compiler import compile_seed_pack
from odin.patterns.intake import compile_pattern_mine
from odin.flow_packs.compiler import compile_flow_packs
from odin.work_atoms.runtime import execute_work_atoms
from odin.worklets.graph import build_worklet_graph
from odin.worklets.compiler import compile_worklet_graph_to_atom_plan
from odin.bus.bus import LocalSemanticBus
from odin.models.workers import build_worker_card, mock_generate
from odin.precompute import score_pre_llm_route
from odin.output.composer import compose_candidate_content
from odin.candidates.artifact import build_candidate_artifact
from odin.candidates.tournament import select_candidate
from odin.core.final_gate import final_gate
from odin.packets.response_packet import build_response_packet
from odin.why_trace.builder import WhyTraceBuilder
from odin.runtime.config import OdinRuntimeConfig, load_runtime_config
from odin.runtime.store import RuntimeStore
from odin.runtime.session import WorkSession
from odin.runtime.repair import build_repair_suggestions

@dataclass
class OdinRuntime:
    root: Path | None = None
    qirc_events_dir: Path | None = None
    default_caller_manifest: dict = field(default_factory=build_default_manifest)
    config: OdinRuntimeConfig = field(default_factory=OdinRuntimeConfig)
    store: RuntimeStore | None = None

    def run_universal_work(self, work: dict, *, caller_manifest: dict | None = None, seed_pack: dict | None = None, pattern_mine: dict | None = None) -> dict:
        caller_manifest = caller_manifest or self.default_caller_manifest
        trace = WhyTraceBuilder(work.get("work_id", "UNKNOWN"))
        ledger = QircLedger(trace.trace_id)
        session = WorkSession(work.get("work_id", "UNKNOWN"), work.get("caller_id", caller_manifest.get("caller_id", "unknown")))
        bus = LocalSemanticBus(store=self.store)
        bus.publish("runtime.work.received", work_id=session.work_id, session_id=session.session_id, trace_id=trace.trace_id, payload={"work_id": work.get("work_id"), "caller_id": work.get("caller_id")}, source="odin.runtime.engine")
        trace.add("ingest", "received_universal_work", data={"work_id": work.get("work_id"), "caller_id": work.get("caller_id")})
        ledger.append("#work.ingest", "work_received", "odin.runtime.engine", {"work_id": work.get("work_id"), "caller_id": work.get("caller_id")})

        errors = []
        errors.extend(validate_caller_manifest(caller_manifest))
        errors.extend(validate_universal_work(work))
        if errors:
            trace.add("binding", "blocked", errors)
            ledger.append("#binding.validate", "binding_blocked", "odin.runtime.engine", {"errors": errors})
            bus.publish("runtime.binding.blocked", work_id=session.work_id, session_id=session.session_id, trace_id=trace.trace_id, payload={"errors": errors}, source="odin.runtime.engine")
            response_errors = "; ".join(errors)
            trace.add("repair", "suggestions_generated", data={"suggestions": build_repair_suggestions(errors)})
            session.mark("blocked", "binding_validation_failed", {"errors": errors})
            raise OdinValidationError(response_errors)
        session.mark("bound", "caller manifest and universal work contract accepted")
        trace.add("binding", "allowed_candidate_work", ["caller manifest and universal work contract accepted"])
        ledger.append("#binding.validate", "binding_allowed", "odin.runtime.engine", {"caller_id": caller_manifest.get("caller_id")})
        bus.publish("runtime.binding.allowed", work_id=session.work_id, session_id=session.session_id, trace_id=trace.trace_id, payload={"caller_id": caller_manifest.get("caller_id")}, source="odin.runtime.engine")

        seed_pack = seed_pack or work.get("seed_pack") or {"artifact_kind": "odin_app_seed_pack", "pack_id": "empty", "seeds": []}
        compiled_seed = compile_seed_pack(seed_pack, work)
        session.mark("compiled", "seed_pack_compiled", {"status": compiled_seed.get("status")})
        trace.add("seed_pack", compiled_seed["status"], compiled_seed.get("errors", []), {"active": len(compiled_seed.get("active_seeds", []))})
        ledger.append("#seed.prewarm", "seed_pack_compiled", "odin.seeds.compiler", {"pack_id": compiled_seed.get("pack_id"), "status": compiled_seed.get("status")})

        pattern_mine = pattern_mine or work.get("pattern_mine") or {"artifact_kind": "odin_pattern_mine", "mine_id": "empty", "patterns": [], "flow_packs": []}
        compiled_pattern = compile_pattern_mine(pattern_mine)
        compiled_flows = compile_flow_packs(compiled_pattern.get("flow_packs", []))
        trace.add("pattern_mine", compiled_pattern["status"], compiled_pattern.get("errors", []), {"patterns": len(compiled_pattern.get("patterns", [])), "flows": len(compiled_flows)})
        ledger.append("#pattern.match", "pattern_mine_compiled", "odin.patterns.intake", {"mine_id": compiled_pattern.get("mine_id"), "status": compiled_pattern.get("status")})

        worklet_graph = build_worklet_graph(work)
        plan = compile_worklet_graph_to_atom_plan(worklet_graph)
        plan["compiled_seed_pack_ref"] = compiled_seed.get("pack_id")
        plan["compiled_pattern_mine_ref"] = compiled_pattern.get("mine_id")
        session.mark("planned", "worklet_graph_compiled_to_work_atom_plan", {"worklet_count": len(worklet_graph.get("worklets", [])), "atom_count": len(plan.get("atoms", [])), "status": plan.get("status")})
        bus.publish("runtime.worklets.compiled", work_id=session.work_id, session_id=session.session_id, trace_id=trace.trace_id, payload={"graph_id": worklet_graph.get("graph_id"), "plan_id": plan.get("plan_id"), "status": plan.get("status")}, source="odin.worklets.compiler")
        atom_payload = {
            "context": {"work": work, "seed_pack": compiled_seed, "pattern_mine": compiled_pattern},
            "claims": work.get("claim_boundary", {}).get("claims", []),
            "actions": work.get("constraints", {}).get("actions", []),
            "seeds": compiled_seed.get("active_seeds", []),
            "patterns": compiled_pattern.get("patterns", []),
            "tags": work.get("work_intent", {}).get("tags", []),
            "base": work.get("work_intent", {}).get("goal", work.get("work_id", "candidate")),
        }
        atom_execution = execute_work_atoms(plan, atom_payload)
        trace.add("work_atoms", atom_execution.get("status", "executed"), atom_execution.get("errors", []), {"atom_count": len(atom_execution.get("results", []))})
        ledger.append("#work.atom", "work_atoms_executed", "odin.work_atoms.runtime", {"plan_id": plan.get("plan_id"), "atom_count": len(atom_execution.get("results", [])), "status": atom_execution.get("status")})
        bus.publish("runtime.work_atoms.executed", work_id=session.work_id, session_id=session.session_id, trace_id=trace.trace_id, payload={"plan_id": plan.get("plan_id"), "status": atom_execution.get("status"), "errors": atom_execution.get("errors", [])}, source="odin.work_atoms.runtime")

        route_decision = score_pre_llm_route(work)
        if route_decision.get("blocked_reasons"):
            trace.add("pre_llm_route", "blocked_before_provider_dispatch", route_decision.get("blocked_reasons"), route_decision)
            ledger.append("#model.route", "pre_llm_blocked", "odin.precompute.route_score", {"blocked_reasons": route_decision.get("blocked_reasons")})
            session.mark("blocked", "pre_llm_route_blocked", {"reasons": route_decision.get("blocked_reasons")})
            raise OdinValidationError("pre-LLM route blocked work before provider dispatch: " + "; ".join(route_decision.get("blocked_reasons", [])))
        route = route_decision.get("route")
        worker = build_worker_card("mock_worker_001", route_decision.get("selected_worker_class", "mock_local"))
        if route_decision.get("requires_model"):
            projection = mock_generate(worker, work, atom_execution, route)
        else:
            projection = {
                "artifact_kind": "odin_deterministic_no_model_output",
                "protocol_version": "7.1",
                "route": route,
                "summary": f"Deterministic candidate route for {work.get('work_id')}; no model/provider executed.",
                "candidate_only": True,
                "model_inference_verified": False,
                "claim_boundary": "deterministic_no_model_output_not_live_inference_or_truth",
            }
        session.mark("projected", "worker_projection_or_deterministic_output_created", {"route": route, "worker_id": worker.get("worker_id"), "requires_model": route_decision.get("requires_model")})
        trace.add("pre_llm_route", "selected_candidate_worker", [route], {"worker_id": worker["worker_id"], "route_decision": route_decision})
        ledger.append("#model.route", "route_selected", "odin.precompute.route_score", {"route": route, "worker_id": worker["worker_id"], "requires_model": route_decision.get("requires_model")})

        composed_output = compose_candidate_content(work=work, route_decision=route_decision, deterministic_output=projection if not route_decision.get("requires_model") else None, provider_result=projection if route_decision.get("requires_model") else None, worker_card=worker)
        content = {
            "worklet_graph": worklet_graph,
            "work_atom_execution": atom_execution,
            "compiled_seed_pack": compiled_seed,
            "compiled_pattern_mine": compiled_pattern,
            "compiled_flow_packs": compiled_flows,
            "model_projection": projection,
            "pre_llm_route": route_decision,
            "output_composition": composed_output,
            "app_apply_instruction": "app_must_review_and_apply_or_reject",
        }
        candidate = build_candidate_artifact(work, content, trace.trace_id)
        ok, gate_reasons = final_gate(candidate)
        trace.add("final_gate", "allowed" if ok else "blocked", gate_reasons)
        ledger.append("#gate.final", "candidate_allowed" if ok else "candidate_blocked", "odin.core.final_gate", {"candidate_id": candidate.get("candidate_id"), "reasons": gate_reasons})
        if not ok:
            session.mark("blocked", "final_gate_blocked", {"reasons": gate_reasons})
            raise OdinValidationError("final gate blocked candidate: " + "; ".join(gate_reasons))
        session.mark("gated", "final_gate_allowed", {"reasons": gate_reasons})

        selected = select_candidate([candidate])
        trace_doc = trace.build()
        ledger.append("#candidate.emit", "candidate_emitted", "odin.candidates.artifact", {"candidate_id": candidate.get("candidate_id")})
        bus.publish("runtime.candidate.emitted", work_id=session.work_id, session_id=session.session_id, trace_id=trace.trace_id, payload={"candidate_id": candidate.get("candidate_id")}, source="odin.candidates.artifact")
        ledger.append("#why.trace", "why_trace_ready", "odin.why_trace.builder", {"trace_id": trace.trace_id, "step_count": len(trace_doc.get("steps", []))})
        qirc_digest = ledger.digest()
        response = build_response_packet(work.get("work_id"), work.get("caller_id"), [candidate], trace.trace_id)
        response["selected_candidate_id"] = selected["selected"].get("candidate_id") if selected.get("selected") else None
        response["why_trace"] = trace_doc
        response["qirc_digest"] = qirc_digest
        response["bus_digest"] = {"artifact_kind": "odin_local_semantic_bus_digest", "event_count": len(bus.events), "events": bus.list_events(), "candidate_only": True, "claim_boundary": "local_bus_digest_no_network_no_apply"}
        session.mark("emitted", "candidate_response_ready", {"candidate_id": selected["selected"].get("candidate_id") if selected.get("selected") else None})
        response["runtime_status"] = "candidate_generated"
        response["work_session"] = session.to_dict()
        response["runtime_config"] = self.config.to_dict()
        response["claim_boundary"] = "runtime_candidate_no_host_or_model_proof_claim"
        if self.qirc_events_dir:
            ledger.write_jsonl(self.qirc_events_dir / f"{trace.trace_id}.jsonl")
        if self.store:
            self.store.write_session(response)
        return response


def load_json(path: Path | str) -> dict:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def run_universal_work_file(path: Path | str, *, seed_pack_path: Path | str | None = None, pattern_mine_path: Path | str | None = None, caller_manifest_path: Path | str | None = None) -> dict:
    work = load_json(path)
    seed_pack = load_json(seed_pack_path) if seed_pack_path else None
    pattern_mine = load_json(pattern_mine_path) if pattern_mine_path else None
    caller = load_json(caller_manifest_path) if caller_manifest_path else None
    return OdinRuntime().run_universal_work(work, caller_manifest=caller, seed_pack=seed_pack, pattern_mine=pattern_mine)
