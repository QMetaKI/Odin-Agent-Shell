"""ExpressionPacket for FINAL-PR-08 Projection Candidate Spine.

near_code and near_artifact are text descriptions only.
They are NOT executed, NOT applied, and NOT proof of code correctness.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from odin.projection_candidate_spine.candidate_graph import CandidateNode

CLAIM_BOUNDARY = "projection_candidate_spine_prepares_candidates_not_runtime_execution"


@dataclass
class ExpressionPacket:
    packet_id: str
    candidate_node: CandidateNode
    near_code: str | None
    near_artifact: str | None
    proof_boundary: str
    trace_receipt_id: str | None = None
    candidate_only: bool = True
    claim_boundary: str = CLAIM_BOUNDARY
    near_code_execution: bool = False

    def to_dict(self) -> dict:
        return {
            "packet_id": self.packet_id,
            "candidate_node": self.candidate_node.to_dict(),
            "near_code": self.near_code,
            "near_artifact": self.near_artifact,
            "proof_boundary": self.proof_boundary,
            "trace_receipt_id": self.trace_receipt_id,
            "candidate_only": self.candidate_only,
            "claim_boundary": self.claim_boundary,
            "near_code_execution": self.near_code_execution,
        }


def _deterministic_packet_id(node_id: str, near_code: str | None) -> str:
    payload = json.dumps({"node_id": node_id, "near_code": near_code}, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"expression_packet_{digest}"


def build_expression_packet(
    candidate_node: CandidateNode,
    near_code: str | None = None,
    near_artifact: str | None = None,
    trace_receipt_id: str | None = None,
) -> ExpressionPacket:
    """Build an ExpressionPacket.

    near_code is text only — it is never evaluated, executed, or applied.
    near_artifact is a description only — it is never applied.
    """
    packet_id = _deterministic_packet_id(candidate_node.node_id, near_code)
    return ExpressionPacket(
        packet_id=packet_id,
        candidate_node=candidate_node,
        near_code=near_code,
        near_artifact=near_artifact,
        proof_boundary=CLAIM_BOUNDARY,
        trace_receipt_id=trace_receipt_id,
        near_code_execution=False,
    )
