from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .events import build_bus_event, event_to_json_line


@dataclass
class LocalSemanticBus:
    store: object | None = None
    ledger_path: Path | None = None
    events: list[dict] = field(default_factory=list)

    def publish(
        self,
        event_type: str,
        *,
        work_id: str | None = None,
        session_id: str | None = None,
        trace_id: str | None = None,
        payload: dict | None = None,
        source: str = "odin.runtime",
    ) -> dict:
        event = build_bus_event(
            event_type=event_type,
            work_id=work_id,
            session_id=session_id,
            trace_id=trace_id,
            payload=payload or {},
            source=source,
        )
        self.events.append(event)
        if self.store is not None and hasattr(self.store, "write_bus_event"):
            self.store.write_bus_event(event)
        if self.ledger_path is not None:
            self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
            with self.ledger_path.open("a", encoding="utf-8") as handle:
                handle.write(event_to_json_line(event) + "\n")
        return event

    def list_events(self) -> list[dict]:
        return list(self.events)

    def status(self) -> dict:
        return {
            "artifact_kind": "odin_local_semantic_bus_status",
            "protocol_version": "7.1",
            "event_count": len(self.events),
            "local_only": True,
            "candidate_only": True,
            "claim_boundary": "local_bus_status_not_network_or_apply_proof",
        }
