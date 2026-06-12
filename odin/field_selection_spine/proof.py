"""Proof packet builder for FINAL-PR-07 Field Selection Spine."""
from __future__ import annotations

import json
from pathlib import Path

from odin.field_selection_spine.fields import CLAIM_BOUNDARY

REQUIRED_PROVEN = ["review_axes_defined", "coherence_scorer_deterministic", "field_selection_candidate_only", "why_trace_recorded"]
REQUIRED_NOT_PROVEN = [
    "autonomous_decision_authority", "final_truth_claim", "model_inference", "provider_execution", "app_apply",
    "app_state_mutation", "external_send", "production_readiness", "security_certification",
]


def build_proof_packet() -> dict:
    return {
        "artifact_kind": "odin_field_selection_spine_proof_packet",
        "proven": list(REQUIRED_PROVEN),
        "not_proven": list(REQUIRED_NOT_PROVEN),
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_only": True,
        "app_owned_apply": True,
    }


def persist_proof_packet(repo_root: Path | str = ".") -> dict:
    packet = build_proof_packet()
    out = Path(repo_root) / "reports" / "final_pr_07_field_selection_spine_proof_packet.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return packet
