from pathlib import Path
import json

from odin import cli
from odin.shadow_runtime.qirc_gold_spine_shadow import run_qirc_gold_spine_shadow
from odin.shadow_runtime.qirc_hot_window_shadow import build_qirc_hot_window
from odin.shadow_runtime.qirc_seed_prewarm_shadow import prewarm_qirc_seeds
from odin.shadow_runtime.qirc_admissibility_shadow import decide_qirc_admissibility
from odin.shadow_runtime.qirc_ring_radar_shadow import build_qirc_ring_radar
from odin.shadow_runtime.qirc_why_trace_shadow import build_qirc_why_trace
from odin.shadow_runtime.qirc_runtime_pack_shadow import build_qirc_capability_slice_channels

ROOT = Path(__file__).resolve().parents[1]

def test_qirc_gold_spine_validation_clean():
    assert cli.validate_qirc_gold_spine() == []

def test_qirc_gold_spine_flow_and_block():
    work = json.loads((ROOT / "examples/shadow_runtime/qirc_gold_spine_flow.valid.json").read_text())
    assert run_qirc_gold_spine_shadow(work)["ok"] is True
    blocked = json.loads((ROOT / "examples/shadow_runtime/qirc_gold_spine_block.invalid.json").read_text())
    result = run_qirc_gold_spine_shadow(blocked)
    assert result["ok"] is False and result["decision"] == "block"

def test_qirc_hot_window_seed_admissibility_ring_why_pack():
    events = [{"channel":"#context.raw_digest","event_type":"digest","work_id":"W1","payload_summary":{"n":1}}, {"channel":"#context.raw_digest","event_type":"digest","work_id":"W1","payload_summary":{"n":2}}, {"channel":"#seed.activate","event_type":"seed_activation_completed","work_id":"W1","payload_summary":{"active_seed_count":3}}]
    hot = build_qirc_hot_window(events, max_events=4)
    assert hot["raw_payload_included"] is False
    seeds = prewarm_qirc_seeds(["wedding", "rewrite"], budget=5)
    assert "claim_boundary" in seeds["active_seeds"]
    gate = decide_qirc_admissibility(True, "small", remote_allowed=False)
    assert gate["decision"] == "go" and gate["blocked_routes"][0]["route"] == "remote"
    radar = build_qirc_ring_radar({"R0_boundary":0.9,"R6_model":0.2})
    assert radar["rings"]["R0_boundary"]["status"] == "active"
    why = build_qirc_why_trace("schema_repair", {"3b_micro":0.84,"7b_quality":0.61}, seeds["active_seeds"])
    assert why["final_gate"] == "candidate_only_preserved"
    pack = build_qirc_capability_slice_channels("low_memory_strict")
    assert "#model.heavy" in pack["excluded_channels"]

def test_qirc_pr45_to_pr49_and_real_pr15_registered():
    tasks = json.loads((ROOT / "registries/codex_task_registry.json").read_text())["tasks"]
    task_ids = {task["id"] for task in tasks}
    for tid in ["PR-45","PR-46","PR-47","PR-48","PR-49"]:
        assert tid in task_ids
    bundles = json.loads((ROOT / "registries/codex_pr_bundle_registry.json").read_text())["bundles"]
    assert any(bundle["id"] == "REAL-PR-15" and "PR-49" in bundle["internal_tasks"] for bundle in bundles)
