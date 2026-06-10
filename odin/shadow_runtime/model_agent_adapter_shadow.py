# SPDX-License-Identifier: GPL-2.0-only
"""Shadow module: Model Agent Adapter Boundary.

This module is code-near, non-authoritative, candidate-only and intentionally
contains no real model calls, no sockets, no app mutation and no external sends.
Codex must convert this into real implementation only behind Odin gates.
"""

from __future__ import annotations


def describe() -> dict:
    return {
        "shadow_module": "model_agent_adapter_shadow",
        "boundary": "candidate_only_no_apply",
        "forbidden": ["app_apply", "external_send", "authority_transfer"],
        "real_target": "odin/agents/model_agent_adapter.py",
    }


def build_shadow_packet(work_id: str) -> dict:
    return {
        "work_id": work_id,
        "status": "shadow_candidate_only",
        "module": "model_agent_adapter_shadow",
        "requires_final_gate": True,
    }
