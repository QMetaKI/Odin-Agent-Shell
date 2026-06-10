from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(frozen=True)
class ShadowIRFragment:
    fragment_id: str
    source_ref: str
    target_module: str
    runtime_contract: str
    forbidden: tuple[str, ...] = ("app_mutation", "external_send")
    claim_boundary: str = "shadow_ir_is_blueprint_only"


def validate_shadow_ir_fragment(fragment: ShadowIRFragment) -> list[str]:
    errors: list[str] = []
    if "app_mutation" not in fragment.forbidden:
        errors.append("missing_forbidden_app_mutation")
    if "external_send" not in fragment.forbidden:
        errors.append("missing_forbidden_external_send")
    if fragment.claim_boundary != "shadow_ir_is_blueprint_only":
        errors.append("invalid_claim_boundary")
    return errors
