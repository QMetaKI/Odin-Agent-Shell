from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/v7_1_1/check_b1_app_boundary_universal_work_qirc_spine.py"
TIMESTAMP = "2026-01-01T00:00:00Z"
B1_IDS = [f"V711-R100-{i:03d}" for i in range(22, 48)]
FORBIDDEN_ACTIONS = {
    "mutate_app_state", "write_app_storage", "write_project_file", "send_external_message",
    "send_network_request", "publish_public_room", "execute_provider", "execute_live_model",
    "bypass_final_gate", "grant_app_authority",
}
FAILURE_REASONS = {
    "direct_apply_requested", "external_send_requested", "app_state_mutation_requested",
    "project_file_write_requested", "provider_execution_requested", "live_model_execution_requested",
    "missing_binding", "missing_claim_boundary",
}
CHANNELS = {
    "#odin.work", "#odin.context", "#odin.lens", "#odin.precompute", "#odin.worklet",
    "#odin.slot", "#odin.gaptext", "#odin.model_packet", "#odin.critic", "#odin.candidate",
    "#odin.final_gate", "#odin.trace", "#odin.receipt", "#app.digest", "#app.boundary",
}
FORBIDDEN_INTENTS = {
    "apply_app_change", "mutate_app_state", "write_project_file", "send_external_message",
    "publish_public_channel", "execute_provider", "execute_live_model", "bypass_final_gate",
}


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def b1_mapping():
    plan = load("registries/v7_1_1_actual_codex_bundle_plan.json")
    return next(item for item in plan["actual_bundles"] if item["bundle_id"] == "B1")


def run_tool(out: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), "--repo-root", str(ROOT), "--out", str(out), "--generated-at-utc", TIMESTAMP, *extra],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def required_fields(schema_rel: str) -> set[str]:
    return set(load(schema_rel).get("required", []))


def test_01_actual_bundle_plan_registry_exists():
    assert (ROOT / "registries/v7_1_1_actual_codex_bundle_plan.json").exists()


def test_02_b1_mapping_exists():
    assert b1_mapping()["actual_pr"] == "PR-27"


def test_03_b1_maps_slice_range():
    assert b1_mapping()["slice_range"] == "V711-R100-022..047"


def test_04_b1_contains_exactly_26_canonical_slice_ids():
    assert b1_mapping()["slice_ids"] == B1_IDS
    assert len(b1_mapping()["slice_ids"]) == 26


def test_05_b1_contains_no_out_of_range_slice_ids():
    assert not [sid for sid in b1_mapping()["slice_ids"] if sid not in B1_IDS]


def test_06_b1_absorbs_pr27_family():
    assert "PR-27-APP-BOUNDARY-UNIVERSAL-WORK" in b1_mapping()["absorbed_future_pr_families"]


def test_07_b1_absorbs_pr28_family():
    assert "PR-28-QIRC-SEMANTIC-BUS" in b1_mapping()["absorbed_future_pr_families"]


def test_08_canonical_ladder_not_rewritten_by_bundle_plan():
    ladder = load("registries/v7_1_1_road_to_100_ladder.json")
    assert ladder["registry_id"] == "odin.v7_1_1_road_to_100_ladder"
    assert ladder["canonical_slice_count"] == 190
    assert {s["id"] for s in ladder["slices"]}.issuperset(B1_IDS)
    assert "actual_bundles" not in ladder


def test_09_app_manifest_schema_exists():
    assert (ROOT / "schemas/v7_1_1_app_manifest.schema.json").exists()


def test_10_app_manifest_contract_registry_exists():
    assert (ROOT / "registries/v7_1_1_app_manifest_contract.json").exists()


def test_11_app_manifest_example_validates_structurally():
    example = load("examples/v7_1_1/app_manifest.example.json")
    assert required_fields("schemas/v7_1_1_app_manifest.schema.json").issubset(example)


def test_12_app_manifest_contains_required_forbidden_actions():
    assert FORBIDDEN_ACTIONS.issubset(set(load("examples/v7_1_1/app_manifest.example.json")["forbidden_actions"]))


def test_13_binding_schema_exists():
    assert (ROOT / "schemas/v7_1_1_binding_contract.schema.json").exists()


def test_14_binding_contract_registry_exists():
    assert (ROOT / "registries/v7_1_1_binding_contract_registry.json").exists()


def test_15_binding_requires_candidate_only():
    assert load("registries/v7_1_1_binding_contract_registry.json")["candidate_only_required"] is True
    assert load("examples/v7_1_1/binding_contract.example.json")["candidate_only"] is True


def test_16_binding_cannot_authorize_app_apply_state_external_send():
    binding = load("examples/v7_1_1/binding_contract.example.json")
    assert binding["app_owned_apply"] is True
    assert binding["app_owned_state"] is True
    assert binding["app_owned_external_send"] is True


def test_17_universal_work_schema_exists():
    assert (ROOT / "schemas/v7_1_1_universal_work.schema.json").exists()


def test_18_universal_work_contract_exists():
    assert (ROOT / "registries/v7_1_1_universal_work_contract.json").exists()


def test_19_universal_work_lifecycle_includes_required_states():
    states = set(load("registries/v7_1_1_universal_work_contract.json")["required_lifecycle_states"])
    assert {"received", "manifest_checked", "binding_checked", "compiled", "ready_for_context", "blocked", "needs_context", "cannot_safely_complete"}.issubset(states)


def test_20_universal_work_failure_reasons_include_hidden_authority_reasons():
    reasons = set(load("registries/v7_1_1_universal_work_contract.json")["required_failure_reasons"])
    assert FAILURE_REASONS.issubset(reasons)


def test_21_semantic_bus_event_schema_exists():
    assert (ROOT / "schemas/v7_1_1_semantic_bus_event.schema.json").exists()


def test_22_semantic_bus_channel_schema_exists():
    assert (ROOT / "schemas/v7_1_1_semantic_bus_channel.schema.json").exists()


def test_23_semantic_bus_registry_includes_required_channel_families():
    channels = {c["channel"] for c in load("registries/v7_1_1_semantic_bus_spine_registry.json")["channels"]}
    assert CHANNELS.issubset(channels)


def test_24_semantic_bus_forbidden_intents_include_hidden_authority_controls():
    intents = set(load("registries/v7_1_1_semantic_bus_spine_registry.json")["required_forbidden_event_intents"])
    assert FORBIDDEN_INTENTS.issubset(intents)


def test_25_b1_static_validator_tool_exists():
    assert TOOL.exists()


def test_26_b1_static_validator_runs_with_deterministic_timestamp(tmp_path):
    out = tmp_path / "report.json"
    result = run_tool(out)
    assert result.returncode == 0, result.stderr + result.stdout
    assert json.loads(out.read_text())["generated_at_utc"] == TIMESTAMP


def test_27_b1_generated_report_has_correct_report_id():
    assert load("reports/v7_1_1_b1_app_boundary_universal_work_qirc_spine_report.json")["report_id"] == "odin.v7_1_1_b1_app_boundary_universal_work_qirc_spine_report"


def test_28_b1_generated_report_has_zero_hard_violations():
    assert load("reports/v7_1_1_b1_app_boundary_universal_work_qirc_spine_report.json")["hard_violations"] == []


def test_29_tool_fails_closed_when_bundle_registry_missing(tmp_path):
    out = tmp_path / "report.json"
    result = run_tool(out, "--bundle-plan", str(tmp_path / "missing.json"))
    assert result.returncode != 0
    assert json.loads(out.read_text())["hard_violations"]


def test_30_tool_flags_injected_manifest_that_allows_direct_apply(tmp_path):
    manifest = load("examples/v7_1_1/app_manifest.example.json")
    manifest["forbidden_actions"].remove("mutate_app_state")
    injected = tmp_path / "manifest.json"
    injected.write_text(json.dumps(manifest))
    out = tmp_path / "report.json"
    result = run_tool(out, "--app-manifest", str(injected))
    assert result.returncode != 0
    assert any("mutation" in v or "mutate" in v for v in json.loads(out.read_text())["hard_violations"])


def test_31_tool_flags_injected_binding_candidate_only_false(tmp_path):
    binding = load("examples/v7_1_1/binding_contract.example.json")
    binding["candidate_only"] = False
    injected = tmp_path / "binding.json"
    injected.write_text(json.dumps(binding))
    out = tmp_path / "report.json"
    result = run_tool(out, "--binding", str(injected))
    assert result.returncode != 0
    assert any("candidate_only" in v for v in json.loads(out.read_text())["hard_violations"])


def test_32_tool_flags_injected_semantic_bus_event_send_external_message(tmp_path):
    event = load("examples/v7_1_1/semantic_bus_event.example.json")
    event["intent"] = "send_external_message"
    injected = tmp_path / "event.json"
    injected.write_text(json.dumps(event))
    out = tmp_path / "report.json"
    result = run_tool(out, "--semantic-event", str(injected))
    assert result.returncode != 0
    assert any("send_external_message" in v for v in json.loads(out.read_text())["hard_violations"])


def test_33_tool_flags_injected_semantic_bus_event_bypass_final_gate(tmp_path):
    event = load("examples/v7_1_1/semantic_bus_event.example.json")
    event["intent"] = "bypass_final_gate"
    injected = tmp_path / "event.json"
    injected.write_text(json.dumps(event))
    out = tmp_path / "report.json"
    result = run_tool(out, "--semantic-event", str(injected))
    assert result.returncode != 0
    assert any("bypass_final_gate" in v for v in json.loads(out.read_text())["hard_violations"])


def test_34_tool_writes_only_to_requested_out(tmp_path):
    out = tmp_path / "only-report.json"
    before = {p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*")}
    result = run_tool(out)
    after = {p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*")}
    assert result.returncode == 0, result.stderr + result.stdout
    assert after - before == {"only-report.json"}


def test_35_report_does_not_leak_absolute_local_paths():
    text = (ROOT / "reports/v7_1_1_b1_app_boundary_universal_work_qirc_spine_report.json").read_text()
    assert str(ROOT) not in text
    assert "/workspace/" not in text


def test_36_pr25_operational_coverage_gap_tests_still_pass():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/test_v7_1_1_operational_coverage_gap_compiler.py", "-p", "no:cacheprovider"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_37_pr26_canon_boundary_integrity_tests_still_pass():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/test_v7_1_1_canon_boundary_integrity.py", "-p", "no:cacheprovider"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_38_file_manifest_remains_free_of_ignored_generated_local_artifacts():
    ignored = {".odin_runtime", "egg-info", "__pycache__", ".pytest_cache", "build", "dist"}
    bad = []
    for item in load("FILE_MANIFEST.json")["files"]:
        if ignored.intersection(Path(item["path"]).parts):
            bad.append(item["path"])
    assert bad == []
