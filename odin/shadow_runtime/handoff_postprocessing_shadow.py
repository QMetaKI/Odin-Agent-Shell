"""Shadow module for Handoff Postprocessing.

Candidate-only, no runtime proof, no model calls, no sockets, no app mutation.
"""
from __future__ import annotations

CANDIDATE_ONLY = True
APP_APPLY = False
EXTERNAL_SEND = False
RUNTIME_PROOF = False


def build_shadow_packet(source: dict) -> dict:
    """Return a deterministic shadow packet describing the future real module behavior."""
    return {
        "artifact_kind": "odin_handoff_postprocessing_shadow",
        "protocol_version": "7.1-shadow",
        "candidate_only": CANDIDATE_ONLY,
        "app_apply": APP_APPLY,
        "external_send": EXTERNAL_SEND,
        "runtime_proof": RUNTIME_PROOF,
        "source_kind": source.get("source_kind", "unknown"),
        "claim_boundary": "shadow_candidate_only_no_execution",
        "required_next_gate": "handoff_review_gate",
    }
