"""Shadow module for AI Git Safety.

This file is code-near but non-executing. It documents the mechanical target
for Codex. It must not perform app mutation, external send, socket work, or
real model calls.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass(frozen=True)
class ShadowAIGitSafetyPacket:
    packet_id: str
    work_id: str
    decision: str
    reasons: List[str] = field(default_factory=list)
    blocked: List[str] = field(default_factory=list)
    trace: Dict[str, Any] = field(default_factory=dict)


def build_shadow_ai_git_safety(work: Dict[str, Any]) -> ShadowAIGitSafetyPacket:
    """Return a deterministic candidate-only shadow packet."""
    forbidden = work.get("forbidden", []) or []
    blocked = [item for item in forbidden if item in {"direct_apply", "external_send", "hidden_tool_use"}]
    decision = "block" if blocked else "allow_candidate"
    return ShadowAIGitSafetyPacket(
        packet_id="shadow-ai_git_safety",
        work_id=str(work.get("work_id", "WORK-SHADOW")),
        decision=decision,
        reasons=["candidate_only", "app_apply_boundary_preserved", "trace_required"],
        blocked=blocked,
        trace={"shadow_runtime": True, "authority": "odin_internal_candidate_only"},
    )
