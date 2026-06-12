"""Local candidate execution policy — blocked by default — FINAL-PR-05.

Claim boundary: final_pr_05_local_candidate_blocked_by_default_not_model_inference
candidate_only: true
local_only: true
"""
from __future__ import annotations

from dataclasses import dataclass, field

CLAIM_BOUNDARY = "final_pr_05_local_candidate_blocked_by_default_not_model_inference"

SUPPORTED_LOCAL_CANDIDATES = ["ollama_candidate", "llama_cpp_candidate"]


@dataclass
class LocalCandidatePolicy:
    provider_id: str
    local_candidate_execution_allowed: bool = False
    requires_explicit_future_gate: bool = True
    ci_skip_if_missing: bool = True
    ci_must_not_require_binary: bool = True
    network_forbidden: bool = True
    api_key_forbidden: bool = True
    claim_boundary: str = CLAIM_BOUNDARY

    def as_dict(self) -> dict:
        return {
            "artifact_kind": "odin_local_candidate_policy",
            "provider_id": self.provider_id,
            "local_candidate_execution_allowed": self.local_candidate_execution_allowed,
            "requires_explicit_future_gate": self.requires_explicit_future_gate,
            "ci_skip_if_missing": self.ci_skip_if_missing,
            "ci_must_not_require_binary": self.ci_must_not_require_binary,
            "network_forbidden": self.network_forbidden,
            "api_key_forbidden": self.api_key_forbidden,
            "candidate_only": True,
            "local_only": True,
            "claim_boundary": self.claim_boundary,
        }

    def check_attempt(self) -> dict:
        return {
            "allowed": False,
            "reason": "local_candidate_execution_blocked_by_default",
            "requires_explicit_future_gate": self.requires_explicit_future_gate,
            "provider_id": self.provider_id,
            "candidate_only": True,
            "claim_boundary": self.claim_boundary,
        }


DEFAULT_LOCAL_CANDIDATE_POLICIES: dict[str, LocalCandidatePolicy] = {
    "ollama_candidate": LocalCandidatePolicy(provider_id="ollama_candidate"),
    "llama_cpp_candidate": LocalCandidatePolicy(provider_id="llama_cpp_candidate"),
}

DEFAULT_LOCAL_CANDIDATE_POLICY = LocalCandidatePolicy(provider_id="default")


def get_local_candidate_policy(provider_id: str) -> LocalCandidatePolicy:
    return DEFAULT_LOCAL_CANDIDATE_POLICIES.get(provider_id, LocalCandidatePolicy(provider_id=provider_id))


def list_local_candidate_policies() -> list[dict]:
    return [p.as_dict() for p in DEFAULT_LOCAL_CANDIDATE_POLICIES.values()]
