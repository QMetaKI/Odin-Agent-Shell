from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CapabilitySliceShadow:
    slice_id: str
    caller_id: str
    resource_profile: str
    allowed_capabilities: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    runtime_pack_ref: str
    claim_boundary: str = "capability_slice_may_only_narrow"


def validate_capability_slice_shadow(slice_: CapabilitySliceShadow) -> list[str]:
    errors: list[str] = []
    for cap in ["direct_apply", "external_send"]:
        if cap in slice_.allowed_capabilities:
            errors.append(f"forbidden_allowed_capability:{cap}")
    if not slice_.runtime_pack_ref:
        errors.append("missing_runtime_pack_ref")
    return errors
