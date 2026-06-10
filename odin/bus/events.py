from __future__ import annotations

import json
from typing import Any

from odin.runtime.ids import stable_digest, stable_id, utc_stamp

FORBIDDEN_EVENT_MARKERS = ("app.apply", "app_apply", "external.send", "external_send", "mutate_app_state")


def sanitize_bus_event_type(event_type: str) -> tuple[str, str]:
    normalized = str(event_type or "runtime.event")
    lowered = normalized.lower()
    if any(marker in lowered for marker in FORBIDDEN_EVENT_MARKERS):
        return "runtime.boundary_rejected", f"downgraded_forbidden_event_type:{normalized}"
    return normalized, "accepted"


def _payload_digest(payload: Any) -> str:
    try:
        redaction_shape = {
            "type": type(payload).__name__,
            "keys": sorted(payload.keys()) if isinstance(payload, dict) else None,
            "digest": stable_digest(payload, 24),
        }
    except Exception:
        redaction_shape = {"type": type(payload).__name__, "digest": stable_digest(str(payload), 24)}
    return stable_digest(redaction_shape, 24)


def build_bus_event(
    *,
    event_type: str,
    work_id: str | None,
    session_id: str | None,
    trace_id: str | None,
    payload: Any | None = None,
    source: str = "odin.runtime",
) -> dict:
    safe_type, boundary_status = sanitize_bus_event_type(event_type)
    digest = _payload_digest(payload or {})
    event_basis = {
        "event_type": safe_type,
        "work_id": work_id or "UNKNOWN",
        "session_id": session_id or "UNKNOWN",
        "trace_id": trace_id or "UNKNOWN",
        "payload_digest": digest,
        "source": source,
    }
    return {
        "artifact_kind": "odin_runtime_bus_event_record",
        "protocol_version": "7.1",
        "event_id": stable_id("BUS", event_basis, 16),
        "event_type": safe_type,
        "work_id": work_id or "UNKNOWN",
        "session_id": session_id or "UNKNOWN",
        "trace_id": trace_id or "UNKNOWN",
        "source": source,
        "payload_digest": digest,
        "payload_ref": "redacted_local_payload_digest_only",
        "created_at": utc_stamp(),
        "candidate_only": True,
        "local_only": True,
        "boundary_status": boundary_status,
        "claim_boundary": "local_semantic_bus_event_no_app_apply_no_external_send_no_network_transport",
    }


def event_to_json_line(event: dict) -> str:
    return json.dumps(event, ensure_ascii=False, sort_keys=True)
