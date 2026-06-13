"""ProjectionSet for FINAL-PR-08 Projection Candidate Spine."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

from odin.projection_candidate_spine.candidate_graph import CandidateNode, build_candidate_graph
from odin.projection_candidate_spine.materialization import MATERIALIZATION_LEVELS

CLAIM_BOUNDARY = "projection_candidate_spine_prepares_candidates_not_runtime_execution"
PROJECTION_MATERIALIZATION_LEVEL = "M5_projection_set"


@dataclass
class ProjectionSet:
    projection_id: str
    source_context: dict
    candidate_nodes: list[CandidateNode]
    materialization_level: str = PROJECTION_MATERIALIZATION_LEVEL
    candidate_only: bool = True
    claim_boundary: str = CLAIM_BOUNDARY

    def to_dict(self) -> dict:
        return {
            "projection_id": self.projection_id,
            "source_context": dict(self.source_context),
            "candidate_nodes": [n.to_dict() for n in self.candidate_nodes],
            "materialization_level": self.materialization_level,
            "candidate_only": self.candidate_only,
            "claim_boundary": self.claim_boundary,
        }


def _deterministic_projection_id(source_context: dict) -> str:
    payload = json.dumps(source_context, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"projection_set_{digest}"


def build_projection_set(
    source_context: dict,
    candidate_nodes: list[CandidateNode],
) -> ProjectionSet:
    projection_id = _deterministic_projection_id(source_context)
    return ProjectionSet(
        projection_id=projection_id,
        source_context=dict(source_context),
        candidate_nodes=list(candidate_nodes),
    )


def build_projection_set_from_field_selection(field_selection) -> ProjectionSet:
    """Build a ProjectionSet from a PR07 FieldSelection object or dict."""
    if hasattr(field_selection, "to_dict"):
        fs_dict = field_selection.to_dict()
    elif isinstance(field_selection, dict):
        fs_dict = dict(field_selection)
    else:
        fs_dict = {
            name: getattr(field_selection, name)
            for name in ("dominant_field", "route_recommendation", "claim_boundary", "candidate_only")
            if hasattr(field_selection, name)
        }

    source_context: dict = {
        "field_selection_available": True,
        "candidate_only": fs_dict.get("candidate_only", True),
        "app_owned_apply": fs_dict.get("app_owned_apply", True),
        "claim_boundary": fs_dict.get("claim_boundary", "field_selection_scores_routes_not_truth"),
    }

    dominant = fs_dict.get("dominant_field")
    if isinstance(dominant, dict):
        source_context["field_id"] = dominant.get("field_id", "unknown")
        source_context["field_confidence"] = dominant.get("confidence", 0.0)
        why_trace_id = dominant.get("why_trace_id")
        if why_trace_id:
            source_context["why_trace_id"] = why_trace_id
    elif hasattr(dominant, "field_id"):
        source_context["field_id"] = dominant.field_id

    route_recommendation = fs_dict.get("route_recommendation", "")
    if route_recommendation:
        source_context["route_recommendation"] = route_recommendation

    why_trace = fs_dict.get("why_trace")
    if isinstance(why_trace, dict):
        trace_id = why_trace.get("trace_id")
        if trace_id:
            source_context["field_why_trace_id"] = trace_id

    field_id = source_context.get("field_id", "unknown")

    import hashlib as _hashlib
    _payload = json.dumps(source_context, sort_keys=True, separators=(",", ":"))
    _digest = _hashlib.sha256(_payload.encode("utf-8")).hexdigest()[:12]
    node_id = f"candidate_node_{_digest}"

    node = CandidateNode(
        node_id=node_id,
        label=f"field_selection:{field_id}",
        materialization_level="M6_candidate_artifact",
        content_summary=f"Candidate derived from field selection route: {field_id}",
        proof_boundary=CLAIM_BOUNDARY,
    )

    return build_projection_set(source_context, [node])
