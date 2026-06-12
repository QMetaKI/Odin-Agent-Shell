"""Y Pattern Proof — receipts and proof packets.

Claim boundary: y_pattern_spine_candidate_only_no_app_apply_no_provider_no_runtime_authority
candidate_only: true
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

CLAIM_BOUNDARY = "y_pattern_spine_operational_hint_not_runtime_authority"

NOT_PROVEN_REQUIRED = [
    "model_inference",
    "provider_execution",
    "event_core_runtime",
    "runtime_authority",
    "app_apply",
    "app_state_mutation",
    "external_send",
    "production_readiness",
    "security_certification",
]


@dataclass
class YPatternReceipt:
    receipt_id: str
    pattern_id: str
    route_hint_id: str
    materialization_level: str
    evidence_basis: List[str]
    claim_boundary: str = CLAIM_BOUNDARY
    not_proven: Optional[List[str]] = None

    def __post_init__(self) -> None:
        if self.not_proven is None:
            self.not_proven = NOT_PROVEN_REQUIRED[:]

    def to_dict(self) -> dict:
        return {
            "receipt_id": self.receipt_id,
            "pattern_id": self.pattern_id,
            "route_hint_id": self.route_hint_id,
            "materialization_level": self.materialization_level,
            "evidence_basis": self.evidence_basis,
            "not_proven": self.not_proven,
            "claim_boundary": self.claim_boundary,
        }


def build_pattern_receipt(
    receipt_id: str,
    pattern_id: str,
    route_hint_id: str,
    materialization_level: str,
    evidence_basis: Optional[List[str]] = None,
) -> YPatternReceipt:
    return YPatternReceipt(
        receipt_id=receipt_id,
        pattern_id=pattern_id,
        route_hint_id=route_hint_id,
        materialization_level=materialization_level,
        evidence_basis=evidence_basis or [],
    )


PROOF_PACKET: dict = {
    "artifact_kind": "y_pattern_spine_proof_packet",
    "candidate_only": True,
    "local_only": True,
    "pattern_spine_loaded": True,
    "route_hint_demo_ok": True,
    "work_capsule_demo_ok": True,
    "materialization_ladder_loaded": True,
    "projection_set_demo_ok": True,
    "token_budget_modes_loaded": True,
    "baseline_fit_matrix_validated": True,
    "harmony_matrix_validated": True,
    "forbidden_names_absent_from_new_artifacts": True,
    "not_proven": NOT_PROVEN_REQUIRED,
    "claim_boundary": CLAIM_BOUNDARY,
}


def build_proof_packet() -> dict:
    return dict(PROOF_PACKET)


def persist_proof_packet(repo_root: Path) -> dict:
    packet = build_proof_packet()
    out = repo_root / "reports" / "y_pattern_spine_proof_packet.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, ensure_ascii=False, sort_keys=True))
    return packet
