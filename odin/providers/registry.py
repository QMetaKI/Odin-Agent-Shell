"""Provider registry — FINAL-PR-04.

Claim boundary: provider_probe_candidate_only_no_model_execution_no_api_key_no_external_network
candidate_only: true
local_only: true
"""
from __future__ import annotations

from .policy import PROVIDER_POLICIES

PROVIDER_REGISTRY: dict[str, dict] = {
    pid: policy.as_dict()
    for pid, policy in PROVIDER_POLICIES.items()
}

REQUIRED_PROVIDER_IDS = ["none", "mock", "ollama_candidate", "llama_cpp_candidate"]


def list_provider_ids() -> list[str]:
    return list(PROVIDER_REGISTRY.keys())


def get_provider_entry(provider_id: str) -> dict | None:
    return PROVIDER_REGISTRY.get(provider_id)


def validate_registry() -> list[str]:
    errors = []
    for pid in REQUIRED_PROVIDER_IDS:
        if pid not in PROVIDER_REGISTRY:
            errors.append(f"missing required provider in registry: {pid}")
            continue
        entry = PROVIDER_REGISTRY[pid]
        if entry.get("execution_allowed", True):
            errors.append(f"provider {pid} has execution_allowed=True (forbidden for FINAL-PR-04)")
        if pid in ("ollama_candidate", "llama_cpp_candidate"):
            if entry.get("remote", True):
                errors.append(f"provider {pid} has remote=True (forbidden)")
            if entry.get("requires_api_key", True):
                errors.append(f"provider {pid} has requires_api_key=True (forbidden)")
    return errors
