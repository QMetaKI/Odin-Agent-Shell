from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ShadowReason:
    code: str
    message: str


@dataclass
class ShadowBusEvent:
    event_id: str
    channel: str
    event_type: str
    work_id: str
    trace_id: str
    source_module: str
    privacy_class: str = "local_only"
    payload: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ShadowContextCapsule:
    capsule_id: str
    work_id: str
    task_center: str
    must_use: List[str] = field(default_factory=list)
    must_not_use: List[str] = field(default_factory=list)
    style: str = "clear"
    claim_boundary: str = "candidate_projection_only"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ShadowWorkletNode:
    node_id: str
    worklet_type: str
    preferred_route: str
    output: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ShadowWorkletGraph:
    graph_id: str
    work_id: str
    nodes: List[ShadowWorkletNode]
    claim_boundary: str = "worklet_graph_candidate_only"

    def to_dict(self) -> Dict[str, Any]:
        return {**asdict(self), "nodes": [node.to_dict() for node in self.nodes]}


@dataclass
class ShadowSlotContract:
    slot_id: str
    slot_class: str
    model_route: str
    max_input_tokens: int
    max_output_tokens: int
    forbidden_claims: List[str]
    requires_trace: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ShadowModelRoutePlan:
    route_class: str
    selected_route: str
    latency_mode: str
    reason: List[str]
    fallbacks: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ShadowCandidate:
    candidate_id: str
    candidate_type: str
    work_id: str
    content: Dict[str, Any]
    candidate_only: bool = True
    requires_app_apply_gate: bool = True
    claim_status: str = "shadow_projection"
    evidence_status: str = "not_externally_verified"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ShadowCandidateDNA:
    candidate_dna_id: str
    candidate_id: str
    work_id: str
    trace_id: str
    bus_event_count: int
    active_lenses: List[str]
    route: str
    claim_boundary: str = "candidate_projection_only"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ShadowRuntimeResult:
    ok: bool
    work_id: str
    trace_id: str
    reasons: List[ShadowReason] = field(default_factory=list)
    events: List[ShadowBusEvent] = field(default_factory=list)
    context_capsule: Optional[ShadowContextCapsule] = None
    worklet_graph: Optional[ShadowWorkletGraph] = None
    slot_contract: Optional[ShadowSlotContract] = None
    model_route_plan: Optional[ShadowModelRoutePlan] = None
    candidate: Optional[ShadowCandidate] = None
    candidate_dna: Optional[ShadowCandidateDNA] = None

    def reason_codes(self) -> List[str]:
        return [reason.code for reason in self.reasons]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "work_id": self.work_id,
            "trace_id": self.trace_id,
            "reasons": [asdict(r) for r in self.reasons],
            "events": [e.to_dict() for e in self.events],
            "context_capsule": self.context_capsule.to_dict() if self.context_capsule else None,
            "worklet_graph": self.worklet_graph.to_dict() if self.worklet_graph else None,
            "slot_contract": self.slot_contract.to_dict() if self.slot_contract else None,
            "model_route_plan": self.model_route_plan.to_dict() if self.model_route_plan else None,
            "candidate": self.candidate.to_dict() if self.candidate else None,
            "candidate_dna": self.candidate_dna.to_dict() if self.candidate_dna else None,
        }
