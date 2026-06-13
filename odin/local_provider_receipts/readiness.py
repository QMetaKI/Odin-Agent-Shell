"""Provider readiness receipt builder — FINAL-PR-11."""
from __future__ import annotations

import hashlib
import json

from odin.local_provider_receipts.provider_ids import (
    CLAIM_BOUNDARY,
    NOT_PROVEN_BASE,
    RECOGNIZED_PROVIDER_IDS,
)


def _sha256_id(prefix: str, payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    h = hashlib.sha256(raw.encode()).hexdigest()[:16]
    return f"{prefix}{h}"


def build_provider_readiness_receipt(
    provider_id: str,
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build a provider readiness receipt.

    Always deterministic. Never executes model. Never contacts provider.
    evidence_class is always structural_evidence for this function.
    """
    recognized = provider_id in RECOGNIZED_PROVIDER_IDS
    receipt_id = _sha256_id(
        "provider_readiness_",
        {"provider_id": provider_id, "generated_at_utc": generated_at_utc},
    )
    return {
        "artifact_kind": "odin_provider_readiness_receipt",
        "receipt_id": receipt_id,
        "provider_id": provider_id,
        "recognized": recognized,
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "app_apply": False,
        "external_send": False,
        "public_network": False,
        "execution_allowed": False,
        "execution_performed": False,
        "model_inference": False,
        "provider_execution": False,
        "evidence_class": "structural_evidence",
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(NOT_PROVEN_BASE),
        "generated_at_utc": generated_at_utc,
        "note": (
            "Structural readiness receipt only. "
            "Does not prove provider availability or model quality."
        ),
    }
