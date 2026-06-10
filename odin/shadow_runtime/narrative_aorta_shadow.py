"""Narrative Aorta shadow mapping.

Human-readable Fairy nodes must map to typed Y* and runtime contracts.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class NarrativeAortaNodeShadow:
    node_id: str
    fairy_label: str
    ystar_node_ref: str
    runtime_contract_ref: str
    ring: str
    authority_posture: str
    forbidden_edges: tuple[str, ...]
    output_artifacts: tuple[str, ...]
    trace_label: str


def validate_aorta_node_shadow(node: NarrativeAortaNodeShadow) -> list[str]:
    errors: list[str] = []
    if not node.ystar_node_ref:
        errors.append("missing_ystar_node_ref")
    if not node.runtime_contract_ref:
        errors.append("missing_runtime_contract_ref")
    if "app_apply" not in node.forbidden_edges:
        errors.append("missing_forbidden_app_apply")
    if "external_send" not in node.forbidden_edges:
        errors.append("missing_forbidden_external_send")
    if not node.trace_label:
        errors.append("missing_trace_label")
    return errors
