from __future__ import annotations
from dataclasses import dataclass, field
from odin.runtime.ids import stable_id, utc_stamp

ALLOWED_STATES = ["created", "bound", "compiled", "planned", "projected", "gated", "emitted", "blocked"]

@dataclass
class WorkSession:
    work_id: str
    caller_id: str
    session_id: str = ""
    state: str = "created"
    transitions: list[dict] = field(default_factory=list)

    def __post_init__(self):
        if not self.session_id:
            self.session_id = stable_id("WORKSESSION", {"work_id": self.work_id, "caller_id": self.caller_id}, 12)
        self.mark("created", "session_initialized")

    def mark(self, state: str, reason: str, data: dict | None = None) -> None:
        if state not in ALLOWED_STATES:
            raise ValueError(f"invalid work session state: {state}")
        self.state = state
        self.transitions.append({"state": state, "reason": reason, "data": data or {}, "at": utc_stamp()})

    def to_dict(self) -> dict:
        return {
            "artifact_kind": "odin_work_session",
            "protocol_version": "7.1",
            "session_id": self.session_id,
            "work_id": self.work_id,
            "caller_id": self.caller_id,
            "state": self.state,
            "transitions": self.transitions,
            "candidate_only": True,
            "claim_boundary": "work_session_tracks_candidate_flow_no_app_apply",
        }
