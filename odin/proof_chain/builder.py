"""Proof chain builder — FINAL-PR-05.

Claim boundary: final_pr_05_proof_chain_cross_reference_not_production_proof
candidate_only: true
local_only: true
"""
from __future__ import annotations

import time
from pathlib import Path

from .registry import PROOF_CHAIN_REGISTRY, check_report_exists

ROOT = Path(__file__).resolve().parents[2]

CLAIM_BOUNDARY = "final_pr_05_proof_chain_cross_reference_not_production_proof"

NOT_PROVEN = [
    "production_readiness",
    "live_model_inference",
    "app_state_mutation",
    "external_send_authority",
]


def build_proof_chain() -> dict:
    entries = []
    for pr_key in PROOF_CHAIN_REGISTRY:
        status = check_report_exists(pr_key)
        entry = dict(PROOF_CHAIN_REGISTRY[pr_key])
        entry["report_exists"] = status["report_exists"]
        entry["proof_exists"] = status["proof_exists"]
        entries.append(entry)

    return {
        "artifact_kind": "odin_final_pr_proof_chain",
        "candidate_only": True,
        "local_only": True,
        "pr_count": len(entries),
        "entries": entries,
        "not_proven": NOT_PROVEN,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "claim_boundary": CLAIM_BOUNDARY,
    }
