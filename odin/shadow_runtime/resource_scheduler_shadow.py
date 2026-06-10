from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List

@dataclass
class ShadowResourcePosture:
    profile: str
    latency_mode: str
    route_ceiling: str
    reasons: List[str]
    disabled_features: List[str]
    boundary: str = "resource_posture_shadow_no_hardware_claim"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def plan_shadow_resource_posture(resource_profile: str = "standard_local", latency_mode: str = "interactive") -> ShadowResourcePosture:
    disabled: List[str] = []
    reasons: List[str] = [f"resource_profile={resource_profile}", f"latency_mode={latency_mode}"]
    if resource_profile == "low_memory_strict":
        ceiling = "3b_micro"
        disabled = ["heavy_tournament", "normal_7b_route", "large_context", "remote_default", "developer_labs_heavy"]
    elif resource_profile == "standard_local":
        ceiling = "3b_7b_8b_hybrid"
        disabled = ["70b_batch", "remote_default"]
    elif resource_profile == "quality_local":
        ceiling = "3b_13b_14b_quality_hybrid"
        disabled = ["70b_batch", "remote_default"]
    elif resource_profile == "heavy_local":
        ceiling = "3b_22b_32b_heavy_local" if latency_mode in {"batch", "overnight"} else "3b_7b_8b_hybrid"
        disabled = ["remote_default"]
    elif resource_profile == "max_local_batch":
        ceiling = "70b_class_local_offload_batch"
        disabled = ["interactive_heavy_route", "remote_default"]
    else:
        ceiling = "3b_7b_8b_hybrid"
        reasons.append("unknown_profile_defaulted")
    return ShadowResourcePosture(resource_profile, latency_mode, ceiling, reasons, disabled)
