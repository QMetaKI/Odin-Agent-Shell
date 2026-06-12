"""Seed Work Capsule compiler — deterministic routing context packager.

Claim boundary: operational_seed_spine_routes_work_not_authority
candidate_only: true
app_owned_apply: true

The capsule compiler packages deterministic routing context.
It never executes the work. Capsule IDs are deterministic (SHA256).
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import List, Any

from odin.operational_seed_spine.intent_seeds import get_seed
from odin.operational_seed_spine.role_profiles import get_role_profile
from odin.operational_seed_spine.selector import SeedRoute
from odin.operational_seed_spine.qirc_hints import build_qirc_hints
from odin.operational_seed_spine.token_budget import get_token_budget

CLAIM_BOUNDARY = "operational_seed_spine_routes_work_not_authority"

NOT_PROVEN = [
    "autonomous_reasoning",
    "model_inference",
    "provider_execution",
    "app_apply",
    "app_state_mutation",
    "external_send",
    "production_readiness",
    "security_certification",
]


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _deterministic_capsule_id(route: SeedRoute) -> str:
    payload = {
        "seed_id": route.selected_seed_id,
        "role_profile_id": route.selected_role_profile_id,
        "fallback_used": route.fallback_used,
        "selection_priority": route.selection_priority,
        "matched_trigger_shapes": sorted(route.matched_trigger_shapes),
    }
    digest = hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()[:16]
    return f"seed_capsule_{digest}"


@dataclass
class SeedWorkCapsule:
    capsule_id: str
    seed_id: str
    seed_family: str
    role_profile_id: str
    input_requirements: List[str]
    output_shape: str
    preferred_surfaces: List[str]
    qirc_hints: List[dict]
    token_budget: dict
    validator_expectations: List[str]
    proof_boundary: str
    candidate_only: bool = True
    app_owned_apply: bool = True
    claim_boundary: str = CLAIM_BOUNDARY
    not_proven: List[str] = field(default_factory=lambda: NOT_PROVEN[:])

    def to_dict(self) -> dict:
        return {
            "capsule_id": self.capsule_id,
            "seed_id": self.seed_id,
            "seed_family": self.seed_family,
            "role_profile_id": self.role_profile_id,
            "input_requirements": self.input_requirements,
            "output_shape": self.output_shape,
            "preferred_surfaces": self.preferred_surfaces,
            "qirc_hints": self.qirc_hints,
            "token_budget": self.token_budget,
            "validator_expectations": self.validator_expectations,
            "proof_boundary": self.proof_boundary,
            "candidate_only": self.candidate_only,
            "app_owned_apply": self.app_owned_apply,
            "claim_boundary": self.claim_boundary,
            "not_proven": self.not_proven,
        }


def compile_work_capsule(route: SeedRoute) -> SeedWorkCapsule:
    """Compile a deterministic SeedWorkCapsule from a SeedRoute."""
    seed = get_seed(route.selected_seed_id)
    if seed is None:
        raise ValueError(f"Unknown seed_id: {route.selected_seed_id!r}")

    capsule_id = _deterministic_capsule_id(route)
    qirc_hints = build_qirc_hints(seed.qirc_event_hints)
    token_budget = get_token_budget(seed.token_budget_key)

    return SeedWorkCapsule(
        capsule_id=capsule_id,
        seed_id=seed.seed_id,
        seed_family=seed.family,
        role_profile_id=route.selected_role_profile_id,
        input_requirements=seed.input_requirements,
        output_shape=seed.output_shape,
        preferred_surfaces=seed.preferred_surfaces,
        qirc_hints=qirc_hints,
        token_budget=token_budget,
        validator_expectations=seed.validator_expectations,
        proof_boundary=seed.proof_boundary,
        candidate_only=True,
        app_owned_apply=True,
        claim_boundary=CLAIM_BOUNDARY,
        not_proven=NOT_PROVEN[:],
    )
