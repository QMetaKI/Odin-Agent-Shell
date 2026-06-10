"""Agent Work Packet builder and validator for Odin Agent Operator Mode."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from odin.agent_operator.profiles import get_profile
from odin.agent_operator.guards import HARD_FORBIDDEN_ACTIONS

_ROOT = Path(__file__).resolve().parents[2]


def build_agent_work_packet(
    agent_profile_id: str,
    task_source: str,
    objective: str,
    repo_scope: dict[str, Any] | None = None,
    allowed_files: list[str] | None = None,
    forbidden_files: list[str] | None = None,
    required_commands: list[str] | None = None,
    acceptance_gates: list[str] | None = None,
    required_context: list[str] | None = None,
    packet_id: str | None = None,
) -> dict[str, Any]:
    """Build a valid Agent Work Packet from a profile and task description."""
    profile = get_profile(agent_profile_id)
    if profile is None:
        raise ValueError(f"Unknown agent profile: {agent_profile_id!r}")

    pid = packet_id or f"AWP-{agent_profile_id.upper()}-CANDIDATE"
    return {
        "artifact_kind": "odin_agent_work_packet",
        "schema_version": "1.0",
        "packet_id": pid,
        "agent_profile_id": agent_profile_id,
        "task_source": task_source,
        "objective": objective,
        "repo_scope": repo_scope or {"root": ".", "branch": "main"},
        "allowed_files": allowed_files or profile.get("default_allowed_files", []),
        "forbidden_files": forbidden_files or profile.get("default_forbidden_files", []),
        "forbidden_actions": sorted(HARD_FORBIDDEN_ACTIONS),
        "required_context": required_context or profile.get("default_required_context", []),
        "required_commands": required_commands or profile.get("default_required_commands", []),
        "acceptance_gates": acceptance_gates or profile.get("default_acceptance_gates", ["validate-all passes", "pytest passes"]),
        "proof_boundaries": [
            "no_app_apply_by_agent",
            "no_external_send_by_agent",
            "no_hidden_tool_execution",
            "candidate_only_output",
        ],
        "claim_boundaries": [
            "candidate_patch_only",
            "no_runtime_proof_claimed",
            "no_host_validation_claimed",
        ],
        "senior_reviewer_required": True,
        "senior_code_reviewer_required": True,
        "thor_compatibility": profile.get("thor_compatibility", {
            "status": "conceptual",
            "claim_boundary": "thor_compatibility_conceptual_not_verified",
        }),
        "future_target_flags": [],
        "candidate_only": True,
        "app_owned_apply": True,
        "external_send_default": False,
        "network_transport_default": False,
        "hidden_tool_execution_allowed": False,
        "created_by": f"odin.agent_operator.packets (profile={agent_profile_id})",
        "created_at_policy": "deterministic_fixture",
    }


def validate_agent_work_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate an Agent Work Packet against hard invariants.

    Returns {"status": "ok"} or {"status": "invalid", "errors": [...]}
    """
    errors: list[str] = []
    required_fields = [
        "artifact_kind", "schema_version", "packet_id", "agent_profile_id",
        "task_source", "objective", "repo_scope", "allowed_files",
        "forbidden_files", "forbidden_actions", "required_context",
        "required_commands", "acceptance_gates", "proof_boundaries",
        "claim_boundaries", "senior_reviewer_required", "senior_code_reviewer_required",
        "thor_compatibility", "future_target_flags",
        "candidate_only", "app_owned_apply", "external_send_default",
        "network_transport_default", "hidden_tool_execution_allowed",
        "created_by", "created_at_policy",
    ]
    for field in required_fields:
        if field not in packet:
            errors.append(f"missing required field: {field}")

    # Hard invariants
    if packet.get("candidate_only") is not True:
        errors.append("candidate_only must be true")
    if packet.get("app_owned_apply") is not True:
        errors.append("app_owned_apply must be true")
    if packet.get("external_send_default") is not False:
        errors.append("external_send_default must be false")
    if packet.get("network_transport_default") is not False:
        errors.append("network_transport_default must be false")
    if packet.get("hidden_tool_execution_allowed") is not False:
        errors.append("hidden_tool_execution_allowed must be false")
    if packet.get("artifact_kind") != "odin_agent_work_packet":
        errors.append("artifact_kind must be odin_agent_work_packet")

    # Forbidden actions must include app_state_apply
    if "app_state_apply" not in packet.get("forbidden_actions", []):
        errors.append("forbidden_actions must include app_state_apply")

    if errors:
        return {"status": "invalid", "errors": errors}
    return {"status": "ok", "errors": []}
