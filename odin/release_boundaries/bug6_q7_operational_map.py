"""Bug6/Q7 Operational Map — FINAL-PR-10++.

Claim boundary: final_pr_10_boundary_gated_release_operationalization_not_release_certification
candidate_only: true
app_owned_apply: true

Translates Bug6/Q7 internal scanning concepts into neutral Odin release-boundary
language. Bug6 = authority drift scanner. Q7 = boundary coherence scanner.

Bug6 and Q7 are release-boundary lenses only. They do not create agent authority.
They do not have independent runtime execution.
"""
from __future__ import annotations

import hashlib
import json

_CLAIM_BOUNDARY = "final_pr_10_boundary_gated_release_operationalization_not_release_certification"
_GENERATED_AT = "2026-01-01T00:00:00Z"


def _make_id(key: str) -> str:
    digest = hashlib.sha256(f"bug6_q7_{key}".encode()).hexdigest()[:16]
    return f"bug6_q7_{key}_{digest}"


_DRIFT_MAP = [
    {
        "internal_term": "Bug6",
        "neutral_release_term": "authority_drift_scanner",
        "drift_detected": "authority_drift",
        "description": "Scans for any Odin subsystem acquiring authority it is not permitted to hold.",
        "repo_evidence": "odin/operational_spine/ — all outputs carry candidate_only: true and app_owned_apply: true.",
        "validator_evidence": "validate-operational-spine, validate-boundary-matrix pass.",
        "release_gate": "No authority drift detected in current PR09/PR10 operational spine.",
        "not_proven": ["live_model_inference", "production_readiness", "external_authority"],
        "claim_boundary": "bug6_authority_drift_scanner_not_agent_authority",
    },
    {
        "internal_term": "Q7",
        "neutral_release_term": "boundary_coherence_scanner",
        "drift_detected": "boundary_coherence_violations",
        "description": "Scans for boundary incoherence across Odin subsystems — mismatched claim boundaries, missing not_proven lists, or inconsistent candidate_only flags.",
        "repo_evidence": "All proof packets in reports/ include not_proven and claim_boundary.",
        "validator_evidence": "validate-all, validate-boundary-matrix pass.",
        "release_gate": "No boundary incoherence detected in current PR09/PR10 release artifacts.",
        "not_proven": ["live_model_inference", "production_readiness", "security_certification"],
        "claim_boundary": "q7_boundary_coherence_scanner_not_agent_authority",
    },
    {
        "internal_term": "ring_drift",
        "neutral_release_term": "authority_layer_confusion",
        "drift_detected": "ring_authority_violation",
        "description": "Occurs when a lower authority ring acts as if it holds higher ring authority.",
        "repo_evidence": "Ring 0 (host app) owns apply. Odin Rings 1-7 are candidate-only.",
        "validator_evidence": "validate-ring-authority-map passes.",
        "release_gate": "Ring authority map validates clean separation. Ring 0 owns apply.",
        "not_proven": ["ring_authority_externally_certified"],
        "claim_boundary": "ring_drift_scanner_not_authority_grant",
    },
    {
        "internal_term": "projection_truth_drift",
        "neutral_release_term": "model_output_treated_as_verified_truth",
        "drift_detected": "model_projection_truth_violation",
        "description": "Occurs when model output is treated as ground truth without critic/final gate receipt.",
        "repo_evidence": "odin/operational_spine/ — ModelWorkPacket includes model_projection_is_not_truth: true.",
        "validator_evidence": "validate-modelworkpacket-enforcement, validate-small-model-route-plan pass.",
        "release_gate": "Model projection not truth enforced in ModelWorkPacket and final gate.",
        "not_proven": ["live_model_inference", "real_model_benchmark"],
        "claim_boundary": "projection_truth_drift_scanner_not_benchmark",
    },
    {
        "internal_term": "apply_drift",
        "neutral_release_term": "odin_tries_to_mutate_app_state",
        "drift_detected": "app_state_mutation_by_odin",
        "description": "Occurs when Odin attempts to directly mutate app state without host app authorization.",
        "repo_evidence": "No app state mutation paths in odin/operational_spine/ or odin/release_boundaries/.",
        "validator_evidence": "validate-operational-spine, validate-boundary-matrix pass.",
        "release_gate": "No app state mutation detected. app_owned_apply: true enforced.",
        "not_proven": ["app_state_mutation_prevention_formally_verified"],
        "claim_boundary": "apply_drift_scanner_not_apply_authority",
    },
    {
        "internal_term": "send_drift",
        "neutral_release_term": "odin_tries_external_send",
        "drift_detected": "unauthorized_external_send",
        "description": "Occurs when Odin attempts external send without explicit host app receipt.",
        "repo_evidence": "odin/operational_spine/provider_seam.py — external disabled by default.",
        "validator_evidence": "validate-operational-spine, validate-deferred-system-lift pass.",
        "release_gate": "No external send paths active. Local-only default enforced.",
        "not_proven": ["external_send_formally_blocked"],
        "claim_boundary": "send_drift_scanner_not_send_authority",
    },
    {
        "internal_term": "provider_drift",
        "neutral_release_term": "provider_treated_as_authority",
        "drift_detected": "provider_authority_violation",
        "description": "Occurs when provider output is treated as authoritative without final gate.",
        "repo_evidence": "odin/operational_spine/provider_seam.py — provider_execution: false. Provider is not authority.",
        "validator_evidence": "validate-operational-spine, validate-modelworkpacket-enforcement pass.",
        "release_gate": "Provider not authority enforced. Provider seam disabled by default.",
        "not_proven": ["provider_execution", "provider_authority"],
        "claim_boundary": "provider_drift_scanner_not_provider_authority",
    },
    {
        "internal_term": "qirc_drift",
        "neutral_release_term": "qirc_treated_as_app_authority",
        "drift_detected": "qirc_authority_violation",
        "description": "Occurs when QIRC bus events are treated as app authority or cause app state mutation.",
        "repo_evidence": "odin/qirc_core/ — local_only: true; no app state mutation paths.",
        "validator_evidence": "validate-all, validate-boundary-matrix pass.",
        "release_gate": "QIRC not app authority enforced. Local-only QIRC bus confirmed.",
        "not_proven": ["qirc_authority_formally_verified"],
        "claim_boundary": "qirc_drift_scanner_not_qirc_authority",
    },
    {
        "internal_term": "artifact_drift",
        "neutral_release_term": "historical_target_docs_treated_as_current_proof",
        "drift_detected": "artifact_currency_violation",
        "description": "Occurs when historical or target-only documents are cited as proof of current runtime behavior.",
        "repo_evidence": "Artifact currency index classifies docs as current_runtime, historical_supporting, or target_only.",
        "validator_evidence": "validate-artifact-currency, validate-pre-release-super-audit pass.",
        "release_gate": "Artifact currency classification enforced. Historical/target docs not current proof.",
        "not_proven": ["artifact_currency_externally_audited"],
        "claim_boundary": "artifact_drift_scanner_not_currency_certifier",
    },
    {
        "internal_term": "claim_drift",
        "neutral_release_term": "claim_made_without_scoped_receipt",
        "drift_detected": "unsupported_release_claim",
        "description": "Occurs when a claim is made without a scoped receipt from the system asserting it.",
        "repo_evidence": "All PR09/PR10 proof packets include not_proven and claim_boundary.",
        "validator_evidence": "validate-all, validate-boundary-matrix, validate-final-release-preflight pass.",
        "release_gate": "Receipt before claim enforced. All overclaims blocked by boundary matrix.",
        "not_proven": ["claim_governance_externally_audited"],
        "claim_boundary": "claim_drift_scanner_not_claim_certifier",
    },
]


def build_bug6_q7_operational_map() -> dict:
    """Build the Bug6/Q7 operational map in neutral Odin release language.

    Bug6 = authority drift scanner. Q7 = boundary coherence scanner.
    These are release-boundary lenses only — not independent agents.
    """
    rows = {}
    for row in _DRIFT_MAP:
        key = row["internal_term"]
        rows[key] = dict(row, drift_map_id=_make_id(key))

    return json.loads(json.dumps({
        "artifact_kind": "odin_final_pr_10_bug6_q7_operational_map",
        "candidate_only": True,
        "app_owned_apply": True,
        "claim_boundary": _CLAIM_BOUNDARY,
        "generated_at_utc": _GENERATED_AT,
        "scanner_definitions": {
            "Bug6": "authority_drift_scanner — scans for Odin subsystems acquiring forbidden authority.",
            "Q7": "boundary_coherence_scanner — scans for inconsistent claim boundaries and missing not_proven lists.",
        },
        "axioms": [
            "Bug6 and Q7 are release-boundary lenses only.",
            "They do not create independent agent authority.",
            "They do not have runtime execution authority.",
            "Public wording uses neutral Odin terms.",
        ],
        "drift_count": len(rows),
        "drift_map": rows,
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
