from __future__ import annotations

def build_compile_plan(mode: str, resource_profile: str) -> dict:
    if mode not in {"aot", "cached_capability", "debug_interpreted_fallback"}:
        return {"status": "blocked", "reason": "unknown_compile_mode"}
    if mode == "debug_interpreted_fallback":
        return {"status": "limited", "heavy_routes": False, "resource_profile": resource_profile}
    return {"status": "planned", "mode": mode, "resource_profile": resource_profile, "hot_path": False}
