"""Deterministic mock provider — FINAL-PR-05.

Claim boundary: final_pr_05_execution_gate_mock_only_not_model_quality_not_production
candidate_only: true
local_only: true

Mock execution is local and deterministic. It is NOT model inference.
No randomness, no model semantics, no quality claim.
"""
from __future__ import annotations

import hashlib
import time

CLAIM_BOUNDARY = "final_pr_05_execution_gate_mock_only_not_model_quality_not_production"


def _normalize_input(input_text: str) -> str:
    return input_text.strip().lower()[:200]


def _make_input_ref(input_text: str) -> str:
    return "INREF-" + hashlib.sha256(input_text.encode()).hexdigest()[:12]


class MockProvider:
    """Deterministic mock provider. No model. No inference. No randomness."""

    def execute(self, input_text: str, trace_ref: str | None = None, receipt_ref: str | None = None) -> dict:
        normalized = _normalize_input(input_text)
        input_ref = _make_input_ref(input_text)
        if trace_ref is None:
            trace_ref = "TRACE-" + hashlib.sha256(f"mock:{input_ref}".encode()).hexdigest()[:16]
        if receipt_ref is None:
            receipt_ref = "RCPT-" + hashlib.sha256(trace_ref.encode()).hexdigest()[:16]
        candidate_text = f"Mock candidate response for: {normalized}"
        return {
            "artifact_kind": "odin_mock_execution_response_packet",
            "provider_id": "mock",
            "execution_kind": "mock_deterministic",
            "mock_execution": True,
            "real_provider_execution": False,
            "model_inference": False,
            "candidate_only": True,
            "local_only": True,
            "app_apply": False,
            "external_send": False,
            "input_ref": input_ref,
            "candidate_text": candidate_text,
            "trace_ref": trace_ref,
            "receipt_ref": receipt_ref,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "claim_boundary": CLAIM_BOUNDARY,
        }


def build_mock_response(input_text: str, trace_ref: str | None = None, receipt_ref: str | None = None) -> dict:
    provider = MockProvider()
    return provider.execute(input_text=input_text, trace_ref=trace_ref, receipt_ref=receipt_ref)
