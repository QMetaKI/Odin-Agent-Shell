from __future__ import annotations
from .pack_manifest import build_pack_manifest

def compile_cached_capability_shadow(caller_id: str, resource_profile: str, capabilities: list[str]) -> dict:
    safe_caps = [cap for cap in capabilities if cap not in {"direct_apply", "external_send"}]
    manifest = build_pack_manifest(f"capability_slice_{caller_id}_{resource_profile}", resource_profile, safe_caps)
    return {"status": "cached_capability_compiled_shadow", "caller_id": caller_id, "manifest": manifest}
