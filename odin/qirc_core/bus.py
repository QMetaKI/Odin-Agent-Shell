"""QIRC Core in-memory event bus.

Claim boundary: qirc_core_first_slice_local_only_not_public_network_not_app_apply
local_only: true
candidate_only: true
No app state mutation. No external sends. No provider execution.
"""
from __future__ import annotations

from odin.qirc_core.channels import REQUIRED_CHANNELS, is_valid_channel
from odin.qirc_core.events import build_qirc_event
from odin.qirc_core.policy import DEFAULT_POLICY, CLAIM_BOUNDARY

_GLOBAL_BUS: list[dict] = []


class QircBus:
    """Thin wrapper around the module-level bus for object-oriented access."""

    def append(self, channel: str, kind: str, source: str, payload: dict | None = None,
               trace_ref: str | None = None, receipt_ref: str | None = None) -> dict:
        return append_event(channel=channel, kind=kind, source=source,
                            payload=payload, trace_ref=trace_ref, receipt_ref=receipt_ref)

    def list(self, channel: str | None = None) -> list[dict]:
        return list_events(channel)

    def clear(self) -> None:
        clear_bus()

    def summary(self) -> dict:
        return bus_summary()


def _get_bus() -> list[dict]:
    return _GLOBAL_BUS


def append_event(channel: str, kind: str, source: str, payload: dict | None = None, trace_ref: str | None = None, receipt_ref: str | None = None) -> dict:
    original_channel = channel
    if not is_valid_channel(channel):
        channel = "#odin.warning"
        payload = {"original_channel": original_channel, **(payload or {})}
    event = build_qirc_event(channel=channel, kind=kind, source=source, payload=payload or {}, trace_ref=trace_ref, receipt_ref=receipt_ref)
    _GLOBAL_BUS.append(event)
    return event


def list_events(channel: str | None = None) -> list[dict]:
    if channel is None:
        return list(_GLOBAL_BUS)
    return [e for e in _GLOBAL_BUS if e.get("channel") == channel]


def clear_bus() -> None:
    _GLOBAL_BUS.clear()


def bus_summary() -> dict:
    policy_errors = DEFAULT_POLICY.check()
    return {
        "artifact_kind": "odin_qirc_bus_summary",
        "event_count": len(_GLOBAL_BUS),
        "channels": sorted({e["channel"] for e in _GLOBAL_BUS}),
        "available_channels": REQUIRED_CHANNELS,
        "policy_safe": len(policy_errors) == 0,
        "policy_errors": policy_errors,
        "candidate_only": True,
        "local_only": True,
        "app_state_mutated": False,
        "external_sent": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }
