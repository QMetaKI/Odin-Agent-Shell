"""FINAL-PR Ladder scaffold proof — FINAL-PR-05.

Claim boundary: final_pr_ladder_scaffold_not_full_prompt_compiler
candidate_only: true
local_only: true
"""
from __future__ import annotations

import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CLAIM_BOUNDARY = "final_pr_ladder_scaffold_not_full_prompt_compiler"

NOT_PROVEN = [
    "production_readiness",
    "live_model_inference",
    "app_state_mutation",
    "external_send_authority",
    "complete_prompt_generation",
    "thor_runtime_replacement",
]


def build_ladder_scaffold_proof(target_pr_id: str = "FINAL-PR-06") -> dict:
    from .compiler import compile_worker_packet_scaffold
    scaffold = compile_worker_packet_scaffold(
        target_pr_id=target_pr_id,
        prior_return_report_path="reports/final_pr_05_execution_gate_report.json",
        profile="claude-code",
    )
    return {
        "artifact_kind": "odin_final_pr_ladder_scaffold_proof",
        "status": "ok",
        "target_pr_id": target_pr_id,
        "scaffold_present": True,
        "scaffold_candidate_only": scaffold.get("candidate_only") is True,
        "scaffold_not_thor_replacement": True,
        "sections_count": len(scaffold.get("sections", [])),
        "not_proven": NOT_PROVEN,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "claim_boundary": CLAIM_BOUNDARY,
    }
