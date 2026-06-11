"""Proof boundary utilities for Odin Agent Operator Mode."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[2]
_AGENT_PROOF_REGISTRY = _ROOT / "registries" / "agent_proof_boundary_registry_v1.json"

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


def _load_agent_proof_registry_receipts() -> dict[str, str]:
    """Load receipt statuses from agent_proof_boundary_registry_v1.json if available."""
    if not _AGENT_PROOF_REGISTRY.exists():
        return {}
    try:
        data = json.loads(_AGENT_PROOF_REGISTRY.read_text(encoding="utf-8"))
        receipts = data.get("receipts", {})
        return {k: v.get("status", "missing") for k, v in receipts.items()}
    except Exception:
        return {}


def emit_proof_boundary_summary(packet: dict[str, Any]) -> dict[str, Any]:
    """Emit a proof boundary status for a packet.

    Checks both packet proof_boundaries and the agent_proof_boundary_registry_v1.json
    for receipt closure (LRH-PR-18 closes the three required receipts via registry).
    Does not close proof gaps through authority expansion — only reports receipt status.
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

    registry_receipts = _load_agent_proof_registry_receipts()
    registry_receipt_map = {
        "no_app_apply_by_agent": "no_app_apply_by_agent_receipt",
        "no_external_send_by_agent": "no_external_send_by_agent_receipt",
        "no_hidden_tool_execution": "no_hidden_tool_execution_receipt",
    }

    for req in required_receipts:
        in_packet = any(req in b for b in declared_lower)
        registry_key = registry_receipt_map.get(req, "")
        in_registry = registry_receipts.get(registry_key) == "closed"
        if not in_packet and not in_registry:
            missing.append(f"missing required proof boundary token: {req}")

    return {
        "status": "gaps_present" if missing else "ok",
        "declared_boundaries": boundaries,
        "registry_receipts_checked": bool(registry_receipts),
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
