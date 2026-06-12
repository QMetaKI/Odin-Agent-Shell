"""Execution gate — FINAL-PR-05.

Claim boundary: final_pr_05_execution_gate_mock_only_not_model_quality_not_production
candidate_only: true
local_only: true
"""
from .gateway import ExecutionGateway, execute_candidate
from .policy import ExecutionGatePolicy, DEFAULT_EXECUTION_GATE_POLICY
from .mock_provider import MockProvider, build_mock_response
from .local_candidate_policy import LocalCandidatePolicy, DEFAULT_LOCAL_CANDIDATE_POLICY
from .proof import build_execution_gate_proof_packet

__all__ = [
    "ExecutionGateway",
    "execute_candidate",
    "ExecutionGatePolicy",
    "DEFAULT_EXECUTION_GATE_POLICY",
    "MockProvider",
    "build_mock_response",
    "LocalCandidatePolicy",
    "DEFAULT_LOCAL_CANDIDATE_POLICY",
    "build_execution_gate_proof_packet",
]
