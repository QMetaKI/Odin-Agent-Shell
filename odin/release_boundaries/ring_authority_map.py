"""Ring / Authority Map — FINAL-PR-10++.

Claim boundary: final_pr_10_boundary_gated_release_operationalization_not_release_certification
candidate_only: true
app_owned_apply: true

Maps Odin's authority rings from host app (Ring 0) through release governance (Ring 7)
and external proof (Ring X).

This module does NOT grant authority. Ring 0 owns apply and domain truth.
Odin operates in Rings 1-7 as candidate-only.
"""
from __future__ import annotations

import hashlib
import json

_CLAIM_BOUNDARY = "final_pr_10_boundary_gated_release_operationalization_not_release_certification"
_GENERATED_AT = "2026-01-01T00:00:00Z"


def _make_id(ring_id: str) -> str:
    digest = hashlib.sha256(f"ring_authority_{ring_id}".encode()).hexdigest()[:16]
    return f"ring_authority_{ring_id}_{digest}"


_RINGS = [
    {
        "ring_id": "ring_0",
        "name": "Host App / User Apply Authority",
        "owns": [
            "app_state_apply",
            "domain_truth",
            "final_state_transitions",
            "external_send_authority",
            "security_certification_authority",
            "production_readiness_authority",
        ],
        "does_not_own": [],
        "allowed_inputs": ["odin_candidate_artifacts", "odin_response_packets"],
        "allowed_outputs": ["applied_app_state", "user_visible_results", "receipts_to_odin"],
        "forbidden_authority": [],
        "receipt_requirements": "None required — Ring 0 is the authority source.",
        "claim_boundary": "ring_0_is_app_authority_not_odin",
        "candidate_only": False,
    },
    {
        "ring_id": "ring_1",
        "name": "Odin Candidate Kernel",
        "owns": [
            "candidate_artifact_generation",
            "work_packet_orchestration",
            "operational_spine_execution",
        ],
        "does_not_own": [
            "app_apply",
            "domain_truth",
            "external_send",
            "production_readiness",
            "security_certification",
        ],
        "allowed_inputs": ["universal_work_request", "work_context", "receipts_from_ring_0"],
        "allowed_outputs": ["candidate_artifacts", "response_packets", "trace_receipts"],
        "forbidden_authority": ["app_apply", "domain_truth", "external_send"],
        "receipt_requirements": "Requires host app receipt for any non-local operation.",
        "claim_boundary": "ring_1_candidate_kernel_not_app_authority",
        "candidate_only": True,
    },
    {
        "ring_id": "ring_2",
        "name": "Universal Work / ModelWorkPacket Layer",
        "owns": [
            "work_packet_validation",
            "model_work_packet_enforcement",
            "output_contract_binding",
        ],
        "does_not_own": [
            "app_apply",
            "model_inference_authority",
            "provider_execution_authority",
        ],
        "allowed_inputs": ["universal_work_input", "work_context", "seed_route"],
        "allowed_outputs": ["validated_modelworkpacket", "output_contract", "not_proven_list"],
        "forbidden_authority": ["app_apply", "provider_execution", "truth_authority"],
        "receipt_requirements": "Requires final gate receipt before candidate release.",
        "claim_boundary": "ring_2_universal_work_candidate_not_authority",
        "candidate_only": True,
    },
    {
        "ring_id": "ring_3",
        "name": "QIRC / Semantic Bus Coordination",
        "owns": [
            "local_event_coordination",
            "channel_routing",
            "trace_emission",
        ],
        "does_not_own": [
            "app_state",
            "app_authority",
            "external_send",
            "provider_execution",
        ],
        "allowed_inputs": ["local_events", "trace_receipts", "odin_activity"],
        "allowed_outputs": ["local_qirc_events", "trace_receipts", "channel_summaries"],
        "forbidden_authority": ["app_state_mutation", "app_authority", "external_send"],
        "receipt_requirements": "QIRC coordination is local-only; no external receipts.",
        "claim_boundary": "ring_3_qirc_local_coordinator_not_app_authority",
        "candidate_only": True,
    },
    {
        "ring_id": "ring_4",
        "name": "Provider / Worker Projection",
        "owns": [
            "model_projection_candidate_generation",
            "provider_seam_negotiation",
        ],
        "does_not_own": [
            "truth_authority",
            "app_apply",
            "final_gate_authority",
            "external_send_authority",
        ],
        "allowed_inputs": ["modelworkpacket", "work_context", "provider_config"],
        "allowed_outputs": ["projection_candidates", "provider_status_packets"],
        "forbidden_authority": ["truth_authority", "app_apply", "external_send"],
        "receipt_requirements": "Provider execution requires explicit host app receipt. Disabled by default.",
        "claim_boundary": "ring_4_provider_projection_not_truth",
        "candidate_only": True,
    },
    {
        "ring_id": "ring_5",
        "name": "Critic / Final Gate / Candidate Selection",
        "owns": [
            "candidate_evaluation",
            "critic_cascade_execution",
            "final_gate_decision",
            "candidate_selection",
        ],
        "does_not_own": [
            "app_apply",
            "truth_authority",
            "release_certification",
        ],
        "allowed_inputs": ["projection_candidates", "critic_criteria", "output_contract"],
        "allowed_outputs": ["final_gate_result", "selected_candidate", "critic_receipts"],
        "forbidden_authority": ["app_apply", "release_certification", "truth_authority"],
        "receipt_requirements": "Final gate result is a receipt for Ring 1 release.",
        "claim_boundary": "ring_5_critic_final_gate_not_release_authority",
        "candidate_only": True,
    },
    {
        "ring_id": "ring_6",
        "name": "Proof / Trace / Receipt",
        "owns": [
            "proof_chain_assembly",
            "trace_receipt_generation",
            "claim_scoping",
        ],
        "does_not_own": [
            "production_readiness_proof",
            "security_certification_proof",
            "live_model_inference_proof",
        ],
        "allowed_inputs": ["trace_events", "candidate_artifacts", "critic_receipts"],
        "allowed_outputs": ["proof_packets", "scoped_receipts", "trace_summaries"],
        "forbidden_authority": ["production_readiness", "security_certification", "release_certification"],
        "receipt_requirements": "All proof packets include not_proven list and claim_boundary.",
        "claim_boundary": "ring_6_proof_chain_scoped_not_production_proof",
        "candidate_only": True,
    },
    {
        "ring_id": "ring_7",
        "name": "Release / Claim Governance",
        "owns": [
            "release_claim_validation",
            "artifact_currency_classification",
            "boundary_matrix_enforcement",
            "release_preflight_gating",
        ],
        "does_not_own": [
            "production_readiness_certification",
            "security_certification",
            "release_certification",
            "final_pr_11_release_closure",
        ],
        "allowed_inputs": ["boundary_matrix", "proof_packets", "evidence_closure_index"],
        "allowed_outputs": ["release_preflight_result", "allowed_claims_list", "forbidden_claims_list"],
        "forbidden_authority": ["production_readiness", "security_certification", "release_certification"],
        "receipt_requirements": "Release governance outputs include final_pr_11_remains_deferred: true.",
        "claim_boundary": "ring_7_release_governance_not_release_certification",
        "candidate_only": True,
    },
    {
        "ring_id": "ring_x",
        "name": "External / Remote / Host-specific Proof Required",
        "owns": [],
        "does_not_own": [
            "local_authority",
            "odin_candidate_authority",
        ],
        "allowed_inputs": ["external_audit_receipt", "host_app_receipt", "third_party_certification"],
        "allowed_outputs": ["external_proof_receipt"],
        "forbidden_authority": ["everything_without_explicit_receipt"],
        "receipt_requirements": "All Ring X claims require external receipts not provided by Odin.",
        "claim_boundary": "ring_x_external_proof_required_not_local_claim",
        "candidate_only": True,
    },
]


def build_ring_authority_map() -> dict:
    """Build the ring authority map.

    Maps authority rings from host app (Ring 0) to external proof (Ring X).
    Ring 0 owns apply and domain truth. Odin operates in Rings 1-7 as candidate-only.
    """
    rings = {}
    for ring in _RINGS:
        rid = ring["ring_id"]
        rings[rid] = dict(ring, ring_authority_id=_make_id(rid))

    return json.loads(json.dumps({
        "artifact_kind": "odin_final_pr_10_ring_authority_map",
        "candidate_only": True,
        "app_owned_apply": True,
        "claim_boundary": _CLAIM_BOUNDARY,
        "generated_at_utc": _GENERATED_AT,
        "ring_count": len(rings),
        "rings": rings,
        "key_axioms": [
            "Ring 0 owns apply and domain truth — Odin does not.",
            "QIRC (Ring 3) does not own app state.",
            "Providers (Ring 4) do not own truth.",
            "Release governance (Ring 7) does not certify production.",
            "Ring X requires external receipts not provided by Odin.",
        ],
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
            "security_certification",
            "release_certification",
        ],
        "final_pr_11_remains_deferred": True,
    }))
