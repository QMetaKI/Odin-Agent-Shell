from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import json
from odin.runtime.ids import stable_id, utc_stamp
from odin.semantic_bus.event_envelope import validate_semantic_event

DEFAULT_CHANNELS = {
    "#work.ingest", "#binding.validate", "#seed.prewarm", "#pattern.match",
    "#work.atom", "#model.route", "#candidate.emit", "#why.trace", "#gate.final",
}


def build_event(channel: str, event_type: str, source_module: str, trace_id: str, payload: dict) -> dict:
    event = {
        "artifact_kind": "odin_semantic_event",
        "protocol_version": "7.1",
        "event_id": stable_id("EVT", {"channel": channel, "event_type": event_type, "trace_id": trace_id, "payload": payload}, 14),
        "channel": channel,
        "event_type": event_type,
        "source_module": source_module,
        "trace_id": trace_id,
        "privacy_class": payload.get("privacy_class", "local_candidate"),
        "payload": payload,
        "created_at": utc_stamp(),
    }
    errors = validate_semantic_event(event)
    if errors:
        raise ValueError("invalid qirc event: " + "; ".join(errors))
    return event

@dataclass
class QircLedger:
    trace_id: str
    events: list[dict] = field(default_factory=list)

    def append(self, channel: str, event_type: str, source_module: str, payload: dict) -> dict:
        if channel not in DEFAULT_CHANNELS:
            channel = "#why.trace"
            payload = {"wrapped_unknown_channel": channel, **payload}
        event = build_event(channel, event_type, source_module, self.trace_id, payload)
        self.events.append(event)
        return event

    def digest(self) -> dict:
        return {
            "artifact_kind": "odin_qirc_digest",
            "protocol_version": "7.1",
            "trace_id": self.trace_id,
            "event_count": len(self.events),
            "channels": sorted({e["channel"] for e in self.events}),
            "events": self.events,
            "claim_boundary": "local_digest_only_no_network_receipt",
        }

    def write_jsonl(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            for event in self.events:
                f.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\\n")
