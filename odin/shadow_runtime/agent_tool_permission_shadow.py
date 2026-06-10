# SPDX-License-Identifier: GPL-2.0-only
"""Shadow module: Agent Tool Permission Boundary.

This module is code-near, non-authoritative, candidate-only and intentionally
contains no real model calls, no sockets, no app mutation and no external sends.
Codex must convert this into real implementation only behind Odin gates.
"""

from __future__ import annotations


def describe() -> dict:
    return {
        "shadow_module": "agent_tool_permission_shadow",
        "boundary": "candidate_only_no_apply",
        "forbidden": ["app_apply", "external_send", "authority_transfer"],
        "real_target": "odin/agents/tool_permission.py",
    }


def build_shadow_packet(work_id: str) -> dict:
    return {
        "work_id": work_id,
        "status": "shadow_candidate_only",
        "module": "agent_tool_permission_shadow",
        "requires_final_gate": True,
    }
