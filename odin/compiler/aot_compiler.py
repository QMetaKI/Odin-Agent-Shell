from __future__ import annotations
from .pack_manifest import build_pack_manifest
from .pack_validator import validate_pack_manifest

def compile_aot_shadow(pack_id: str, resource_profile: str, capabilities: list[str]) -> dict:
    manifest = build_pack_manifest(pack_id, resource_profile, capabilities)
    errors = validate_pack_manifest(manifest)
    return {"status": "compiled_shadow" if not errors else "blocked", "manifest": manifest, "errors": errors}
