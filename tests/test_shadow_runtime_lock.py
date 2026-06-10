import json
from pathlib import Path

from odin import cli
from odin.shadow_runtime import run_shadow_pipeline
from odin.shadow_runtime.model_route_shadow import choose_shadow_route

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def test_shadow_runtime_validation_clean():
    assert cli.validate_shadow_runtime() == []


def test_valid_shadow_pipeline_candidate_only():
    work = load("examples/shadow_runtime/markdown_rewrite_shadow_flow.valid.json")
    result = run_shadow_pipeline(work)
    assert result.ok is True
    assert result.candidate is not None
    assert result.candidate.candidate_only is True
    assert result.candidate.requires_app_apply_gate is True
    assert result.model_route_plan.selected_route == "3b_7b_8b_hybrid"
    channels = {event.channel for event in result.events}
    assert "#work.received" in channels
    assert "#candidate.ready" in channels


def test_direct_apply_is_blocked():
    work = load("examples/shadow_runtime/direct_apply_blocked.invalid.json")
    result = run_shadow_pipeline(work)
    assert result.ok is False
    assert "direct_apply_forbidden" in result.reason_codes()


def test_shadow_route_ladder_quality_and_low_memory():
    assert choose_shadow_route("standard_local").selected_route == "3b_7b_8b_hybrid"
    assert choose_shadow_route("low_memory_strict").selected_route == "3b_micro_critic_router"
    assert choose_shadow_route("quality_local", latency_mode="draft", quality_target="premium").selected_route == "3b_13b_14b_quality_hybrid"


def test_pr23_and_real_pr09_registered():
    tasks = load("registries/codex_task_registry.json")["tasks"]
    assert any(task["id"] == "PR-23" for task in tasks)
    bundles = load("registries/codex_pr_bundle_registry.json")["bundles"]
    assert any(bundle["id"] == "REAL-PR-09" and "PR-23" in bundle["internal_tasks"] for bundle in bundles)
