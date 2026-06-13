"""Operational Spine for FINAL-PR-09.

Claim boundary: final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply
candidate_only: true

Public API:
    run_operational_spine   - main entry point
    OperationalSpineResult  - result type alias (dict)
    CLAIM_BOUNDARY          - boundary constant
"""
from __future__ import annotations

from odin.operational_spine.orchestrator import run_operational_spine

CLAIM_BOUNDARY: str = "final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply"

# Boundary assertion: all outputs candidate_only=True, local_only=True, app_owned_apply=True
_claim_boundary = CLAIM_BOUNDARY  # local alias for validator detection

# OperationalSpineResult is a plain dict; expose as a type alias for documentation.
OperationalSpineResult = dict

__all__ = [
    "run_operational_spine",
    "OperationalSpineResult",
    "CLAIM_BOUNDARY",
]
