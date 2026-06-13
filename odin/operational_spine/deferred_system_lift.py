"""Deferred System Lift plan for FINAL-PR-09 Operational Spine.

Claim boundary: final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply
candidate_only: true

Classifies deferred systems by their current implementation status.
No model execution, no provider calls, no app state mutations.
"""
from __future__ import annotations

CLAIM_BOUNDARY = "final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply"

_NOT_PROVEN = [
    "production_readiness",
    "live_model_inference",
    "app_state_mutation",
    "external_send_authority",
    "system_completeness",
]

# Status values:
#   already_repo_real            - fully present in repo
#   minimal_runtime_hook_in_pr09 - minimal hook wired in this PR
#   schema_and_packet_only_in_pr09 - schema defined, no runtime execution
#   future_pr_required           - not implemented, future PR needed
#   external_receipt_required    - requires external receipt/execution authority

_SYSTEMS = [
    {
        "name": "Context Distillery",
        "status": "future_pr_required",
        "purpose": "Distill work context into dense capsules for model consumption.",
        "small_model_relevance": "high — reduces context window load for 3B/7B models",
        "qshabang_relevance": "ki_ohne_ki, resonance_fit",
        "current_repo_evidence": "odin/projection_candidate_spine/ (partial context capsule shape)",
        "pr09_action": "schema shape referenced in context_capsule field of orchestrator",
        "future_action": "Implement full distillation pipeline in future PR",
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    },
    {
        "name": "Artifact Lenses",
        "status": "schema_and_packet_only_in_pr09",
        "purpose": "Structured views/transforms on candidate artifacts for downstream roles.",
        "small_model_relevance": "medium — shapes artifact for 3B extractor and 7B composer",
        "qshabang_relevance": "candidate_reality, qooo_style_orchestration",
        "current_repo_evidence": "odin/projection_candidate_spine/candidate_graph.py, odin/operational_spine/modelworkpacket_builder.py (artifact_lens field)",
        "pr09_action": "artifact_lens dict field defined and threaded through orchestrator",
        "future_action": "Implement lens transform functions in future PR",
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    },
    {
        "name": "Slot Forge",
        "status": "schema_and_packet_only_in_pr09",
        "purpose": "Constructs and validates slot contracts for model work packets.",
        "small_model_relevance": "high — 3B slot_filler role depends on slot contracts",
        "qshabang_relevance": "ki_ohne_ki, candidate_reality",
        "current_repo_evidence": "odin/slots/, odin/operational_spine/model_roles.py (slot_preparation role)",
        "pr09_action": "slot_contract dict field defined and threaded through orchestrator",
        "future_action": "Implement full slot forge in future PR",
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    },
    {
        "name": "Gaptext Compiler",
        "status": "schema_and_packet_only_in_pr09",
        "purpose": "Compiles gap analysis into gaptext for model work packets.",
        "small_model_relevance": "medium — 7B writer and hybrid roles use gaptext",
        "qshabang_relevance": "narrative_compiler, candidate_reality",
        "current_repo_evidence": "odin/operational_spine/model_roles.py (7b_writer allowed_inputs: gaptext)",
        "pr09_action": "gaptext dict field defined and threaded through orchestrator",
        "future_action": "Implement gaptext compilation pipeline in future PR",
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    },
    {
        "name": "Semantic Cache",
        "status": "future_pr_required",
        "purpose": "Cache semantic fingerprints of candidate results to avoid redundant model calls.",
        "small_model_relevance": "high — cache hit avoids 3B/7B model invocation entirely",
        "qshabang_relevance": "ki_ohne_ki, resonance_fit",
        "current_repo_evidence": "odin/operational_spine/model_roles.py (cache_fingerprint_lookup no-model role)",
        "pr09_action": "cache_fingerprint_lookup role defined in model_roles registry",
        "future_action": "Implement semantic cache storage and lookup in future PR",
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    },
    {
        "name": "Work Memory",
        "status": "future_pr_required",
        "purpose": "Short-term work context memory across multi-turn interactions.",
        "small_model_relevance": "medium — enables multi-turn coherence for 3B/7B",
        "qshabang_relevance": "seeds_pattern_mines, narrative_compiler",
        "current_repo_evidence": "odin/work_atoms/, odin/universal_work/",
        "pr09_action": "work_id threaded through all orchestrator packets",
        "future_action": "Implement work memory persistence in future PR",
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    },
    {
        "name": "Minicheck",
        "status": "future_pr_required",
        "purpose": "Lightweight fact-check and claim-boundary check on candidate outputs.",
        "small_model_relevance": "high — 3B quick_critic and boundary_check roles",
        "qshabang_relevance": "mirror_critics, q_gates",
        "current_repo_evidence": "odin/operational_spine/model_roles.py (3b_refusal_boundary_check role)",
        "pr09_action": "3b_refusal_boundary_check role defined; critic_plan field in route plan",
        "future_action": "Implement minicheck runtime in future PR",
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    },
    {
        "name": "Critic Cascade",
        "status": "minimal_runtime_hook_in_pr09",
        "purpose": "Multi-stage critic pipeline for candidate quality assurance.",
        "small_model_relevance": "high — 3B and 7B critic roles in cascade",
        "qshabang_relevance": "mirror_critics",
        "current_repo_evidence": "odin/operational_spine/model_roles.py (3b_quick_critic, 7b_complex_critic), critic_plan field in route plan and modelworkpacket",
        "pr09_action": "critic_plan field defined in SmallModelRoutePlan and ModelWorkPacket; roles registered",
        "future_action": "Implement full cascade execution in future PR",
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    },
    {
        "name": "Candidate Tournament",
        "status": "future_pr_required",
        "purpose": "Tournament-style selection among multiple candidate artifacts.",
        "small_model_relevance": "high — multiple 3B/7B candidates compete",
        "qshabang_relevance": "candidate_reality, mirror_critics",
        "current_repo_evidence": "odin/projection_candidate_spine/compare.py",
        "pr09_action": "projection_candidate_spine referenced in orchestrator",
        "future_action": "Implement candidate tournament runtime in future PR",
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    },
    {
        "name": "Style Stabilizer",
        "status": "future_pr_required",
        "purpose": "Stabilizes style consistency across candidate outputs.",
        "small_model_relevance": "medium — 3B style_check role",
        "qshabang_relevance": "qooo_style_orchestration",
        "current_repo_evidence": "odin/operational_spine/model_roles.py (3b_style_check role), odin/system_palette/",
        "pr09_action": "3b_style_check role defined in model_roles registry",
        "future_action": "Implement style stabilizer runtime in future PR",
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    },
    {
        "name": "Anti-Generic Engine",
        "status": "future_pr_required",
        "purpose": "Detects and penalizes generic, low-signal candidate outputs.",
        "small_model_relevance": "medium — post-generation quality gate",
        "qshabang_relevance": "mirror_critics, resonance_fit",
        "current_repo_evidence": "odin/quality/",
        "pr09_action": "quality module referenced; no direct hook in PR-09",
        "future_action": "Implement anti-generic scoring in future PR",
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    },
    {
        "name": "Taste Dials",
        "status": "future_pr_required",
        "purpose": "User/operator configurable taste parameters for candidate generation.",
        "small_model_relevance": "low-medium — style and quality targeting",
        "qshabang_relevance": "qooo_style_orchestration",
        "current_repo_evidence": "odin/system_palette/",
        "pr09_action": "quality_target field in SmallModelRoutePlan as placeholder",
        "future_action": "Implement taste dials configuration in future PR",
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    },
    {
        "name": "Model Dojo",
        "status": "future_pr_required",
        "purpose": "Local model fine-tune and evaluation harness for small models.",
        "small_model_relevance": "high — direct 3B/7B model improvement pipeline",
        "qshabang_relevance": "ki_ohne_ki, q_gates",
        "current_repo_evidence": "odin/models/",
        "pr09_action": "model_tier field in model_roles registry as schema anchor",
        "future_action": "Implement model dojo pipeline in future PR",
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    },
    {
        "name": "Scoreboard",
        "status": "future_pr_required",
        "purpose": "Tracks and surfaces model and candidate quality metrics over time.",
        "small_model_relevance": "medium — benchmarks 3B/7B candidate quality",
        "qshabang_relevance": "resonance_fit, candidate_reality",
        "current_repo_evidence": "odin/precompute/route_score.py (partial scoring)",
        "pr09_action": "not_proven list includes real_model_benchmark as placeholder",
        "future_action": "Implement scoreboard persistence in future PR",
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    },
    {
        "name": "SDK/App Bridge receipts",
        "status": "already_repo_real",
        "purpose": "Receipt and proof tracking between Odin and the app/SDK layer.",
        "small_model_relevance": "low — cross-cutting infrastructure",
        "qshabang_relevance": "app_sovereignty, q_gates",
        "current_repo_evidence": "odin/proof_chain/ — exists and is real",
        "pr09_action": "proof_refs and receipt_refs threaded through orchestrator",
        "future_action": "Extend as needed when new receipt types are required",
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    },
]

_STATUS_SUMMARY: dict[str, list[str]] = {}
for _s in _SYSTEMS:
    _STATUS_SUMMARY.setdefault(_s["status"], []).append(_s["name"])


def build_deferred_system_lift_plan() -> dict:
    """Build the deferred system lift plan dict.

    Returns a candidate-only classification of all deferred systems.
    No execution, no app state.
    """
    return {
        "artifact_kind": "odin_deferred_system_lift_plan",
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "systems": [dict(s) for s in _SYSTEMS],
        "systems_count": len(_SYSTEMS),
        "status_summary": {k: list(v) for k, v in _STATUS_SUMMARY.items()},
        "not_proven": list(_NOT_PROVEN),
    }
