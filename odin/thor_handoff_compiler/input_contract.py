"""Thor Handoff Compiler input contract builder — FINAL-PR-11."""
from __future__ import annotations

import hashlib
import json

CLAIM_BOUNDARY = "thor_handoff_compiler_v0_compiles_worker_packets_not_thor_runtime"

_NOT_PROVEN = [
    "production_readiness",
    "security_certification",
    "release_certification",
    "real_model_benchmark",
    "model_quality_superiority",
    "thor_runtime_execution",
    "agent_autonomy",
    "app_apply",
    "external_send",
    "public_network",
]


def _sha256_id(prefix: str, payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    h = hashlib.sha256(raw.encode()).hexdigest()[:16]
    return f"{prefix}{h}"


def build_handoff_input_contract(
    *,
    objective: str,
    repo_evidence: list[str],
    allowed_edits: list[str],
    forbidden_edits: list[str],
    acceptance_gates: list[str],
    claim_boundary: str,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build a deterministic Thor handoff input contract.

    Output is a compile artifact for Claude Code / Codex work.
    NOT a Thor runtime execution. NOT agent autonomy.
    """
    contract_id = _sha256_id(
        "thor_input_",
        {
            "objective": objective,
            "claim_boundary": claim_boundary,
            "generated_at_utc": generated_at_utc,
        },
    )
    return {
        "artifact_kind": "odin_thor_handoff_input_contract",
        "contract_id": contract_id,
        "objective": objective,
        "repo_evidence": list(repo_evidence),
        "allowed_edits": list(allowed_edits),
        "forbidden_edits": list(forbidden_edits),
        "acceptance_gates": list(acceptance_gates),
        "claim_boundary": claim_boundary,
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
        "generated_at_utc": generated_at_utc,
    }
