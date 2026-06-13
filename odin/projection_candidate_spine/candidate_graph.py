"""CandidateNode and CandidateGraph for FINAL-PR-08 Projection Candidate Spine."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

from odin.projection_candidate_spine.materialization import validate_materialization_level

CLAIM_BOUNDARY = "projection_candidate_spine_prepares_candidates_not_runtime_execution"


@dataclass
class CandidateNode:
    node_id: str
    label: str
    materialization_level: str
    content_summary: str
    proof_boundary: str
    receipt_link_id: str | None = None
    candidate_only: bool = True
    claim_boundary: str = CLAIM_BOUNDARY

    def __post_init__(self) -> None:
        if not validate_materialization_level(self.materialization_level):
            raise ValueError(f"invalid materialization_level: {self.materialization_level!r}")

    def to_dict(self) -> dict:
        return {
            "node_id": self.node_id,
            "label": self.label,
            "materialization_level": self.materialization_level,
            "content_summary": self.content_summary,
            "proof_boundary": self.proof_boundary,
            "receipt_link_id": self.receipt_link_id,
            "candidate_only": self.candidate_only,
            "claim_boundary": self.claim_boundary,
        }


@dataclass
class CandidateGraph:
    graph_id: str
    nodes: list[CandidateNode]
    edges: list[dict]
    entry_node_id: str
    candidate_only: bool = True
    claim_boundary: str = CLAIM_BOUNDARY

    def to_dict(self) -> dict:
        return {
            "graph_id": self.graph_id,
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": list(self.edges),
            "entry_node_id": self.entry_node_id,
            "candidate_only": self.candidate_only,
            "claim_boundary": self.claim_boundary,
        }


def _deterministic_graph_id(
    nodes: list[CandidateNode],
    edges: list[dict],
    entry_node_id: str,
) -> str:
    payload = json.dumps(
        {
            "node_ids": [n.node_id for n in nodes],
            "edges": edges,
            "entry_node_id": entry_node_id,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"candidate_graph_{digest}"


def _build_derived_from_chain(nodes: list[CandidateNode]) -> list[dict]:
    edges = []
    for i in range(len(nodes) - 1):
        edges.append({
            "from_node_id": nodes[i].node_id,
            "to_node_id": nodes[i + 1].node_id,
            "relation": "derived_from",
        })
    return edges


def build_candidate_graph(
    nodes: list[CandidateNode],
    edges: list[dict] | None = None,
    entry_node_id: str | None = None,
) -> CandidateGraph:
    if not nodes:
        raise ValueError("nodes must be non-empty")
    resolved_entry = entry_node_id if entry_node_id is not None else nodes[0].node_id
    resolved_edges: list[dict]
    if edges is not None:
        resolved_edges = list(edges)
    elif len(nodes) > 1:
        resolved_edges = _build_derived_from_chain(nodes)
    else:
        resolved_edges = []
    graph_id = _deterministic_graph_id(nodes, resolved_edges, resolved_entry)
    return CandidateGraph(
        graph_id=graph_id,
        nodes=list(nodes),
        edges=resolved_edges,
        entry_node_id=resolved_entry,
    )
