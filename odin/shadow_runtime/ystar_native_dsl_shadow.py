"""Y* Native DSL shadow validation.

Y* is typed narrative IR. It stages and enriches but does not own authority.
"""
from __future__ import annotations
from dataclasses import dataclass

REQUIRED_CENTER = {"candidate_only", "app_authority", "final_gate"}

@dataclass(frozen=True)
class YStarNativeUnitShadow:
    unit_id: str
    story_ref: str
    center: dict
    rings: tuple[str, ...]
    flow: tuple[str, ...]
    forbidden: tuple[str, ...]
    emits: tuple[str, ...]
    holes: tuple[str, ...] = ()
    claim_boundary: str = "ystar_staging_only"


def validate_ystar_unit_shadow(unit: YStarNativeUnitShadow) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_CENTER - set(unit.center)
    for key in sorted(missing):
        errors.append(f"missing_center:{key}")
    if unit.center.get("candidate_only") is not True:
        errors.append("candidate_only_not_true")
    if unit.center.get("app_authority") != "preserve":
        errors.append("app_authority_not_preserved")
    if unit.center.get("final_gate") != "odin":
        errors.append("final_gate_not_odin")
    if "app_mutation" not in unit.forbidden:
        errors.append("missing_forbidden_app_mutation")
    if "external_send" not in unit.forbidden:
        errors.append("missing_forbidden_external_send")
    if unit.claim_boundary != "ystar_staging_only":
        errors.append("invalid_claim_boundary")
    return errors
