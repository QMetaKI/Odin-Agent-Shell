"""Execution gate policy — FINAL-PR-05.

Claim boundary: final_pr_05_execution_gate_mock_only_not_model_quality_not_production
candidate_only: true
local_only: true
"""
from __future__ import annotations

from dataclasses import dataclass, field

CLAIM_BOUNDARY = "final_pr_05_execution_gate_mock_only_not_model_quality_not_production"


@dataclass
class ExecutionGatePolicy:
    execution_gate_enabled: bool = True
    mock_execution_allowed: bool = True
    local_candidate_execution_allowed: bool = False
    remote_execution_allowed: bool = False
    api_key_required: bool = False
    api_key_reads_allowed: bool = False
    external_network_allowed: bool = False
    app_apply_allowed: bool = False
    app_state_mutation_allowed: bool = False
    external_send_allowed: bool = False
    candidate_only: bool = True
    local_only: bool = True
    claim_boundary: str = CLAIM_BOUNDARY

    def as_dict(self) -> dict:
        return {
            "artifact_kind": "odin_execution_gate_policy",
            "execution_gate_enabled": self.execution_gate_enabled,
            "mock_execution_allowed": self.mock_execution_allowed,
            "local_candidate_execution_allowed": self.local_candidate_execution_allowed,
            "remote_execution_allowed": self.remote_execution_allowed,
            "api_key_required": self.api_key_required,
            "api_key_reads_allowed": self.api_key_reads_allowed,
            "external_network_allowed": self.external_network_allowed,
            "app_apply_allowed": self.app_apply_allowed,
            "app_state_mutation_allowed": self.app_state_mutation_allowed,
            "external_send_allowed": self.external_send_allowed,
            "candidate_only": self.candidate_only,
            "local_only": self.local_only,
            "claim_boundary": self.claim_boundary,
        }

    def check_mock_execution(self) -> tuple[bool, str]:
        if not self.execution_gate_enabled:
            return False, "execution_gate_disabled"
        if not self.mock_execution_allowed:
            return False, "mock_execution_not_allowed"
        return True, "allowed"

    def check_local_candidate(self) -> tuple[bool, str]:
        if not self.local_candidate_execution_allowed:
            return False, "local_candidate_execution_blocked_by_default"
        return True, "allowed"

    def check_remote(self) -> tuple[bool, str]:
        if self.remote_execution_allowed:
            return False, "remote_execution_forbidden"
        return False, "remote_execution_blocked"

    def check_api_key_read(self) -> tuple[bool, str]:
        if self.api_key_reads_allowed:
            return False, "api_key_reads_forbidden"
        return False, "api_key_reads_blocked"


DEFAULT_EXECUTION_GATE_POLICY = ExecutionGatePolicy()
