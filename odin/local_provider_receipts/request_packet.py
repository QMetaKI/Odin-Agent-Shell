"""Provider request packet builder — FINAL-PR-11."""
from __future__ import annotations

import hashlib
import json

from odin.local_provider_receipts.provider_ids import CLAIM_BOUNDARY, NOT_PROVEN_BASE

_MAX_INPUT_CHARS_HARD_LIMIT = 8000
_MAX_TIMEOUT_HARD_LIMIT = 60


def _sha256_id(prefix: str, payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    h = hashlib.sha256(raw.encode()).hexdigest()[:16]
    return f"{prefix}{h}"


def build_provider_request_packet(
    provider_id: str,
    prompt: str,
    *,
    model_hint: str | None = None,
    max_input_chars: int = 4000,
    timeout_seconds: int = 30,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build a provider request packet with input clamping.

    Clamps max_input_chars to _MAX_INPUT_CHARS_HARD_LIMIT.
    Clamps timeout_seconds to _MAX_TIMEOUT_HARD_LIMIT.
    Truncates prompt to max_input_chars.
    Never executes provider. Never sends externally.
    """
    clamped_chars = min(max_input_chars, _MAX_INPUT_CHARS_HARD_LIMIT)
    clamped_timeout = min(timeout_seconds, _MAX_TIMEOUT_HARD_LIMIT)
    truncated_prompt = prompt[:clamped_chars]
    input_hash = hashlib.sha256(truncated_prompt.encode()).hexdigest()[:32]
    packet_id = _sha256_id(
        "provider_req_",
        {
            "provider_id": provider_id,
            "input_hash": input_hash,
            "model_hint": model_hint,
            "generated_at_utc": generated_at_utc,
        },
    )
    return {
        "artifact_kind": "odin_provider_request_packet",
        "packet_id": packet_id,
        "provider_id": provider_id,
        "prompt_truncated": truncated_prompt,
        "input_hash": input_hash,
        "model_hint": model_hint,
        "max_input_chars": clamped_chars,
        "timeout_seconds": clamped_timeout,
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "app_apply": False,
        "external_send": False,
        "public_network": False,
        "evidence_class": "structural_evidence",
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(NOT_PROVEN_BASE),
        "generated_at_utc": generated_at_utc,
    }
