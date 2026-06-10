"""Shadow Runtime — Model Agent Card.

Model/Agent Capability Cards describe allowed slots, blocked work, privacy and traceability.

Non-authority rules:
- no real model calls
- no sockets
- no app mutation
- no external send
- no runtime proof claims
"""
from __future__ import annotations


def describe() -> dict:
    return {
        "shadow_module": "model_agent_card_shadow.py",
        "status": "shadow_only_candidate_preparation",
        "candidate_only": True,
        "app_apply": False,
        "external_send": False,
        "purpose": 'Model/Agent Capability Cards describe allowed slots, blocked work, privacy and traceability.',
    }


def build_shadow_packet(work_id: str = "WORK-SHADOW") -> dict:
    return {
        "artifact_kind": "odin_shadow_packet",
        "work_id": work_id,
        "module": "model_agent_card_shadow.py",
        "authority_scope": "odin_internal_candidate_only",
        "requires_app_apply_gate": True,
        "why_trace_required": True,
    }
