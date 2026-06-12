from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "v7_1_1" / "check_b6_acceptance_dojo_scoreboard_closure.py"
B6_IDS = [f"V711-R100-{i:03d}" for i in range(170, 190)]
REQ_ACCEPTANCE = {
    "claim_boundary_integrity", "non_claim_presence", "evidence_ref_presence",
    "response_packet_completeness", "candidate_lineage_traceability",
    "privacy_class_preserved", "storage_trace_receipt_consistency",
    "receipt_partition_consistency", "final_gate_advisory_boundary",
    "provider_policy_disabled_defaults", "thor_odin_bridge_static_only",
    "sdk_app_bridge_no_app_authority", "no_runtime_proof_claim", "no_release_proof_claim",
}
TRAINING_MODES = {"static_review", "contract_drill", "boundary_drill", "evidence_drill", "closure_drill", "regression_drill"}
SCORING_DIMS = {
    "contract_compliance", "claim_boundary_compliance", "evidence_completeness", "traceability",
    "privacy_discipline", "receipt_partition_integrity", "provider_boundary_integrity",
    "app_authority_boundary", "thor_bridge_static_boundary", "final_gate_advisory_boundary",
    "regression_preservation", "closure_readiness",
}
CLOSURE_CHECKS = {
    "canonical_ladder_preserved", "actual_bundle_plan_complete", "b1_mapping_preserved",
    "b2_mapping_preserved", "b3_mapping_preserved", "b4_mapping_preserved", "b5_mapping_preserved",
    "claim_boundaries_present", "non_claims_present", "no_forbidden_runtime_claims",
    "no_app_authority_leak", "no_final_gate_elevation", "no_provider_execution",
    "no_network_default", "no_hidden_remote_fallback", "evidence_substrate_present",
    "acceptance_harness_present", "scoreboard_present", "closure_report_present",
    "known_gaps_present", "b7_plus_recommendations_present",
}
STATUSES = {"ready_static", "warn_static", "blocked_static", "deferred_to_b7_plus", "requires_human_review", "cannot_safely_complete"}
GUARDS = {
    "no_release_certification", "no_production_readiness", "no_deployment_proof", "no_runtime_proof",
    "no_provider_execution_proof", "no_live_model_quality_proof", "no_security_certification",
    "no_app_authority", "no_final_gate_elevation", "no_receipt_truth_elevation",
}


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def schema_enums(node):
    found = set()
    if isinstance(node, dict):
        if isinstance(node.get("enum"), list):
            found.update(node["enum"])
        for v in node.values():
            found |= schema_enums(v)
    elif isinstance(node, list):
        for v in node:
            found |= schema_enums(v)
    return found


def run_tool(repo: Path, out: Path):
    spec = importlib.util.spec_from_file_location("b6tool", TOOL)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    code = mod.main(["--repo-root", str(repo), "--out", str(out), "--generated-at-utc", "2026-01-01T00:00:00Z"])
    return code, json.loads(out.read_text(encoding="utf-8"))


def clone_minimal(tmp_path: Path) -> Path:
    dst = tmp_path / "repo"
    dst.mkdir(parents=True, exist_ok=True)
    for d in ["schemas", "registries", "examples", "reports", "tools"]:
        shutil.copytree(ROOT / d, dst / d)
    return dst


def artifact_paths(name: str):
    return [
        f"schemas/v7_1_1_{name}.schema.json",
        f"registries/v7_1_1_{name}_registry.json",
        f"examples/v7_1_1/{name}.example.json",
    ]


def test_b6_bundle_mapping_and_previous_bundles_preserved():
    plan = load("registries/v7_1_1_actual_codex_bundle_plan.json")
    bundle = next(b for b in plan["actual_bundles"] if b["bundle_id"] == "B6")
    assert bundle["actual_pr"] == "PR-32"
    assert bundle["slice_range"] == "V711-R100-170..189"
    assert bundle["exact_slice_count"] == 20
    assert bundle["slice_ids"] == B6_IDS
    assert all(170 <= int(s.rsplit("-", 1)[1]) <= 189 for s in bundle["slice_ids"])
    assert bundle["absorbed_future_pr_families"] == ["PR-38-ACCEPTANCE-DOJO-SCOREBOARD-CLOSURE"]
    expected = {"B1": ("PR-27", "V711-R100-022..047"), "B2": ("PR-28", "V711-R100-048..075"), "B3": ("PR-29", "V711-R100-076..105"), "B4": ("PR-30", "V711-R100-106..137"), "B5": ("PR-31", "V711-R100-138..169")}
    for bid, (pr, rng) in expected.items():
        old = next(b for b in plan["actual_bundles"] if b["bundle_id"] == bid)
        assert old["actual_pr"] == pr and old["slice_range"] == rng
    ladder = load("registries/v7_1_1_road_to_100_ladder.json")
    assert set(B6_IDS).issubset({s["id"] for s in ladder["slices"]})
    assert ladder["canonical_slice_count"] >= 190


def test_b6_contract_files_and_positive_boundaries():
    for name in ["acceptance_harness", "dojo_session", "scoreboard", "closure_checklist", "closure_readiness_matrix", "road_to_100_closure_report", "closure_guard", "b7_plus_handoff_plan"]:
        for rel in artifact_paths(name):
            assert (ROOT / rel).exists(), rel
    acc_schema = load("schemas/v7_1_1_acceptance_harness.schema.json")
    acc = load("examples/v7_1_1/acceptance_harness.example.json")
    for field in ["response_packet_id", "candidate_artifact_id", "candidate_dna_id", "final_gate_advisory_id", "receipt_boundary_id", "storage_record_id", "trace_record_id", "receipt_ledger_id"]:
        assert field in acc_schema["required"] and field in acc
    assert REQ_ACCEPTANCE.issubset({c["check_kind"] for c in acc["acceptance_checks"]})
    assert "not_app_acceptance" in acc["non_claims"] and "not_release_certification" in acc["non_claims"]
    assert TRAINING_MODES.issubset(schema_enums(load("schemas/v7_1_1_dojo_session.schema.json")))
    dojo_text = json.dumps(load("examples/v7_1_1/dojo_session.example.json"))
    assert "does_not_execute_models" in dojo_text and "does_not_mutate_app_state" in dojo_text
    scoreboard = load("examples/v7_1_1/scoreboard.example.json")
    assert SCORING_DIMS.issubset(set(scoreboard["scoring_dimensions"]))
    assert "not_correctness_proof" in scoreboard["non_claims"] and "not_benchmark_proof" in scoreboard["non_claims"]
    checklist = load("examples/v7_1_1/closure_checklist.example.json")
    assert CLOSURE_CHECKS.issubset(set(checklist["required_checks"]))
    assert "not_release_approval" in checklist["non_claims"]
    matrix = load("examples/v7_1_1/closure_readiness_matrix.example.json")
    assert STATUSES.issubset(schema_enums(load("schemas/v7_1_1_closure_readiness_matrix.schema.json")))
    assert all({"row_id", "subject_ref", "status", "reason", "evidence_refs", "blocking_claim_refs", "pending_claim_refs", "deferred_to"}.issubset(r) for r in matrix["readiness_rows"])
    closure = load("examples/v7_1_1/road_to_100_closure_report.example.json")
    assert closure["known_gaps"] and closure["b7_plus_recommendations"]
    assert "not_release_certification" in closure["non_claims"]
    guards = load("registries/v7_1_1_closure_guard_registry.json")
    assert GUARDS.issubset({g["closure_guard_id"] for g in guards["closure_guards"]})
    handoff = load("examples/v7_1_1/b7_plus_handoff_plan.example.json")
    assert handoff["required_policy_before_provider_runtime"] and handoff["required_receipt_before_provider_runtime"]


def test_boundary_preservation_and_no_forbidden_b6_imports():
    assert "not_apply_gate" in json.dumps(load("examples/v7_1_1/final_gate_advisory.example.json"))
    receipt = load("examples/v7_1_1/receipt_ledger.example.json")
    assert receipt["is_absolute_truth"] is False and receipt["is_runtime_proof"] is False
    assert "disabled" in json.dumps(load("examples/v7_1_1/provider_policy.example.json")).lower()
    assert "static" in json.dumps(load("examples/v7_1_1/thor_odin_bridge_prep.example.json")).lower()
    sdk_text = json.dumps(load("examples/v7_1_1/sdk_app_bridge_prep.example.json"))
    assert "does_not_apply_changes" in sdk_text and "does_not_own_app_state" in sdk_text
    text = TOOL.read_text(encoding="utf-8")
    for bad in ["import requests", "import httpx", "import openai", "import ollama", "import llama_cpp", "API_KEY"]:
        assert bad not in text


def test_b6_static_validator_runs_and_report_is_clean(tmp_path):
    out = tmp_path / "report.json"
    code, report = run_tool(ROOT, out)
    assert code == 0
    assert report["report_id"] == "odin.v7_1_1_b6_acceptance_dojo_scoreboard_closure_report"
    assert report["generated_at_utc"] == "2026-01-01T00:00:00Z"
    assert report["hard_violations"] == []
    assert report["slice_coverage"] == B6_IDS
    assert report["known_gaps"] and report["b7_plus_recommendations"]
    assert str(ROOT) not in json.dumps(report)
    assert not any(part in json.dumps(load("FILE_MANIFEST.json")) for part in [".thor/", ".odin_runtime/", "__pycache__", ".pytest_cache", "egg-info"])


def test_tool_fails_closed_when_bundle_registry_missing(tmp_path):
    repo = clone_minimal(tmp_path)
    (repo / "registries" / "v7_1_1_actual_codex_bundle_plan.json").unlink()
    code, report = run_tool(repo, tmp_path / "out.json")
    assert code == 1
    assert "actual bundle registry missing" in report["hard_violations"]


def mutate_example(repo: Path, rel: str, mutator):
    p = repo / rel
    data = json.loads(p.read_text(encoding="utf-8"))
    mutator(data)
    p.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_negative_contract_mutations_are_flagged(tmp_path):
    cases = []
    cases.append(("missing response_packet_id", "examples/v7_1_1/acceptance_harness.example.json", lambda d: d.pop("response_packet_id"), "Acceptance Harness consumes response_packet_id"))
    cases.append(("app acceptance claim", "examples/v7_1_1/acceptance_harness.example.json", lambda d: d.update({"acceptance_mode": "app_acceptance"}), "Acceptance Harness mode is not app acceptance"))
    cases.append(("production readiness claim", "examples/v7_1_1/scoreboard.example.json", lambda d: d.update({"claim_boundary": "scoreboard_claims_production_readiness"}), "Scoreboard has no production readiness claim"))
    cases.append(("release approval claim", "examples/v7_1_1/closure_checklist.example.json", lambda d: d.update({"claim_boundary": "closure_checklist_claims_release_approval"}), "Closure Checklist has no release approval claim"))
    cases.append(("deployment proof claim", "examples/v7_1_1/closure_readiness_matrix.example.json", lambda d: d.update({"claim_boundary": "closure_matrix_claims_deployment_proof"}), "Closure Matrix has no deployment proof claim"))
    cases.append(("missing known gaps", "examples/v7_1_1/road_to_100_closure_report.example.json", lambda d: d.update({"known_gaps": []}), "Closure Report includes required known_gaps"))
    cases.append(("missing B7 recs", "examples/v7_1_1/road_to_100_closure_report.example.json", lambda d: d.update({"b7_plus_recommendations": []}), "Closure Report includes B7+ recommendations"))
    cases.append(("missing provider policy prereq", "examples/v7_1_1/b7_plus_handoff_plan.example.json", lambda d: d.update({"required_policy_before_provider_runtime": []}), "B7+ Handoff Plan includes provider runtime policy prerequisite"))
    for label, rel, mutator, expected in cases:
        repo = clone_minimal(tmp_path / label.replace(" ", "_"))
        mutate_example(repo, rel, mutator)
        code, report = run_tool(repo, tmp_path / f"{label}.json")
        assert code == 1, label
        assert any(expected in v for v in report["hard_violations"]), report["hard_violations"]


def test_negative_registry_and_boundary_mutations_are_flagged(tmp_path):
    repo = clone_minimal(tmp_path / "guard")
    p = repo / "registries" / "v7_1_1_closure_guard_registry.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["closure_guards"] = [g for g in data["closure_guards"] if g["closure_guard_id"] != "no_release_certification"]
    p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    code, report = run_tool(repo, tmp_path / "guard.json")
    assert code == 1 and any("Closure Guard includes required" in v for v in report["hard_violations"])

    repo = clone_minimal(tmp_path / "fga")
    mutate_example(repo, "examples/v7_1_1/final_gate_advisory.example.json", lambda d: d.update({"non_claims": [], "claim_boundary": "final_gate_as_apply_gate"}))
    code, report = run_tool(repo, tmp_path / "fga.json")
    assert code == 1 and any("Final Gate Advisory remains not Apply Gate" in v for v in report["hard_violations"])

    repo = clone_minimal(tmp_path / "provider")
    TOOL_DST = repo / "tools" / "v7_1_1" / "check_b6_acceptance_dojo_scoreboard_closure.py"
    TOOL_DST.write_text(TOOL_DST.read_text(encoding="utf-8") + "\nimport requests\n", encoding="utf-8")
    code, report = run_tool(repo, tmp_path / "provider.json")
    assert code == 1 and any("forbidden import" in v for v in report["hard_violations"])


def test_tool_writes_only_requested_out(tmp_path):
    repo = clone_minimal(tmp_path / "write_scope")
    before = {p.relative_to(repo).as_posix(): p.stat().st_mtime_ns for p in repo.rglob("*") if p.is_file()}
    out = tmp_path / "nested" / "only_report.json"
    code, _ = run_tool(repo, out)
    after = {p.relative_to(repo).as_posix(): p.stat().st_mtime_ns for p in repo.rglob("*") if p.is_file()}
    assert code == 0
    assert before == after
    assert out.exists()
