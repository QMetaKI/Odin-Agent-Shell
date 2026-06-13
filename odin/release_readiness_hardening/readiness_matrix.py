"""Release Readiness Hardening — Readiness Matrix.

Claim boundary: release_readiness_hardening_prepares_release_closure_not_certification
candidate_only: true
app_owned_apply: true

This module builds the release readiness matrix for FINAL-PR-12.
It does NOT certify production readiness, security, or release closure.
It does NOT execute models, apply app state, or send externally.
"""
from __future__ import annotations

CLAIM_BOUNDARY = "release_readiness_hardening_prepares_release_closure_not_certification"

NOT_PROVEN = [
    "production_readiness",
    "security_certification",
    "release_certification",
    "general_live_model_inference",
    "real_model_benchmark",
    "model_superiority",
    "app_apply",
    "external_send",
    "public_network",
    "final_pr_13_release_closure",
]

_ROWS = [
    {
        "category": "candidate_only_release_wording",
        "description": (
            "All Odin outputs are candidates only. Release wording confirms candidate_only: true "
            "in all spine, packet, and proof outputs. App owns apply decision."
        ),
        "readiness_status": "ready_structural",
        "evidence_refs": [
            "odin/operational_spine/orchestrator.py — candidate_only: true",
            "odin/packets/ — candidate_only in all packet types",
            "odin/proof_chain/ — not_proven lists in all proof packets",
            "validate-operational-spine passes",
        ],
        "notes": "Structural evidence confirmed across codebase. No receipt required beyond repo.",
    },
    {
        "category": "app_owned_apply_wording",
        "description": (
            "App-owned apply boundary is wired throughout the operational spine. "
            "Odin never applies state; the host app owns all apply decisions."
        ),
        "readiness_status": "ready_structural",
        "evidence_refs": [
            "odin/operational_spine/ — app_owned_apply: true in all work packets",
            "odin/release_boundaries/boundary_matrix.py — app_owned_apply boundary row",
            "validate-operational-spine passes",
        ],
        "notes": "Structural evidence confirmed. Wording ready for FINAL-PR-13.",
    },
    {
        "category": "local_provider_receipt_wording",
        "description": (
            "Local provider execution is disabled by default. When enabled by the host, "
            "receipts are host-scoped. Wording reflects host-scoped, not WAN/LAN claim."
        ),
        "readiness_status": "ready_host_scoped",
        "evidence_refs": [
            "odin/local_provider_receipts/ — host-scoped receipt harness",
            "odin/operational_spine/provider_seam.py — disabled_by_default: true",
            "validate-deferred-system-lift passes",
        ],
        "notes": "Host-scoped receipt path exists. Receipt is host-scoped only, not general inference claim.",
    },
    {
        "category": "host_scoped_receipt_boundary",
        "description": (
            "Receipt boundary correctly separates structural evidence (repo-provable) from "
            "host-scoped receipts (runtime, local-only) and external receipts (not available)."
        ),
        "readiness_status": "ready_structural",
        "evidence_refs": [
            "odin/local_provider_receipts/ — host_scoped: true",
            "odin/proof_chain/ — receipt classification",
            "odin/release_boundaries/evidence_closure.py",
        ],
        "notes": "Classification boundary is structurally defined.",
    },
    {
        "category": "claim_compiler_policy",
        "description": (
            "Claims compiler policy separates structural claims, host-scoped claims, "
            "external-receipt-required claims, and forbidden claims."
        ),
        "readiness_status": "ready_structural",
        "evidence_refs": [
            "odin/claims_compiler/ — claim policy module",
            "odin/release_boundaries/boundary_matrix.py — boundary rows",
            "validate-all passes",
        ],
        "notes": "Policy is structurally defined. No runtime certification required.",
    },
    {
        "category": "semantic_kernel_coverage",
        "description": (
            "Semantic kernel IR objects are defined and validated. "
            "Coverage closure confirmed by validate-final-pr-11-5-semantic-kernel-coverage."
        ),
        "readiness_status": "ready_structural",
        "evidence_refs": [
            "odin/semantic_kernel_closure/ — IR, pipeline, contracts, receipts",
            "validate-final-pr-11-5-semantic-kernel-coverage passes",
            "validate-all passes",
        ],
        "notes": "Semantic kernel coverage closed in FINAL-PR-11.5.",
    },
    {
        "category": "v711_coverage_closure",
        "description": (
            "V711 coverage compiler maps all v7.1.1 spec items to repo evidence. "
            "Coverage closure confirmed."
        ),
        "readiness_status": "ready_structural",
        "evidence_refs": [
            "odin/v711_coverage_compiler/ — coverage compiler",
            "validate-all passes",
        ],
        "notes": "V711 coverage closed in prior PRs.",
    },
    {
        "category": "agent_operator_modes",
        "description": (
            "Agent operator modes are defined and validated. "
            "Handoff compiler, profiles, guards, and return reports all present."
        ),
        "readiness_status": "ready_structural",
        "evidence_refs": [
            "odin/agent_operator/ — modes, packets, guards, proofs, returns",
            "odin/agent_operator_modes/ — mode definitions",
            "validate-agent-operator-mode passes",
        ],
        "notes": "Agent operator mode infrastructure closed in prior PRs.",
    },
    {
        "category": "command_surface_closure",
        "description": (
            "CLI command surface index, alias policy, and coverage are being built in FINAL-PR-12 "
            "as preparatory work. Full closure deferred to FINAL-PR-13."
        ),
        "readiness_status": "deferred_to_final_pr_13",
        "evidence_refs": [
            "odin/command_surface_closure/ — FINAL-PR-12 prep modules",
            "validate-command-surface-closure (FINAL-PR-12)",
        ],
        "notes": "Inventory and index built in FINAL-PR-12. Final closure in FINAL-PR-13.",
    },
    {
        "category": "docs_readiness",
        "description": (
            "Docs readiness index and update plans are being built in FINAL-PR-12. "
            "Full docs closure deferred to FINAL-PR-13."
        ),
        "readiness_status": "deferred_to_final_pr_13",
        "evidence_refs": [
            "odin/docs_readiness/ — FINAL-PR-12 prep modules",
            "validate-docs-readiness (FINAL-PR-12)",
        ],
        "notes": "Plans prepared in FINAL-PR-12. Actual doc updates in FINAL-PR-13.",
    },
    {
        "category": "packaging_boundary",
        "description": (
            "Packaging boundary inventory and manifest plan are being built in FINAL-PR-12. "
            "Actual packaging deferred to FINAL-PR-13."
        ),
        "readiness_status": "deferred_to_final_pr_13",
        "evidence_refs": [
            "odin/packaging_boundary_prep/ — FINAL-PR-12 prep modules",
            "validate-packaging-boundary-prep (FINAL-PR-12)",
        ],
        "notes": "Inventory only. No signed package, no installer, no distribution claim.",
    },
    {
        "category": "security_certification_boundary",
        "description": (
            "Security certification is explicitly not claimed. No external audit receipt exists. "
            "All proof packets list security_certification in not_proven."
        ),
        "readiness_status": "external_receipt_required",
        "evidence_refs": [
            "odin/release_boundaries/boundary_matrix.py — no_security_certification_without_receipt row",
            "All proof packets — security_certification in not_proven",
        ],
        "notes": "External security audit required for any security certification claim. Not available.",
    },
    {
        "category": "production_readiness_boundary",
        "description": (
            "Production readiness is explicitly not claimed. No external production validation receipt exists. "
            "All proof packets list production_readiness in not_proven."
        ),
        "readiness_status": "external_receipt_required",
        "evidence_refs": [
            "odin/release_boundaries/boundary_matrix.py — no_production_ready_claim_without_receipt row",
            "All proof packets — production_readiness in not_proven",
        ],
        "notes": "External production validation required. Not available in FINAL-PR-12.",
    },
    {
        "category": "release_certification_boundary",
        "description": (
            "Release certification is explicitly deferred to FINAL-PR-13. "
            "No release certification artifacts exist in FINAL-PR-12."
        ),
        "readiness_status": "external_receipt_required",
        "evidence_refs": [
            "All FINAL-PR-12 proof packets — release_certification in not_proven",
            "final_pr_13_remains_deferred: true in all FINAL-PR-12 artifacts",
        ],
        "notes": "FINAL-PR-13 performs release closure. FINAL-PR-12 prepares inputs only.",
    },
    {
        "category": "model_performance_boundary",
        "description": (
            "Model performance benchmarks are not claimed. No empirical model receipt exists. "
            "Route plans describe structure, not measured performance."
        ),
        "readiness_status": "external_receipt_required",
        "evidence_refs": [
            "odin/operational_spine/small_model_route_plan.py — route plan, not benchmark",
            "All proof packets — real_model_benchmark in not_proven",
        ],
        "notes": "Empirical model benchmark receipt required. Not available.",
    },
]


def build_release_readiness_matrix(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build the release readiness matrix for FINAL-PR-12.

    Returns a structured dict describing the readiness of each release category.
    This is not release certification. FINAL-PR-13 remains deferred.
    """
    return {
        "artifact_kind": "odin_release_readiness_hardening_matrix",
        "candidate_only": True,
        "app_owned_apply": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "rows": _ROWS,
        "not_proven": NOT_PROVEN,
    }
