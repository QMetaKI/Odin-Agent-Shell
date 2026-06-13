"""SmallModelRoutePlan builder for FINAL-PR-09 Operational Spine.

Claim boundary: final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply
candidate_only: true

Builds route plan dicts. No model execution — plan only.
"""
from __future__ import annotations

import hashlib
import json

CLAIM_BOUNDARY = "final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply"

_NOT_PROVEN = [
    "live_model_inference",
    "real_model_benchmark",
    "provider_execution",
    "app_apply",
    "app_state_mutation",
    "external_send",
    "production_readiness",
]

_RESOURCE_PROFILES = {
    "deterministic": {
        "selected_route": "deterministic_no_model",
        "requires_model": False,
        "latency_mode": "instant",
        "quality_target": "schema_valid",
        "selected_roles": ["deterministic_candidate_shape", "trace_receipt_construction"],
        "critic_plan": "no_critic_deterministic_route",
    },
    "small": {
        "selected_route": "3b_primary",
        "requires_model": True,
        "latency_mode": "interactive",
        "quality_target": "standard",
        "selected_roles": ["3b_router", "3b_slot_filler", "3b_quick_critic"],
        "critic_plan": "3b_quick_critic_post_slot_fill",
    },
    "medium": {
        "selected_route": "7b_primary",
        "requires_model": True,
        "latency_mode": "standard",
        "quality_target": "high",
        "selected_roles": ["7b_planner", "7b_candidate_composer", "7b_complex_critic"],
        "critic_plan": "7b_complex_critic_post_compose",
    },
    "hybrid": {
        "selected_route": "3b_7b_hybrid",
        "requires_model": True,
        "latency_mode": "balanced",
        "quality_target": "high",
        "selected_roles": [
            "3b_scout",
            "7b_synthesizer",
            "3b_quick_critic",
        ],
        "critic_plan": "hybrid_3b_scout_7b_synthesize_3b_check",
    },
}

_FALLBACK_PROFILES = {
    "deterministic": [],
    "small": ["deterministic"],
    "medium": ["small", "deterministic"],
    "hybrid": ["small", "deterministic"],
}


def _sha256_id(prefix: str, payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    h = hashlib.sha256(raw.encode()).hexdigest()[:16]
    return f"{prefix}{h}"


def build_small_model_route_plan(
    work_id: str,
    resource_profile: str = "small",
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build a SmallModelRoutePlan dict.

    This is a plan only — no model is executed, no provider is called.
    """
    profile_key = resource_profile if resource_profile in _RESOURCE_PROFILES else "small"
    profile = _RESOURCE_PROFILES[profile_key]
    fallback_profiles = _FALLBACK_PROFILES.get(profile_key, ["deterministic"])

    route_id = _sha256_id(
        "small_model_route_",
        {
            "work_id": work_id,
            "resource_profile": profile_key,
            "generated_at_utc": generated_at_utc,
        },
    )

    fallbacks = [
        {
            "profile": fb,
            "selected_route": _RESOURCE_PROFILES[fb]["selected_route"],
            "requires_model": _RESOURCE_PROFILES[fb]["requires_model"],
        }
        for fb in fallback_profiles
    ]

    return {
        "artifact_kind": "odin_small_model_route_plan",
        "route_id": route_id,
        "work_id": work_id,
        "resource_profile": profile_key,
        "latency_mode": profile["latency_mode"],
        "quality_target": profile["quality_target"],
        "requires_model": profile["requires_model"],
        "selected_route": profile["selected_route"],
        "selected_roles": list(profile["selected_roles"]),
        "critic_plan": profile["critic_plan"],
        "fallbacks": fallbacks,
        "generated_at_utc": generated_at_utc,
        "not_proven": list(_NOT_PROVEN),
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "claim_boundary": CLAIM_BOUNDARY,
    }
