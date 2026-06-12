#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Any

REPORT_ID = "odin.v7_1_1_b1_app_boundary_universal_work_qirc_spine_report"
B1_RANGE = "V711-R100-022..047"
B1_IDS = [f"V711-R100-{i:03d}" for i in range(22, 48)]
B1_FAMILIES = ["PR-27-APP-BOUNDARY-UNIVERSAL-WORK", "PR-28-QIRC-SEMANTIC-BUS"]
FORBIDDEN_ACTIONS = {
    "mutate_app_state", "write_app_storage", "write_project_file",
    "send_external_message", "send_network_request", "publish_public_room",
    "execute_provider", "execute_live_model", "bypass_final_gate",
    "grant_app_authority",
}
APP_OWNED = {
    "app_state", "domain_truth", "domain_database", "project_files", "persistence",
    "apply_gate", "external_send", "user_permissions", "domain_business_rules",
}
ODIN_OWNED = {
    "work_intake_validation", "manifest_validation", "binding_validation",
    "universal_work_validation", "candidate_generation",
    "semantic_event_coordination_contracts", "claim_boundary_validation",
    "final_gate_recommendation",
}
LIFECYCLE_STATES = {
    "received", "manifest_checked", "binding_checked", "artifact_validated",
    "verb_resolved", "output_contract_checked", "privacy_checked",
    "model_policy_checked", "qirc_policy_checked", "compiled", "ready_for_context",
    "blocked", "needs_context", "cannot_safely_complete",
}
FAILURE_REASONS = {
    "missing_manifest", "missing_binding", "unknown_artifact_family",
    "forbidden_transformation_verb", "forbidden_output_contract",
    "privacy_class_denied", "candidate_only_false", "direct_apply_requested",
    "external_send_requested", "app_state_mutation_requested",
    "project_file_write_requested", "provider_execution_requested",
    "live_model_execution_requested", "qirc_channel_denied", "missing_claim_boundary",
}
CHANNELS = {
    "#odin.work", "#odin.context", "#odin.lens", "#odin.precompute",
    "#odin.worklet", "#odin.slot", "#odin.gaptext", "#odin.model_packet",
    "#odin.critic", "#odin.candidate", "#odin.final_gate", "#odin.trace",
    "#odin.receipt", "#app.digest", "#app.boundary",
}
FORBIDDEN_INTENTS = {
    "apply_app_change", "mutate_app_state", "write_project_file",
    "send_external_message", "publish_public_channel", "execute_provider",
    "execute_live_model", "bypass_final_gate",
}
EXPECTED_FILES = [
    "registries/v7_1_1_actual_codex_bundle_plan.json",
    "schemas/v7_1_1_app_manifest.schema.json",
    "registries/v7_1_1_app_manifest_contract.json",
    "examples/v7_1_1/app_manifest.example.json",
    "schemas/v7_1_1_binding_contract.schema.json",
    "registries/v7_1_1_binding_contract_registry.json",
    "examples/v7_1_1/binding_contract.example.json",
    "schemas/v7_1_1_universal_work.schema.json",
    "registries/v7_1_1_universal_work_contract.json",
    "examples/v7_1_1/universal_work.example.json",
    "schemas/v7_1_1_semantic_bus_event.schema.json",
    "schemas/v7_1_1_semantic_bus_channel.schema.json",
    "registries/v7_1_1_semantic_bus_spine_registry.json",
    "examples/v7_1_1/semantic_bus_event.example.json",
    "examples/v7_1_1/semantic_bus_channel.example.json",
    "schemas/v7_1_1_b1_app_boundary_universal_work_qirc_spine_report.schema.json",
]
IGNORED_PARTS = (".odin_runtime", "egg-info", "__pycache__", ".pytest_cache", "build", "dist")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel_display(repo: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo.resolve()).as_posix()
    except ValueError:
        return path.name


def add_check(bucket: list[dict[str, Any]], check_id: str, ok: bool, detail: str) -> None:
    bucket.append({"check_id": check_id, "status": "ok" if ok else "violation", "detail": detail})


def validate(args: argparse.Namespace) -> dict[str, Any]:
    repo = Path(args.repo_root).resolve()
    violations: list[str] = []
    app_checks: list[dict[str, Any]] = []
    binding_checks: list[dict[str, Any]] = []
    work_checks: list[dict[str, Any]] = []
    bus_checks: list[dict[str, Any]] = []
    hidden_checks: list[dict[str, Any]] = []

    for rel in EXPECTED_FILES:
        if not (repo / rel).exists():
            violations.append(f"missing expected file: {rel}")

    bundle_path = Path(args.bundle_plan) if args.bundle_plan else repo / "registries/v7_1_1_actual_codex_bundle_plan.json"
    ladder_path = repo / "registries/v7_1_1_road_to_100_ladder.json"
    manifest_path = Path(args.app_manifest) if args.app_manifest else repo / "examples/v7_1_1/app_manifest.example.json"
    binding_path = Path(args.binding) if args.binding else repo / "examples/v7_1_1/binding_contract.example.json"
    work_registry_path = repo / "registries/v7_1_1_universal_work_contract.json"
    bus_registry_path = repo / "registries/v7_1_1_semantic_bus_spine_registry.json"
    event_path = Path(args.semantic_event) if args.semantic_event else repo / "examples/v7_1_1/semantic_bus_event.example.json"

    source_refs = ["registries/v7_1_1_road_to_100_ladder.json", rel_display(repo, bundle_path)]
    schema_refs = [rel for rel in EXPECTED_FILES if rel.startswith("schemas/")]
    registry_refs = [rel for rel in EXPECTED_FILES if rel.startswith("registries/")]

    ladder = None
    bundle = None
    try:
        ladder = load_json(ladder_path)
        bundle = load_json(bundle_path)
    except Exception as exc:
        violations.append(f"bundle or ladder load failed: {exc}")

    b1 = None
    canonical_ids = set()
    if ladder:
        canonical_ids = {s.get("id") for s in ladder.get("slices", [])}
    if bundle:
        bundles = bundle.get("actual_bundles", [])
        for item in bundles:
            if item.get("bundle_id") == "B1" or item.get("actual_pr") == "PR-27":
                b1 = item
                break
        if not b1:
            violations.append("B1 bundle mapping missing")
        else:
            ids = b1.get("slice_ids", [])
            families = b1.get("absorbed_future_pr_families", [])
            if b1.get("slice_range") != B1_RANGE:
                violations.append("B1 slice range mismatch")
            if ids != B1_IDS:
                violations.append("B1 slice IDs must exactly cover V711-R100-022..047")
            if len(ids) != 26:
                violations.append("B1 must include exactly 26 slice IDs")
            if [x for x in ids if x not in B1_IDS]:
                violations.append("B1 includes out-of-range slice IDs")
            if not set(B1_FAMILIES).issubset(set(families)) or len(families) != 2:
                violations.append("B1 absorbed future PR families mismatch")
            if any(x not in canonical_ids for x in ids):
                violations.append("B1 references slice IDs absent from canonical ladder")

    try:
        manifest = load_json(manifest_path)
        missing = sorted(FORBIDDEN_ACTIONS - set(manifest.get("forbidden_actions", [])))
        add_check(app_checks, "manifest_forbidden_actions", not missing, f"missing={missing}")
        missing_app = sorted(APP_OWNED - set(manifest.get("app_owned_authorities", [])))
        add_check(app_checks, "manifest_app_owned_authorities", not missing_app, f"missing={missing_app}")
        odin_values = {x.get("authority") if isinstance(x, dict) else x for x in manifest.get("odin_owned_authorities", [])}
        missing_odin = sorted(ODIN_OWNED - odin_values)
        add_check(app_checks, "manifest_odin_owned_candidate_authorities", not missing_odin, f"missing={missing_odin}")
        if any((isinstance(x, dict) and x.get("candidate_only") is not True) for x in manifest.get("odin_owned_authorities", [])):
            violations.append("manifest Odin-owned authorities must remain candidate-only")
        if not manifest.get("claim_boundary") or not manifest.get("non_claims"):
            violations.append("manifest missing claim boundary or non-claims")
        if "mutate_app_state" not in manifest.get("forbidden_actions", []):
            violations.append("manifest allows direct app state mutation")
    except Exception as exc:
        violations.append(f"manifest validation failed: {exc}")

    try:
        binding = load_json(binding_path)
        add_check(binding_checks, "binding_candidate_only", binding.get("candidate_only") is True, "candidate_only must be true")
        if binding.get("candidate_only") is not True:
            violations.append("binding candidate_only must be true")
        for key in ["app_owned_apply", "app_owned_state", "app_owned_external_send"]:
            add_check(binding_checks, f"binding_{key}", binding.get(key) is True, f"{key} must remain true")
            if binding.get(key) is not True:
                violations.append(f"binding cannot transfer {key} to Odin")
        if not binding.get("claim_boundary"):
            violations.append("binding missing claim boundary")
    except Exception as exc:
        violations.append(f"binding validation failed: {exc}")

    try:
        work_registry = load_json(work_registry_path)
        states = set(work_registry.get("required_lifecycle_states", []))
        failures = set(work_registry.get("required_failure_reasons", []))
        add_check(work_checks, "universal_work_lifecycle", LIFECYCLE_STATES.issubset(states), "required lifecycle states present")
        add_check(work_checks, "universal_work_failure_reasons", FAILURE_REASONS.issubset(failures), "required failure reasons present")
        if not LIFECYCLE_STATES.issubset(states):
            violations.append("Universal Work lifecycle states incomplete")
        if not FAILURE_REASONS.issubset(failures):
            violations.append("Universal Work failure reasons incomplete")
        if not work_registry.get("claim_boundary"):
            violations.append("Universal Work contract missing claim boundary")
    except Exception as exc:
        violations.append(f"Universal Work validation failed: {exc}")

    try:
        bus = load_json(bus_registry_path)
        channel_names = {c.get("channel") for c in bus.get("channels", [])}
        intents = set(bus.get("required_forbidden_event_intents", []))
        add_check(bus_checks, "semantic_bus_channels", CHANNELS.issubset(channel_names), "required channel families present")
        add_check(bus_checks, "semantic_bus_forbidden_intents", FORBIDDEN_INTENTS.issubset(intents), "required forbidden intents present")
        if not CHANNELS.issubset(channel_names):
            violations.append("Semantic Bus channels incomplete")
        if not FORBIDDEN_INTENTS.issubset(intents):
            violations.append("Semantic Bus forbidden intents incomplete")
        if any(c.get("local_only") is not True for c in bus.get("channels", [])):
            violations.append("Semantic Bus channels must be local-only contracts")
        event = load_json(event_path)
        intent = event.get("intent")
        add_check(hidden_checks, "semantic_event_intent_not_forbidden", intent not in FORBIDDEN_INTENTS, f"intent={intent}")
        if intent in FORBIDDEN_INTENTS:
            violations.append(f"semantic bus event uses forbidden intent: {intent}")
        if event.get("candidate_only") is not True:
            violations.append("semantic bus event candidate_only must be true")
    except Exception as exc:
        violations.append(f"Semantic Bus validation failed: {exc}")

    manifest_data = None
    binding_data = None
    try:
        manifest_data = load_json(manifest_path)
        binding_data = load_json(binding_path)
    except Exception:
        pass
    if manifest_data:
        for action in ["write_project_file", "send_external_message", "execute_provider", "execute_live_model", "bypass_final_gate", "publish_public_room"]:
            ok = action in manifest_data.get("forbidden_actions", [])
            add_check(hidden_checks, f"hidden_authority_{action}_forbidden", ok, "manifest forbids hidden authority intent")
            if not ok:
                violations.append(f"manifest does not forbid {action}")
    if binding_data:
        for action in ["write_project_file", "send_external_message", "execute_provider", "execute_live_model", "bypass_final_gate"]:
            if action not in binding_data.get("forbidden_actions", []):
                violations.append(f"binding does not forbid {action}")

    file_manifest_path = repo / "FILE_MANIFEST.json"
    if file_manifest_path.exists():
        try:
            fm = load_json(file_manifest_path)
            bad = []
            for item in fm.get("files", []):
                path_value = item.get("path", "")
                parts = set(Path(path_value).parts)
                if any(part in parts for part in IGNORED_PARTS):
                    bad.append(path_value)
            if bad:
                violations.append(f"FILE_MANIFEST contains ignored/local artifacts: {bad[:5]}")
        except Exception as exc:
            violations.append(f"FILE_MANIFEST validation failed: {exc}")

    out_path = Path(args.out)
    try:
        out_resolved = out_path.resolve()
        if not out_resolved.parent.exists():
            violations.append("requested report parent does not exist")
    except Exception as exc:
        violations.append(f"requested report path invalid: {exc}")

    report = {
        "report_id": REPORT_ID,
        "version": "7.1.1",
        "status": "local_contract_spine_report_not_runtime_proof",
        "generated_at_utc": args.generated_at_utc,
        "claim_boundary": "b1_report_is_static_contract_validation_not_runtime_completion",
        "bundle": {
            "actual_pr": "PR-27",
            "bundle_id": "B1",
            "slice_range": B1_RANGE,
            "slice_count": 26,
            "claim_boundary": "bundle_report_maps_contract_spine_not_runtime_completion",
        },
        "source_refs": source_refs,
        "schema_refs": schema_refs,
        "registry_refs": registry_refs,
        "slice_coverage": [{"slice_id": x, "status": "mapped_not_runtime_proof"} for x in B1_IDS],
        "absorbed_future_pr_families": B1_FAMILIES,
        "app_manifest_checks": app_checks,
        "binding_contract_checks": binding_checks,
        "universal_work_checks": work_checks,
        "semantic_bus_checks": bus_checks,
        "hidden_authority_checks": hidden_checks,
        "hard_violations": violations,
        "non_claims": [
            "no runtime completion claim",
            "no production readiness claim",
            "no release certification claim",
            "no security certification claim",
            "no target-host proof claim",
            "no live model inference proof claim",
            "no model quality proof claim",
            "no QIRC server runtime proof claim",
            "no provider execution proof claim",
            "no app-owned apply/state/external-send authority claim",
        ],
        "senior_reviewer_notes": [
            "B1 maps canonical slices while preserving the canonical ladder as source input.",
            "Contracts keep app state, apply, persistence, and external send app-owned.",
            "QIRC/Semantic Bus entries are local coordination contracts only.",
        ],
        "senior_code_reviewer_notes": [
            "Validator is deterministic for a supplied timestamp and writes only the requested report path.",
            "Negative hidden-authority checks fail closed on forbidden manifest, binding, and event inputs.",
            "No provider, live model, network, or QIRC server behavior is executed.",
        ],
    }
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--generated-at-utc", required=True)
    parser.add_argument("--bundle-plan")
    parser.add_argument("--app-manifest")
    parser.add_argument("--binding")
    parser.add_argument("--semantic-event")
    args = parser.parse_args(argv)
    report = validate(args)
    out = Path(args.out)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if not report["hard_violations"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
