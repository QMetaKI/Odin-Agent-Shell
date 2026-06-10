from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List

CANONICAL_STATES = [
    "WORK_RECEIVED",
    "BINDING_CHECKED",
    "POLICY_CHECKED",
    "EVENT_DIGEST_ACCEPTED",
    "UNIVERSAL_WORK_VALIDATED",
    "SEMANTIC_BUS_BATCH_STARTED",
    "CONTEXT_CAPSULE_CREATED",
    "SYSTEM_PROFILE_SELECTED",
    "PRECOMPUTE_DONE",
    "WORKLET_GRAPH_BUILT",
    "SLOT_FORGED",
    "MODEL_ROUTE_SELECTED",
    "MODEL_WORK_PACKET_BUILT",
    "MODEL_RESPONSE_PROJECTED",
    "CRITIC_CASCADE_DONE",
    "CANDIDATE_COMPOSED",
    "FINAL_GATE_DONE",
    "RESPONSE_PACKET_READY",
]

FAILURE_STATES = [
    "BINDING_INVALID",
    "PRIVACY_DENIED",
    "ARTIFACT_BLOCKED",
    "VERB_FORBIDDEN",
    "OUTPUT_CONTRACT_INVALID",
    "CONTEXT_TOO_BROAD",
    "MODEL_ROUTE_BLOCKED",
    "CLAIM_BOUNDARY_HIT",
    "SCHEMA_INVALID",
    "NEEDS_CONTEXT",
    "CANNOT_SAFELY_COMPLETE",
]

@dataclass
class ShadowStateMachinePlan:
    machine_id: str
    work_id: str
    success_states: List[str]
    failure_states: List[str]
    current_state: str
    terminal_success: str = "RESPONSE_PACKET_READY"
    terminal_failure: str = "CANNOT_SAFELY_COMPLETE"
    boundary: str = "state_machine_shadow_no_runtime_execution_claim"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def build_shadow_state_machine(work_id: str, *, failed: bool = False, failure_state: str = "CANNOT_SAFELY_COMPLETE") -> ShadowStateMachinePlan:
    current = failure_state if failed else "RESPONSE_PACKET_READY"
    return ShadowStateMachinePlan(
        machine_id=f"SM-{work_id}",
        work_id=work_id,
        success_states=list(CANONICAL_STATES),
        failure_states=list(FAILURE_STATES),
        current_state=current,
    )
