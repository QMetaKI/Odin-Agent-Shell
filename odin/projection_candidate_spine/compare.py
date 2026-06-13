"""CandidateComparison for FINAL-PR-08 Projection Candidate Spine."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from odin.projection_candidate_spine.candidate_graph import CandidateNode
from odin.projection_candidate_spine.materialization import materialization_index

CLAIM_BOUNDARY = "projection_candidate_spine_prepares_candidates_not_runtime_execution"

DEFAULT_COMPARISON_AXES = [
    "materialization_proximity",
    "content_summary_length",
    "label_specificity",
]

NOT_PROVEN_DEFAULT = [
    "generated_code_correctness_unless_tested",
    "production_readiness",
    "runtime_execution",
    "app_apply",
]


@dataclass
class CandidateComparison:
    comparison_id: str
    node_a_id: str
    node_b_id: str
    winner_id: str | None
    comparison_axes: list[str]
    not_proven: list[str]
    candidate_only: bool = True
    claim_boundary: str = CLAIM_BOUNDARY

    def to_dict(self) -> dict:
        return {
            "comparison_id": self.comparison_id,
            "node_a_id": self.node_a_id,
            "node_b_id": self.node_b_id,
            "winner_id": self.winner_id,
            "comparison_axes": list(self.comparison_axes),
            "not_proven": list(self.not_proven),
            "candidate_only": self.candidate_only,
            "claim_boundary": self.claim_boundary,
        }


def _deterministic_comparison_id(node_a_id: str, node_b_id: str) -> str:
    payload = json.dumps({"a": node_a_id, "b": node_b_id}, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"candidate_comparison_{digest}"


def compare_candidate_nodes(
    node_a: CandidateNode,
    node_b: CandidateNode,
    comparison_axes: list[str] | None = None,
) -> CandidateComparison:
    """Compare two CandidateNodes deterministically.

    winner_id is a recommendation only — not authority, not proof.
    """
    axes = list(comparison_axes) if comparison_axes is not None else list(DEFAULT_COMPARISON_AXES)
    comparison_id = _deterministic_comparison_id(node_a.node_id, node_b.node_id)

    try:
        idx_a = materialization_index(node_a.materialization_level)
        idx_b = materialization_index(node_b.materialization_level)
        if idx_a < idx_b:
            winner_id = node_a.node_id
        elif idx_b < idx_a:
            winner_id = node_b.node_id
        else:
            len_a = len(node_a.content_summary)
            len_b = len(node_b.content_summary)
            if len_a <= len_b:
                winner_id = node_a.node_id
            else:
                winner_id = node_b.node_id
    except ValueError:
        winner_id = None

    return CandidateComparison(
        comparison_id=comparison_id,
        node_a_id=node_a.node_id,
        node_b_id=node_b.node_id,
        winner_id=winner_id,
        comparison_axes=axes,
        not_proven=list(NOT_PROVEN_DEFAULT),
    )
