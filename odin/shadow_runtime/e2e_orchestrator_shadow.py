from __future__ import annotations

from typing import Any, Dict

from .api_shadow import build_shadow_api_plan
from .app_qirc_bridge_shadow import validate_shadow_app_qirc_digest
from .artifact_lens_context_shadow import build_shadow_context_distillation_plan, select_shadow_lenses
from .bounded_code_shadow import build_shadow_bounded_code_plan
from .candidate_shadow import make_shadow_response_packet
from .candidate_tournament_shadow import run_shadow_candidate_tournament
from .failure_recovery_shadow import plan_shadow_failure_recovery
from .low_memory_shadow import build_low_memory_shadow_plan
from .model_dojo_shadow import score_shadow_model_dojo
from .pipeline import run_shadow_pipeline
from .policy_engine_shadow import evaluate_shadow_policy
from .provider_adapter_shadow import build_shadow_provider_adapter_plan
from .resource_scheduler_shadow import plan_shadow_resource_posture
from .security_redaction_shadow import redact_shadow_payload
from .state_machine_shadow import build_shadow_state_machine
from .storage_trace_shadow import build_shadow_trace_record
from .support_bundle_shadow import build_shadow_support_bundle_manifest
from .thor_bridge_shadow import build_shadow_thor_bridge_plan
from .windows_runtime_shadow import build_shadow_windows_runtime_plan
from .worklet_slot_shadow import build_shadow_gaptext, build_shadow_worklet_plan


def run_near_final_shadow_runtime(
    work: Dict[str, Any],
    *,
    resource_profile: str = "standard_local",
    latency_mode: str = "interactive",
    quality_target: str = "standard",
    provider: str = "mock",
    remote_allowed: bool = False,
) -> Dict[str, Any]:
    """Near-final mechanical shadow of Odin's future runtime.

    This function is intentionally pure and local. It is the closest code-near
    representation of the full Odin flow, but it does not start servers, call
    models, mutate app state, write files, send network traffic or claim runtime
    validation.
    """
    work_id = work.get("work_id", "WORK-MISSING")
    policy = evaluate_shadow_policy(work, remote_allowed=remote_allowed)
    resource = plan_shadow_resource_posture(resource_profile, latency_mode)
    redaction = redact_shadow_payload(work)

    if not policy.ok:
        failure_codes = ["CLAIM_BOUNDARY_HIT" if "tests_passed" in policy.blocked_markers or "runtime_verified" in policy.blocked_markers else "OUTPUT_CONTRACT_INVALID"]
        return {
            "artifact_kind": "odin_near_final_shadow_runtime_result",
            "protocol_version": "7.1-shadow-near-final",
            "ok": False,
            "work_id": work_id,
            "policy": policy.to_dict(),
            "resource_posture": resource.to_dict(),
            "redaction": redaction,
            "state_machine": build_shadow_state_machine(work_id, failed=True, failure_state="CLAIM_BOUNDARY_HIT").to_dict(),
            "failure_recovery": plan_shadow_failure_recovery(failure_codes),
            "boundary": "near_final_shadow_no_runtime_execution",
        }

    spine = run_shadow_pipeline(
        work,
        resource_profile=resource_profile,
        latency_mode=latency_mode,
        quality_target=quality_target,
        remote_allowed=remote_allowed,
    )
    route = spine.model_route_plan.selected_route if spine.model_route_plan else resource.route_ceiling
    lenses = select_shadow_lenses(work)
    context_plan = build_shadow_context_distillation_plan(work)
    worklet_plan = build_shadow_worklet_plan(work, route=route)
    gaptext = build_shadow_gaptext(work)
    provider_plan = build_shadow_provider_adapter_plan(route, provider=provider)
    api_plan = build_shadow_api_plan("/v7/universal-work/run", work)
    tournament = run_shadow_candidate_tournament(work)
    trace = build_shadow_trace_record(work, spine.trace_id)
    support_bundle = build_shadow_support_bundle_manifest(work_id)
    runtime_plan = build_shadow_windows_runtime_plan(resource_profile)
    model_dojo = score_shadow_model_dojo(route)
    thor_plan = build_shadow_thor_bridge_plan(work)
    bounded_code_plan = build_shadow_bounded_code_plan(work)
    low_memory_plan = build_low_memory_shadow_plan(work) if resource_profile == "low_memory_strict" else None
    app_qirc_validation = validate_shadow_app_qirc_digest(work.get("app_qirc_bridge_digest", {"digest_mode": "summary_only"}))

    response_packet = None
    if spine.candidate and spine.candidate_dna:
        response_packet = make_shadow_response_packet(work, spine.candidate, spine.candidate_dna)

    return {
        "artifact_kind": "odin_near_final_shadow_runtime_result",
        "protocol_version": "7.1-shadow-near-final",
        "ok": spine.ok,
        "work_id": work_id,
        "trace_id": spine.trace_id,
        "policy": policy.to_dict(),
        "resource_posture": resource.to_dict(),
        "redaction": redaction,
        "state_machine": build_shadow_state_machine(work_id, failed=not spine.ok).to_dict(),
        "active_lenses": lenses,
        "context_plan": context_plan,
        "worklet_plan": worklet_plan,
        "gaptext": gaptext,
        "provider_plan": provider_plan,
        "api_plan": api_plan,
        "tournament": tournament,
        "trace": trace,
        "support_bundle": support_bundle,
        "windows_runtime_plan": runtime_plan,
        "model_dojo_profile": model_dojo,
        "thor_plan": thor_plan,
        "bounded_code_plan": bounded_code_plan,
        "low_memory_plan": low_memory_plan,
        "app_qirc_validation": app_qirc_validation,
        "spine": spine.to_dict(),
        "response_packet": response_packet,
        "codex_conversion_rule": "convert shadow objects to real modules without changing authority boundaries",
        "forbidden_runtime_claims": ["live_model_called", "server_started", "app_state_mutated", "external_send_performed"],
        "boundary": "near_final_shadow_no_runtime_execution_no_external_effects",
    }
