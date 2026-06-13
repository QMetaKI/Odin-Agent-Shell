"""Thor Handoff Compiler v0 — core compiler functions — FINAL-PR-11.

Deterministic. No model needed. No Thor runtime claim. No agent autonomy.
Output is a compile artifact for Claude Code / Codex worker use.
"""
from __future__ import annotations

import hashlib
import json

from odin.thor_handoff_compiler.input_contract import CLAIM_BOUNDARY, _NOT_PROVEN, _sha256_id


def compile_agent_operator_work_packet(input_contract: dict) -> dict:
    """Compile an Agent Operator Work Packet from input contract."""
    packet_id = _sha256_id("aowp_", {"contract_id": input_contract.get("contract_id", "")})
    return {
        "artifact_kind": "odin_agent_operator_work_packet_compiled",
        "packet_id": packet_id,
        "objective": input_contract.get("objective"),
        "inputs": input_contract.get("repo_evidence", []),
        "allowed_edits": input_contract.get("allowed_edits", []),
        "forbidden_edits": input_contract.get("forbidden_edits", []),
        "acceptance_gates": input_contract.get("acceptance_gates", []),
        "claim_boundary": input_contract.get("claim_boundary"),
        "candidate_only": True,
        "app_owned_apply": True,
        "app_apply": False,
        "external_send": False,
        "public_network": False,
        "thor_runtime_execution": False,
        "agent_autonomy": False,
        "evidence_class": "structural_evidence",
        "compiler_claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(_NOT_PROVEN),
        "generated_at_utc": input_contract.get("generated_at_utc", "2026-01-01T00:00:00Z"),
        "compiled_from": input_contract.get("contract_id"),
    }


def compile_acceptance_matrix(input_contract: dict) -> dict:
    """Compile an Acceptance Matrix from input contract."""
    matrix_id = _sha256_id("acc_matrix_", {"contract_id": input_contract.get("contract_id", "")})
    gates = input_contract.get("acceptance_gates", [])
    rows = [
        {
            "gate": gate,
            "required": True,
            "verification_method": "validate_* command or pytest",
            "evidence_class": "structural_evidence",
        }
        for gate in gates
    ]
    return {
        "artifact_kind": "odin_acceptance_matrix_compiled",
        "matrix_id": matrix_id,
        "objective": input_contract.get("objective"),
        "rows": rows,
        "candidate_only": True,
        "app_owned_apply": True,
        "compiler_claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(_NOT_PROVEN),
        "generated_at_utc": input_contract.get("generated_at_utc", "2026-01-01T00:00:00Z"),
    }


def compile_validator_plan(input_contract: dict) -> dict:
    """Compile a Validator Plan from input contract."""
    plan_id = _sha256_id("val_plan_", {"contract_id": input_contract.get("contract_id", "")})
    gates = input_contract.get("acceptance_gates", [])
    checks = [
        {
            "check": f"validate_{i+1}",
            "description": gate,
            "stdlib_only": True,
            "deterministic": True,
        }
        for i, gate in enumerate(gates)
    ]
    return {
        "artifact_kind": "odin_validator_plan_compiled",
        "plan_id": plan_id,
        "checks": checks,
        "stdlib_only": True,
        "no_model_required": True,
        "deterministic": True,
        "candidate_only": True,
        "compiler_claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(_NOT_PROVEN),
        "generated_at_utc": input_contract.get("generated_at_utc", "2026-01-01T00:00:00Z"),
    }


def compile_pr_body_skeleton(input_contract: dict) -> dict:
    """Compile a PR Body Skeleton from input contract."""
    skel_id = _sha256_id("pr_body_", {"contract_id": input_contract.get("contract_id", "")})
    objective = input_contract.get("objective", "")
    claim_boundary = input_contract.get("claim_boundary", "")
    gates = input_contract.get("acceptance_gates", [])
    allowed = input_contract.get("allowed_edits", [])
    forbidden = input_contract.get("forbidden_edits", [])

    body = (
        f"## Motivation\n{objective}\n\n"
        f"## Scope\n"
        + "\n".join(f"- {a}" for a in allowed)
        + "\n\n## Non-Scope\n"
        + "\n".join(f"- {f}" for f in forbidden)
        + "\n\n## Acceptance Gates\n"
        + "\n".join(f"- [ ] {g}" for g in gates)
        + f"\n\n## Claim Boundary\n`{claim_boundary}`\n"
        + "\n## Not Proven\n"
        + "\n".join(f"- {np}" for np in _NOT_PROVEN)
    )

    return {
        "artifact_kind": "odin_pr_body_skeleton_compiled",
        "skeleton_id": skel_id,
        "pr_body_text": body,
        "candidate_only": True,
        "compiler_claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(_NOT_PROVEN),
        "generated_at_utc": input_contract.get("generated_at_utc", "2026-01-01T00:00:00Z"),
    }


def compile_thor_handoff_bundle(input_contract: dict) -> dict:
    """Compile a full Thor Handoff Bundle from input contract.

    Output is a compile artifact. NOT Thor runtime execution.
    """
    bundle_id = _sha256_id("thor_bundle_", {"contract_id": input_contract.get("contract_id", "")})
    aowp = compile_agent_operator_work_packet(input_contract)
    acceptance = compile_acceptance_matrix(input_contract)
    validator = compile_validator_plan(input_contract)
    pr_body = compile_pr_body_skeleton(input_contract)

    return {
        "artifact_kind": "odin_thor_handoff_bundle",
        "bundle_id": bundle_id,
        "repo_cognition_summary": {
            "repo_evidence": input_contract.get("repo_evidence", []),
            "claim_boundary": input_contract.get("claim_boundary"),
        },
        "objective": input_contract.get("objective"),
        "scope": input_contract.get("allowed_edits", []),
        "non_scope": input_contract.get("forbidden_edits", []),
        "allowed_edits": input_contract.get("allowed_edits", []),
        "forbidden_edits": input_contract.get("forbidden_edits", []),
        "acceptance_gates": input_contract.get("acceptance_gates", []),
        "agent_operator_work_packet": aowp,
        "acceptance_matrix": acceptance,
        "validator_plan": validator,
        "pr_body_skeleton": pr_body,
        "return_report_contract": {
            "required_sections": [
                "branch",
                "base_commit",
                "files_created",
                "files_modified",
                "tests_run",
                "full_suite_result",
                "claim_boundary",
                "not_proven",
            ]
        },
        "claim_boundary": input_contract.get("claim_boundary"),
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "app_apply": False,
        "external_send": False,
        "public_network": False,
        "thor_runtime_execution": False,
        "agent_autonomy": False,
        "evidence_class": "structural_evidence",
        "compiler_claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(_NOT_PROVEN),
        "generated_at_utc": input_contract.get("generated_at_utc", "2026-01-01T00:00:00Z"),
        "compiler_note": (
            "This bundle is a compile artifact for Claude Code / Codex worker use. "
            "It does not claim Thor runtime execution. "
            "It does not grant agent autonomy."
        ),
    }
