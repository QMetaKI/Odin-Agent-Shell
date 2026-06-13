"""Main entry point: run_local_provider_receipt — FINAL-PR-11."""
from __future__ import annotations

from odin.local_provider_receipts.provider_ids import (
    CLAIM_BOUNDARY,
    NOT_PROVEN_BASE,
    RECOGNIZED_PROVIDER_IDS,
)
from odin.local_provider_receipts.readiness import build_provider_readiness_receipt
from odin.local_provider_receipts.request_packet import build_provider_request_packet


def run_local_provider_receipt(
    provider_id: str,
    prompt: str,
    *,
    allow_local_provider_execution: bool = False,
    model_hint: str | None = None,
    timeout_seconds: int = 30,
    max_input_chars: int = 4000,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build a local provider receipt.

    Default: execution disabled, returns structural_evidence receipt.
    If allow_local_provider_execution=True AND env var set, delegates to executor.
    Never raises. Never mutates app state. Never sends externally.
    """
    readiness = build_provider_readiness_receipt(provider_id, generated_at_utc=generated_at_utc)
    request = build_provider_request_packet(
        provider_id,
        prompt,
        model_hint=model_hint,
        max_input_chars=max_input_chars,
        timeout_seconds=timeout_seconds,
        generated_at_utc=generated_at_utc,
    )
    input_hash = request["input_hash"]

    if provider_id not in RECOGNIZED_PROVIDER_IDS:
        return {
            "artifact_kind": "odin_provider_execution_receipt",
            "status": "provider_not_allowed",
            "provider_id": provider_id,
            "input_hash": input_hash,
            "execution_allowed": False,
            "execution_performed": False,
            "model_inference": False,
            "provider_execution": False,
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
            "readiness": readiness,
        }

    if not allow_local_provider_execution:
        return {
            "artifact_kind": "odin_provider_execution_receipt",
            "status": "execution_not_enabled",
            "provider_id": provider_id,
            "input_hash": input_hash,
            "execution_allowed": False,
            "execution_performed": False,
            "model_inference": False,
            "provider_execution": False,
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
            "readiness": readiness,
        }

    from odin.local_provider_receipts.executor import run_executor
    return run_executor(
        provider_id=provider_id,
        prompt=prompt,
        allow_local_provider_execution=allow_local_provider_execution,
        model_hint=model_hint,
        timeout_seconds=timeout_seconds,
        max_input_chars=max_input_chars,
        generated_at_utc=generated_at_utc,
    )
