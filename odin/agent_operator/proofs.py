"""Proof boundary utilities for Odin Agent Operator Mode."""

from __future__ import annotations

from typing import Any

PROOF_GAP_TOKENS = {
    "runtime_verified",
    "host_validated",
    "model_inference_verified",
    "network_verified",
    "security_verified",
    "production_ready",
    "deploy_verified",
    "patch_applied",
    "tests_passed",
    "full_implementation_complete",
}


def emit_proof_boundary_summary(packet: dict[str, Any]) -> dict[str, Any]:
    """Emit a proof boundary status for a packet.

    Does not close proof gaps — only reports them.
    """
    boundaries = packet.get("proof_boundaries", [])
    missing: list[str] = []
    if not boundaries:
        missing.append("no proof_boundaries declared")
    required_receipts = [
        "no_app_apply_by_agent",
        "no_external_send_by_agent",
        "no_hidden_tool_execution",
    ]
    declared_lower = [b.lower() for b in boundaries]
    for req in required_receipts:
        if not any(req in b for b in declared_lower):
            missing.append(f"missing required proof boundary token: {req}")

    return {
        "status": "gaps_present" if missing else "ok",
        "declared_boundaries": boundaries,
        "missing_receipts": missing,
        "claim_boundary": "proof_boundary_report_not_proof_closure",
    }


def check_required_commands(packet: dict[str, Any], run_commands: list[str]) -> dict[str, Any]:
    """Check that all required commands from a packet were declared as run.

    Returns {"status": "ok"} or {"status": "incomplete", "missing": [...]}
    """
    required = packet.get("required_commands", [])
    missing = [cmd for cmd in required if cmd not in run_commands]
    if missing:
        return {
            "status": "incomplete",
            "missing": missing,
            "claim_boundary": "required_commands_check_not_runtime_proof",
        }
    return {
        "status": "ok",
        "missing": [],
        "claim_boundary": "required_commands_check_not_runtime_proof",
    }
