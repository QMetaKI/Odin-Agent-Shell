"""Reports builder — FINAL-PR-10++.

Claim boundary: final_pr_10_boundary_gated_release_operationalization_not_release_certification
candidate_only: true
app_owned_apply: true

Builds and writes all FINAL-PR-10++ reports.
"""
from __future__ import annotations

import json
from pathlib import Path

from odin.release_boundaries.boundary_matrix import build_boundary_matrix
from odin.release_boundaries.ring_authority_map import build_ring_authority_map
from odin.release_boundaries.bug6_q7_operational_map import build_bug6_q7_operational_map
from odin.release_boundaries.qshabang_release_gate_map import build_qshabang_release_gate_map
from odin.release_boundaries.model_role_authority import build_model_role_authority_matrix
from odin.release_boundaries.artifact_currency import build_artifact_currency_index
from odin.release_boundaries.evidence_closure import build_release_evidence_closure_index
from odin.release_boundaries.final_preflight import run_final_release_preflight

_CLAIM_BOUNDARY = "final_pr_10_boundary_gated_release_operationalization_not_release_certification"
_GENERATED_AT = "2026-01-01T00:00:00Z"


def build_all_reports(repo_root: Path | None = None) -> dict:
    """Build all FINAL-PR-10++ reports and return them as a dict."""
    return {
        "boundary_matrix": build_boundary_matrix(),
        "ring_authority_map": build_ring_authority_map(),
        "bug6_q7_operational_map": build_bug6_q7_operational_map(),
        "qshabang_release_gate_map": build_qshabang_release_gate_map(),
        "model_role_authority": build_model_role_authority_matrix(),
        "artifact_currency": build_artifact_currency_index(),
        "evidence_closure": build_release_evidence_closure_index(),
        "preflight": run_final_release_preflight(),
    }


def build_proof_packet() -> dict:
    """Build the FINAL-PR-10++ proof packet."""
    return {
        "artifact_kind": "odin_final_pr_10_boundary_release_proof_packet",
        "candidate_only": True,
        "app_owned_apply": True,
        "claim_boundary": _CLAIM_BOUNDARY,
        "generated_at_utc": _GENERATED_AT,
        "proven": [
            "boundary_matrix_exists",
            "ring_authority_map_exists",
            "bug6_q7_operational_map_exists",
            "qshabang_release_gate_map_exists",
            "model_role_authority_matrix_exists",
            "artifact_currency_index_exists",
            "release_evidence_closure_index_exists",
            "final_release_preflight_exists",
            "final_pr_11_remains_deferred",
        ],
        "not_proven": [
            "release_certification",
            "production_readiness",
            "security_certification",
            "live_model_inference",
            "real_model_benchmark",
            "provider_execution",
            "app_apply",
            "app_state_mutation",
            "external_send",
            "public_network",
        ],
    }


def write_reports(repo_root: Path) -> None:
    """Write all FINAL-PR-10++ reports to disk."""
    reports_dir = repo_root / "reports"
    reports_dir.mkdir(exist_ok=True)

    reports = build_all_reports(repo_root)

    (reports_dir / "final_pr_10_boundary_matrix_report.json").write_text(
        json.dumps(reports["boundary_matrix"], indent=2), encoding="utf-8"
    )
    (reports_dir / "final_pr_10_ring_authority_map.json").write_text(
        json.dumps(reports["ring_authority_map"], indent=2), encoding="utf-8"
    )
    (reports_dir / "final_pr_10_bug6_q7_operational_map.json").write_text(
        json.dumps(reports["bug6_q7_operational_map"], indent=2), encoding="utf-8"
    )
    (reports_dir / "final_pr_10_qshabang_release_gate_report.json").write_text(
        json.dumps(reports["qshabang_release_gate_map"], indent=2), encoding="utf-8"
    )
    (reports_dir / "final_pr_10_model_role_authority_report.json").write_text(
        json.dumps(reports["model_role_authority"], indent=2), encoding="utf-8"
    )
    (reports_dir / "final_pr_10_release_evidence_closure_index.json").write_text(
        json.dumps(reports["evidence_closure"], indent=2), encoding="utf-8"
    )
    (reports_dir / "final_pr_10_artifact_currency_report.json").write_text(
        json.dumps(reports["artifact_currency"], indent=2), encoding="utf-8"
    )
    (reports_dir / "final_pr_10_release_preflight_report.json").write_text(
        json.dumps(reports["preflight"], indent=2), encoding="utf-8"
    )
    (reports_dir / "final_pr_10_boundary_release_proof_packet.json").write_text(
        json.dumps(build_proof_packet(), indent=2), encoding="utf-8"
    )
