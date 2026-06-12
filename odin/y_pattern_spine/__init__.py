"""Y Pattern Spine — neutral operational pattern layer.

Claim boundary: y_pattern_spine_candidate_only_no_app_apply_no_provider_no_runtime_authority
candidate_only: true
app_owned_apply: true
"""
from __future__ import annotations

from odin.y_pattern_spine.patterns import (
    YPattern,
    PATTERN_FAMILIES,
    get_pattern,
    list_patterns,
    list_families,
)
from odin.y_pattern_spine.profiles import YRouteHint, build_route_hint_demo
from odin.y_pattern_spine.materialization import (
    YMaterializationLevel,
    MATERIALIZATION_LADDER,
    get_level,
)
from odin.y_pattern_spine.scoring import YSelectionScore, score_route
from odin.y_pattern_spine.explain import YProjectionSet, build_projection_set_demo
from odin.y_pattern_spine.proof import (
    YPatternReceipt,
    build_pattern_receipt,
    build_proof_packet,
)
from odin.y_pattern_spine.token_budget import YTokenBudget, TOKEN_BUDGET_MODES
from odin.y_pattern_spine.capsules import YWorkCapsule, build_work_capsule_demo

__all__ = [
    "YPattern",
    "PATTERN_FAMILIES",
    "get_pattern",
    "list_patterns",
    "list_families",
    "YRouteHint",
    "build_route_hint_demo",
    "YMaterializationLevel",
    "MATERIALIZATION_LADDER",
    "get_level",
    "YSelectionScore",
    "score_route",
    "YProjectionSet",
    "build_projection_set_demo",
    "YPatternReceipt",
    "build_pattern_receipt",
    "build_proof_packet",
    "YTokenBudget",
    "TOKEN_BUDGET_MODES",
    "YWorkCapsule",
    "build_work_capsule_demo",
]
