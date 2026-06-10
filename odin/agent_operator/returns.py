"""Return report builder for Odin Agent Operator Mode."""

from __future__ import annotations

from typing import Any


def build_return_report_skeleton(
    packet_id: str,
    agent_profile_id: str,
    implemented: list[str] | None = None,
    changed_files: list[str] | None = None,
    skipped: list[str] | None = None,
    blocked: list[str] | None = None,
) -> dict[str, Any]:
    """Build an Agent Return Report skeleton from a packet ID and profile.

    The skeleton marks proof boundaries as gaps — the agent fills them in.
    """
    return {
        "artifact_kind": "odin_agent_return_report",
        "schema_version": "1.0",
        "packet_id": packet_id,
        "agent_profile_id": agent_profile_id,
        "implemented": implemented or [],
        "changed_files": changed_files or [],
        "commands_run": [],
        "results": {},
        "skipped": skipped or [],
        "blocked": blocked or [],
        "proof_boundaries": [
            "no_app_apply_by_agent",
            "no_external_send_by_agent",
            "no_hidden_tool_execution",
            "candidate_only_output",
        ],
        "senior_reviewer_simulation": {
            "architecture": "skeleton — fill in after implementation",
            "scope": "skeleton — fill in after implementation",
            "risks": [],
            "verdict": "not_ready",
            "verdict_reason": "skeleton not yet filled",
        },
        "senior_code_reviewer_simulation": {
            "code_repo": "skeleton — fill in after implementation",
            "tests": "skeleton — fill in after implementation",
            "fixes_applied": [],
            "verdict": "not_ready",
        },
        "ready_for_review": False,
        "claim_boundary": "return_report_skeleton_not_proof_closed",
        "next_recommended_pr": "LRH-PR-03 — Portable Local Runtime Starter",
    }


def validate_return_report(report: dict[str, Any]) -> dict[str, Any]:
    """Validate a return report for required fields and proof boundaries.

    Returns {"status": "ok"} or {"status": "invalid", "errors": [...]}
    """
    errors: list[str] = []
    required_fields = [
        "artifact_kind", "schema_version", "packet_id", "agent_profile_id",
        "implemented", "changed_files", "commands_run", "results",
        "skipped", "blocked", "proof_boundaries",
        "senior_reviewer_simulation", "senior_code_reviewer_simulation",
        "ready_for_review", "claim_boundary",
    ]
    for field in required_fields:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("artifact_kind") != "odin_agent_return_report":
        errors.append("artifact_kind must be odin_agent_return_report")
    if not report.get("proof_boundaries"):
        errors.append("proof_boundaries must not be empty")
    if errors:
        return {"status": "invalid", "errors": errors}
    return {"status": "ok", "errors": []}
