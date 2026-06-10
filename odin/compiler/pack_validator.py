from __future__ import annotations

def validate_pack_manifest(manifest: dict) -> list[str]:
    errors: list[str] = []
    if manifest.get("artifact_kind") != "odin_runtime_pack":
        errors.append("wrong_artifact_kind")
    load_policy = manifest.get("load_policy", {})
    if load_policy.get("requires_validation") is not True:
        errors.append("requires_validation_missing")
    if load_policy.get("rollback_on_failure") is not True:
        errors.append("rollback_missing")
    forbidden = set(manifest.get("forbidden_capabilities", []))
    for cap in ["direct_apply", "external_send", "unverified_runtime_claim"]:
        if cap not in forbidden:
            errors.append(f"missing_forbidden_capability:{cap}")
    return errors
