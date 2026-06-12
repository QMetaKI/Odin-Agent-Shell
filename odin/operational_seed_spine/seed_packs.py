"""Seed Packs — deterministic groupings of intent seeds.

Claim boundary: operational_seed_spine_routes_work_not_authority
candidate_only: true

Seed packs do not imply autonomy. They are routing groupings only.
Every seed ID referenced by a pack must exist in INTENT_SEEDS.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from odin.operational_seed_spine.intent_seeds import INTENT_SEEDS, REQUIRED_SEED_IDS

CLAIM_BOUNDARY = "operational_seed_spine_routes_work_not_authority"

_KNOWN_SEED_IDS = frozenset(s.seed_id for s in INTENT_SEEDS)


@dataclass
class SeedPack:
    pack_id: str
    family: str
    seed_ids: List[str]
    allowed_use: List[str]
    forbidden_use: List[str]
    claim_boundary: str = CLAIM_BOUNDARY

    def __post_init__(self) -> None:
        missing = [sid for sid in self.seed_ids if sid not in _KNOWN_SEED_IDS]
        if missing:
            raise ValueError(f"SeedPack {self.pack_id!r} references unknown seed IDs: {missing}")

    def to_dict(self) -> dict:
        return {
            "pack_id": self.pack_id,
            "family": self.family,
            "seed_ids": self.seed_ids,
            "allowed_use": self.allowed_use,
            "forbidden_use": self.forbidden_use,
            "claim_boundary": self.claim_boundary,
            "candidate_only": True,
        }


SEED_PACKS: List[SeedPack] = [
    SeedPack(
        pack_id="core_cognition",
        family="context",
        seed_ids=["repo_cognition", "doc_architecture", "prompt_to_work"],
        allowed_use=["repo_exploration", "doc_preparation", "work_routing"],
        forbidden_use=["app_apply", "external_send", "model_inference"],
        claim_boundary=CLAIM_BOUNDARY,
    ),
    SeedPack(
        pack_id="implementation",
        family="compiler",
        seed_ids=["code_change", "prompt_to_work", "execution_gate"],
        allowed_use=["code_candidate_preparation", "work_routing", "gate_check"],
        forbidden_use=["app_apply", "external_send", "autonomous_execution"],
        claim_boundary=CLAIM_BOUNDARY,
    ),
    SeedPack(
        pack_id="evidence_audit",
        family="evidence",
        seed_ids=["review_audit", "proof_receipt", "debug_error_triage"],
        allowed_use=["audit_preparation", "proof_binding", "triage"],
        forbidden_use=["app_apply", "external_send", "production_certification"],
        claim_boundary=CLAIM_BOUNDARY,
    ),
    SeedPack(
        pack_id="runtime_surface",
        family="route",
        seed_ids=["local_hub_ui", "provider_probe", "qirc_event"],
        allowed_use=["hub_surface", "provider_readiness_check", "qirc_hint_mapping"],
        forbidden_use=["app_apply", "external_send", "provider_execution"],
        claim_boundary=CLAIM_BOUNDARY,
    ),
    SeedPack(
        pack_id="boundary_closure",
        family="boundary",
        seed_ids=["execution_gate", "release_closure", "proof_receipt"],
        allowed_use=["gate_check", "release_scoping", "proof_binding"],
        forbidden_use=["app_apply", "external_send", "autonomous_deploy"],
        claim_boundary=CLAIM_BOUNDARY,
    ),
    SeedPack(
        pack_id="full_spine",
        family="route",
        seed_ids=REQUIRED_SEED_IDS,
        allowed_use=["complete_routing", "all_seed_access"],
        forbidden_use=["app_apply", "external_send", "model_inference", "production_readiness"],
        claim_boundary=CLAIM_BOUNDARY,
    ),
]

REQUIRED_SEED_PACK_IDS = [
    "core_cognition",
    "implementation",
    "evidence_audit",
    "runtime_surface",
    "boundary_closure",
    "full_spine",
]

_PACK_INDEX: dict[str, SeedPack] = {p.pack_id: p for p in SEED_PACKS}


def get_seed_pack(pack_id: str) -> SeedPack | None:
    return _PACK_INDEX.get(pack_id)


def validate_seed_packs() -> list[str]:
    errors = []
    for pack in SEED_PACKS:
        for sid in pack.seed_ids:
            if sid not in _KNOWN_SEED_IDS:
                errors.append(f"SeedPack {pack.pack_id!r} references unknown seed_id {sid!r}")
    for required in REQUIRED_SEED_PACK_IDS:
        if required not in _PACK_INDEX:
            errors.append(f"Missing required seed pack: {required!r}")
    return errors
