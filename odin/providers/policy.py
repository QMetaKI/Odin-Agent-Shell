"""Provider policy definitions — FINAL-PR-04.

Claim boundary: provider_probe_candidate_only_no_model_execution_no_api_key_no_external_network
candidate_only: true
local_only: true

Policy does NOT execute providers. Policy only describes readiness gates.
"""
from __future__ import annotations

from dataclasses import dataclass, field

CLAIM_BOUNDARY = "provider_probe_candidate_only_no_model_execution_no_api_key_no_external_network"


@dataclass
class ProviderPolicy:
    provider_id: str
    provider_kind: str
    probe_allowed: bool
    execution_allowed: bool
    remote: bool
    local: bool
    requires_api_key: bool
    candidate_only: bool
    default_enabled: bool
    claim_boundary: str = CLAIM_BOUNDARY
    notes: str = ""

    def as_dict(self) -> dict:
        return {
            "provider_id": self.provider_id,
            "provider_kind": self.provider_kind,
            "probe_allowed": self.probe_allowed,
            "execution_allowed": self.execution_allowed,
            "remote": self.remote,
            "local": self.local,
            "requires_api_key": self.requires_api_key,
            "candidate_only": self.candidate_only,
            "default_enabled": self.default_enabled,
            "claim_boundary": self.claim_boundary,
            "notes": self.notes,
        }


PROVIDER_POLICIES: dict[str, ProviderPolicy] = {
    "none": ProviderPolicy(
        provider_id="none",
        provider_kind="none",
        probe_allowed=True,
        execution_allowed=False,
        remote=False,
        local=True,
        requires_api_key=False,
        candidate_only=True,
        default_enabled=True,
        notes="No provider active. Safe default state.",
    ),
    "mock": ProviderPolicy(
        provider_id="mock",
        provider_kind="mock",
        probe_allowed=True,
        execution_allowed=False,
        remote=False,
        local=True,
        requires_api_key=False,
        candidate_only=True,
        default_enabled=True,
        notes="Mock provider returns deterministic demo candidates only. No model inference.",
    ),
    "ollama_candidate": ProviderPolicy(
        provider_id="ollama_candidate",
        provider_kind="local_candidate",
        probe_allowed=True,
        execution_allowed=False,
        remote=False,
        local=True,
        requires_api_key=False,
        candidate_only=True,
        default_enabled=False,
        notes="Ollama binary availability probe only. No model run, no chat, no generate, no embeddings.",
    ),
    "llama_cpp_candidate": ProviderPolicy(
        provider_id="llama_cpp_candidate",
        provider_kind="local_candidate",
        probe_allowed=True,
        execution_allowed=False,
        remote=False,
        local=True,
        requires_api_key=False,
        candidate_only=True,
        default_enabled=False,
        notes="llama.cpp binary availability probe only. No model load, no inference.",
    ),
}


def get_policy(provider_id: str) -> ProviderPolicy | None:
    return PROVIDER_POLICIES.get(provider_id)


def list_policies() -> list[dict]:
    return [p.as_dict() for p in PROVIDER_POLICIES.values()]
