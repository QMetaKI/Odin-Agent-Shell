"""QIRC Core channel registry — local-only default channels.

Claim boundary: qirc_core_first_slice_local_only_not_public_network_not_app_apply
"""
from __future__ import annotations

REQUIRED_CHANNELS = [
    "#odin.runtime",
    "#odin.activity",
    "#odin.trace",
    "#odin.receipt",
    "#odin.handoff",
    "#odin.dev",
    "#odin.warning",
    "#odin.model",  # FINAL-PR-04: provider probe and model status events
]

_CHANNEL_SET = set(REQUIRED_CHANNELS)


def is_valid_channel(channel: str) -> bool:
    return channel in _CHANNEL_SET


def list_channels() -> list[dict]:
    return [
        {
            "channel": ch,
            "local_only": True,
            "candidate_only": True,
            "claim_boundary": "qirc_core_first_slice_local_only_not_public_network_not_app_apply",
        }
        for ch in REQUIRED_CHANNELS
    ]
