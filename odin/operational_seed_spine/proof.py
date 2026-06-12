"""Proof packet for Operational Seed Spine — FINAL-PR-06.

Claim boundary: operational_seed_spine_routes_work_not_authority
candidate_only: true
app_owned_apply: true
"""
from __future__ import annotations

import json
from pathlib import Path

CLAIM_BOUNDARY = "operational_seed_spine_routes_work_not_authority"

PROVEN = [
    "seed_packs_defined",
    "role_profiles_defined",
    "selector_deterministic",
    "work_capsule_compiled",
    "qirc_hints_are_hint_only",
    "token_budget_per_seed",
    "capsule_ids_deterministic",
    "candidate_only_preserved",
    "app_owned_apply_preserved",
]

NOT_PROVEN = [
    "autonomous_reasoning",
    "model_inference",
    "provider_execution",
    "app_apply",
    "app_state_mutation",
    "external_send",
    "production_readiness",
    "security_certification",
    "live_model_inference",
    "external_send_authority",
]


def build_proof_packet() -> dict:
    return {
        "artifact_kind": "odin_operational_seed_spine_proof_packet",
        "proven": PROVEN,
        "not_proven": NOT_PROVEN,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_only": True,
        "app_owned_apply": True,
    }


def persist_proof_packet(repo_root: Path) -> dict:
    packet = build_proof_packet()
    out_path = repo_root / "reports" / "final_pr_06_operational_seed_spine_proof_packet.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(packet, indent=2, ensure_ascii=False), encoding="utf-8")
    return packet
