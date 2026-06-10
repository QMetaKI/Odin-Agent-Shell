from __future__ import annotations

from typing import Any, Dict, List

from .types import ShadowCandidate, ShadowCandidateDNA


def make_shadow_candidate(work: Dict[str, Any], route: str) -> ShadowCandidate:
    output_contract = work.get("output_contract", {})
    candidate_type = output_contract.get("artifact_type", "generic_candidate")
    content = {
        "shadow_notice": "code-near candidate only; no real model was called",
        "verb": work.get("work_intent", {}).get("verb"),
        "goal": work.get("work_intent", {}).get("goal"),
        "route": route,
        "shape": output_contract.get("shape", "candidate"),
    }
    return ShadowCandidate(
        candidate_id=f"CAND-{work['work_id']}",
        candidate_type=candidate_type,
        work_id=work["work_id"],
        content=content,
    )


def make_shadow_candidate_dna(work: Dict[str, Any], candidate: ShadowCandidate, trace_id: str, event_count: int, route: str, active_lenses: List[str] | None = None) -> ShadowCandidateDNA:
    return ShadowCandidateDNA(
        candidate_dna_id=f"DNA-{candidate.candidate_id}",
        candidate_id=candidate.candidate_id,
        work_id=work["work_id"],
        trace_id=trace_id,
        bus_event_count=event_count,
        active_lenses=active_lenses or ["text_lens"],
        route=route,
    )


def make_shadow_response_packet(work: Dict[str, Any], candidate: ShadowCandidate, dna: ShadowCandidateDNA) -> Dict[str, Any]:
    return {
        "artifact_kind": "odin_response_packet_shadow",
        "protocol_version": "7.1-shadow",
        "work_id": work["work_id"],
        "caller_id": work.get("caller_id"),
        "candidates": [candidate.to_dict()],
        "candidate_dna": dna.to_dict(),
        "claim_status": "shadow_projection",
        "requires_app_apply_gate": True,
        "odin_executes_actions": False,
    }
