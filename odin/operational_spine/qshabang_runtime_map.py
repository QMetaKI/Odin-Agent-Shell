"""QShabang Runtime Map for FINAL-PR-09 Operational Spine.

Claim boundary: final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply
candidate_only: true

Maps the operational architecture components of the Odin runtime.
No model execution, no provider calls, no app state mutations.
"""
from __future__ import annotations

CLAIM_BOUNDARY = "final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply"

_NOT_PROVEN = [
    "production_readiness",
    "live_model_inference",
    "app_state_mutation",
    "external_send_authority",
    "runtime_completeness",
    "model_benchmark",
]

_COMPONENTS = [
    {
        "name": "ki_ohne_ki",
        "odin_term": "Ki-ohne-Ki",
        "description": "Deterministic precompute and no-model routes. Work that never needs a model call.",
        "repo_evidence": "odin/precompute/, odin/operational_spine/small_model_route_plan.py (deterministic_no_model route)",
        "deferred": False,
        "candidate_only": True,
    },
    {
        "name": "q_gates",
        "odin_term": "Q-Gates",
        "description": "Claim, evidence, and reality gates. Guard boundaries between candidate and applied state.",
        "repo_evidence": "odin/execution_gate/, odin/proof_chain/, odin/field_selection_spine/fields.py (claim_boundary_integrity)",
        "deferred": False,
        "candidate_only": True,
    },
    {
        "name": "mirror_critics",
        "odin_term": "Mirror Critics / Critic Cascade",
        "description": "Critic Cascade for candidate quality. Multiple critic passes at different model tiers.",
        "repo_evidence": "odin/operational_spine/model_roles.py (3b_quick_critic, 7b_complex_critic), odin/quality/",
        "deferred": True,
        "candidate_only": True,
    },
    {
        "name": "resonance_fit",
        "odin_term": "Resonance Fit",
        "description": "Coherence and fit scoring for candidate artifacts against work context.",
        "repo_evidence": "odin/field_selection_spine/coherence.py, odin/precompute/route_score.py",
        "deferred": False,
        "candidate_only": True,
    },
    {
        "name": "seeds_pattern_mines",
        "odin_term": "Seeds / Pattern Mines",
        "description": "Seed continuity and flow packs. Intent seeds and pattern library for work routing.",
        "repo_evidence": "odin/operational_seed_spine/, odin/seeds/, odin/flow_packs/",
        "deferred": False,
        "candidate_only": True,
    },
    {
        "name": "narrative_compiler",
        "odin_term": "Narrative Compiler",
        "description": "Work-flow pack and shadow runtime preparation. Compiles work packets into narrative flow.",
        "repo_evidence": "odin/compiler/, odin/shadow_runtime/, odin/flow_packs/",
        "deferred": True,
        "candidate_only": True,
    },
    {
        "name": "qirc",
        "odin_term": "QIRC",
        "description": "Local semantic coordination and receipt bus. Internal event/hint routing without network.",
        "repo_evidence": "odin/qirc/, odin/qirc_core/, odin/qirc_hints.py",
        "deferred": False,
        "candidate_only": True,
    },
    {
        "name": "app_sovereignty",
        "odin_term": "App Sovereignty",
        "description": "App-owned apply, state, and external-send. Odin never applies; app decides.",
        "repo_evidence": "odin/execution_gate/, CLAIM_BOUNDARY.md, AGENTS.md (app_owned_apply)",
        "deferred": False,
        "candidate_only": True,
    },
    {
        "name": "candidate_reality",
        "odin_term": "Candidate Reality",
        "description": "Candidate Artifact and Response Packet. The output of all Odin work — always candidate_only.",
        "repo_evidence": "odin/candidates/, odin/packets/, odin/operational_spine/modelworkpacket_builder.py",
        "deferred": False,
        "candidate_only": True,
    },
    {
        "name": "qooo_style_orchestration",
        "odin_term": "QOOO Style Orchestration",
        "description": "Route director and system profile compiler. Orchestrates route selection and style profiles.",
        "repo_evidence": "odin/system_palette/, odin/operational_spine/small_model_route_plan.py, odin/operational_spine/model_roles.py",
        "deferred": True,
        "candidate_only": True,
    },
    {
        "name": "bug6_q7",
        "odin_term": "Bug6/Q7",
        "description": "Authority drift and boundary scanners. Detects claim boundary violations and authority drift.",
        "repo_evidence": "odin/runtime_security/, odin/proof_chain/, CLAIM_BOUNDARY.md",
        "deferred": True,
        "candidate_only": True,
    },
]

_RUNTIME_EVIDENCE = [
    "odin/precompute/ — deterministic route scoring",
    "odin/operational_seed_spine/ — intent seed routing",
    "odin/field_selection_spine/ — field selection and coherence",
    "odin/projection_candidate_spine/ — projection candidate building",
    "odin/execution_gate/ — app authority gate",
    "odin/qirc/ — local semantic coordination",
    "odin/proof_chain/ — receipt and proof tracking",
    "odin/operational_spine/ — orchestrator and model role registry (PR-09)",
]

_DEFERRED_ITEMS = [
    "mirror_critics: Critic Cascade full implementation (future PR)",
    "narrative_compiler: Shadow runtime full compilation (future PR)",
    "qooo_style_orchestration: Full style profile compiler (future PR)",
    "bug6_q7: Authority drift scanner runtime (future PR)",
]


def build_qshabang_operational_map() -> dict:
    """Build the QShabang operational map dict.

    Returns a candidate-only architectural map. No execution, no app state.
    """
    return {
        "artifact_kind": "odin_qshabang_operational_map",
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "components": [dict(c) for c in _COMPONENTS],
        "components_count": len(_COMPONENTS),
        "runtime_evidence": list(_RUNTIME_EVIDENCE),
        "deferred_items": list(_DEFERRED_ITEMS),
        "not_proven": list(_NOT_PROVEN),
    }
