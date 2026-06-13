"""Recognized local provider IDs for FINAL-PR-11 receipt harness."""
from __future__ import annotations

CLAIM_BOUNDARY = "local_provider_receipt_harness_scoped_local_receipts_not_quality_benchmark"

RECOGNIZED_PROVIDER_IDS: set[str] = {
    "ollama_candidate",
    "llama_cpp_candidate",
    "mock_provider",
    "deterministic_no_provider",
}

EXECUTABLE_PROVIDER_IDS: set[str] = {
    "ollama_candidate",
    "llama_cpp_candidate",
}

NOT_PROVEN_BASE: list[str] = [
    "production_readiness",
    "security_certification",
    "release_certification",
    "real_model_benchmark",
    "model_quality_superiority",
    "live_model_inference",
    "app_apply",
    "app_state_mutation",
    "external_send",
    "public_network",
]
