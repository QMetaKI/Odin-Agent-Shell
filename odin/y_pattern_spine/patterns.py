"""Y Pattern definitions — families, YPattern objects.

Claim boundary: y_pattern_spine_candidate_only_no_app_apply_no_provider_no_runtime_authority
candidate_only: true
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

CLAIM_BOUNDARY = "y_pattern_spine_candidate_only_no_app_apply_no_provider_no_runtime_authority"

PATTERN_FAMILIES = [
    "orientation",
    "token_efficiency",
    "review",
    "route_selection",
    "work_state",
    "lineage",
    "center_first",
    "candidate_set",
    "compile_near",
    "projection",
    "operator_pattern",
    "ai_without_ai",
    "scope_compression",
    "balance_axis",
]


@dataclass
class YPattern:
    pattern_id: str
    neutral_name: str
    family: str
    intent_seed: str
    role_profile: str
    route_hint: str
    allowed_use: List[str]
    forbidden_use: List[str]
    source_class: str
    normal_user_visible: bool
    dev_mode_visible: bool
    claim_boundary: str = CLAIM_BOUNDARY
    odin_target_surface: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "pattern_id": self.pattern_id,
            "neutral_name": self.neutral_name,
            "family": self.family,
            "intent_seed": self.intent_seed,
            "role_profile": self.role_profile,
            "route_hint": self.route_hint,
            "allowed_use": self.allowed_use,
            "forbidden_use": self.forbidden_use,
            "source_class": self.source_class,
            "normal_user_visible": self.normal_user_visible,
            "dev_mode_visible": self.dev_mode_visible,
            "claim_boundary": self.claim_boundary,
            "odin_target_surface": self.odin_target_surface,
        }


_PATTERNS: List[YPattern] = [
    YPattern(
        pattern_id="y_intent_seeds",
        neutral_name="intent_seeds",
        family="orientation",
        intent_seed="small task-intent primitives shaping Handoff Context",
        role_profile="context_shaper",
        route_hint="inject into handoff_context.task_intent and work capsule task_intent",
        allowed_use=["handoff_context", "work_capsule_task_intent", "universal_work_prep"],
        forbidden_use=["app_state_mutation", "model_authority", "apply_permission"],
        source_class="metamodel_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="handoff_context",
    ),
    YPattern(
        pattern_id="y_role_profiles",
        neutral_name="role_profiles",
        family="orientation",
        intent_seed="worker/reviewer posture hints",
        role_profile="posture_hint",
        route_hint="attach to model_work_packet as posture_hint, never authority",
        allowed_use=["model_work_packet_posture", "dev_mode_explanation", "worker_context"],
        forbidden_use=["decision_authority", "model_command", "app_approval"],
        source_class="metamodel_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="model_work_packet",
    ),
    YPattern(
        pattern_id="y_coherence_scores",
        neutral_name="coherence_scores",
        family="review",
        intent_seed="relevance and coherence ranking hints",
        role_profile="ranking_explainer",
        route_hint="surface in dev_mode explanation, not in decision logic",
        allowed_use=["dev_mode_explanation", "route_ranking_hint", "candidate_ranking"],
        forbidden_use=["decision_authority", "proof_claim", "model_selection_override"],
        source_class="metamodel_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="dev_mode",
    ),
    YPattern(
        pattern_id="y_review_axes",
        neutral_name="review_axes",
        family="review",
        intent_seed="structured review lenses: clarity/novelty, care/force, center/expansion, evidence/assumption",
        role_profile="senior_reviewer",
        route_hint="use as audit lens in senior_reviewer pass, not judgment authority",
        allowed_use=["senior_reviewer_audit", "validator_lens", "proof_aid"],
        forbidden_use=["judgment_authority", "blocking_gate_without_evidence", "model_override"],
        source_class="metamodel_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="validator",
    ),
    YPattern(
        pattern_id="y_center_first_routing",
        neutral_name="center_first_routing",
        family="center_first",
        intent_seed="center→adjacent→expansion→return reduces feature sprawl",
        role_profile="route_orderer",
        route_hint="apply to route_hint candidate_routes ordering before expansion",
        allowed_use=["route_hint_ordering", "scope_discipline", "pareto_scope_policy"],
        forbidden_use=["hidden_controller", "forced_route_without_evidence", "app_apply"],
        source_class="foundation_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="handoff_context",
    ),
    YPattern(
        pattern_id="y_candidate_set_routing",
        neutral_name="candidate_set_routing",
        family="candidate_set",
        intent_seed="multiple routes stay candidates until evidence selects",
        role_profile="route_candidate_holder",
        route_hint="populate candidate_routes list in YRouteHint",
        allowed_use=["route_hint_candidates", "evidence_selection", "validator_selection"],
        forbidden_use=["forcing_single_route_without_evidence", "hidden_controller"],
        source_class="foundation_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="handoff_context",
    ),
    YPattern(
        pattern_id="y_selection_math",
        neutral_name="selection_math",
        family="route_selection",
        intent_seed="bounded route_score/confidence/hole_density object",
        role_profile="score_calculator",
        route_hint="attach YSelectionScore to route hint, bounded 0–1, never >1 claims",
        allowed_use=["route_hint_score", "confidence_hint", "hole_density_measure"],
        forbidden_use=["proof_claim", "authority", "production_certification"],
        source_class="foundation_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="trace_receipt",
    ),
    YPattern(
        pattern_id="y_work_state_spine",
        neutral_name="work_state_spine",
        family="work_state",
        intent_seed="task/work/session state, not app state",
        role_profile="work_state_tracker",
        route_hint="track in work_capsule and model_work_packet state fields only",
        allowed_use=["work_capsule_state", "model_work_packet_state", "session_tracking"],
        forbidden_use=["app_state_mutation", "external_send", "db_write"],
        source_class="foundation_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="universal_work",
    ),
    YPattern(
        pattern_id="y_lineage_trace",
        neutral_name="lineage_trace",
        family="lineage",
        intent_seed="why-this-route / source-file / diff-intent trace",
        role_profile="trace_recorder",
        route_hint="attach to YProjectionSet lineage_trace field",
        allowed_use=["trace_receipt", "proof_packet_lineage", "dev_mode_explanation"],
        forbidden_use=["git_apply", "commit_authority", "external_send"],
        source_class="foundation_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="trace_receipt",
    ),
    YPattern(
        pattern_id="y_expression_packet",
        neutral_name="expression_packet",
        family="projection",
        intent_seed="human-friendly explanation projection only",
        role_profile="expression_projector",
        route_hint="populate YProjectionSet.expression_projection field",
        allowed_use=["human_explanation", "dev_mode_summary", "normal_user_summary"],
        forbidden_use=["code_truth", "apply_authority", "model_decision"],
        source_class="metamodel_source",
        normal_user_visible=True,
        dev_mode_visible=True,
        odin_target_surface="candidate_artifact",
    ),
    YPattern(
        pattern_id="y_shadow_candidate_graph",
        neutral_name="shadow_candidate_graph",
        family="compile_near",
        intent_seed="compile-near shape of candidate work, not runtime",
        role_profile="compile_near_tracer",
        route_hint="attach compile-near hints to YWorkCapsule, not execution",
        allowed_use=["compile_near_candidate", "candidate_artifact_shape", "dev_mode_shape"],
        forbidden_use=["runtime_execution", "app_apply", "model_override"],
        source_class="ynet_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="candidate_artifact",
    ),
    YPattern(
        pattern_id="y_projection_spine",
        neutral_name="projection_spine",
        family="projection",
        intent_seed="correlates human-clear, expression, machine projections",
        role_profile="projection_correlator",
        route_hint="build YProjectionSet with all three projections",
        allowed_use=["human_machine_correlation", "dev_mode_explanation", "candidate_response_prep"],
        forbidden_use=["authority", "truth_claim", "apply_permission"],
        source_class="metamodel_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="candidate_artifact",
    ),
    YPattern(
        pattern_id="y_materialization_ladder",
        neutral_name="materialization_ladder",
        family="work_state",
        intent_seed="M0–M9 readiness levels for work preparation",
        role_profile="readiness_tracker",
        route_hint="use YMaterializationLevel to track work preparation stage",
        allowed_use=["work_capsule_readiness", "handoff_readiness", "dev_mode_level"],
        forbidden_use=["completion_claim", "production_ready_claim", "deploy_authority"],
        source_class="foundation_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="universal_work",
    ),
    YPattern(
        pattern_id="y_token_capsules",
        neutral_name="token_capsules",
        family="token_efficiency",
        intent_seed="compact context packets for local Claude Code / local LLM workers",
        role_profile="token_optimizer",
        route_hint="use YWorkCapsule with minimal token_budget for worker prompts",
        allowed_use=["worker_prompt_scoping", "minimal_context", "token_budget_hint"],
        forbidden_use=["full_repo_context_claim", "model_truth", "authority"],
        source_class="foundation_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="model_work_packet",
    ),
    YPattern(
        pattern_id="y_operator_pattern_mine",
        neutral_name="operator_pattern_mine",
        family="operator_pattern",
        intent_seed="neutral pattern retrieval: function→operator→state→recurrence→derivation",
        role_profile="pattern_miner",
        route_hint="use for source-pattern advisory only, no runtime import",
        allowed_use=["source_pattern_advisory", "route_hint_seed", "dev_mode_background"],
        forbidden_use=["runtime_import", "religious_interpretation", "persona_injection"],
        source_class="operator_pattern_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="trace_receipt",
    ),
    YPattern(
        pattern_id="y_ai_without_ai_precompute",
        neutral_name="ai_without_ai_precompute",
        family="ai_without_ai",
        intent_seed="deterministic pre-model prep: route hints, caches, schemas, validators",
        role_profile="precompute_preparer",
        route_hint="populate all deterministic fields before model work",
        allowed_use=["schema_prep", "validator_prep", "route_hint_prep", "capsule_prep"],
        forbidden_use=["model_execution", "provider_call", "external_send"],
        source_class="foundation_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="universal_work",
    ),
    YPattern(
        pattern_id="y_pareto_scope_policy",
        neutral_name="pareto_scope_policy",
        family="scope_compression",
        intent_seed="smallest useful path before expansion",
        role_profile="scope_limiter",
        route_hint="prefer minimal token_budget mode; expand only with evidence",
        allowed_use=["scope_discipline", "token_budget_minimal_first", "center_first_routing"],
        forbidden_use=["full_expansion_without_evidence", "broad_mining"],
        source_class="foundation_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="handoff_context",
    ),
    YPattern(
        pattern_id="y_care_force_axis",
        neutral_name="care_force_axis",
        family="balance_axis",
        intent_seed="balance heuristic: clarity/care/stability vs force/edge/action",
        role_profile="balance_heuristic",
        route_hint="attach balance_axis hint to work capsule and review axes",
        allowed_use=["review_balance_hint", "dev_mode_explanation", "senior_reviewer_lens"],
        forbidden_use=["persona_injection", "religious_interpretation", "authority"],
        source_class="foundation_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="dev_mode",
    ),
    YPattern(
        pattern_id="y_local_worker_efficiency",
        neutral_name="local_worker_efficiency",
        family="token_efficiency",
        intent_seed="reduce tokens: route hint + work capsule + exact files + validators",
        role_profile="efficiency_optimizer",
        route_hint="always set token_budget_hint before dispatching worker packet",
        allowed_use=["worker_packet_token_reduction", "capsule_scoping", "validator_injection"],
        forbidden_use=["omit_validators", "full_repo_dump", "authority"],
        source_class="foundation_source",
        normal_user_visible=False,
        dev_mode_visible=True,
        odin_target_surface="model_work_packet",
    ),
]

_PATTERN_MAP = {p.pattern_id: p for p in _PATTERNS}


def get_pattern(pattern_id: str) -> Optional[YPattern]:
    return _PATTERN_MAP.get(pattern_id)


def list_patterns() -> List[YPattern]:
    return list(_PATTERNS)


def list_families() -> List[str]:
    return list(PATTERN_FAMILIES)



