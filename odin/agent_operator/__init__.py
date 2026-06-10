"""Odin Agent Operator Mode — candidate-only, permission-gated, proof-bound."""

from odin.agent_operator.packets import build_agent_work_packet, validate_agent_work_packet
from odin.agent_operator.profiles import load_profile_registry, get_profile
from odin.agent_operator.guards import validate_permission_card, check_forbidden_actions, check_file_scope
from odin.agent_operator.proofs import emit_proof_boundary_summary, check_required_commands
from odin.agent_operator.returns import build_return_report_skeleton, validate_return_report

__all__ = [
    "build_agent_work_packet",
    "validate_agent_work_packet",
    "load_profile_registry",
    "get_profile",
    "validate_permission_card",
    "check_forbidden_actions",
    "check_file_scope",
    "emit_proof_boundary_summary",
    "check_required_commands",
    "build_return_report_skeleton",
    "validate_return_report",
]
