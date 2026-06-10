"""Code-near non-authoritative Shadow Runtime for Odin Agent Shell v7.1.

This package is a build blueprint, not runtime proof. It performs pure in-memory
candidate shaping for tests and Codex guidance.
"""

from .pipeline import run_shadow_pipeline
from .types import ShadowRuntimeResult
from .artifact_lens_context_shadow import select_shadow_lenses, build_shadow_context_distillation_plan
from .worklet_slot_shadow import build_shadow_worklet_plan, build_shadow_gaptext
from .candidate_tournament_shadow import run_shadow_candidate_tournament
from .low_memory_shadow import build_low_memory_shadow_plan
from .thor_bridge_shadow import build_shadow_thor_bridge_plan
from .bounded_code_shadow import build_shadow_bounded_code_plan
from .storage_trace_shadow import build_shadow_trace_record
from .api_shadow import build_shadow_api_plan
from .app_qirc_bridge_shadow import validate_shadow_app_qirc_digest
from .model_dojo_shadow import score_shadow_model_dojo
from .security_redaction_shadow import redact_shadow_payload
from .support_bundle_shadow import build_shadow_support_bundle_manifest
from .windows_runtime_shadow import build_shadow_windows_runtime_plan
from .sdk_template_shadow import validate_shadow_sdk_template

__all__ = [
    "run_shadow_pipeline", "ShadowRuntimeResult", "select_shadow_lenses", "build_shadow_context_distillation_plan",
    "build_shadow_worklet_plan", "build_shadow_gaptext", "run_shadow_candidate_tournament", "build_low_memory_shadow_plan",
    "build_shadow_thor_bridge_plan", "build_shadow_bounded_code_plan", "build_shadow_trace_record", "build_shadow_api_plan",
    "validate_shadow_app_qirc_digest", "score_shadow_model_dojo", "redact_shadow_payload", "build_shadow_support_bundle_manifest",
    "build_shadow_windows_runtime_plan", "validate_shadow_sdk_template",
]

from .e2e_orchestrator_shadow import run_near_final_shadow_runtime
from .policy_engine_shadow import evaluate_shadow_policy
from .resource_scheduler_shadow import plan_shadow_resource_posture
from .state_machine_shadow import build_shadow_state_machine

# v0.6.1 Odin Core / QLI / DFAS exports
try:
    from .qli_master_interface_shadow import run_qli_master_shadow
except Exception:  # pragma: no cover - shadow optional import guard
    run_qli_master_shadow = None

# v0.6.2 QIRC Gold Spine exports
try:
    from .qirc_gold_spine_shadow import run_qirc_gold_spine_shadow
    from .qirc_hot_window_shadow import build_qirc_hot_window
    from .qirc_seed_prewarm_shadow import prewarm_qirc_seeds
    from .qirc_admissibility_shadow import decide_qirc_admissibility
    from .qirc_ring_radar_shadow import build_qirc_ring_radar
    from .qirc_why_trace_shadow import build_qirc_why_trace
    from .qirc_runtime_pack_shadow import build_qirc_capability_slice_channels
except Exception:  # pragma: no cover
    run_qirc_gold_spine_shadow = None
# v0.6.9 app seed pack compiler shadow modules are intentionally imported lazily.
