# SPDX-License-Identifier: GPL-2.0-only
"""Shadow module: Universal LLM Work Construct.

This module is code-near, non-authoritative, candidate-only and intentionally
contains no real model calls, no sockets, no app mutation and no external sends.
Codex must convert this into real implementation only behind Odin gates.
"""

from __future__ import annotations


def describe() -> dict:
    return {
        "shadow_module": "universal_llm_work_construct_shadow",
        "boundary": "candidate_only_no_apply",
        "forbidden": ["app_apply", "external_send", "authority_transfer"],
        "real_target": "odin/universal_work/universal_llm_work_construct.py",
    }


def build_shadow_packet(work_id: str) -> dict:
    return {
        "work_id": work_id,
        "status": "shadow_candidate_only",
        "module": "universal_llm_work_construct_shadow",
        "requires_final_gate": True,
    }
