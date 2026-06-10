from __future__ import annotations

def build_qirc_hot_window(events: list[dict], max_events: int = 16) -> dict:
    compact = []
    seen = set()
    for event in events[-max_events:]:
        key = (event.get("channel"), event.get("event_type"), event.get("work_id"))
        if key in seen:
            continue
        seen.add(key)
        compact.append({"channel": event.get("channel"), "event_type": event.get("event_type"), "summary": event.get("payload_summary", {})})
    return {"artifact_kind": "odin_qirc_hot_window", "protocol_version": "7.1", "event_count": len(compact), "events": compact, "raw_payload_included": False}
