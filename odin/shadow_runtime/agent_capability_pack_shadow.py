"""Shadow Runtime — Agent Capability Pack.

Capability Packs bind worker classes to runtime slices and candidate outputs.

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
        "shadow_module": "agent_capability_pack_shadow.py",
        "status": "shadow_only_candidate_preparation",
        "candidate_only": True,
        "app_apply": False,
        "external_send": False,
        "purpose": 'Capability Packs bind worker classes to runtime slices and candidate outputs.',
    }


def build_shadow_packet(work_id: str = "WORK-SHADOW") -> dict:
    return {
        "artifact_kind": "odin_shadow_packet",
        "work_id": work_id,
        "module": "agent_capability_pack_shadow.py",
        "authority_scope": "odin_internal_candidate_only",
        "requires_app_apply_gate": True,
        "why_trace_required": True,
    }
