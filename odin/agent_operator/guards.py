"""Guard checks for Odin Agent Operator Mode."""

from __future__ import annotations

from typing import Any

HARD_FORBIDDEN_ACTIONS = {
    "app_state_apply",
    "external_send",
    "hidden_tool_execution",
    "provider_api_call_without_receipt",
    "claiming_proof_without_receipt",
    "secret_exfiltration",
    "network_transport_by_default",
    "domain_state_mutation",
    "unbounded_file_edit",
}

HARD_DENIED_PERMISSION_FIELDS = {
    "may_apply_app_state",
    "may_send_external",
    "may_call_provider_api",
    "may_use_hidden_tools",
    "may_mutate_domain_state",
}


def check_forbidden_actions(packet: dict[str, Any]) -> dict[str, Any]:
    """Check that a packet does not declare or request forbidden actions.

    Returns {"status": "ok"} or {"status": "blocked", "violations": [...]}
    """
    violations: list[str] = []
    declared = set(packet.get("forbidden_actions", []))
    for hard in HARD_FORBIDDEN_ACTIONS:
        if hard not in declared:
            violations.append(f"missing required forbidden_action: {hard}")
    # Check invariants
    if packet.get("candidate_only") is not True:
        violations.append("candidate_only must be true")
    if packet.get("app_owned_apply") is not True:
        violations.append("app_owned_apply must be true")
    if packet.get("external_send_default") is not False:
        violations.append("external_send_default must be false")
    if packet.get("network_transport_default") is not False:
        violations.append("network_transport_default must be false")
    if packet.get("hidden_tool_execution_allowed") is not False:
        violations.append("hidden_tool_execution_allowed must be false")
    if violations:
        return {"status": "blocked", "violations": violations}
    return {"status": "ok", "violations": []}


def check_file_scope(
    packet: dict[str, Any], changed_files: list[str]
) -> dict[str, Any]:
    """Check that changed files respect the packet's allowed/forbidden lists.

    Returns {"status": "ok"} or {"status": "blocked", "violations": [...]}
    """
    violations: list[str] = []
    allowed = packet.get("allowed_files", [])
    forbidden = packet.get("forbidden_files", [])

    for cf in changed_files:
        if forbidden and any(cf.startswith(f.rstrip("*")) for f in forbidden if f):
            violations.append(f"forbidden file change: {cf}")
        if allowed and not any(
            cf == a or cf.startswith(a.rstrip("*")) for a in allowed if a
        ):
            violations.append(f"file not in allowed list: {cf}")

    if violations:
        return {"status": "blocked", "violations": violations}
    return {"status": "ok", "violations": []}


def validate_permission_card(card: dict[str, Any]) -> dict[str, Any]:
    """Validate that a permission card has all hard-denied fields set to False.

    Returns {"status": "ok"} or {"status": "blocked", "violations": [...]}
    """
    violations: list[str] = []
    for field in HARD_DENIED_PERMISSION_FIELDS:
        if card.get(field) is not False:
            violations.append(f"permission card must have {field}=false")
    if violations:
        return {"status": "blocked", "violations": violations}
    return {"status": "ok", "violations": []}
