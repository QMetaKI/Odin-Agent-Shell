"""v7.1.1 Target Loader — loads v7.1.1 target canon.

Claim boundary: v711_coverage_compiler_maps_target_to_repo_evidence_not_runtime_completion
candidate_only: true
"""
from __future__ import annotations

_TARGETS = [
    {
        "target_id": "small_model_power",
        "target_name": "Small Model Power",
        "target_priority": "high",
        "target_source": "v711_master_arch",
    },
    {
        "target_id": "universal_work",
        "target_name": "Universal Work",
        "target_priority": "high",
        "target_source": "v711_master_arch",
    },
    {
        "target_id": "app_boundary",
        "target_name": "App Boundary",
        "target_priority": "high",
        "target_source": "v711_master_arch",
    },
    {
        "target_id": "context_distillery",
        "target_name": "Context Distillery",
        "target_priority": "high",
        "target_source": "v711_master_arch",
    },
    {
        "target_id": "artifact_lenses",
        "target_name": "Artifact Lenses",
        "target_priority": "medium",
        "target_source": "v711_master_arch",
    },
    {
        "target_id": "worklet_graph",
        "target_name": "Worklet Graph",
        "target_priority": "medium",
        "target_source": "v711_master_arch",
    },
    {
        "target_id": "slot_forge",
        "target_name": "Slot Forge",
        "target_priority": "medium",
        "target_source": "v711_master_arch",
    },
    {
        "target_id": "gaptext_compiler",
        "target_name": "Gaptext Compiler",
        "target_priority": "medium",
        "target_source": "v711_master_arch",
    },
    {
        "target_id": "modelworkpacket",
        "target_name": "ModelWorkPacket",
        "target_priority": "high",
        "target_source": "v711_master_arch",
    },
    {
        "target_id": "hybrid_director",
        "target_name": "Hybrid Director",
        "target_priority": "medium",
        "target_source": "v711_master_arch",
    },
    {
        "target_id": "provider_runtime",
        "target_name": "Provider Runtime",
        "target_priority": "high",
        "target_source": "v711_operational_target",
    },
    {
        "target_id": "critic_cascade",
        "target_name": "Critic Cascade",
        "target_priority": "high",
        "target_source": "v711_master_arch",
    },
    {
        "target_id": "candidate_tournament",
        "target_name": "Candidate Tournament",
        "target_priority": "medium",
        "target_source": "v711_master_arch",
    },
    {
        "target_id": "candidate_dna",
        "target_name": "Candidate DNA",
        "target_priority": "medium",
        "target_source": "v711_master_arch",
    },
    {
        "target_id": "response_packet",
        "target_name": "Response Packet",
        "target_priority": "high",
        "target_source": "v711_master_arch",
    },
    {
        "target_id": "final_gate",
        "target_name": "Final Gate",
        "target_priority": "high",
        "target_source": "v711_master_arch",
    },
    {
        "target_id": "semantic_bus",
        "target_name": "Semantic Bus",
        "target_priority": "high",
        "target_source": "v711_master_arch",
    },
    {
        "target_id": "trace_receipt_proof",
        "target_name": "Trace / Receipt / Proof",
        "target_priority": "high",
        "target_source": "v711_master_arch",
    },
    {
        "target_id": "artifact_currency",
        "target_name": "Artifact Currency",
        "target_priority": "medium",
        "target_source": "v711_road_to_100",
    },
    {
        "target_id": "release_boundary_gates",
        "target_name": "Release Boundary Gates",
        "target_priority": "high",
        "target_source": "v711_road_to_100",
    },
    {
        "target_id": "local_provider_receipts",
        "target_name": "Local Provider Receipts",
        "target_priority": "high",
        "target_source": "v711_operational_target",
    },
    {
        "target_id": "route_evaluation_receipts",
        "target_name": "Route Evaluation Receipts",
        "target_priority": "high",
        "target_source": "v711_operational_target",
    },
    {
        "target_id": "thor_handoff_compiler",
        "target_name": "Thor Handoff Compiler",
        "target_priority": "high",
        "target_source": "v711_operational_target",
    },
    {
        "target_id": "claims_compiler",
        "target_name": "Claims Compiler",
        "target_priority": "medium",
        "target_source": "v711_road_to_100",
    },
    {
        "target_id": "sdk_api_app_bridge",
        "target_name": "SDK / API / App Bridge",
        "target_priority": "high",
        "target_source": "v711_operational_target",
    },
    {
        "target_id": "y_pattern_operationalization",
        "target_name": "Y Pattern Operationalization",
        "target_priority": "medium",
        "target_source": "v711_road_to_100",
    },
]


def load_v711_targets(*, repo_root: str = ".") -> dict:
    """Load v7.1.1 target canon. Returns dict keyed by target_id."""
    return {t["target_id"]: t for t in _TARGETS}
