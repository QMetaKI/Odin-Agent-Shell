"""Proof chain registry — references to prior final PR proofs — FINAL-PR-05.

Claim boundary: final_pr_05_proof_chain_cross_reference_not_production_proof
candidate_only: true
local_only: true
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CLAIM_BOUNDARY = "final_pr_05_proof_chain_cross_reference_not_production_proof"

PROOF_CHAIN_REGISTRY = {
    "final_pr_01": {
        "pr_id": "FINAL-PR-01",
        "label": "Simple Local Hub",
        "report_path": "reports/final_pr_01_simple_local_hub_report.json",
        "candidate_only": True,
        "description": "Simple local hub with localhost-only HTTP server.",
    },
    "final_pr_02": {
        "pr_id": "FINAL-PR-02",
        "label": "Model / Apps / Demo",
        "report_path": "reports/final_pr_02_model_apps_demo_report.json",
        "candidate_only": True,
        "description": "Model picker, connected apps, demo universal work.",
    },
    "final_pr_03": {
        "pr_id": "FINAL-PR-03",
        "label": "QIRC Core / Dev Mode",
        "report_path": "reports/final_pr_03_qirc_devmode_report.json",
        "proof_path": "reports/final_pr_03_qirc_devmode_proof_packet.json",
        "candidate_only": True,
        "description": "QIRC event bus, dev mode, trace/receipt viewers.",
    },
    "final_pr_04": {
        "pr_id": "FINAL-PR-04",
        "label": "Provider Probe + Security Smoke",
        "report_path": "reports/final_pr_04_provider_probe_security_report.json",
        "proof_path": "reports/final_pr_04_provider_probe_security_proof_packet.json",
        "candidate_only": True,
        "description": "Provider probe, runtime security smoke, provider policy.",
    },
    "final_pr_05": {
        "pr_id": "FINAL-PR-05",
        "label": "Execution Gate + Ladder Scaffold",
        "report_path": "reports/final_pr_05_execution_gate_report.json",
        "proof_path": "reports/final_pr_05_execution_gate_proof_packet.json",
        "candidate_only": True,
        "description": "Execution gate, mock execution, local candidate policy, proof chain, ladder scaffold.",
    },
}


def get_proof_entry(pr_key: str) -> dict | None:
    return PROOF_CHAIN_REGISTRY.get(pr_key)


def list_proof_entries() -> list[dict]:
    return list(PROOF_CHAIN_REGISTRY.values())


def check_report_exists(pr_key: str) -> dict:
    entry = PROOF_CHAIN_REGISTRY.get(pr_key, {})
    report_path = entry.get("report_path")
    proof_path = entry.get("proof_path")
    report_exists = (ROOT / report_path).exists() if report_path else False
    proof_exists = (ROOT / proof_path).exists() if proof_path else None
    return {
        "pr_id": entry.get("pr_id", pr_key),
        "report_path": report_path,
        "report_exists": report_exists,
        "proof_path": proof_path,
        "proof_exists": proof_exists,
    }
