from __future__ import annotations

def build_pack_manifest(pack_id: str, resource_profile: str, capabilities: list[str]) -> dict:
    return {
        "artifact_kind": "odin_runtime_pack",
        "protocol_version": "7.1",
        "pack_id": pack_id,
        "resource_profile": resource_profile,
        "capabilities": capabilities,
        "forbidden_capabilities": ["direct_apply", "external_send", "unverified_runtime_claim"],
        "load_policy": {"requires_validation": True, "rollback_on_failure": True},
        "claim_boundary": "runtime_pack_manifest_only",
    }
