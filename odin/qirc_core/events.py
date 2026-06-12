"""QIRC Core event packet schema and builder.

Claim boundary: qirc_core_first_slice_local_only_not_public_network_not_app_apply
"""
from __future__ import annotations

import hashlib
import json
import time

CLAIM_BOUNDARY = "qirc_core_first_slice_local_only_not_public_network_not_app_apply"

REQUIRED_EVENT_FIELDS = [
    "event_id",
    "channel",
    "kind",
    "source",
    "candidate_only",
    "local_only",
    "payload",
    "claim_boundary",
]


def _stable_event_id(channel: str, kind: str, source: str, payload: dict) -> str:
    raw = json.dumps({"channel": channel, "kind": kind, "source": source, "payload": payload}, sort_keys=True)
    return "QEVT-" + hashlib.sha256(raw.encode()).hexdigest()[:16]


def build_qirc_event(
    channel: str,
    kind: str,
    source: str,
    payload: dict | None = None,
    trace_ref: str | None = None,
    receipt_ref: str | None = None,
) -> dict:
    if payload is None:
        payload = {}
    event_id = _stable_event_id(channel, kind, source, payload)
    return {
        "event_id": event_id,
        "channel": channel,
        "kind": kind,
        "source": source,
        "candidate_only": True,
        "local_only": True,
        "payload": payload,
        "trace_ref": trace_ref,
        "receipt_ref": receipt_ref,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def validate_event_shape(event: dict) -> list[str]:
    errors = []
    for field in REQUIRED_EVENT_FIELDS:
        if field not in event:
            errors.append(f"event missing field: {field}")
    if event.get("candidate_only") is not True:
        errors.append("event must have candidate_only: true")
    if event.get("local_only") is not True:
        errors.append("event must have local_only: true")
    if not event.get("claim_boundary"):
        errors.append("event must have claim_boundary")
    return errors
