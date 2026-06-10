"""Shadow module for MVP V1 Power Mode.

This is code-near, candidate-only planning. It performs no model calls, no socket binding,
no app mutation, no external send, and no host validation claim.
"""
from __future__ import annotations


def build_shadow_packet(input_packet: dict | None = None) -> dict:
    input_packet = input_packet or {}
    return {
        "artifact_kind": "odin_shadow_packet",
        "protocol_version": "7.1",
        "shadow_module": "mvp_v1_power_mode_shadow",
        "status": "candidate_plan_only",
        "input_keys": sorted(input_packet.keys()),
        "boundaries": ["candidate_only", "app_owned_apply", "no_runtime_proof", "gpl_2_0_only"],
    }
