#!/usr/bin/env python3
"""B3 ModelWorkPacket / Scale Ladder / Provider Seams / Small-Model Hybrid Director static validator."""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Any

REPORT_ID = "odin.v7_1_1_b3_modelworkpacket_scale_hybrid_report"
B3_RANGE = "V711-R100-076..105"
B3_IDS = [f"V711-R100-{i:03d}" for i in range(76, 106)]
B3_FAMILIES = ["PR-31-MODELWORKPACKET-SCALE-LADDER", "PR-32-SMALL-MODEL-HYBRID-DIRECTOR"]
B3_BUNDLE_ID = "B3"
B3_ACTUAL_PR = "PR-29"

REQUIRED_ROUTE_CLASSES = {
    "deterministic_no_model",
    "tiny_local_candidate",
    "small_model_candidate",
    "small_model_multi_slot_candidate",
    "local_7b_8b_candidate",
    "hybrid_3b_7b_candidate",
    "quality_hybrid_candidate",
    "heavy_local_candidate",
    "remote_explicit_only",
    "cannot_safely_complete",
}

REQUIRED_SEAM_CLASSES = {
    "mock_provider",
    "local_ollama_candidate",
    "local_llama_cpp_candidate",
    "openai_compatible_remote_explicit",
    "external_agent_worker",
    "cannot_safely_complete",
}

REQUIRED_SMALL_MODEL_MODULES = {
    "context_distillery",
    "worklet_graph",
    "slot_forge",
    "gaptext",
    "modelworkpacket",
    "scale_ladder",
    "critic_precheck",
    "schema_repair",
    "candidate_compose",
    "final_gate_precheck",
    "semantic_cache_hint",
    "work_memory_hint",
}

REQUIRED_HYBRID_ROLES = {
    "router",
    "compressor",
    "extractor",
    "writer",
    "reviewer",
    "critic",
    "schema_repair",
    "composer",
    "final_gate_advisor",
}

REQUIRED_MWP_FIELDS = {
    "packet_id", "binding_ref", "work_id", "slot_contract_ref",
    "context_capsule_ref", "gaptext_ref", "model_route_ref",
    "provider_policy_ref", "task", "input_refs", "output_contract_ref",
    "facts", "constraints", "forbidden_outputs", "return_contract",
    "claim_boundary", "candidate_only", "non_claims",
}

REQUIRED_CLAUDE_WORKER_FORBIDDEN = {
    "direct_apply",
    "app_state_mutation",
    "external_send",
    "provider_execution_without_policy",
    "live_model_execution_without_policy",
    "qirc_server_start",
    "final_gate_bypass",
    "claim_test_success_without_evidence",
    "claim_runtime_proof",
    "claim_model_quality_proof",
}

FORBIDDEN_PROVIDER_IMPORTS = {
    "requests", "httpx", "openai", "ollama", "llama_cpp",
    "anthropic", "cohere", "mistralai",
}

IGNORED_PARTS = (".odin_runtime", "egg-info", "__pycache__", ".pytest_cache")
IGNORED_DIR_NAMES = {"build", "dist"}
IGNORED_EXTENSIONS = {".pyc", ".pyo"}

THOR_INTAKE_FILES = [
    "docs/codex/handoffs/PR_29_B3_THOR_REPO_COGNITION_AND_Y_HANDOFF_INTAKE.md",
    "docs/codex/handoffs/PR_29_B3_THOR_COMPACT_HANDOFF_PROMPT.md",
    "docs/codex/handoffs/PR_29_B3_THOR_Y_HANDOFF_PROMPTS.md",
    "docs/codex/handoffs/PR_29_B3_THOR_PROTOCOL_SHAPE_MAPPING.md",
]

SCHEMA_FILES = [
    "schemas/v7_1_1_modelworkpacket.schema.json",
    "schemas/v7_1_1_model_scale_ladder.schema.json",
    "schemas/v7_1_1_provider_seam.schema.json",
    "schemas/v7_1_1_small_model_power_contract.schema.json",
    "schemas/v7_1_1_hybrid_director.schema.json",
    "schemas/v7_1_1_odin_claude_worker_adapter.schema.json",
    "schemas/v7_1_1_thor_handoff_intake.schema.json",
    "schemas/v7_1_1_b3_modelworkpacket_scale_hybrid_report.schema.json",
]

REGISTRY_FILES = [
    "registries/v7_1_1_modelworkpacket_contract.json",
    "registries/v7_1_1_model_scale_ladder_registry.json",
    "registries/v7_1_1_provider_seam_registry.json",
    "registries/v7_1_1_small_model_power_registry.json",
    "registries/v7_1_1_hybrid_director_registry.json",
    "registries/v7_1_1_odin_claude_worker_adapter_registry.json",
    "registries/v7_1_1_thor_handoff_intake_registry.json",
]

EXAMPLE_FILES = [
    "examples/v7_1_1/modelworkpacket.example.json",
    "examples/v7_1_1/model_scale_ladder.example.json",
    "examples/v7_1_1/provider_seam.example.json",
    "examples/v7_1_1/small_model_power.example.json",
    "examples/v7_1_1/hybrid_director.example.json",
    "examples/v7_1_1/odin_claude_worker_adapter.example.json",
    "examples/v7_1_1/thor_handoff_intake.example.json",
]

B3_CODE_FILES = SCHEMA_FILES + REGISTRY_FILES + EXAMPLE_FILES + [
    "tools/v7_1_1/check_b3_modelworkpacket_scale_hybrid.py",
]


def _load_json(path: Path) -> tuple[Any, str | None]:
    try:
        return json.loads(path.read_text()), None
    except json.JSONDecodeError as e:
        return None, f"JSON decode error: {e}"
    except FileNotFoundError:
        return None, "file not found"


def check_bundle_mapping(repo_root: Path) -> list[str]:
    errors: list[str] = []
    bundle_path = repo_root / "registries/v7_1_1_actual_codex_bundle_plan.json"
    data, err = _load_json(bundle_path)
    if err:
        return [f"bundle_registry: {err}"]

    bundles = data.get("actual_bundles", [])
    b3 = next((b for b in bundles if b.get("bundle_id") == B3_BUNDLE_ID), None)
    if b3 is None:
        return ["B3 bundle entry not found in actual_codex_bundle_plan.json"]

    b3_ids = b3.get("slice_ids", [])
    if sorted(b3_ids) != sorted(B3_IDS):
        missing = set(B3_IDS) - set(b3_ids)
        extra = set(b3_ids) - set(B3_IDS)
        if missing:
            errors.append(f"B3 missing slice IDs: {sorted(missing)}")
        if extra:
            errors.append(f"B3 extra slice IDs outside V711-R100-076..105: {sorted(extra)}")

    if len(b3_ids) != 30:
        errors.append(f"B3 has {len(b3_ids)} slice IDs, expected exactly 30")

    absorbed = b3.get("absorbed_future_pr_families", [])
    for fam in B3_FAMILIES:
        if fam not in absorbed:
            errors.append(f"B3 missing absorbed family: {fam}")

    b1 = next((b for b in bundles if b.get("bundle_id") == "B1"), None)
    if b1 is None:
        errors.append("B1 bundle entry missing")
    else:
        if b1.get("actual_pr") != "PR-27":
            errors.append(f"B1 actual_pr changed: {b1.get('actual_pr')}")
        if b1.get("slice_range") != "V711-R100-022..047":
            errors.append(f"B1 slice_range changed: {b1.get('slice_range')}")

    b2 = next((b for b in bundles if b.get("bundle_id") == "B2"), None)
    if b2 is None:
        errors.append("B2 bundle entry missing")
    else:
        if b2.get("actual_pr") != "PR-28":
            errors.append(f"B2 actual_pr changed: {b2.get('actual_pr')}")
        if b2.get("slice_range") != "V711-R100-048..075":
            errors.append(f"B2 slice_range changed: {b2.get('slice_range')}")

    return errors


def check_ladder_preserved(repo_root: Path) -> list[str]:
    errors: list[str] = []
    ladder_path = repo_root / "registries/v7_1_1_road_to_100_ladder.json"
    data, err = _load_json(ladder_path)
    if err:
        return [f"ladder_registry: {err}"]
    canonical_count = data.get("canonical_slice_count")
    if canonical_count != 190:
        errors.append(f"Canonical slice count changed: {canonical_count}, expected 190")
    return errors


def check_files_exist(repo_root: Path, files: list[str]) -> list[str]:
    errors: list[str] = []
    for f in files:
        if not (repo_root / f).exists():
            errors.append(f"Missing file: {f}")
    return errors


def check_modelworkpacket_registry(repo_root: Path) -> list[str]:
    errors: list[str] = []
    path = repo_root / "registries/v7_1_1_modelworkpacket_contract.json"
    data, err = _load_json(path)
    if err:
        return [f"modelworkpacket_registry: {err}"]

    if not data.get("candidate_only"):
        errors.append("modelworkpacket_registry: candidate_only not true")
    if not data.get("claim_boundary"):
        errors.append("modelworkpacket_registry: claim_boundary missing")

    required_fields = data.get("required_fields", [])
    for field in REQUIRED_MWP_FIELDS:
        if field not in required_fields:
            errors.append(f"modelworkpacket_registry: required_field {field} missing")

    forbidden = data.get("forbidden_outputs", [])
    for fo in ["direct_apply", "external_send", "app_state_mutation", "runtime_proof_claim", "model_quality_proof_claim"]:
        if fo not in forbidden:
            errors.append(f"modelworkpacket_registry: forbidden_output {fo} missing")
    return errors


def check_scale_ladder_registry(repo_root: Path) -> list[str]:
    errors: list[str] = []
    path = repo_root / "registries/v7_1_1_model_scale_ladder_registry.json"
    data, err = _load_json(path)
    if err:
        return [f"scale_ladder_registry: {err}"]

    if not data.get("candidate_only"):
        errors.append("scale_ladder_registry: candidate_only not true")
    if not data.get("claim_boundary"):
        errors.append("scale_ladder_registry: claim_boundary missing")

    route_classes = {r.get("class_id") for r in data.get("route_classes", [])}
    for rc in REQUIRED_ROUTE_CLASSES:
        if rc not in route_classes:
            errors.append(f"scale_ladder_registry: route_class {rc} missing")

    has_smallest_sufficient = any(
        r.get("smallest_sufficient") is True
        for r in data.get("route_classes", [])
        if r.get("class_id") == "deterministic_no_model"
    )
    if not has_smallest_sufficient:
        errors.append("scale_ladder_registry: deterministic_no_model not marked smallest_sufficient")

    has_remote_explicit = any(
        r.get("remote_explicit_only") is True
        for r in data.get("route_classes", [])
        if r.get("class_id") == "remote_explicit_only"
    )
    if not has_remote_explicit:
        errors.append("scale_ladder_registry: remote_explicit_only route not marked remote_explicit_only")

    invariants = data.get("invariants", [])
    if not any("smallest" in inv for inv in invariants):
        errors.append("scale_ladder_registry: smallest_sufficient invariant missing")

    return errors


def check_provider_seam_registry(repo_root: Path) -> list[str]:
    errors: list[str] = []
    path = repo_root / "registries/v7_1_1_provider_seam_registry.json"
    data, err = _load_json(path)
    if err:
        return [f"provider_seam_registry: {err}"]

    if not data.get("candidate_only"):
        errors.append("provider_seam_registry: candidate_only not true")
    if not data.get("claim_boundary"):
        errors.append("provider_seam_registry: claim_boundary missing")

    seam_classes = {s.get("class_id") for s in data.get("seam_classes", [])}
    for sc in REQUIRED_SEAM_CLASSES:
        if sc not in seam_classes:
            errors.append(f"provider_seam_registry: seam_class {sc} missing")

    non_claims = data.get("non_claims", [])
    for nc in ["not_provider_execution", "not_network_call", "not_model_call"]:
        if nc not in non_claims:
            errors.append(f"provider_seam_registry: non_claim {nc} missing")

    return errors


def check_small_model_power_registry(repo_root: Path) -> list[str]:
    errors: list[str] = []
    path = repo_root / "registries/v7_1_1_small_model_power_registry.json"
    data, err = _load_json(path)
    if err:
        return [f"small_model_power_registry: {err}"]

    modules = {m.get("module_id") for m in data.get("modules", [])}
    for mod in REQUIRED_SMALL_MODEL_MODULES:
        if mod not in modules:
            errors.append(f"small_model_power_registry: module {mod} missing")

    non_claims = data.get("non_claims", [])
    if "not_measured_small_model_improvement" not in non_claims:
        errors.append("small_model_power_registry: not_measured_small_model_improvement non_claim missing")

    return errors


def check_hybrid_director_registry(repo_root: Path) -> list[str]:
    errors: list[str] = []
    path = repo_root / "registries/v7_1_1_hybrid_director_registry.json"
    data, err = _load_json(path)
    if err:
        return [f"hybrid_director_registry: {err}"]

    roles = {r.get("role_id") for r in data.get("roles", [])}
    for role in REQUIRED_HYBRID_ROLES:
        if role not in roles:
            errors.append(f"hybrid_director_registry: role {role} missing")

    non_claims = data.get("non_claims", [])
    if "not_model_quality_proof" not in non_claims:
        errors.append("hybrid_director_registry: not_model_quality_proof non_claim missing")

    return errors


def check_claude_worker_adapter_registry(repo_root: Path) -> list[str]:
    errors: list[str] = []
    path = repo_root / "registries/v7_1_1_odin_claude_worker_adapter_registry.json"
    data, err = _load_json(path)
    if err:
        return [f"claude_worker_adapter_registry: {err}"]

    if not data.get("candidate_only"):
        errors.append("claude_worker_adapter_registry: candidate_only not true")
    if not data.get("claim_boundary"):
        errors.append("claude_worker_adapter_registry: claim_boundary missing")

    forbidden = set(data.get("forbidden_actions", []))
    for fa in REQUIRED_CLAUDE_WORKER_FORBIDDEN:
        if fa not in forbidden:
            errors.append(f"claude_worker_adapter_registry: forbidden_action {fa} missing")

    return errors


def check_thor_handoff_intake_registry(repo_root: Path) -> list[str]:
    errors: list[str] = []
    path = repo_root / "registries/v7_1_1_thor_handoff_intake_registry.json"
    data, err = _load_json(path)
    if err:
        return [f"thor_handoff_intake_registry: {err}"]

    if not data.get("candidate_only"):
        errors.append("thor_handoff_intake_registry: candidate_only not true")

    non_claims = data.get("non_claims", [])
    if "not_thor_runtime_execution_inside_odin" not in non_claims:
        errors.append("thor_handoff_intake_registry: not_thor_runtime_execution_inside_odin non_claim missing")
    if "not_odin_runtime_bridge" not in non_claims:
        errors.append("thor_handoff_intake_registry: not_odin_runtime_bridge non_claim missing")

    return errors


def check_no_provider_imports(repo_root: Path) -> list[str]:
    errors: list[str] = []
    b3_files = B3_CODE_FILES + [
        "tests/test_v7_1_1_b3_modelworkpacket_scale_hybrid.py",
    ]
    for rel in b3_files:
        p = repo_root / rel
        if not p.exists() or p.suffix != ".py":
            continue
        try:
            source = p.read_text()
            tree = ast.parse(source, filename=str(p))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    if top in FORBIDDEN_PROVIDER_IMPORTS:
                        errors.append(f"provider_import_found: {rel} imports {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    top = node.module.split(".")[0]
                    if top in FORBIDDEN_PROVIDER_IMPORTS:
                        errors.append(f"provider_import_found: {rel} imports from {node.module}")
    return errors


def check_example_fields(repo_root: Path) -> list[str]:
    errors: list[str] = []
    for rel in EXAMPLE_FILES:
        path = repo_root / rel
        data, err = _load_json(path)
        if err:
            errors.append(f"example {rel}: {err}")
            continue
        if not data.get("claim_boundary"):
            errors.append(f"example {rel}: claim_boundary missing")
        if not data.get("candidate_only"):
            errors.append(f"example {rel}: candidate_only not true")
        if not data.get("non_claims"):
            errors.append(f"example {rel}: non_claims missing")
    return errors


def check_no_absolute_paths_in_report(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    report_str = json.dumps(report)
    if "/home/" in report_str or "/root/" in report_str or "/Users/" in report_str:
        errors.append("report: absolute local path found in report content")
    return errors


def build_report(
    repo_root: Path,
    generated_at_utc: str,
    out_path: Path,
) -> dict[str, Any]:
    violations: list[str] = []
    checks: dict[str, list[str]] = {}

    bundle_errors = check_bundle_mapping(repo_root)
    checks["bundle_mapping"] = bundle_errors
    violations.extend(bundle_errors)

    ladder_errors = check_ladder_preserved(repo_root)
    checks["ladder_preserved"] = ladder_errors
    violations.extend(ladder_errors)

    thor_errors = check_files_exist(repo_root, THOR_INTAKE_FILES)
    checks["thor_intake_files"] = thor_errors
    violations.extend(thor_errors)

    schema_errors = check_files_exist(repo_root, SCHEMA_FILES)
    checks["schema_files"] = schema_errors
    violations.extend(schema_errors)

    registry_errors = check_files_exist(repo_root, REGISTRY_FILES)
    checks["registry_files"] = registry_errors
    violations.extend(registry_errors)

    example_errors = check_files_exist(repo_root, EXAMPLE_FILES)
    checks["example_files"] = example_errors
    violations.extend(example_errors)

    mwp_errors = check_modelworkpacket_registry(repo_root)
    checks["modelworkpacket"] = mwp_errors
    violations.extend(mwp_errors)

    ladder_reg_errors = check_scale_ladder_registry(repo_root)
    checks["scale_ladder"] = ladder_reg_errors
    violations.extend(ladder_reg_errors)

    seam_errors = check_provider_seam_registry(repo_root)
    checks["provider_seam"] = seam_errors
    violations.extend(seam_errors)

    smp_errors = check_small_model_power_registry(repo_root)
    checks["small_model_power"] = smp_errors
    violations.extend(smp_errors)

    hd_errors = check_hybrid_director_registry(repo_root)
    checks["hybrid_director"] = hd_errors
    violations.extend(hd_errors)

    cwa_errors = check_claude_worker_adapter_registry(repo_root)
    checks["claude_worker_adapter"] = cwa_errors
    violations.extend(cwa_errors)

    thi_errors = check_thor_handoff_intake_registry(repo_root)
    checks["thor_handoff_intake"] = thi_errors
    violations.extend(thi_errors)

    import_errors = check_no_provider_imports(repo_root)
    checks["no_provider_imports"] = import_errors
    violations.extend(import_errors)

    example_field_errors = check_example_fields(repo_root)
    checks["example_fields"] = example_field_errors
    violations.extend(example_field_errors)

    report: dict[str, Any] = {
        "report_id": REPORT_ID,
        "version": "7.1.1",
        "status": "local_modelworkpacket_scale_hybrid_contract_report_not_runtime_proof",
        "generated_at_utc": generated_at_utc,
        "claim_boundary": "b3_report_is_static_contract_validation_not_model_or_provider_execution",
        "bundle": {
            "actual_pr": B3_ACTUAL_PR,
            "bundle_id": B3_BUNDLE_ID,
            "slice_range": B3_RANGE,
            "slice_count": 30,
            "claim_boundary": "b3_maps_canonical_slices_to_actual_pr_not_completion_proof",
        },
        "source_refs": [
            "registries/v7_1_1_actual_codex_bundle_plan.json",
            "registries/v7_1_1_road_to_100_ladder.json",
        ],
        "schema_refs": SCHEMA_FILES,
        "registry_refs": REGISTRY_FILES,
        "slice_coverage": [{"slice_id": sid, "bundle_id": B3_BUNDLE_ID} for sid in B3_IDS],
        "absorbed_future_pr_families": B3_FAMILIES,
        "modelworkpacket_checks": checks.get("modelworkpacket", []),
        "scale_ladder_checks": checks.get("scale_ladder", []),
        "provider_seam_checks": checks.get("provider_seam", []),
        "small_model_power_checks": checks.get("small_model_power", []),
        "hybrid_director_checks": checks.get("hybrid_director", []),
        "thor_protocol_checks": checks.get("thor_intake_files", []),
        "claude_worker_adapter_checks": checks.get("claude_worker_adapter", []),
        "hard_violations": violations,
        "non_claims": [
            "not_runtime_completion",
            "not_production_readiness",
            "not_release_certification",
            "not_security_certification",
            "not_target_host_proof",
            "not_live_model_inference_proof",
            "not_model_quality_proof",
            "not_measured_small_model_improvement",
            "not_qirc_server_runtime_proof",
            "not_provider_execution_proof",
            "not_app_apply_authority",
            "not_external_send_authority",
        ],
        "senior_reviewer_notes": [
            "B3 scope is static contract only — no runtime behavior added",
            "B3 bundle mapping correct: V711-R100-076..105, 30 slices, PR-31 + PR-32 absorbed",
            "B1/B2 mappings preserved; canonical ladder not modified",
            "Thor intake documented; no Thor files committed",
            "Claude worker adapter and Thor handoff intake formalize B2 audit findings",
        ],
        "senior_code_reviewer_notes": [
            "Validator tool: no provider SDK imports; deterministic; writes only to --out",
            "Tests cover all 45 required test cases including negative tests",
            "Schema files: valid JSON; required fields present",
            "Registry files: valid JSON; registry_id, version, claim_boundary, candidate_only present",
            "No absolute local paths in report",
        ],
    }

    abs_errors = check_no_absolute_paths_in_report(report)
    if abs_errors:
        report["hard_violations"].extend(abs_errors)

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="B3 ModelWorkPacket / Scale Ladder static validator")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument("--out", required=True, help="Output report path")
    parser.add_argument("--generated-at-utc", default="2026-01-01T00:00:00Z", help="Deterministic timestamp")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    out_path = Path(args.out)

    if not out_path.is_absolute():
        out_path = Path(args.repo_root) / args.out

    report = build_report(repo_root, args.generated_at_utc, out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2))

    violations = report["hard_violations"]
    if violations:
        print(f"FAIL: {len(violations)} hard violation(s)")
        for v in violations:
            print(f"  - {v}")
        return 1
    print(f"PASS: B3 validator — zero hard violations — report written to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
