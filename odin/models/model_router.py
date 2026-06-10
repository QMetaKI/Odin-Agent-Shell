from __future__ import annotations
DEFAULT_ROUTE = "3b_7b_8b_hybrid"

LADDER = [
    "deterministic_no_model",
    "1b_2b_micro",
    "3b_micro_critic_router",
    "3b_multi_slot",
    "7b_8b_quality",
    "3b_7b_8b_hybrid",
    "3b_13b_14b_quality_hybrid",
    "3b_22b_32b_heavy_local",
    "moe_heavy_local_offload",
    "70b_class_local_offload_batch",
    "remote_optional_explicit",
    "cannot_safely_complete",
]


def choose_route(resource_profile: str, latency_mode: str = "interactive", quality_target: str = "standard", requires_model: bool = True) -> str:
    if not requires_model:
        return "deterministic_no_model"
    if resource_profile == "low_memory_strict":
        return "3b_micro_critic_router"
    if latency_mode == "interactive":
        return DEFAULT_ROUTE
    if resource_profile == "quality_local" and quality_target in {"high", "premium"}:
        return "3b_13b_14b_quality_hybrid"
    if resource_profile == "heavy_local" and latency_mode in {"batch", "overnight"}:
        return "3b_22b_32b_heavy_local"
    if resource_profile == "remote_optional" and quality_target == "remote_explicit":
        return "remote_optional_explicit"
    return DEFAULT_ROUTE
