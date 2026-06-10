"""Shadow module for App Seed Pack Compiler v7.1.

Non-executing, candidate-only, no plugin execution, no app mutation.
"""
from __future__ import annotations


def validate_seed_pack_manifest_shadow(packet: dict) -> dict:
    """Return a deterministic shadow candidate for Codex conversion."""
    forbidden = set(packet.get("forbidden_actions", []))
    if "execute_code" in forbidden or packet.get("attempts_app_mutation"):
        return {"status": "blocked", "reason": "seed_pack_security_boundary", "candidate_only": True}
    return {
        "status": "candidate",
        "stage": "app_seed_pack_compiler",
        "input_kind": packet.get("artifact_kind", "unknown"),
        "candidate_only": True,
        "no_app_mutation": True,
        "no_external_send": True,
        "next": "validate_manifest_then_compile_seed_profile",
    }
