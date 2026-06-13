"""Provider receipt report builder — FINAL-PR-11."""
from __future__ import annotations

from odin.local_provider_receipts.provider_ids import CLAIM_BOUNDARY, NOT_PROVEN_BASE, RECOGNIZED_PROVIDER_IDS
from odin.local_provider_receipts.readiness import build_provider_readiness_receipt


def build_provider_receipt_harness_report(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build a structural report on the provider receipt harness."""
    receipts = {
        pid: build_provider_readiness_receipt(pid, generated_at_utc=generated_at_utc)
        for pid in sorted(RECOGNIZED_PROVIDER_IDS)
    }
    return {
        "artifact_kind": "odin_provider_receipt_harness_report",
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "app_apply": False,
        "external_send": False,
        "public_network": False,
        "execution_performed": False,
        "model_inference": False,
        "provider_execution": False,
        "evidence_class": "structural_evidence",
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(NOT_PROVEN_BASE),
        "provider_readiness_receipts": receipts,
        "recognized_provider_ids": sorted(RECOGNIZED_PROVIDER_IDS),
        "generated_at_utc": generated_at_utc,
    }


def build_local_provider_doctor_report(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build a doctor report for local provider harness status."""
    return {
        "artifact_kind": "odin_local_provider_doctor_report",
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "evidence_class": "structural_evidence",
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(NOT_PROVEN_BASE),
        "execution_by_default": False,
        "recognized_providers": sorted(RECOGNIZED_PROVIDER_IDS),
        "execution_gate_rules": [
            "allow_local_provider_execution=True required",
            "ODIN_ENABLE_LOCAL_PROVIDER_EXECUTION=1 env var required",
            "provider_id must be in executable set",
            "timeout_seconds <= 60",
            "max_input_chars <= 8000",
            "no shell=True",
            "no remote URL",
            "no API key",
            "no public network",
        ],
        "generated_at_utc": generated_at_utc,
    }
