"""Documentation Readiness — Doc Index.

Claim boundary: docs_readiness_prepares_user_docs_not_release_certification
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "docs_readiness_prepares_user_docs_not_release_certification"

_DOCS = [
    {
        "category": "operator_start",
        "doc_path": "README.md",
        "status": "exists",
        "description": "Primary entry point for operators and developers",
        "needs_update": False,
        "update_priority": "low",
    },
    {
        "category": "operator_start",
        "doc_path": "START_HERE.md",
        "status": "exists_if_present",
        "description": "Quick-start guide for new operators",
        "needs_update": False,
        "update_priority": "low",
    },
    {
        "category": "developer_start",
        "doc_path": "AGENTS.md",
        "status": "exists",
        "description": "Agent operator development guide and boundary rules",
        "needs_update": False,
        "update_priority": "low",
    },
    {
        "category": "developer_start",
        "doc_path": "CLAUDE.md",
        "status": "exists",
        "description": "Claude Code project instructions and required reads",
        "needs_update": False,
        "update_priority": "low",
    },
    {
        "category": "claims_boundary",
        "doc_path": "CLAIM_BOUNDARY.md",
        "status": "exists",
        "description": "Claim boundary definitions for all modules",
        "needs_update": False,
        "update_priority": "low",
    },
    {
        "category": "local_provider_receipts",
        "doc_path": "docs/release/FINAL_PR_11_LOCAL_PROVIDER_RECEIPT_HARNESS.md",
        "status": "exists",
        "description": "Local provider receipt harness documentation",
        "needs_update": False,
        "update_priority": "low",
    },
    {
        "category": "semantic_kernel",
        "doc_path": "docs/release/FINAL_PR_11_5_SEMANTIC_KERNEL_CLOSURE.md",
        "status": "exists",
        "description": "Semantic kernel closure documentation from FINAL-PR-11.5",
        "needs_update": False,
        "update_priority": "low",
    },
    {
        "category": "release_readiness",
        "doc_path": "docs/release/FINAL_PR_12_RELEASE_READINESS_MATRIX.md",
        "status": "created_in_pr12",
        "description": "Release readiness matrix for FINAL-PR-12",
        "needs_update": False,
        "update_priority": "n_a",
    },
    {
        "category": "release_readiness",
        "doc_path": "docs/rebaseline/FINAL_PR_12_RELEASE_READINESS_HARDENING.md",
        "status": "created_in_pr12",
        "description": "FINAL-PR-12 rebaseline summary",
        "needs_update": False,
        "update_priority": "n_a",
    },
    {
        "category": "non_claims",
        "doc_path": "docs/codex/audits/FINAL_PR_12_SENIOR_REVIEW.md",
        "status": "created_in_pr12",
        "description": "Senior reviewer simulation for non-claims confirmation",
        "needs_update": False,
        "update_priority": "n_a",
    },
    {
        "category": "historical_evidence",
        "doc_path": "docs/codex/reports/FINAL_PR_11_5_SEMANTIC_KERNEL_COVERAGE_RETURN_REPORT.md",
        "status": "historical",
        "description": "FINAL-PR-11.5 return report (historical evidence)",
        "needs_update": False,
        "update_priority": "n_a",
    },
    {
        "category": "historical_evidence",
        "doc_path": "docs/rebaseline/FINAL_PR_11_5_SEMANTIC_KERNEL_COVERAGE.md",
        "status": "historical",
        "description": "FINAL-PR-11.5 rebaseline summary (historical evidence)",
        "needs_update": False,
        "update_priority": "n_a",
    },
]


def build_docs_readiness_index(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_docs_readiness_index",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "docs": _DOCS,
        "not_proven": ["user_documentation_complete", "release_certification", "production_readiness"],
    }
