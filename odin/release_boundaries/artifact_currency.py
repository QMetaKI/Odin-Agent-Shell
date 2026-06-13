"""Artifact Currency Index — FINAL-PR-10++.

Claim boundary: final_pr_10_boundary_gated_release_operationalization_not_release_certification
candidate_only: true
app_owned_apply: true

Classifies artifacts by their currency for release claims.
Historical and target-only docs may not prove current runtime behavior.
External receipt required items cannot be claimed locally.
"""
from __future__ import annotations

import hashlib
import json

_CLAIM_BOUNDARY = "final_pr_10_boundary_gated_release_operationalization_not_release_certification"
_GENERATED_AT = "2026-01-01T00:00:00Z"


def _make_id(path: str) -> str:
    digest = hashlib.sha256(f"artifact_currency_{path}".encode()).hexdigest()[:16]
    return f"artifact_currency_{digest}"


_ARTIFACTS = [
    {
        "path": "README.md",
        "currency_class": "current_supporting",
        "reason": "Current project overview. Not a runtime proof.",
        "allowed_release_use": "project_description, entrypoint_reference",
        "forbidden_release_use": "runtime_proof, live_model_proof, security_certification",
    },
    {
        "path": "START_HERE.md",
        "currency_class": "current_supporting",
        "reason": "Current entry guide. Not a runtime proof.",
        "allowed_release_use": "developer_onboarding, navigation",
        "forbidden_release_use": "runtime_proof, security_certification",
    },
    {
        "path": "CANON_ENTRY.md",
        "currency_class": "current_supporting",
        "reason": "Current canonical entry point. Not a runtime proof.",
        "allowed_release_use": "canonical_navigation, lineage_reference",
        "forbidden_release_use": "runtime_proof, security_certification",
    },
    {
        "path": "SYSTEM_MAP.json",
        "currency_class": "current_runtime",
        "reason": "Current system structure map. Reflects actual repo state after each PR.",
        "allowed_release_use": "system_structure_reference, file_existence_check",
        "forbidden_release_use": "live_model_proof, security_certification, production_readiness",
    },
    {
        "path": "FILE_MANIFEST.json",
        "currency_class": "current_runtime",
        "reason": "Current file manifest. Reflects actual repo files after each PR.",
        "allowed_release_use": "file_existence_check, manifest_validation",
        "forbidden_release_use": "live_model_proof, security_certification, production_readiness",
    },
    {
        "path": "docs/MASTER_ARCHITECTURE_V7_1_1.md",
        "currency_class": "current_supporting",
        "reason": "Current architecture document. Not a runtime proof.",
        "allowed_release_use": "architecture_reference, design_lineage",
        "forbidden_release_use": "runtime_proof, live_model_proof",
    },
    {
        "path": "docs/V7_1_1_OPERATIONAL_TARGET_SYNTHESIS.md",
        "currency_class": "target_only",
        "reason": "Operational target synthesis — describes intended future state, not current implementation.",
        "allowed_release_use": "target_reference, roadmap_lineage",
        "forbidden_release_use": "current_runtime_proof, implemented_feature_claim",
    },
    {
        "path": "docs/codex/audits/pre_release_super_audit/00_EXECUTIVE_BRIEF.md",
        "currency_class": "current_release_evidence",
        "reason": "PR48 pre-release super audit executive brief — current release evidence for its audit scope.",
        "allowed_release_use": "audit_lineage, release_evidence_reference",
        "forbidden_release_use": "production_readiness_proof, security_certification",
    },
    {
        "path": "docs/rebaseline/FINAL_PR_09_OPERATIONAL_SPINE.md",
        "currency_class": "current_release_evidence",
        "reason": "FINAL-PR-09++ operational spine rebaseline doc — current evidence for PR09 scope.",
        "allowed_release_use": "pr09_evidence_reference, operational_spine_lineage",
        "forbidden_release_use": "live_model_proof, production_readiness_proof",
    },
    {
        "path": "docs/release/FINAL_PR_09_OPERATIONAL_SPINE_EVIDENCE_INDEX.md",
        "currency_class": "current_release_evidence",
        "reason": "FINAL-PR-09++ evidence index — current evidence for PR09 operational spine scope.",
        "allowed_release_use": "pr09_evidence_index_reference",
        "forbidden_release_use": "live_model_proof, production_readiness_proof, security_certification",
    },
    {
        "path": "docs/release/FINAL_PR_09_SMALL_MODEL_POWER_MAP.md",
        "currency_class": "current_release_evidence",
        "reason": "FINAL-PR-09++ small model power map — current route plan evidence, not quality benchmark.",
        "allowed_release_use": "small_model_route_reference",
        "forbidden_release_use": "real_model_benchmark, live_model_inference_proof",
    },
    {
        "path": "docs/release/FINAL_PR_09_QSHABANG_OPERATIONAL_MAP.md",
        "currency_class": "current_release_evidence",
        "reason": "FINAL-PR-09++ Q-Shabang operational map — current neutral mechanics evidence.",
        "allowed_release_use": "qshabang_map_reference, neutral_mechanics_evidence",
        "forbidden_release_use": "qshabang_as_authority, live_model_proof",
    },
    {
        "path": "odin/operational_spine/",
        "currency_class": "current_runtime",
        "reason": "FINAL-PR-09++ operational spine module — current candidate-only runtime implementation.",
        "allowed_release_use": "operational_spine_evidence, candidate_only_runtime_reference",
        "forbidden_release_use": "live_model_proof, production_readiness_proof, security_certification",
    },
    {
        "path": "reports/final_pr_09_operational_spine_report.json",
        "currency_class": "current_release_evidence",
        "reason": "FINAL-PR-09++ operational spine validator report — current evidence of PR09 scope.",
        "allowed_release_use": "pr09_validator_evidence",
        "forbidden_release_use": "live_model_proof, production_readiness_proof",
    },
    {
        "path": "reports/final_pr_09_operational_spine_proof_packet.json",
        "currency_class": "current_release_evidence",
        "reason": "FINAL-PR-09++ proof packet — current scoped proof for PR09 claims.",
        "allowed_release_use": "pr09_proof_reference",
        "forbidden_release_use": "live_model_proof, production_readiness_proof, security_certification",
    },
    {
        "path": "docs/codex/audits/pre_release_super_audit/",
        "currency_class": "current_release_evidence",
        "reason": "PR48 pre-release super audit — current release evidence for PR48 audit scope.",
        "allowed_release_use": "audit_evidence_reference",
        "forbidden_release_use": "production_readiness_proof, security_certification",
    },
    {
        "path": "registries/v7_1_1_operational_target_registry.json",
        "currency_class": "target_only",
        "reason": "V7.1.1 operational target registry — targets, not confirmed implementations.",
        "allowed_release_use": "target_reference, roadmap_lineage",
        "forbidden_release_use": "implemented_feature_claim, runtime_proof",
    },
    {
        "path": "docs/MASTER_ARCHITECTURE_V7_1.md",
        "currency_class": "historical_supporting",
        "reason": "V7.1 architecture — historical lineage document. Superseded by V7.1.1.",
        "allowed_release_use": "architecture_lineage_reference",
        "forbidden_release_use": "current_runtime_proof, implemented_feature_claim",
    },
    {
        "path": "odin/release_boundaries/",
        "currency_class": "current_runtime",
        "reason": "FINAL-PR-10++ release boundaries module — current candidate-only boundary maps.",
        "allowed_release_use": "release_boundary_evidence, candidate_only_boundary_reference",
        "forbidden_release_use": "production_readiness_proof, security_certification, release_certification",
    },
    {
        "path": "reports/final_pr_10_release_preflight_report.json",
        "currency_class": "current_release_evidence",
        "reason": "FINAL-PR-10++ release preflight report — current evidence of PR10 release gates.",
        "allowed_release_use": "pr10_preflight_evidence",
        "forbidden_release_use": "production_readiness_proof, security_certification, release_certification",
    },
]

_CURRENCY_CLASSES = [
    "current_runtime",
    "current_release_evidence",
    "current_supporting",
    "historical_supporting",
    "superseded",
    "target_only",
    "external_receipt_required",
]


def build_artifact_currency_index() -> dict:
    """Build the artifact currency index.

    Classifies artifacts by their currency for release claims.
    Historical and target-only docs may not prove current runtime behavior.
    """
    artifacts = {}
    for artifact in _ARTIFACTS:
        path = artifact["path"]
        artifacts[path] = dict(
            artifact,
            artifact_id=_make_id(path),
            candidate_only=True,
            claim_boundary=_CLAIM_BOUNDARY,
        )

    return json.loads(json.dumps({
        "artifact_kind": "odin_final_pr_10_artifact_currency_index",
        "candidate_only": True,
        "app_owned_apply": True,
        "claim_boundary": _CLAIM_BOUNDARY,
        "generated_at_utc": _GENERATED_AT,
        "currency_classes": _CURRENCY_CLASSES,
        "axioms": [
            "Historical docs may support lineage but may not prove current runtime.",
            "Target docs may not prove implementation.",
            "External receipt required items cannot be claimed locally.",
            "current_runtime class indicates active, committed, tested implementation.",
        ],
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
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
