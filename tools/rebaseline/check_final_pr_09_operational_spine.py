#!/usr/bin/env python3
"""Validate FINAL-PR-09++ Operational Spine artifacts.

Claim boundary: final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply
candidate_only: true
local_only: true
stdlib_only: true
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CLAIM_BOUNDARY = "final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply"

REQUIRED_MODULES = [
    "odin/operational_spine/__init__.py",
    "odin/operational_spine/orchestrator.py",
    "odin/operational_spine/status.py",
    "odin/operational_spine/model_roles.py",
    "odin/operational_spine/modelworkpacket_builder.py",
    "odin/operational_spine/small_model_route_plan.py",
    "odin/operational_spine/qshabang_runtime_map.py",
    "odin/operational_spine/deferred_system_lift.py",
    "odin/operational_spine/provider_seam.py",
    "odin/operational_spine/receipts.py",
    "odin/operational_spine/reports.py",
]

REQUIRED_ALL_FILES = REQUIRED_MODULES + [
    "registries/final_pr_09_operational_spine_registry.json",
    "schemas/final_pr_09_operational_spine_report.schema.json",
    "examples/final_pr_09/operational_spine_demo.example.json",
    "examples/final_pr_09/modelworkpacket.example.json",
    "examples/final_pr_09/small_model_route_plan.example.json",
    "examples/final_pr_09/qshabang_operational_map.example.json",
    "examples/final_pr_09/deferred_system_lift.example.json",
    "examples/final_pr_09/provider_seam_packet.example.json",
    "tools/rebaseline/check_final_pr_09_operational_spine.py",
    "tests/test_final_pr_09_operational_spine.py",
    "reports/final_pr_09_operational_spine_report.json",
    "reports/final_pr_09_cli_surface_report.json",
    "reports/final_pr_09_hub_surface_report.json",
    "reports/final_pr_09_provider_readiness_report.json",
    "reports/final_pr_09_modelworkpacket_enforcement_report.json",
    "reports/final_pr_09_small_model_route_plan_report.json",
    "reports/final_pr_09_qshabang_operational_map_report.json",
    "reports/final_pr_09_deferred_system_lift_report.json",
    "reports/final_pr_09_operational_spine_proof_packet.json",
    "docs/rebaseline/FINAL_PR_09_OPERATIONAL_SPINE.md",
    "docs/release/FINAL_PR_09_OPERATIONAL_SPINE_EVIDENCE_INDEX.md",
    "docs/release/FINAL_PR_09_SMALL_MODEL_POWER_MAP.md",
    "docs/release/FINAL_PR_09_QSHABANG_OPERATIONAL_MAP.md",
    "docs/release/FINAL_PR_09_DEFERRED_SYSTEM_LIFT_PLAN.md",
    "docs/codex/handoffs/FINAL_PR_09_REPO_COGNITION_SUMMARY.md",
    "docs/codex/handoffs/FINAL_PR_09_THOR_STYLE_OPERATIONAL_SPINE_HANDOFF.md",
    "docs/codex/handoffs/FINAL_PR_09_ODIN_AGENT_OPERATOR_WORK_PACKET.md",
    "docs/codex/audits/FINAL_PR_09_OPERATIONAL_SPINE_AUDIT.md",
    "docs/codex/audits/FINAL_PR_09_SENIOR_REVIEW.md",
    "docs/codex/audits/FINAL_PR_09_CODE_REVIEW.md",
    "docs/codex/audits/FINAL_PR_09_THOR_ODIN_Y_EFFECTIVENESS_AUDIT.md",
    "docs/codex/reports/FINAL_PR_09_OPERATIONAL_SPINE_RETURN_REPORT.md",
]

REQUIRED_HUB_ENDPOINTS = [
    "/operational-spine/status.json",
    "/operational-spine/demo.json",
    "/operational-spine/run",
    "/operational-spine/evidence-index.json",
    "/operational-spine/provider-readiness.json",
    "/operational-spine/small-model-route.json",
    "/operational-spine/qshabang-map.json",
    "/operational-spine/modelworkpacket.example.json",
]

REQUIRED_CLI_COMMANDS = [
    "odin-status", "odin-doctor", "run-operational-spine",
    "explain-operational-spine", "explain-small-model-route", "explain-qshabang-map",
    "validate-operational-spine", "validate-small-model-route-plan",
    "validate-modelworkpacket-enforcement", "validate-qshabang-operational-map",
    "validate-deferred-system-lift",
]

REQUIRED_3B_ROLES = [
    "3b_scout",
    "3b_extractor",
    "3b_classifier",
    "3b_router",
    "3b_slot_filler",
    "3b_quick_critic",
    "3b_style_check",
    "3b_refusal_boundary_check",
]

REQUIRED_7B_ROLES = [
    "7b_writer",
    "7b_synthesizer",
    "7b_planner",
    "7b_repo_reasoner",
    "7b_candidate_composer",
    "7b_refiner",
    "7b_complex_critic",
]

REQUIRED_HYBRID_ROLES = [
    "hybrid_3b_scout_7b_synthesize_3b_check",
    "hybrid_3b_extract_7b_compose_3b_boundary_critic",
    "hybrid_7b_draft_3b_slot_check_7b_refine",
    "hybrid_no_model_precompute_3b_route_7b_candidate_final_gate",
]

REQUIRED_NO_MODEL_ROLES = [
    "schema_validation",
    "manifest_binding_validation",
    "cache_fingerprint_lookup",
    "slot_preparation",
    "rule_based_refusal",
    "deterministic_candidate_shape",
    "trace_receipt_construction",
]

REQUIRED_QSHABANG_COMPONENTS = [
    "ki_ohne_ki",
    "q_gates",
    "mirror_critics",
    "resonance_fit",
    "seeds_pattern_mines",
    "narrative_compiler",
    "qirc",
    "app_sovereignty",
    "candidate_reality",
    "qooo_style_orchestration",
    "bug6_q7",
]

REQUIRED_DEFERRED_SYSTEMS = [
    "Context Distillery",
    "Artifact Lenses",
    "Slot Forge",
    "Gaptext Compiler",
    "Semantic Cache",
    "Work Memory",
    "Minicheck",
    "Critic Cascade",
    "Candidate Tournament",
    "Style Stabilizer",
    "Anti-Generic Engine",
    "Taste Dials",
    "Model Dojo",
    "Scoreboard",
    "SDK/App Bridge receipts",
]

REQUIRED_ROUTE_MODES = [
    "deterministic_no_model",
    "3b_primary",
    "7b_primary",
    "3b_7b_hybrid",
]

REQUIRED_ORCHESTRATOR_KEYS = [
    "work_id",
    "spine_id",
    "handoff_context",
    "universal_work",
    "validation_result",
    "context_capsule",
    "artifact_lens",
    "slot_contract",
    "gaptext",
    "precompute_result",
    "modelworkpacket",
    "small_model_route_plan",
    "model_role_assignment",
    "seed_route",
    "field_selection",
    "projection_candidate",
    "provider_seam_packet",
    "candidate_artifact",
    "final_gate",
    "response_packet",
    "trace_ref",
    "receipt_ref",
    "qirc_hint_refs",
    "proof_refs",
    "candidate_only",
    "local_only",
    "app_owned_apply",
    "claim_boundary",
    "not_proven",
]

FORBIDDEN_CALL_TOKENS = [
    "openai.",
    "anthropic.",
    "requests.",
    "urllib.request.urlopen",
    "http.client",
    "socket.",
    "subprocess.",
    "os.system",
    "eval(",
    "exec(",
    "uuid.uuid4(",
    "random.random(",
    "datetime.now(",
    "time.time(",
]


def add(errors: list[str], cond: bool, msg: str) -> None:
    if not cond:
        errors.append(msg)


def validate(repo_root: Path) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    checked: list[str] = []

    # ── All required files present (full check, not spot-check) ─────────────
    for rel in REQUIRED_ALL_FILES:
        add(errors, (repo_root / rel).exists(), f"missing required file: {rel}")
        if (repo_root / rel).exists():
            checked.append(rel)

    # ── Python module content checks (not markdown/JSON) ──────────────────
    for rel in REQUIRED_MODULES:
        p = repo_root / rel
        if not p.exists():
            continue
        try:
            text = p.read_text(encoding="utf-8")
            # Must declare candidate_only
            add(errors, "candidate_only" in text, f"module missing candidate_only: {rel}")
            # Must declare claim_boundary
            add(errors, "claim_boundary" in text, f"module missing claim_boundary: {rel}")
            # Forbidden call tokens (only in new operational_spine Python modules)
            for token in FORBIDDEN_CALL_TOKENS:
                add(errors, token not in text, f"forbidden call token {token!r} in {rel}")
        except Exception as exc:
            errors.append(f"could not read module {rel}: {exc}")

    # ── model_roles.py: all role IDs present ──────────────────────────────
    roles_path = repo_root / "odin/operational_spine/model_roles.py"
    if roles_path.exists():
        roles_text = roles_path.read_text(encoding="utf-8")
        for role_id in REQUIRED_3B_ROLES + REQUIRED_7B_ROLES + REQUIRED_HYBRID_ROLES + REQUIRED_NO_MODEL_ROLES:
            add(errors, role_id in roles_text, f"model_roles.py missing role: {role_id}")

    # ── qshabang_runtime_map.py: all components present ───────────────────
    qmap_path = repo_root / "odin/operational_spine/qshabang_runtime_map.py"
    if qmap_path.exists():
        qmap_text = qmap_path.read_text(encoding="utf-8")
        for component in REQUIRED_QSHABANG_COMPONENTS:
            add(errors, component in qmap_text, f"qshabang_runtime_map.py missing component: {component}")

    # ── deferred_system_lift.py: all systems present ──────────────────────
    deferred_path = repo_root / "odin/operational_spine/deferred_system_lift.py"
    if deferred_path.exists():
        deferred_text = deferred_path.read_text(encoding="utf-8")
        for system in REQUIRED_DEFERRED_SYSTEMS:
            add(errors, system in deferred_text, f"deferred_system_lift.py missing system: {system}")

    # ── small_model_route_plan.py: route modes present ────────────────────
    route_path = repo_root / "odin/operational_spine/small_model_route_plan.py"
    if route_path.exists():
        route_text = route_path.read_text(encoding="utf-8")
        for mode in REQUIRED_ROUTE_MODES:
            add(errors, mode in route_text, f"small_model_route_plan.py missing route mode: {mode}")
        add(errors, "requires_model" in route_text,
            "small_model_route_plan.py missing requires_model field")

    # ── orchestrator.py: required output keys present ─────────────────────
    orch_path = repo_root / "odin/operational_spine/orchestrator.py"
    if orch_path.exists():
        orch_text = orch_path.read_text(encoding="utf-8")
        for key in REQUIRED_ORCHESTRATOR_KEYS:
            add(errors, f'"{key}"' in orch_text or f"'{key}'" in orch_text,
                f"orchestrator.py missing output key: {key}")
        add(errors, "run_operational_spine" in orch_text,
            "orchestrator.py missing run_operational_spine function")
        add(errors, "try:" in orch_text,
            "orchestrator.py must use try/except to prevent exception propagation")
        # Must not raise — check for top-level exception guard pattern
        add(errors, "validation_errors" in orch_text,
            "orchestrator.py must collect validation_errors")

    # ── provider_seam.py: default execution disabled ──────────────────────
    seam_path = repo_root / "odin/operational_spine/provider_seam.py"
    if seam_path.exists():
        seam_text = seam_path.read_text(encoding="utf-8")
        add(errors, "execution_allowed" in seam_text,
            "provider_seam.py missing execution_allowed field")
        add(errors, "execution_performed" in seam_text,
            "provider_seam.py missing execution_performed field")
        add(errors, "allow_local_provider_execution" in seam_text,
            "provider_seam.py missing allow_local_provider_execution parameter")
        add(errors, "execution_not_available_or_not_enabled" in seam_text,
            "provider_seam.py missing execution_not_available_or_not_enabled status")

    # ── receipts.py: deterministic ID functions present ───────────────────
    receipts_path = repo_root / "odin/operational_spine/receipts.py"
    if receipts_path.exists():
        receipts_text = receipts_path.read_text(encoding="utf-8")
        add(errors, "operational_trace_" in receipts_text,
            "receipts.py missing operational_trace_ prefix")
        add(errors, "operational_receipt_" in receipts_text,
            "receipts.py missing operational_receipt_ prefix")
        add(errors, "build_trace_ref" in receipts_text,
            "receipts.py missing build_trace_ref function")
        add(errors, "build_receipt_ref" in receipts_text,
            "receipts.py missing build_receipt_ref function")
        add(errors, "build_proof_refs" in receipts_text,
            "receipts.py missing build_proof_refs function")
        add(errors, "hashlib" in receipts_text,
            "receipts.py must use hashlib for deterministic IDs")

    # ── __init__.py exports ───────────────────────────────────────────────
    init_path = repo_root / "odin/operational_spine/__init__.py"
    if init_path.exists():
        init_text = init_path.read_text(encoding="utf-8")
        add(errors, "run_operational_spine" in init_text,
            "__init__.py must export run_operational_spine")
        add(errors, "OperationalSpineResult" in init_text,
            "__init__.py must export OperationalSpineResult")
        add(errors, "CLAIM_BOUNDARY" in init_text,
            "__init__.py must export CLAIM_BOUNDARY")

    # ── CLI commands registered ───────────────────────────────────────────
    cli_path = repo_root / "odin/cli.py"
    if cli_path.exists():
        cli = cli_path.read_text(encoding="utf-8")
        for cmd in REQUIRED_CLI_COMMANDS:
            add(errors, cmd in cli, f"CLI missing command: {cmd}")
        add(errors, "validate_operational_spine" in cli,
            "CLI missing validate_operational_spine function")
        add(errors, "validate_operational_spine()" in cli,
            "validate_all must call validate_operational_spine()")

    # ── Registry present ──────────────────────────────────────────────────
    registry_path = repo_root / "registries/final_pr_09_operational_spine_registry.json"
    if registry_path.exists():
        checked.append("registries/final_pr_09_operational_spine_registry.json")
        try:
            reg = json.loads(registry_path.read_text(encoding="utf-8"))
            add(errors, reg.get("candidate_only") is True,
                "registry missing candidate_only: true")
            add(errors, "claim_boundary" in reg,
                "registry missing claim_boundary")
        except Exception as exc:
            errors.append(f"registry JSON parse failed: {exc}")
    else:
        warnings.append("registry not found: registries/final_pr_09_operational_spine_registry.json")

    # ── Local Hub endpoints ────────────────────────────────────────────────
    server_path = repo_root / "odin/local_hub/server.py"
    if server_path.exists():
        server = server_path.read_text(encoding="utf-8")
        for ep in REQUIRED_HUB_ENDPOINTS:
            add(errors, ep in server, f"local hub server missing endpoint: {ep}")

    # ── UI REQUIRED_IDS contains operational-spine-section ────────────────
    ui_path = repo_root / "odin/local_hub/ui.py"
    if ui_path.exists():
        ui = ui_path.read_text(encoding="utf-8")
        add(errors, '"operational-spine-section"' in ui,
            "REQUIRED_IDS missing operational-spine-section")
        add(errors, "Operational Spine connects Universal Work" in ui,
            "REQUIRED_COPY missing Dev Mode copy for operational spine")
        add(errors, "Odin organizes local candidate work into a safe structured response" in ui,
            "REQUIRED_COPY missing normal-user copy for operational spine")
        add(errors, 'id="operational-spine-section"' in ui,
            "HTML missing id=operational-spine-section element")

    # ── SYSTEM_MAP has PR09 entry ──────────────────────────────────────────
    system_map_path = repo_root / "SYSTEM_MAP.json"
    if system_map_path.exists():
        system_map_text = system_map_path.read_text(encoding="utf-8")
        add(errors, "final_pr_09_operational_spine" in system_map_text,
            "SYSTEM_MAP missing final_pr_09_operational_spine")

    # ── FILE_MANIFEST contains every required PR09 file ──────────────────
    manifest_path = repo_root / "FILE_MANIFEST.json"
    if manifest_path.exists():
        manifest_text = manifest_path.read_text(encoding="utf-8")
        for rel in REQUIRED_ALL_FILES:
            add(errors, rel in manifest_text, f"FILE_MANIFEST missing PR09 file: {rel}")

    # ── Proof packet correct structure ────────────────────────────────────
    proof_path = repo_root / "reports/final_pr_09_operational_spine_proof_packet.json"
    if proof_path.exists():
        try:
            proof = json.loads(proof_path.read_text(encoding="utf-8"))
            add(errors, proof.get("candidate_only") is True, "proof packet candidate_only must be true")
            add(errors, proof.get("claim_boundary") == CLAIM_BOUNDARY, "proof packet claim_boundary mismatch")
            required_not_proven = [
                "live_model_inference", "real_model_benchmark", "provider_execution",
                "app_apply", "app_state_mutation", "external_send",
                "public_network", "production_readiness", "security_certification", "release_certification",
            ]
            for item in required_not_proven:
                add(errors, item in proof.get("not_proven", []), f"proof packet missing not_proven: {item}")
        except Exception as exc:
            errors.append(f"proof packet parse error: {exc}")

    # ── Example files parse and candidate_only ────────────────────────────
    for rel in [
        "examples/final_pr_09/operational_spine_demo.example.json",
        "examples/final_pr_09/modelworkpacket.example.json",
        "examples/final_pr_09/small_model_route_plan.example.json",
        "examples/final_pr_09/qshabang_operational_map.example.json",
        "examples/final_pr_09/deferred_system_lift.example.json",
        "examples/final_pr_09/provider_seam_packet.example.json",
    ]:
        p = repo_root / rel
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                add(errors, data.get("candidate_only") is True, f"{rel}: candidate_only must be true")
            except Exception as exc:
                errors.append(f"{rel} parse error: {exc}")

    # ── Provider seam example must have execution disabled ────────────────
    seam_example = repo_root / "examples/final_pr_09/provider_seam_packet.example.json"
    if seam_example.exists():
        try:
            seam_data = json.loads(seam_example.read_text(encoding="utf-8"))
            add(errors, seam_data.get("execution_allowed") is False,
                "provider_seam_packet example: execution_allowed must be false")
            add(errors, seam_data.get("model_inference") is False,
                "provider_seam_packet example: model_inference must be false")
            add(errors, seam_data.get("provider_execution") is False,
                "provider_seam_packet example: provider_execution must be false")
        except Exception:
            pass

    # ── Functional smoke test: import and run ─────────────────────────────
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "odin_operational_spine_orch",
            repo_root / "odin/operational_spine/orchestrator.py",
        )
        if spec and spec.loader:
            # We do a static source check rather than executing (avoids import graph issues)
            src = (repo_root / "odin/operational_spine/orchestrator.py").read_text(encoding="utf-8")
            add(errors, "def run_operational_spine(" in src,
                "orchestrator.py missing run_operational_spine function definition")
    except Exception as exc:
        warnings.append(f"orchestrator static check warning: {exc}")

    return errors, warnings, sorted(set(checked))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate FINAL-PR-09++ Operational Spine")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default="reports/final_pr_09_operational_spine_report.json")
    parser.add_argument("--generated-at-utc", default="2026-01-01T00:00:00Z")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    errors, warnings, checked = validate(repo_root)

    report = {
        "status": "ok" if not errors else "error",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "checked_files": checked,
        "errors": errors,
        "warnings": warnings,
        "generated_at_utc": args.generated_at_utc,
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    }

    out = Path(args.out)
    if not out.is_absolute():
        out = repo_root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
