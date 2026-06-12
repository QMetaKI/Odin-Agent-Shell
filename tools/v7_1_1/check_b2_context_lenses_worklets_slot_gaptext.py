#!/usr/bin/env python3
"""B2 Context / Lenses / Worklets / Slot Forge / Gaptext static validator."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REPORT_ID = "odin.v7_1_1_b2_context_lenses_worklets_slot_gaptext_report"
B2_RANGE = "V711-R100-048..075"
B2_IDS = [f"V711-R100-{i:03d}" for i in range(48, 76)]
B2_FAMILIES = ["PR-29-CONTEXT-LENSES", "PR-30-WORKLETS-SLOTS-GAPTEXT"]

REQUIRED_ARTIFACT_FAMILIES = {
    "text_document", "data_config", "code_repo", "app_runtime",
    "game_interactive", "media_reference", "semantic_event", "candidate_artifact",
}
REQUIRED_LENSES = {
    "summarize", "extract", "rewrite", "review", "plan", "classify",
    "compare", "trace", "contract_check", "schema_map", "context_distill",
    "slot_prepare", "gaptext_prepare",
}
REQUIRED_FORBIDDEN_SHAPES = {
    "direct_apply", "external_send", "app_state_mutation",
    "provider_execution", "live_model_execution",
    "qirc_server_claim", "production_readiness_claim",
}
REQUIRED_CAPSULE_FIELDS = {
    "capsule_id", "binding_ref", "work_ref", "task_center",
    "must_use_refs", "must_not_use_refs", "style_constraints",
    "output_constraints", "claim_boundary", "source_refs",
    "omitted_context", "open_questions", "confidence",
    "privacy_class", "candidate_only", "non_claims",
}
DISTILLERY_FORBIDDEN = {
    "raw_app_database_mirror", "secret_capture", "app_state_ownership",
    "external_send", "provider_execution", "live_model_execution",
}
WORKLET_NODE_FIELDS = {
    "node_id", "node_type", "input_refs", "output_contract_ref",
    "slot_contract_ref", "allowed_route", "forbidden_actions", "claim_boundary",
}
WORKLET_FORBIDDEN_ACTIONS = {
    "direct_apply", "external_send", "app_state_mutation",
    "provider_execution_without_policy", "live_model_execution_without_policy",
    "qirc_server_start", "final_gate_bypass",
}
REQUIRED_ROUTE_CLASSES = {
    "deterministic_no_model", "small_model_candidate", "hybrid_candidate",
    "remote_explicit_only", "cannot_safely_complete",
}
SLOT_FIELDS = {
    "slot_contract_id", "binding_ref", "worklet_ref", "input_kind",
    "output_schema_ref", "route_class", "allowed_model_route", "token_budget",
    "forbidden_claims", "retry_policy", "fallback_policy",
    "claim_boundary", "candidate_only", "non_claims",
}
GAPTEXT_FIELDS = {
    "gaptext_id", "binding_ref", "slot_contract_ref", "context_capsule_ref",
    "task_instruction", "facts", "constraints", "forbidden_outputs",
    "required_output_shape", "claim_boundary", "candidate_only", "non_claims",
}
GAPTEXT_FORBIDDEN_OUTPUTS = {
    "direct_apply_instruction", "external_api_call", "app_state_write",
    "runtime_proof_claim",
}
IGNORED_PARTS = (".odin_runtime", "egg-info", "__pycache__", ".pytest_cache")
IGNORED_DIR_NAMES = {"build", "dist"}
IGNORED_EXTENSIONS = {".pyc", ".pyo"}

HANDOFF_FILES = [
    "docs/codex/handoffs/PR_28_B2_THOR_REPO_COGNITION_HANDOFF.md",
    "docs/codex/handoffs/PR_28_B2_THOR_COMPACT_HANDOFF_PROMPT.md",
    "docs/codex/handoffs/PR_28_B2_THOR_HANDOFF_PROMPTS.md",
    "docs/codex/handoffs/PR_28_B2_Y_HANDOFF_INTAKE_SUMMARY.md",
    "docs/codex/handoffs/PR_28_B2_ODIN_CLAUDE_WORK_PACKET.md",
    "docs/codex/audits/PR_28_B2_THOR_ODIN_CLAUDE_CODE_AUDIT.md",
    "registries/v7_1_1_llm_work_audit_findings_registry.json",
]

SCHEMA_FILES = [
    "schemas/v7_1_1_artifact_family.schema.json",
    "schemas/v7_1_1_artifact_lens.schema.json",
    "schemas/v7_1_1_output_contract.schema.json",
    "schemas/v7_1_1_context_capsule.schema.json",
    "schemas/v7_1_1_worklet_graph.schema.json",
    "schemas/v7_1_1_slot_contract.schema.json",
    "schemas/v7_1_1_gaptext.schema.json",
    "schemas/v7_1_1_b2_context_lenses_worklets_slot_gaptext_report.schema.json",
]

REGISTRY_FILES = [
    "registries/v7_1_1_artifact_family_registry.json",
    "registries/v7_1_1_artifact_lens_registry.json",
    "registries/v7_1_1_output_contract_registry.json",
    "registries/v7_1_1_context_distillery_contract.json",
    "registries/v7_1_1_worklet_graph_contract.json",
    "registries/v7_1_1_slot_forge_contract_registry.json",
    "registries/v7_1_1_gaptext_contract.json",
]

EXAMPLE_FILES = [
    "examples/v7_1_1/artifact_family.example.json",
    "examples/v7_1_1/artifact_lens.example.json",
    "examples/v7_1_1/output_contract.example.json",
    "examples/v7_1_1/context_capsule.example.json",
    "examples/v7_1_1/worklet_graph.example.json",
    "examples/v7_1_1/slot_contract.example.json",
    "examples/v7_1_1/gaptext.example.json",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def add_check(bucket: list[dict[str, Any]], check_id: str, ok: bool, detail: str) -> None:
    bucket.append({"check_id": check_id, "status": "ok" if ok else "violation", "detail": detail})


def validate(args: argparse.Namespace) -> dict[str, Any]:
    repo = Path(args.repo_root).resolve()
    violations: list[str] = []
    family_checks: list[dict] = []
    lens_checks: list[dict] = []
    oc_checks: list[dict] = []
    capsule_checks: list[dict] = []
    worklet_checks: list[dict] = []
    slot_checks: list[dict] = []
    gaptext_checks: list[dict] = []

    # --- File existence ---
    for rel in HANDOFF_FILES + SCHEMA_FILES + REGISTRY_FILES + EXAMPLE_FILES:
        if not (repo / rel).exists():
            violations.append(f"missing expected file: {rel}")

    # --- Bundle plan / ladder ---
    bundle_path = repo / "registries/v7_1_1_actual_codex_bundle_plan.json"
    ladder_path = repo / "registries/v7_1_1_road_to_100_ladder.json"

    bundle = None
    ladder = None
    try:
        bundle = load_json(bundle_path)
        ladder = load_json(ladder_path)
    except Exception as exc:
        violations.append(f"bundle or ladder load failed: {exc}")

    canonical_ids: set[str] = set()
    if ladder:
        canonical_ids = {s.get("id") for s in ladder.get("slices", [])}

    b2 = None
    b1 = None
    if bundle:
        for item in bundle.get("actual_bundles", []):
            if item.get("bundle_id") == "B2" or item.get("actual_pr") == "PR-28":
                b2 = item
            if item.get("bundle_id") == "B1" or item.get("actual_pr") == "PR-27":
                b1 = item

        if not b2:
            violations.append("B2 bundle mapping missing from actual_codex_bundle_plan.json")
        else:
            ids = b2.get("slice_ids", [])
            families = b2.get("absorbed_future_pr_families", [])
            sr = b2.get("slice_range", "")
            add_check(family_checks, "b2_slice_range", sr == B2_RANGE,
                      f"slice_range={sr!r} expected {B2_RANGE!r}")
            if sr != B2_RANGE:
                violations.append(f"B2 slice_range mismatch: {sr!r}")
            add_check(family_checks, "b2_exact_28_slices", len(ids) == 28,
                      f"slice count={len(ids)} expected 28")
            if len(ids) != 28:
                violations.append(f"B2 must include exactly 28 slice IDs (got {len(ids)})")
            out_of_range = [x for x in ids if x not in B2_IDS]
            add_check(family_checks, "b2_no_out_of_range_slices", not out_of_range,
                      f"out_of_range={out_of_range}")
            if out_of_range:
                violations.append(f"B2 includes out-of-range slice IDs: {out_of_range}")
            missing_fams = [f for f in B2_FAMILIES if f not in families]
            add_check(family_checks, "b2_absorbed_families", not missing_fams,
                      f"missing absorbed families={missing_fams}")
            if missing_fams:
                violations.append(f"B2 missing absorbed families: {missing_fams}")
            extra_fams = [f for f in families if f not in B2_FAMILIES]
            if extra_fams:
                violations.append(f"B2 has unexpected absorbed families: {extra_fams}")
            if canonical_ids:
                bad_ids = [x for x in ids if x not in canonical_ids]
                if bad_ids:
                    violations.append(f"B2 references slice IDs absent from canonical ladder: {bad_ids}")

        if not b1:
            violations.append("B1 bundle mapping missing — B1 must be preserved")
        else:
            add_check(family_checks, "b1_preserved", True, "B1 bundle mapping present")
            if b1.get("slice_range") != "V711-R100-022..047":
                violations.append("B1 slice_range changed — B1 must be preserved unchanged")
            if b1.get("actual_pr") != "PR-27":
                violations.append("B1 actual_pr changed — B1 must be preserved unchanged")

    # --- Artifact families ---
    fam_path = repo / "registries/v7_1_1_artifact_family_registry.json"
    if fam_path.exists():
        try:
            fam_reg = load_json(fam_path)
            found_fams = {f.get("family_id") for f in fam_reg.get("families", [])}
            missing_fams = sorted(REQUIRED_ARTIFACT_FAMILIES - found_fams)
            add_check(family_checks, "artifact_families_complete", not missing_fams,
                      f"missing={missing_fams}")
            if missing_fams:
                violations.append(f"artifact_family_registry missing families: {missing_fams}")
            if not fam_reg.get("claim_boundary"):
                violations.append("artifact_family_registry missing claim_boundary")
        except Exception as exc:
            violations.append(f"artifact_family_registry load failed: {exc}")

    # --- Lenses ---
    lens_path = repo / "registries/v7_1_1_artifact_lens_registry.json"
    if lens_path.exists():
        try:
            lens_reg = load_json(lens_path)
            found_lenses = {l.get("lens_id") for l in lens_reg.get("lenses", [])}
            missing_lenses = sorted(REQUIRED_LENSES - found_lenses)
            add_check(lens_checks, "artifact_lenses_complete", not missing_lenses,
                      f"missing={missing_lenses}")
            if missing_lenses:
                violations.append(f"artifact_lens_registry missing lenses: {missing_lenses}")
            if not lens_reg.get("claim_boundary"):
                violations.append("artifact_lens_registry missing claim_boundary")
        except Exception as exc:
            violations.append(f"artifact_lens_registry load failed: {exc}")

    # --- Output contracts ---
    oc_path = repo / "registries/v7_1_1_output_contract_registry.json"
    if oc_path.exists():
        try:
            oc_reg = load_json(oc_path)
            for contract in oc_reg.get("contracts", []):
                cid = contract.get("contract_id", "unknown")
                forbidden = set(contract.get("forbidden_shapes", []))
                missing_forbidden = sorted(REQUIRED_FORBIDDEN_SHAPES - forbidden)
                add_check(oc_checks, f"oc_{cid}_forbidden_shapes", not missing_forbidden,
                          f"missing forbidden shapes={missing_forbidden}")
                if missing_forbidden:
                    violations.append(f"output_contract {cid} missing forbidden shapes: {missing_forbidden}")
                if contract.get("candidate_only") is not True:
                    violations.append(f"output_contract {cid} must have candidate_only: true")
                if not contract.get("claim_boundary"):
                    violations.append(f"output_contract {cid} missing claim_boundary")
        except Exception as exc:
            violations.append(f"output_contract_registry load failed: {exc}")

    # --- Context capsule example ---
    cap_path = repo / "examples/v7_1_1/context_capsule.example.json"
    if cap_path.exists():
        try:
            cap = load_json(cap_path)
            missing_fields = sorted(REQUIRED_CAPSULE_FIELDS - set(cap.keys()))
            add_check(capsule_checks, "context_capsule_fields", not missing_fields,
                      f"missing={missing_fields}")
            if missing_fields:
                violations.append(f"context_capsule.example missing fields: {missing_fields}")
            if cap.get("candidate_only") is not True:
                violations.append("context_capsule.example must have candidate_only: true")
            if not cap.get("claim_boundary"):
                violations.append("context_capsule.example missing claim_boundary")
        except Exception as exc:
            violations.append(f"context_capsule.example load failed: {exc}")

    # --- Context distillery invariants ---
    ctx_path = repo / "registries/v7_1_1_context_distillery_contract.json"
    if ctx_path.exists():
        try:
            ctx = load_json(ctx_path)
            forbidden = set(ctx.get("forbidden_actions", []))
            missing_distillery_forbidden = sorted(DISTILLERY_FORBIDDEN - forbidden)
            add_check(capsule_checks, "distillery_forbidden_actions", not missing_distillery_forbidden,
                      f"missing={missing_distillery_forbidden}")
            if missing_distillery_forbidden:
                violations.append(f"context_distillery missing forbidden actions: {missing_distillery_forbidden}")
        except Exception as exc:
            violations.append(f"context_distillery_contract load failed: {exc}")

    # --- Worklet graph ---
    wg_path = repo / "examples/v7_1_1/worklet_graph.example.json"
    if wg_path.exists():
        try:
            wg = load_json(wg_path)
            for node in wg.get("nodes", []):
                nid = node.get("node_id", "unknown")
                missing_node_fields = sorted(WORKLET_NODE_FIELDS - set(node.keys()))
                add_check(worklet_checks, f"worklet_node_{nid}_fields", not missing_node_fields,
                          f"missing={missing_node_fields}")
                if missing_node_fields:
                    violations.append(f"worklet node {nid} missing fields: {missing_node_fields}")
                node_forbidden = set(node.get("forbidden_actions", []))
                missing_wf = sorted(WORKLET_FORBIDDEN_ACTIONS - node_forbidden)
                add_check(worklet_checks, f"worklet_node_{nid}_forbidden", not missing_wf,
                          f"missing forbidden actions={missing_wf}")
                if missing_wf:
                    violations.append(f"worklet node {nid} missing forbidden actions: {missing_wf}")
            if wg.get("candidate_only") is not True:
                violations.append("worklet_graph.example must have candidate_only: true")
            if not wg.get("claim_boundary"):
                violations.append("worklet_graph.example missing claim_boundary")
        except Exception as exc:
            violations.append(f"worklet_graph.example load failed: {exc}")

    # --- Worklet graph contract ---
    wgc_path = repo / "registries/v7_1_1_worklet_graph_contract.json"
    if wgc_path.exists():
        try:
            wgc = load_json(wgc_path)
            if not wgc.get("claim_boundary"):
                violations.append("worklet_graph_contract missing claim_boundary")
        except Exception as exc:
            violations.append(f"worklet_graph_contract load failed: {exc}")

    # --- Slot forge ---
    sf_path = repo / "registries/v7_1_1_slot_forge_contract_registry.json"
    if sf_path.exists():
        try:
            sf = load_json(sf_path)
            found_routes = {r.get("route_class") for r in sf.get("route_classes", [])}
            missing_routes = sorted(REQUIRED_ROUTE_CLASSES - found_routes)
            add_check(slot_checks, "slot_route_classes", not missing_routes,
                      f"missing={missing_routes}")
            if missing_routes:
                violations.append(f"slot_forge_contract_registry missing route classes: {missing_routes}")
            if not sf.get("claim_boundary"):
                violations.append("slot_forge_contract_registry missing claim_boundary")
        except Exception as exc:
            violations.append(f"slot_forge_contract_registry load failed: {exc}")

    # --- Slot contract example ---
    sc_path = repo / "examples/v7_1_1/slot_contract.example.json"
    if sc_path.exists():
        try:
            sc = load_json(sc_path)
            missing_slot_fields = sorted(SLOT_FIELDS - set(sc.keys()))
            add_check(slot_checks, "slot_contract_fields", not missing_slot_fields,
                      f"missing={missing_slot_fields}")
            if missing_slot_fields:
                violations.append(f"slot_contract.example missing fields: {missing_slot_fields}")
            if sc.get("candidate_only") is not True:
                violations.append("slot_contract.example must have candidate_only: true")
            if not sc.get("claim_boundary"):
                violations.append("slot_contract.example missing claim_boundary")
            # slot contract must be contract-only, not implement actual routing
            non_claims = sc.get("non_claims", [])
            if not any("actual model routing" in nc for nc in non_claims):
                violations.append("slot_contract.example must explicitly state it does not implement actual model routing")
        except Exception as exc:
            violations.append(f"slot_contract.example load failed: {exc}")

    # --- Gaptext ---
    gt_path = repo / "examples/v7_1_1/gaptext.example.json"
    if gt_path.exists():
        try:
            gt = load_json(gt_path)
            missing_gt_fields = sorted(GAPTEXT_FIELDS - set(gt.keys()))
            add_check(gaptext_checks, "gaptext_fields", not missing_gt_fields,
                      f"missing={missing_gt_fields}")
            if missing_gt_fields:
                violations.append(f"gaptext.example missing fields: {missing_gt_fields}")
            if gt.get("candidate_only") is not True:
                violations.append("gaptext.example must have candidate_only: true")
            if not gt.get("claim_boundary"):
                violations.append("gaptext.example missing claim_boundary")
            forbidden_outputs = set(gt.get("forbidden_outputs", []))
            missing_go = sorted(GAPTEXT_FORBIDDEN_OUTPUTS - forbidden_outputs)
            add_check(gaptext_checks, "gaptext_forbidden_outputs", not missing_go,
                      f"missing={missing_go}")
            if missing_go:
                violations.append(f"gaptext.example missing forbidden outputs: {missing_go}")
        except Exception as exc:
            violations.append(f"gaptext.example load failed: {exc}")

    # --- Gaptext contract ---
    gtc_path = repo / "registries/v7_1_1_gaptext_contract.json"
    if gtc_path.exists():
        try:
            gtc = load_json(gtc_path)
            if not gtc.get("claim_boundary"):
                violations.append("gaptext_contract missing claim_boundary")
        except Exception as exc:
            violations.append(f"gaptext_contract load failed: {exc}")

    # --- Absolute path check in report ---
    # Report is written to --out, which may contain the repo root path.
    # We just check the source_refs do not include absolute paths for existing refs.
    # (The report itself is generated here, so we skip self-check.)

    # --- FILE_MANIFEST ignored path check ---
    manifest_path = repo / "FILE_MANIFEST.json"
    if manifest_path.exists():
        try:
            mf = load_json(manifest_path)
            for f in mf.get("files", []):
                fp = f.get("path", "")
                fp_parts = set(Path(fp).parts)
                # Check for ignored substrings (cache dirs, egg-info, etc.)
                if any(bad in part for part in fp_parts for bad in IGNORED_PARTS):
                    violations.append(f"FILE_MANIFEST contains ignored path: {fp}")
                    continue
                # Check for exact directory name matches (build/, dist/)
                if fp_parts & IGNORED_DIR_NAMES:
                    violations.append(f"FILE_MANIFEST contains ignored path: {fp}")
                    continue
                # Check for generated file extensions
                if Path(fp).suffix in IGNORED_EXTENSIONS:
                    violations.append(f"FILE_MANIFEST contains ignored path: {fp}")
        except Exception as exc:
            violations.append(f"FILE_MANIFEST load failed: {exc}")

    # --- Compute audit refs ---
    thor_audit_refs = [r for r in HANDOFF_FILES if (repo / r).exists()]

    # --- Source refs ---
    source_refs = [
        "registries/v7_1_1_road_to_100_ladder.json",
        "registries/v7_1_1_actual_codex_bundle_plan.json",
    ]

    report = {
        "report_id": REPORT_ID,
        "version": "7.1.1",
        "status": "local_contract_compiler_report_not_runtime_proof",
        "generated_at_utc": args.generated_at_utc,
        "claim_boundary": "b2_report_is_static_contract_validation_not_runtime_completion",
        "bundle": {
            "bundle_id": "B2",
            "actual_pr": "PR-28",
            "slice_range": B2_RANGE,
            "exact_slice_count": 28,
            "slice_ids": B2_IDS,
        },
        "source_refs": source_refs,
        "schema_refs": SCHEMA_FILES,
        "registry_refs": REGISTRY_FILES,
        "slice_coverage": B2_IDS,
        "absorbed_future_pr_families": B2_FAMILIES,
        "artifact_family_checks": family_checks,
        "lens_checks": lens_checks,
        "output_contract_checks": oc_checks,
        "context_capsule_checks": capsule_checks,
        "worklet_graph_checks": worklet_checks,
        "slot_contract_checks": slot_checks,
        "gaptext_checks": gaptext_checks,
        "thor_odin_claude_audit_refs": thor_audit_refs,
        "hard_violations": violations,
        "non_claims": [
            "not runtime completion",
            "not provider execution",
            "not live model inference",
            "not QIRC server runtime proof",
            "not app apply authority",
            "not production readiness",
            "not release certification",
            "not security certification",
            "not target host proof",
            "not model quality proof",
        ],
        "senior_reviewer_notes": [],
        "senior_code_reviewer_notes": [],
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="B2 Context/Lenses/Worklets/Slot Forge/Gaptext static validator")
    parser.add_argument("--repo-root", default=".", help="Repository root directory")
    parser.add_argument("--out", required=True, help="Output report JSON path")
    parser.add_argument("--generated-at-utc", default="2026-01-01T00:00:00Z",
                        help="Deterministic timestamp for report")
    parser.add_argument("--bundle-plan", help="Override bundle plan path")
    args = parser.parse_args()

    out_path = Path(args.out)
    report = validate(args)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    n_violations = len(report["hard_violations"])
    status = "PASS" if n_violations == 0 else f"FAIL ({n_violations} violations)"
    print(f"B2 validator: {status}")
    if n_violations:
        for v in report["hard_violations"]:
            print(f"  VIOLATION: {v}")
    import sys
    sys.exit(0 if n_violations == 0 else 1)


if __name__ == "__main__":
    main()
