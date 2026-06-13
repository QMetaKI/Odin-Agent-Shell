"""Provider Seam for FINAL-PR-09 Operational Spine.

Claim boundary: final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply
candidate_only: true

Defines the seam between Odin candidate work and external model providers.
Default: no execution, no model inference, no provider calls.
"""
from __future__ import annotations

import hashlib
import json

CLAIM_BOUNDARY = "final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply"

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

# Recognized local provider IDs. None = deterministic (no provider).
_RECOGNIZED_LOCAL_PROVIDERS: set[str | None] = {
    None,
    "mock",
    "ollama_candidate",
    "llama_cpp_candidate",
}


def _sha256_id(prefix: str, payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    h = hashlib.sha256(raw.encode()).hexdigest()[:16]
    return f"{prefix}{h}"


def build_provider_seam_packet(
    provider_id: str | None,
    *,
    mode: str = "deterministic",
    allow_local_provider_execution: bool = False,
) -> dict:
    """Build a provider seam packet.

    Default: execution_allowed=False, execution_performed=False,
    model_inference=False, provider_execution=False.

    Local providers (ollama_candidate, llama_cpp_candidate, mock) return
    execution_not_available_or_not_enabled unless allow_local_provider_execution=True,
    and even then that flag is marked as future/not_implemented.
    """
    seam_id = _sha256_id(
        "provider_seam_",
        {
            "provider_id": provider_id,
            "mode": mode,
            "allow_local_provider_execution": allow_local_provider_execution,
        },
    )

    # Determine base status
    if provider_id is None or mode == "deterministic":
        status = "deterministic_no_provider"
        reason = "no_provider_selected_deterministic_route"
        execution_allowed = False
        execution_performed = False
        model_inference = False
        provider_execution = False
        requires_explicit_permission = False
    elif provider_id in _RECOGNIZED_LOCAL_PROVIDERS:
        requires_explicit_permission = True
        if allow_local_provider_execution:
            # Even with flag, execution is future/not_implemented
            status = "execution_not_available_or_not_enabled"
            reason = "local_provider_execution_flagged_but_not_implemented_future_pr_required"
            execution_allowed = False
            execution_performed = False
            model_inference = False
            provider_execution = False
        else:
            status = "execution_not_available_or_not_enabled"
            reason = "local_provider_execution_requires_explicit_permission_not_granted"
            execution_allowed = False
            execution_performed = False
            model_inference = False
            provider_execution = False
    else:
        # Unrecognized provider — not allowed
        status = "unrecognized_provider_not_allowed"
        reason = f"provider_id '{provider_id}' is not in recognized local provider list"
        execution_allowed = False
        execution_performed = False
        model_inference = False
        provider_execution = False
        requires_explicit_permission = True

    return {
        "artifact_kind": "odin_provider_seam_packet",
        "provider_seam_id": seam_id,
        "provider_id": provider_id,
        "mode": mode,
        "execution_allowed": execution_allowed,
        "execution_performed": execution_performed,
        "requires_explicit_permission": requires_explicit_permission,
        "candidate_only": True,
        "local_only": True,
        "app_apply": False,
        "external_send": False,
        "model_inference": model_inference,
        "provider_execution": provider_execution,
        "status": status,
        "reason": reason,
        "not_proven": list(_NOT_PROVEN),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def validate_provider_seam_packet(packet: dict) -> list[str]:
    """Validate a provider seam packet.

    Returns a list of error strings. Empty list means valid.
    """
    errors: list[str] = []

    if packet.get("candidate_only") is not True:
        errors.append("candidate_only must be True")
    if packet.get("local_only") is not True:
        errors.append("local_only must be True")
    if packet.get("app_apply") is not False:
        errors.append("app_apply must be False")
    if packet.get("external_send") is not False:
        errors.append("external_send must be False")
    if not packet.get("claim_boundary"):
        errors.append("claim_boundary is required")
    if not packet.get("provider_seam_id"):
        errors.append("provider_seam_id is required")
    if not packet.get("status"):
        errors.append("status is required")
    if not packet.get("not_proven"):
        errors.append("not_proven list is required")

    # Execution sanity: if execution_performed=True then execution_allowed must also be True
    if packet.get("execution_performed") is True and packet.get("execution_allowed") is not True:
        errors.append("execution_performed=True requires execution_allowed=True")

    return errors
