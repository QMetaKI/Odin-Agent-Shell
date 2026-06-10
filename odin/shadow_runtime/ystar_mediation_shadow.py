"""Y* mediation directive shadow module."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class YStarMediationDirectiveShadow:
    directive_id: str
    ystar_unit_ref: str
    target_shadow_modules: tuple[str, ...]
    runtime_boundaries: dict
    compile_hints: dict
    holes: tuple[str, ...]
    risk: dict
    claim_boundary: str = "ystar_mediation_is_not_authority"


def validate_ystar_mediation_shadow(directive: YStarMediationDirectiveShadow) -> list[str]:
    errors: list[str] = []
    required = {
        "candidate_only": True,
        "no_app_mutation": True,
        "no_external_send": True,
        "final_gate_required": True,
    }
    for key, expected in required.items():
        if directive.runtime_boundaries.get(key) is not expected:
            errors.append(f"boundary_not_preserved:{key}")
    if not directive.target_shadow_modules:
        errors.append("missing_target_shadow_modules")
    if directive.claim_boundary != "ystar_mediation_is_not_authority":
        errors.append("invalid_claim_boundary")
    return errors
