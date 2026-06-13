"""odin.release_boundaries — FINAL-PR-10++ Boundary-Gated Release Operationalization.

Claim boundary: final_pr_10_boundary_gated_release_operationalization_not_release_certification

This package maps, verifies, and exposes Odin's candidate-only,
app-owned-apply, local-first, and model-role authority boundaries as
validator-backed release gates.

It does NOT:
- certify production readiness
- certify security
- certify release
- execute models
- open providers
- apply app state
- send externally
- implement FINAL-PR-11

candidate_only: true
app_owned_apply: true
"""
from __future__ import annotations

from odin.release_boundaries.boundary_matrix import build_boundary_matrix
from odin.release_boundaries.ring_authority_map import build_ring_authority_map
from odin.release_boundaries.bug6_q7_operational_map import build_bug6_q7_operational_map
from odin.release_boundaries.qshabang_release_gate_map import build_qshabang_release_gate_map
from odin.release_boundaries.model_role_authority import build_model_role_authority_matrix
from odin.release_boundaries.artifact_currency import build_artifact_currency_index
from odin.release_boundaries.evidence_closure import build_release_evidence_closure_index
from odin.release_boundaries.final_preflight import run_final_release_preflight

__all__ = [
    "build_boundary_matrix",
    "build_ring_authority_map",
    "build_bug6_q7_operational_map",
    "build_qshabang_release_gate_map",
    "build_model_role_authority_matrix",
    "build_artifact_currency_index",
    "build_release_evidence_closure_index",
    "run_final_release_preflight",
]
