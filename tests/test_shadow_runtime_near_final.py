from __future__ import annotations

import json
from pathlib import Path

from odin.shadow_runtime.e2e_orchestrator_shadow import run_near_final_shadow_runtime
from odin.shadow_runtime.policy_engine_shadow import evaluate_shadow_policy
from odin.shadow_runtime.resource_scheduler_shadow import plan_shadow_resource_posture
from odin.shadow_runtime.registry_consistency_shadow import shadow_registry_consistency_report
from odin.shadow_runtime.state_machine_shadow import build_shadow_state_machine

ROOT = Path(__file__).resolve().parents[1]


def load_fixture(name: str):
    return json.loads((ROOT / "examples" / "shadow_runtime" / name).read_text(encoding="utf-8"))


def test_near_final_shadow_runtime_valid_flow_covers_major_subsystems():
    work = load_fixture("near_final_shadow_flow.valid.json")
    result = run_near_final_shadow_runtime(work, resource_profile="standard_local", latency_mode="interactive")
    assert result["ok"] is True
    assert result["policy"]["ok"] is True
    assert result["resource_posture"]["route_ceiling"] == "3b_7b_8b_hybrid"
    assert result["response_packet"]["requires_app_apply_gate"] is True
    assert result["provider_plan"]["side_effects"] == "none_in_shadow"
    assert result["windows_runtime_plan"]["localhost_only"] is True
    assert result["app_qirc_validation"]["odin_owns_app_qirc"] is False
    assert "live_model_called" in result["forbidden_runtime_claims"]
    for key in ["context_plan", "worklet_plan", "gaptext", "tournament", "trace", "support_bundle", "spine"]:
        assert key in result and result[key] is not None


def test_near_final_shadow_runtime_blocks_direct_apply_and_non_candidate_contract():
    work = load_fixture("near_final_policy_block.invalid.json")
    result = run_near_final_shadow_runtime(work)
    assert result["ok"] is False
    assert "output_contract_not_candidate_only" in result["policy"]["blocked_markers"]
    assert "app_apply_gate_missing" in result["policy"]["blocked_markers"]
    assert result["state_machine"]["current_state"] == "CLAIM_BOUNDARY_HIT"
    assert "return_conflict_candidate" in result["failure_recovery"]["recommended_actions"] or result["failure_recovery"]["recommended_actions"]


def test_policy_engine_exposes_required_gates():
    work = load_fixture("near_final_shadow_flow.valid.json")
    decision = evaluate_shadow_policy(work)
    assert decision.ok is True
    assert "candidate_only_gate" in decision.required_gates
    assert decision.app_authority.startswith("app_retains")


def test_resource_scheduler_route_ceilings_are_hardware_agnostic():
    assert plan_shadow_resource_posture("low_memory_strict").route_ceiling == "3b_micro"
    assert plan_shadow_resource_posture("standard_local").route_ceiling == "3b_7b_8b_hybrid"
    assert plan_shadow_resource_posture("heavy_local", "batch").route_ceiling == "3b_22b_32b_heavy_local"


def test_state_machine_contains_terminal_states():
    plan = build_shadow_state_machine("WORK-001")
    assert plan.terminal_success == "RESPONSE_PACKET_READY"
    assert "CLAIM_BOUNDARY_HIT" in plan.failure_states


def test_registry_consistency_shadow_report_is_green():
    report = shadow_registry_consistency_report(ROOT)
    assert report["ok"] is True
    assert report["required_count"] >= 12
