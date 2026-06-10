from __future__ import annotations

REQUIRED_CALLER_FIELDS = {"caller_id", "app_name", "protocol_version", "permissions", "apply_boundary"}
FORBIDDEN_PERMISSIONS = {"direct_apply", "external_send", "grant_odin_authority", "bypass_final_gate"}


def validate_caller_manifest(manifest: dict) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_CALLER_FIELDS - set(manifest)
    if missing:
        errors.append(f"caller_manifest missing fields: {sorted(missing)}")
    if manifest.get("protocol_version") not in {"7.1", "0.8.0"}:
        errors.append("caller_manifest protocol_version must be 7.1 or 0.8.0")
    permissions = set(manifest.get("permissions", []))
    forbidden = sorted(permissions & FORBIDDEN_PERMISSIONS)
    if forbidden:
        errors.append("caller_manifest forbidden permissions: " + ", ".join(forbidden))
    boundary = manifest.get("apply_boundary", {})
    if boundary.get("app_owned") is not True:
        errors.append("apply_boundary.app_owned must be true")
    if boundary.get("odin_may_apply") is True:
        errors.append("apply_boundary.odin_may_apply must not be true")
    return errors


def build_default_manifest(caller_id: str = "demo.app") -> dict:
    return {
        "caller_id": caller_id,
        "app_name": "Demo App",
        "protocol_version": "7.1",
        "permissions": ["submit_work", "receive_candidate", "provide_seed_pack", "provide_flow_pack"],
        "apply_boundary": {"app_owned": True, "odin_may_apply": False, "external_send_by_app_only": True},
        "qirc_digest_mode": "digest_only",
    }
