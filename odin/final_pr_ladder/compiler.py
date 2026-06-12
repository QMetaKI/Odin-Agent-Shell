"""FINAL-PR Ladder Compiler scaffold — FINAL-PR-05.

Claim boundary: final_pr_ladder_scaffold_not_full_prompt_compiler
candidate_only: true
local_only: true

This is a scaffold only. It does NOT replace Thor or generate full prompts.
"""
from __future__ import annotations

import time
from pathlib import Path

from .templates import WORKER_PACKET_SECTIONS

ROOT = Path(__file__).resolve().parents[2]

CLAIM_BOUNDARY = "final_pr_ladder_scaffold_not_full_prompt_compiler"

NOT_PROVEN = [
    "complete_prompt_generation",
    "thor_runtime_replacement",
    "production_readiness",
]

VALID_PROFILES = ["claude-code", "codex", "generic"]


class LadderCompiler:
    """Scaffold compiler — produces a worker packet scaffold. Not a Thor replacement."""

    def compile(
        self,
        target_pr_id: str,
        prior_return_report_path: str | None = None,
        profile: str = "claude-code",
    ) -> dict:
        if profile not in VALID_PROFILES:
            profile = "generic"

        prior_report_exists = False
        if prior_return_report_path:
            prior_report_exists = (ROOT / prior_return_report_path).exists()

        return {
            "artifact_kind": "odin_final_pr_worker_packet_scaffold",
            "target_pr_id": target_pr_id,
            "source_return_report": prior_return_report_path or "not_provided",
            "prior_report_exists": prior_report_exists,
            "profile": profile,
            "candidate_only": True,
            "local_only": True,
            "sections": list(WORKER_PACKET_SECTIONS),
            "not_proven": NOT_PROVEN,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "claim_boundary": CLAIM_BOUNDARY,
            "warnings": [
                "This scaffold is not a Thor replacement.",
                "This scaffold does not generate full prompts.",
                "Sections are templates only — fill in with actual PR scope.",
            ],
        }


def compile_worker_packet_scaffold(
    target_pr_id: str,
    prior_return_report_path: str | None = None,
    profile: str = "claude-code",
) -> dict:
    compiler = LadderCompiler()
    return compiler.compile(
        target_pr_id=target_pr_id,
        prior_return_report_path=prior_return_report_path,
        profile=profile,
    )
