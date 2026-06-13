"""ModelWorkPacket builder and validator for FINAL-PR-09 Operational Spine.

Claim boundary: final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply
candidate_only: true

Builds and validates ModelWorkPacket dicts. No model execution.
"""
from __future__ import annotations

import hashlib
import json

CLAIM_BOUNDARY = "final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply"

_REQUIRED_FORBIDDEN_ACTIONS = [
    "app_state_mutation",
    "external_send",
    "hidden_tool_execution",
    "provider_execution_without_receipt",
    "claiming_proof_without_receipt",
    "domain_state_mutation",
    "app_apply",
]

_NOT_PROVEN = [
    "live_model_inference",
    "real_model_benchmark",
    "provider_execution",
    "app_apply",
    "app_state_mutation",
    "external_send",
    "public_network",
    "production_readiness",
    "security_certification",
    "release_certification",
]

_ALLOWED_REMOTE_PROVIDERS: set[str] = set()  # none by default; explicit permission required


def _sha256_id(prefix: str, payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    h = hashlib.sha256(raw.encode()).hexdigest()[:16]
    return f"{prefix}{h}"


def build_modelworkpacket(
    *,
    work_id: str,
    caller_id: str,
    input_refs: list,
    context_capsule: dict,
    artifact_lens: dict,
    transformation_verb: str,
    slot_contract: dict,
    gaptext: dict,
    model_role: dict,
    route_policy: dict,
    provider_policy: dict,
    output_contract: dict,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build a ModelWorkPacket dict.

    This is a schema packet only — no model is executed.
    """
    payload_for_id = {
        "work_id": work_id,
        "caller_id": caller_id,
        "transformation_verb": transformation_verb,
        "generated_at_utc": generated_at_utc,
    }
    packet_id = _sha256_id("modelworkpacket_", payload_for_id)

    return {
        "artifact_kind": "odin_modelworkpacket",
        "packet_id": packet_id,
        "work_id": work_id,
        "caller_id": caller_id,
        "generated_at_utc": generated_at_utc,
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "claim_boundary": CLAIM_BOUNDARY,
        # Core inputs
        "input_refs": list(input_refs),
        "context_capsule": dict(context_capsule),
        "artifact_lens": dict(artifact_lens),
        "transformation_verb": transformation_verb,
        "slot_contract": dict(slot_contract),
        "gaptext": dict(gaptext),
        # Role and routing
        "model_role": dict(model_role),
        "route_policy": dict(route_policy),
        "provider_policy": dict(provider_policy),
        # Contracts
        "output_contract": dict(output_contract),
        # Forbidden actions
        "forbidden_actions": list(_REQUIRED_FORBIDDEN_ACTIONS),
        # Boundaries and budgets
        "privacy_boundary": "local_only_no_external_send",
        "cost_budget": provider_policy.get("cost_budget", "no_model_local"),
        "latency_budget": route_policy.get("latency_budget", "interactive"),
        # Critic and gate
        "critic_plan": route_policy.get("critic_plan", "no_critic_deterministic_route"),
        "final_gate_requirements": output_contract.get(
            "final_gate_requirements",
            {"gate_type": "schema_validation", "candidate_only": True},
        ),
        # Receipt plan
        "receipt_plan": {
            "trace_required": True,
            "receipt_required": True,
            "proof_refs_required": True,
            "candidate_only": True,
        },
        # Not proven
        "not_proven": list(_NOT_PROVEN),
    }


def validate_modelworkpacket(packet: dict) -> list[str]:
    """Validate a ModelWorkPacket dict.

    Returns a list of error strings. Empty list means valid.
    """
    errors: list[str] = []

    # Required boolean flags
    if packet.get("candidate_only") is not True:
        errors.append("candidate_only must be True")
    if packet.get("local_only") is not True:
        errors.append("local_only must be True")

    # Required string fields
    if not packet.get("claim_boundary"):
        errors.append("claim_boundary is required")
    if not packet.get("output_contract"):
        errors.append("output_contract is required")
    if not packet.get("final_gate_requirements"):
        errors.append("final_gate_requirements is required")

    # Forbidden: app-side flags must not be True
    if packet.get("app_apply") is True:
        errors.append("app_apply must not be True (app-owned apply)")
    if packet.get("external_send") is True:
        errors.append("external_send must not be True")
    if packet.get("app_state_mutation") is True:
        errors.append("app_state_mutation must not be True")
    if packet.get("hidden_tool_authority") is True:
        errors.append("hidden_tool_authority must not be True")

    # Provider check: remote provider requires explicit permission
    provider_policy = packet.get("provider_policy") or {}
    provider_id = provider_policy.get("provider_id")
    if provider_id and provider_id not in _ALLOWED_REMOTE_PROVIDERS:
        if provider_policy.get("allow_remote_provider") is not True:
            errors.append(
                f"remote provider '{provider_id}' requires explicit allow_remote_provider=True in provider_policy"
            )

    # not_proven required
    if not packet.get("not_proven"):
        errors.append("not_proven list is required")

    return errors
