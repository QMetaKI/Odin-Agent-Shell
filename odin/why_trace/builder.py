from __future__ import annotations
from dataclasses import dataclass, field
from odin.runtime.ids import stable_id, utc_stamp

@dataclass
class WhyTraceBuilder:
    work_id: str
    trace_id: str | None = None
    steps: list[dict] = field(default_factory=list)

    def __post_init__(self):
        if self.trace_id is None:
            self.trace_id = stable_id("TRACE", self.work_id, 12)

    def add(self, stage: str, decision: str, reasons: list[str] | None = None, data: dict | None = None) -> None:
        self.steps.append({"stage": stage, "decision": decision, "reasons": reasons or [], "data": data or {}, "created_at": utc_stamp()})

    def build(self) -> dict:
        return {
            "artifact_kind": "odin_why_trace",
            "protocol_version": "7.1",
            "trace_id": self.trace_id,
            "work_id": self.work_id,
            "steps": self.steps,
            "redaction": "local_candidate_trace_no_secret_payloads",
            "claim_boundary": "why_trace_explains_candidate_route_not_external_truth",
        }
