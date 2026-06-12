"""Deterministic seed route selector.

Claim boundary: operational_seed_spine_routes_work_not_authority
candidate_only: true

Selection priority (explicit, no randomness):
1. exact trigger_shape match
2. family / surface match
3. preferred default for known work_type
4. deterministic fallback seed

No randomness. No timestamps. No model calls. No network. No app state.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from odin.operational_seed_spine.intent_seeds import INTENT_SEEDS, IntentSeed, get_seed
from odin.operational_seed_spine.role_profiles import ROLE_PROFILES, get_role_profile

CLAIM_BOUNDARY = "operational_seed_spine_routes_work_not_authority"
FALLBACK_SEED_ID = "prompt_to_work"
FALLBACK_ROLE_PROFILE_ID = "router"

_FAMILY_TO_ROLE: dict[str, str] = {
    "context": "router",
    "route": "router",
    "compiler": "builder",
    "evidence": "reviewer",
    "boundary": "guard",
    "economy": "scope_compressor",
    "qirc": "devmode_explainer",
    "safety": "risk_scanner",
}

_WORK_TYPE_TO_SEED: dict[str, str] = {
    "repo": "repo_cognition",
    "code": "code_change",
    "review": "review_audit",
    "proof": "proof_receipt",
    "hub": "local_hub_ui",
    "provider": "provider_probe",
    "gate": "execution_gate",
    "event": "qirc_event",
    "release": "release_closure",
    "doc": "doc_architecture",
    "debug": "debug_error_triage",
    "prompt": "prompt_to_work",
}


@dataclass
class SeedRoute:
    selected_seed_id: str
    selected_role_profile_id: str
    matched_trigger_shapes: List[str]
    missing_input_requirements: List[str]
    fallback_used: bool
    selection_priority: str
    candidate_only: bool = True
    claim_boundary: str = CLAIM_BOUNDARY

    def to_dict(self) -> dict:
        return {
            "selected_seed_id": self.selected_seed_id,
            "selected_role_profile_id": self.selected_role_profile_id,
            "matched_trigger_shapes": self.matched_trigger_shapes,
            "missing_input_requirements": self.missing_input_requirements,
            "fallback_used": self.fallback_used,
            "selection_priority": self.selection_priority,
            "candidate_only": self.candidate_only,
            "claim_boundary": self.claim_boundary,
        }


def _check_missing_inputs(seed: IntentSeed, work_context: dict) -> List[str]:
    provided = set(work_context.keys())
    return [req for req in seed.input_requirements if req not in provided]


def select_seed_route(work_context: dict) -> SeedRoute:
    """Deterministically select a seed route from the work context."""
    work_type = str(work_context.get("work_type", "")).lower()
    surface = str(work_context.get("surface", "")).lower()
    family = str(work_context.get("family", "")).lower()
    trigger_hint = str(work_context.get("trigger_shape", "")).lower()

    # Priority 1: exact trigger_shape match
    if trigger_hint:
        for seed in INTENT_SEEDS:
            if trigger_hint in seed.trigger_shapes:
                role_id = _FAMILY_TO_ROLE.get(seed.family, FALLBACK_ROLE_PROFILE_ID)
                missing = _check_missing_inputs(seed, work_context)
                return SeedRoute(
                    selected_seed_id=seed.seed_id,
                    selected_role_profile_id=role_id,
                    matched_trigger_shapes=[trigger_hint],
                    missing_input_requirements=missing,
                    fallback_used=False,
                    selection_priority="exact_trigger_shape",
                )

    # Also check work_type as an exact trigger shape
    if work_type:
        for seed in INTENT_SEEDS:
            if work_type in seed.trigger_shapes:
                role_id = _FAMILY_TO_ROLE.get(seed.family, FALLBACK_ROLE_PROFILE_ID)
                missing = _check_missing_inputs(seed, work_context)
                return SeedRoute(
                    selected_seed_id=seed.seed_id,
                    selected_role_profile_id=role_id,
                    matched_trigger_shapes=[work_type],
                    missing_input_requirements=missing,
                    fallback_used=False,
                    selection_priority="exact_trigger_shape",
                )

    # Priority 2: family / surface match
    if family:
        for seed in INTENT_SEEDS:
            if seed.family == family or (surface and surface in seed.preferred_surfaces):
                role_id = _FAMILY_TO_ROLE.get(seed.family, FALLBACK_ROLE_PROFILE_ID)
                missing = _check_missing_inputs(seed, work_context)
                return SeedRoute(
                    selected_seed_id=seed.seed_id,
                    selected_role_profile_id=role_id,
                    matched_trigger_shapes=[],
                    missing_input_requirements=missing,
                    fallback_used=False,
                    selection_priority="family_surface_match",
                )

    if surface:
        for seed in INTENT_SEEDS:
            if surface in seed.preferred_surfaces:
                role_id = _FAMILY_TO_ROLE.get(seed.family, FALLBACK_ROLE_PROFILE_ID)
                missing = _check_missing_inputs(seed, work_context)
                return SeedRoute(
                    selected_seed_id=seed.seed_id,
                    selected_role_profile_id=role_id,
                    matched_trigger_shapes=[],
                    missing_input_requirements=missing,
                    fallback_used=False,
                    selection_priority="family_surface_match",
                )

    # Priority 3: preferred default for known work_type
    if work_type and work_type in _WORK_TYPE_TO_SEED:
        seed_id = _WORK_TYPE_TO_SEED[work_type]
        seed = get_seed(seed_id)
        if seed is not None:
            role_id = _FAMILY_TO_ROLE.get(seed.family, FALLBACK_ROLE_PROFILE_ID)
            missing = _check_missing_inputs(seed, work_context)
            return SeedRoute(
                selected_seed_id=seed.seed_id,
                selected_role_profile_id=role_id,
                matched_trigger_shapes=[],
                missing_input_requirements=missing,
                fallback_used=False,
                selection_priority="preferred_default_work_type",
            )

    # Priority 4: deterministic fallback
    seed = get_seed(FALLBACK_SEED_ID)
    assert seed is not None
    missing = _check_missing_inputs(seed, work_context)
    return SeedRoute(
        selected_seed_id=FALLBACK_SEED_ID,
        selected_role_profile_id=FALLBACK_ROLE_PROFILE_ID,
        matched_trigger_shapes=[],
        missing_input_requirements=missing,
        fallback_used=True,
        selection_priority="deterministic_fallback",
    )
