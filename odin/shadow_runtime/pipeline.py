from __future__ import annotations

from typing import Any, Dict

from .boundary import shadow_final_gate
from .candidate_shadow import make_shadow_candidate, make_shadow_candidate_dna
from .model_route_shadow import choose_shadow_route
from .semantic_bus_shadow import make_shadow_bus_batch, validate_shadow_bus_events
from .types import ShadowReason, ShadowRuntimeResult
from .universal_work_shadow import (
    make_shadow_context_capsule,
    make_shadow_slot_contract,
    make_shadow_worklet_graph,
    validate_shadow_universal_work,
)


def run_shadow_pipeline(work: Dict[str, Any], *, resource_profile: str = "standard_local", latency_mode: str = "interactive", quality_target: str = "standard", remote_allowed: bool = False) -> ShadowRuntimeResult:
    work_id = work.get("work_id", "WORK-MISSING")
    trace_id = work.get("trace_id", f"TRACE-{work_id}")
    reasons = validate_shadow_universal_work(work)
    if reasons:
        result = ShadowRuntimeResult(ok=False, work_id=work_id, trace_id=trace_id, reasons=reasons)
        return shadow_final_gate(result)

    route_plan = choose_shadow_route(resource_profile, latency_mode, quality_target, remote_allowed)
    events = make_shadow_bus_batch(work_id, trace_id, route_plan.selected_route)
    bus_reasons = validate_shadow_bus_events(events)

    capsule = make_shadow_context_capsule(work)
    graph = make_shadow_worklet_graph(work, route_plan.selected_route)
    slot = make_shadow_slot_contract(work, route_plan.selected_route)
    candidate = make_shadow_candidate(work, route_plan.selected_route)
    dna = make_shadow_candidate_dna(work, candidate, trace_id, len(events), route_plan.selected_route)

    result = ShadowRuntimeResult(
        ok=not bus_reasons,
        work_id=work_id,
        trace_id=trace_id,
        reasons=list(bus_reasons),
        events=events,
        context_capsule=capsule,
        worklet_graph=graph,
        slot_contract=slot,
        model_route_plan=route_plan,
        candidate=candidate,
        candidate_dna=dna,
    )
    if result.ok:
        result.reasons.append(ShadowReason("shadow_final_gate_ready", "shadow candidate is ready for future real final gate implementation"))
    return shadow_final_gate(result)
