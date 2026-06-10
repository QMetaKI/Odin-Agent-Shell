from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class RuntimePackShadow:
    pack_id: str
    source_shadow_hash: str
    source_ystar_hash: str
    resource_profile: str
    capabilities: tuple[str, ...]
    forbidden_capabilities: tuple[str, ...]
    tests_required: tuple[str, ...]
    rollback_on_failure: bool = True
    claim_boundary: str = "runtime_pack_requires_validation_before_load"


def validate_runtime_pack_shadow(pack: RuntimePackShadow) -> list[str]:
    errors: list[str] = []
    for forbidden in ["direct_apply", "external_send", "unverified_runtime_claim"]:
        if forbidden not in pack.forbidden_capabilities:
            errors.append(f"missing_forbidden_capability:{forbidden}")
    if not pack.rollback_on_failure:
        errors.append("rollback_required")
    if pack.claim_boundary != "runtime_pack_requires_validation_before_load":
        errors.append("invalid_claim_boundary")
    return errors
