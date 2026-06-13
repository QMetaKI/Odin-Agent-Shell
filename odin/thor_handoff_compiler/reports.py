"""Thor Handoff Compiler report builder — FINAL-PR-11."""
from __future__ import annotations

from odin.thor_handoff_compiler.input_contract import CLAIM_BOUNDARY, _NOT_PROVEN


def build_thor_compiler_report(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build a structural report on the Thor Handoff Compiler v0."""
    return {
        "artifact_kind": "odin_thor_handoff_compiler_report",
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "app_apply": False,
        "external_send": False,
        "public_network": False,
        "thor_runtime_execution": False,
        "agent_autonomy": False,
        "evidence_class": "structural_evidence",
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(_NOT_PROVEN),
        "compiler_outputs": [
            "agent_operator_work_packet",
            "acceptance_matrix",
            "validator_plan",
            "pr_body_skeleton",
            "return_report_contract",
            "thor_handoff_bundle",
        ],
        "deterministic": True,
        "no_model_required": True,
        "generated_at_utc": generated_at_utc,
        "compiler_note": (
            "Thor Handoff Compiler v0 is a compile artifact generator. "
            "It does not run Thor. "
            "It does not grant agent autonomy."
        ),
    }
