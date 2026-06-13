"""Deterministic critic — FINAL-PR-11.

Checks candidate boundaries deterministically. No model needed.
Critic is advisory, not final authority, cannot apply.
"""
from __future__ import annotations

from odin.critic_runtime.critic_packet import CLAIM_BOUNDARY, _NOT_PROVEN, build_critic_packet

_FORBIDDEN_ACTION_FLAGS = [
    "app_apply",
    "external_send",
    "public_network",
    "app_state_mutation",
    "hidden_tool_execution",
]

_REQUIRED_BOUNDARY_FIELDS = [
    "candidate_only",
    "claim_boundary",
    "not_proven",
]


def run_deterministic_critic(
    candidate: dict,
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Run deterministic critic checks on a candidate.

    Returns a critic result dict. Critic is advisory. Not final authority.
    No model, no network, no apply.
    """
    packet = build_critic_packet(candidate, critic_mode="deterministic", generated_at_utc=generated_at_utc)
    checks: dict[str, bool] = {}
    warnings: list[str] = []
    errors: list[str] = []

    # Boundary field checks
    for field in _REQUIRED_BOUNDARY_FIELDS:
        present = field in candidate
        checks[f"{field}_present"] = present
        if not present:
            errors.append(f"missing required boundary field: {field}")

    # candidate_only must be True
    if candidate.get("candidate_only") is not True:
        checks["candidate_only_true"] = False
        errors.append("candidate_only must be True")
    else:
        checks["candidate_only_true"] = True

    # claim_boundary must be non-empty string
    cb = candidate.get("claim_boundary")
    checks["claim_boundary_nonempty"] = bool(cb and isinstance(cb, str))
    if not checks["claim_boundary_nonempty"]:
        errors.append("claim_boundary must be a non-empty string")

    # not_proven must be a list
    np = candidate.get("not_proven")
    checks["not_proven_is_list"] = isinstance(np, list)
    if not isinstance(np, list):
        errors.append("not_proven must be a list")

    # Forbidden action flags must be absent or False
    for flag in _FORBIDDEN_ACTION_FLAGS:
        val = candidate.get(flag)
        flag_clean = val is not True
        checks[f"{flag}_clean"] = flag_clean
        if not flag_clean:
            errors.append(f"forbidden action flag is True: {flag}")

    # app_apply must be False
    if candidate.get("app_apply") is True:
        errors.append("app_apply must be False")
        checks["app_apply_false"] = False
    else:
        checks["app_apply_false"] = True

    # external_send must be False
    if candidate.get("external_send") is True:
        errors.append("external_send must be False")
        checks["external_send_false"] = False
    else:
        checks["external_send_false"] = True

    # model_projection_not_truth: warn if candidate claims truth
    if candidate.get("model_projection_is_truth") is True:
        warnings.append("model_projection_is_truth=True violates model_projection_not_truth invariant")
        checks["model_projection_not_truth"] = False
    else:
        checks["model_projection_not_truth"] = True

    # Slot/output contract presence (advisory only)
    has_slot = "slot_contract" in candidate or "slot_completeness" in candidate
    has_output = "output_contract" in candidate
    if not has_slot:
        warnings.append("slot_contract not present (advisory: recommended for structured candidates)")
    if not has_output:
        warnings.append("output_contract not present (advisory only)")

    score = max(0, 100 - len(errors) * 20 - len(warnings) * 5)
    recommendation = "pass" if not errors else "fail"

    return {
        **packet,
        "checks": checks,
        "warnings": warnings,
        "errors": errors,
        "score": score,
        "recommendation": recommendation,
        "not_authority": True,
        "final_gate_required": True,
        "critic_advisory_note": (
            "This critic result is advisory. "
            "It is not a final gate. "
            "App owns apply authority."
        ),
    }
