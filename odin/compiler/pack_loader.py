from __future__ import annotations
from .pack_validator import validate_pack_manifest

def load_pack_shadow(manifest: dict) -> dict:
    errors = validate_pack_manifest(manifest)
    if errors:
        return {"status": "blocked", "errors": errors, "loaded": False}
    return {"status": "loaded_shadow", "loaded": True, "pack_id": manifest.get("pack_id")}
