from __future__ import annotations

from typing import List

from .types import ShadowModelRoutePlan


def choose_shadow_route(resource_profile: str = "standard_local", latency_mode: str = "interactive", quality_target: str = "standard", remote_allowed: bool = False) -> ShadowModelRoutePlan:
    reason: List[str] = []
    fallbacks = ["3b_multi_slot", "ask_context", "cannot_safely_complete"]

    if resource_profile == "low_memory_strict":
        route = "3b_micro_critic_router"
        reason.append("low_memory_strict")
    elif resource_profile == "quality_local" and quality_target in {"high", "premium"} and latency_mode != "interactive":
        route = "3b_13b_14b_quality_hybrid"
        reason.extend(["quality_target", "draft_or_batch_latency"])
    elif resource_profile == "heavy_local" and latency_mode in {"batch", "overnight"}:
        route = "3b_22b_32b_heavy_local"
        reason.extend(["heavy_local", "batch_latency"])
    elif resource_profile == "max_local_batch" and latency_mode == "overnight":
        route = "70b_class_batch"
        reason.extend(["max_local_batch", "overnight_latency"])
    elif resource_profile == "remote_optional" and remote_allowed:
        route = "remote_optional_explicit"
        reason.extend(["remote_explicitly_allowed"])
    else:
        route = "3b_7b_8b_hybrid"
        reason.extend(["default_sweet_spot", "small_model_first"])

    return ShadowModelRoutePlan(
        route_class=resource_profile,
        selected_route=route,
        latency_mode=latency_mode,
        reason=reason,
        fallbacks=fallbacks,
    )
