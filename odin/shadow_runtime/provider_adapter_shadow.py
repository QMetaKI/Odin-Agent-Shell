from __future__ import annotations

from typing import Any, Dict


def build_shadow_provider_adapter_plan(route: str, provider: str = "mock") -> Dict[str, Any]:
    provider = provider or "mock"
    local_only = provider in {"mock", "ollama", "llama_cpp"}
    return {
        "artifact_kind": "odin_shadow_provider_adapter_plan",
        "protocol_version": "7.1-shadow",
        "provider": provider,
        "route": route,
        "adapter_surface": ["list_models", "profile_model", "run_model_work_packet", "cancel", "health"],
        "local_only": local_only,
        "remote_requires_explicit_permission": provider not in {"mock", "ollama", "llama_cpp"},
        "model_io": "ModelWorkPacket in, ModelResponse projection out",
        "side_effects": "none_in_shadow",
        "boundary": "provider_adapter_plan_only_no_live_model_claim",
    }
