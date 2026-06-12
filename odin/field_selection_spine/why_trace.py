"""Public why trace for field selection. No private reasoning is stored."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class FieldWhyTrace:
    trace_id: str
    field_id: str
    reason_tokens: list[str]
    evidence_items: list[str]
    not_proven: list[str]

    def to_dict(self) -> dict:
        return {
            "trace_id": self.trace_id,
            "field_id": self.field_id,
            "reason_tokens": list(self.reason_tokens),
            "evidence_items": list(self.evidence_items),
            "not_proven": list(self.not_proven),
        }


def deterministic_trace_id(field_id: str, reason_tokens: list[str], evidence_items: list[str], not_proven: list[str]) -> str:
    payload = {"field_id": field_id, "reason_tokens": reason_tokens, "evidence_items": evidence_items, "not_proven": not_proven}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "field_trace_" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:24]


def build_field_why_trace(field_id: str, reason_tokens: list[str], evidence_items: list[str], not_proven: list[str]) -> FieldWhyTrace:
    trace_id = deterministic_trace_id(field_id, reason_tokens, evidence_items, not_proven)
    return FieldWhyTrace(trace_id, field_id, list(reason_tokens), list(evidence_items), list(not_proven))
