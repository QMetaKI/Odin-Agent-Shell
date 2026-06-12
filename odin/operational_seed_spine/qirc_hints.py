"""QIRC hint-only layer — converts seed event hints into structured hint records.

Claim boundary: operational_seed_spine_routes_work_not_authority
candidate_only: true

Does not emit events. Does not mutate QIRC bus.
Does not authorize anything. Hint records are hint-only.
Existing QIRC registries may be read as reference shape only.
"""
from __future__ import annotations

from typing import List

CLAIM_BOUNDARY = "operational_seed_spine_routes_work_not_authority"

_DEFAULT_CHANNEL = "dev_mode"
_DEFAULT_AUTHORITY = "hint_only"

_EVENT_TYPE_TO_CHANNEL: dict[str, str] = {
    "work_seed_selected": "dev_mode",
    "repo_cognition_started": "dev_mode",
    "prompt_routed": "dev_mode",
    "code_change_scoped": "dev_mode",
    "review_audit_started": "dev_mode",
    "proof_receipt_bound": "dev_mode",
    "hub_ui_prepared": "dev_mode",
    "provider_probe_initiated": "dev_mode",
    "execution_gate_checked": "dev_mode",
    "release_closure_scoped": "dev_mode",
    "doc_architecture_scoped": "dev_mode",
    "debug_triage_started": "dev_mode",
}


def build_qirc_hints(event_hint_names: List[str]) -> List[dict]:
    """Convert seed qirc_event_hints list into structured hint-only records."""
    records = []
    for event_type in event_hint_names:
        channel = _EVENT_TYPE_TO_CHANNEL.get(event_type, _DEFAULT_CHANNEL)
        records.append({
            "event_type": event_type,
            "channel": channel,
            "authority": _DEFAULT_AUTHORITY,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return records
