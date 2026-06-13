"""v7.1.1 Evidence Mapper — maps targets to repo file evidence.

Claim boundary: v711_coverage_compiler_maps_target_to_repo_evidence_not_runtime_completion
candidate_only: true
"""
from __future__ import annotations

import os
from pathlib import Path

_TARGET_FILE_MAP: dict[str, list[str]] = {
    "small_model_power": [
        "odin/small_model_power/__init__.py",
    ],
    "universal_work": [
        "odin/universal_work/__init__.py",
    ],
    "app_boundary": [
        "odin/release_boundaries/__init__.py",
        "odin/execution_gate/__init__.py",
    ],
    "context_distillery": [
        "odin/worklets/__init__.py",
    ],
    "artifact_lenses": [
        "odin/worklets/__init__.py",
    ],
    "worklet_graph": [
        "odin/worklets/__init__.py",
    ],
    "slot_forge": [
        "odin/slots/__init__.py",
    ],
    "gaptext_compiler": [
        "odin/seeds/__init__.py",
    ],
    "modelworkpacket": [
        "odin/operational_spine/__init__.py",
    ],
    "hybrid_director": [
        "odin/operational_spine/__init__.py",
    ],
    "provider_runtime": [
        "odin/local_provider_receipts/__init__.py",
    ],
    "critic_cascade": [
        "odin/critic_runtime/__init__.py",
        "odin/critic_runtime/cascade.py",
    ],
    "candidate_tournament": [
        "odin/critic_runtime/__init__.py",
    ],
    "candidate_dna": [
        "odin/packets/__init__.py",
    ],
    "response_packet": [
        "odin/packets/__init__.py",
    ],
    "final_gate": [
        "odin/execution_gate/__init__.py",
    ],
    "semantic_bus": [
        "odin/semantic_bus/__init__.py",
    ],
    "trace_receipt_proof": [
        "odin/proof_chain/__init__.py",
    ],
    "artifact_currency": [
        "odin/release_boundaries/__init__.py",
    ],
    "release_boundary_gates": [
        "odin/release_boundaries/__init__.py",
    ],
    "local_provider_receipts": [
        "odin/local_provider_receipts/__init__.py",
        "odin/local_provider_receipts/receipt.py",
        "odin/local_provider_receipts/reports.py",
    ],
    "route_evaluation_receipts": [
        "odin/route_evaluation/__init__.py",
        "odin/route_evaluation/receipt.py",
    ],
    "thor_handoff_compiler": [
        "odin/thor_handoff_compiler/__init__.py",
        "odin/thor_handoff_compiler/compiler.py",
    ],
    "claims_compiler": [
        "odin/claims_compiler/__init__.py",
        "odin/claims_compiler/compiler.py",
    ],
    "sdk_api_app_bridge": [
        "odin_app_sdk/__init__.py",
    ],
    "y_pattern_operationalization": [
        "odin/y_pattern_operationalization_index/__init__.py",
        "odin/y_pattern_operationalization_index/index_builder.py",
    ],
}


def map_targets_to_repo_evidence(
    targets: dict,
    *,
    repo_root: str = ".",
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Map each target to repo file evidence. Returns dict with evidence_map."""
    root = Path(repo_root)
    evidence_map: dict[str, dict] = {}
    for target_id, target in targets.items():
        candidate_files = _TARGET_FILE_MAP.get(target_id, [])
        found = [f for f in candidate_files if (root / f).exists()]
        evidence_map[target_id] = {
            "target_id": target_id,
            "target_name": target["target_name"],
            "repo_evidence": found,
            "candidate_files_checked": candidate_files,
            "files_found": len(found),
            "files_missing": len(candidate_files) - len(found),
            "generated_at_utc": generated_at_utc,
        }
    return {
        "artifact_kind": "odin_v711_evidence_map",
        "candidate_only": True,
        "claim_boundary": "v711_coverage_compiler_maps_target_to_repo_evidence_not_runtime_completion",
        "generated_at_utc": generated_at_utc,
        "evidence_map": evidence_map,
    }
