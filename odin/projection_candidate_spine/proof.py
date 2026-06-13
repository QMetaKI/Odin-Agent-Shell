"""Proof packet for FINAL-PR-08 Projection Candidate Spine."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

CLAIM_BOUNDARY = "projection_candidate_spine_prepares_candidates_not_runtime_execution"

REQUIRED_PROVEN = [
    "materialization_levels_defined",
    "projection_set_candidate_only",
    "candidate_graph_structured",
    "expression_packet_near_code_not_executed",
    "receipt_link_traceable",
]

REQUIRED_NOT_PROVEN = [
    "hidden_runtime",
    "model_inference",
    "provider_execution",
    "app_apply",
    "app_state_mutation",
    "external_send",
    "generated_code_correctness",
    "production_readiness",
    "security_certification",
]


@dataclass
class ProjectionProofBoundary:
    boundary_id: str
    proven: list[str]
    not_proven: list[str]
    claim_boundary: str = CLAIM_BOUNDARY
    candidate_only: bool = True

    def to_dict(self) -> dict:
        return {
            "boundary_id": self.boundary_id,
            "proven": list(self.proven),
            "not_proven": list(self.not_proven),
            "claim_boundary": self.claim_boundary,
            "candidate_only": self.candidate_only,
        }


def build_proof_packet() -> dict:
    return {
        "artifact_kind": "odin_projection_candidate_spine_proof_packet",
        "proven": list(REQUIRED_PROVEN),
        "not_proven": list(REQUIRED_NOT_PROVEN),
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_only": True,
        "app_owned_apply": True,
    }


def persist_proof_packet(repo_root: Path | str = ".") -> dict:
    packet = build_proof_packet()
    out = Path(repo_root) / "reports" / "final_pr_08_projection_candidate_spine_proof_packet.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return packet
