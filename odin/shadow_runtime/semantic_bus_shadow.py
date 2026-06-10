from __future__ import annotations

from typing import Any, Dict, Iterable, List

from .constants import REQUIRED_CHANNELS
from .types import ShadowBusEvent, ShadowReason


def make_shadow_bus_event(index: int, work_id: str, trace_id: str, channel: str, event_type: str, source_module: str, payload: Dict[str, Any] | None = None) -> ShadowBusEvent:
    if not channel.startswith("#"):
        raise ValueError("shadow bus channel must start with #")
    return ShadowBusEvent(
        event_id=f"SBE-{index:04d}",
        channel=channel,
        event_type=event_type,
        work_id=work_id,
        trace_id=trace_id,
        source_module=source_module,
        payload=payload or {},
    )


def make_shadow_bus_batch(work_id: str, trace_id: str, route_hint: str = "standard_local") -> List[ShadowBusEvent]:
    events: List[ShadowBusEvent] = []
    for idx, channel in enumerate(REQUIRED_CHANNELS, start=1):
        module = channel.strip("#").replace(".", "-")
        event_type = channel.strip("#").replace(".", "_")
        payload = {"route_hint": route_hint, "local_only": True}
        events.append(make_shadow_bus_event(idx, work_id, trace_id, channel, event_type, module, payload))
    return events


def validate_shadow_bus_events(events: Iterable[ShadowBusEvent]) -> List[ShadowReason]:
    reasons: List[ShadowReason] = []
    seen_ready = False
    for event in events:
        if not event.channel.startswith("#"):
            reasons.append(ShadowReason("invalid_bus_channel", "bus channel must start with #"))
        if event.privacy_class != "local_only":
            reasons.append(ShadowReason("bus_privacy_invalid", "shadow bus event must be local_only"))
        if event.channel == "#candidate.ready":
            seen_ready = True
    if not seen_ready:
        reasons.append(ShadowReason("candidate_ready_missing", "shadow bus batch must include #candidate.ready"))
    return reasons
