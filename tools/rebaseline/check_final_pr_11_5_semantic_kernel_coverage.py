"""FINAL-PR-11.5 validator: Semantic Kernel Coverage Compiler + Claims Compiler + Y Pattern.

Claim boundary: final_pr_11_5_semantic_kernel_coverage_compiler_not_release_closure
stdlib only, no external dependencies.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CLAIM_BOUNDARY = "final_pr_11_5_semantic_kernel_coverage_compiler_not_release_closure"

_REQUIRED_MODULE_FILES = [
    # v711_coverage_compiler
    "odin/v711_coverage_compiler/__init__.py",
    "odin/v711_coverage_compiler/target_loader.py",
    "odin/v711_coverage_compiler/evidence_mapper.py",
    "odin/v711_coverage_compiler/coverage_matrix.py",
    "odin/v711_coverage_compiler/gap_index.py",
    "odin/v711_coverage_compiler/next_pr_recommender.py",
    "odin/v711_coverage_compiler/reports.py",
    # semantic_kernel_closure
    "odin/semantic_kernel_closure/__init__.py",
    "odin/semantic_kernel_closure/ir.py",
    "odin/semantic_kernel_closure/pipeline.py",
    "odin/semantic_kernel_closure/contracts.py",
    "odin/semantic_kernel_closure/kernel_map.py",
    "odin/semantic_kernel_closure/receipts.py",
    "odin/semantic_kernel_closure/reports.py",
    # y_pattern_operationalization_index
    "odin/y_pattern_operationalization_index/__init__.py",
    "odin/y_pattern_operationalization_index/neutral_terms.py",
    "odin/y_pattern_operationalization_index/status_classifier.py",
    "odin/y_pattern_operationalization_index/index_builder.py",
    "odin/y_pattern_operationalization_index/reports.py",
    # claims_compiler
    "odin/claims_compiler/__init__.py",
    "odin/claims_compiler/claim_types.py",
    "odin/claims_compiler/safe_wording.py",
    "odin/claims_compiler/compiler.py",
    "odin/claims_compiler/reports.py",
    # agent_operator_modes
    "odin/agent_operator_modes/__init__.py",
    "odin/agent_operator_modes/presets.py",
    "odin/agent_operator_modes/modes.py",
    "odin/agent_operator_modes/reports.py",
]

_REQUIRED_EXAMPLES = [
    "examples/final_pr_11_5/v711_coverage_matrix.example.json",
    "examples/final_pr_11_5/v711_gap_index.example.json",
    "examples/final_pr_11_5/semantic_kernel_ir.example.json",
    "examples/final_pr_11_5/semantic_kernel_pipeline.example.json",
    "examples/final_pr_11_5/y_pattern_index.example.json",
    "examples/final_pr_11_5/claims_policy.example.json",
    "examples/final_pr_11_5/agent_operator_mode_matrix.example.json",
]

_REQUIRED_REPORTS = [
    "reports/final_pr_11_5_v711_coverage_report.json",
    "reports/final_pr_11_5_semantic_kernel_closure_report.json",
    "reports/final_pr_11_5_y_pattern_index_report.json",
    "reports/final_pr_11_5_claims_policy_report.json",
    "reports/final_pr_11_5_agent_operator_mode_matrix_report.json",
]

_REQUIRED_REGISTRIES = [
    "registries/final_pr_11_5_semantic_kernel_coverage_registry.json",
]

_REQUIRED_SCHEMAS = [
    "schemas/final_pr_11_5_v711_coverage_matrix.schema.json",
    "schemas/final_pr_11_5_semantic_kernel_closure.schema.json",
]

_REQUIRED_CLI_COMMANDS = [
    "validate-v711-coverage-compiler",
    "validate-semantic-kernel-closure",
    "validate-y-pattern-operationalization-index",
    "validate-claims-compiler",
    "validate-agent-operator-modes",
    "validate-final-pr-11-5-semantic-kernel-coverage",
]

_REQUIRED_DOCS = [
    "docs/rebaseline/FINAL_PR_11_5_SEMANTIC_KERNEL_COVERAGE.md",
]

_REQUIRED_HUB_ENDPOINTS = [
    "/v711-coverage/matrix.json",
    "/semantic-kernel/closure.json",
    "/y-pattern/index.json",
    "/claims/policy.json",
]

_REQUIRED_UI_SECTIONS = [
    "v711-coverage-compiler-section",
    "semantic-kernel-closure-section",
    "y-pattern-operationalization-section",
    "claims-compiler-section",
]


def _load_json(path: Path) -> tuple[dict | list | None, str | None]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f), None
    except Exception as exc:
        return None, str(exc)


def _check_required_files(root: Path, file_list: list[str], label: str) -> list[str]:
    errors = []
    for rel in file_list:
        p = root / rel
        if not p.exists():
            errors.append(f"[{label}] missing: {rel}")
    return errors


def _check_json_files(root: Path, file_list: list[str]) -> list[str]:
    errors = []
    for rel in file_list:
        p = root / rel
        if not p.exists():
            continue
        obj, err = _load_json(p)
        if err:
            errors.append(f"invalid JSON in {rel}: {err}")
    return errors


def _check_no_eval_exec(root: Path) -> list[str]:
    errors = []
    new_modules = [
        root / "odin/v711_coverage_compiler",
        root / "odin/semantic_kernel_closure",
        root / "odin/y_pattern_operationalization_index",
        root / "odin/claims_compiler",
        root / "odin/agent_operator_modes",
    ]
    for module_dir in new_modules:
        if not module_dir.exists():
            continue
        for py_file in module_dir.glob("*.py"):
            text = py_file.read_text(encoding="utf-8", errors="ignore")
            for bad in ["eval(", "exec("]:
                if bad in text:
                    errors.append(f"forbidden {bad!r} in {py_file.relative_to(root)}")
    return errors


def _check_no_datetime_now(root: Path) -> list[str]:
    errors = []
    new_modules = [
        root / "odin/v711_coverage_compiler",
        root / "odin/semantic_kernel_closure",
        root / "odin/y_pattern_operationalization_index",
        root / "odin/claims_compiler",
        root / "odin/agent_operator_modes",
    ]
    for module_dir in new_modules:
        if not module_dir.exists():
            continue
        for py_file in module_dir.glob("*.py"):
            text = py_file.read_text(encoding="utf-8", errors="ignore")
            if "datetime.now()" in text or "datetime.utcnow()" in text:
                errors.append(f"forbidden datetime.now()/utcnow() in {py_file.relative_to(root)}")
    return errors


def _check_cli_commands(root: Path) -> list[str]:
    errors = []
    cli_path = root / "odin/cli.py"
    if not cli_path.exists():
        return ["odin/cli.py missing"]
    text = cli_path.read_text(encoding="utf-8", errors="ignore")
    for cmd in _REQUIRED_CLI_COMMANDS:
        if cmd not in text:
            errors.append(f"CLI command not registered: {cmd}")
    if "validate_final_pr_11_5_semantic_kernel_coverage" not in text:
        errors.append("validate_all() does not call validate_final_pr_11_5_semantic_kernel_coverage")
    return errors


def _check_local_hub_endpoints(root: Path) -> list[str]:
    errors = []
    server_path = root / "odin/local_hub/server.py"
    if not server_path.exists():
        return ["odin/local_hub/server.py missing"]
    text = server_path.read_text(encoding="utf-8", errors="ignore")
    for endpoint in _REQUIRED_HUB_ENDPOINTS:
        if endpoint not in text:
            errors.append(f"Local Hub endpoint not registered: {endpoint}")
    return errors


def _check_ui_sections(root: Path) -> list[str]:
    errors = []
    ui_path = root / "odin/local_hub/ui.py"
    if not ui_path.exists():
        return ["odin/local_hub/ui.py missing"]
    text = ui_path.read_text(encoding="utf-8", errors="ignore")
    for section in _REQUIRED_UI_SECTIONS:
        if section not in text:
            errors.append(f"REQUIRED_IDS missing section: {section}")
    return errors


def _check_system_map(root: Path) -> list[str]:
    errors = []
    sm = root / "SYSTEM_MAP.json"
    if not sm.exists():
        return ["SYSTEM_MAP.json missing"]
    text = sm.read_text(encoding="utf-8", errors="ignore")
    if "final_pr_11_5" not in text:
        errors.append("SYSTEM_MAP.json missing final_pr_11_5 entry")
    return errors


def _check_file_manifest(root: Path) -> list[str]:
    errors = []
    fm = root / "FILE_MANIFEST.json"
    if not fm.exists():
        return ["FILE_MANIFEST.json missing"]
    text = fm.read_text(encoding="utf-8", errors="ignore")
    key_files = [
        "odin/v711_coverage_compiler/__init__.py",
        "odin/semantic_kernel_closure/__init__.py",
        "odin/y_pattern_operationalization_index/__init__.py",
        "odin/claims_compiler/__init__.py",
        "odin/agent_operator_modes/__init__.py",
        "tests/test_final_pr_11_5_semantic_kernel_coverage.py",
        "tools/rebaseline/check_final_pr_11_5_semantic_kernel_coverage.py",
    ]
    for rel in key_files:
        if rel not in text:
            errors.append(f"FILE_MANIFEST.json missing entry for {rel}")
    return errors


def _functional_check_v711_coverage() -> list[str]:
    errors = []
    try:
        from odin.v711_coverage_compiler.coverage_matrix import build_v711_coverage_matrix
        matrix = build_v711_coverage_matrix()
        if matrix.get("candidate_only") is not True:
            errors.append("v711 coverage matrix: candidate_only must be True")
        if matrix.get("artifact_kind") != "odin_v711_coverage_matrix":
            errors.append("v711 coverage matrix: wrong artifact_kind")
        coverage = matrix.get("coverage", [])
        if len(coverage) < 20:
            errors.append(f"v711 coverage matrix: too few rows ({len(coverage)}), expected >= 20")
        for row in coverage:
            if "not_proven" not in row:
                errors.append(f"v711 coverage row missing not_proven: {row.get('target_id')}")
            if "target_id" not in row:
                errors.append("v711 coverage row missing target_id")
    except Exception as exc:
        errors.append(f"v711 coverage matrix functional check failed: {exc}")
    return errors


def _functional_check_v711_gap_index() -> list[str]:
    errors = []
    try:
        from odin.v711_coverage_compiler.gap_index import build_v711_gap_index
        gap = build_v711_gap_index()
        if gap.get("candidate_only") is not True:
            errors.append("v711 gap index: candidate_only must be True")
        if gap.get("artifact_kind") != "odin_v711_gap_index":
            errors.append("v711 gap index: wrong artifact_kind")
        gaps = gap.get("gaps", [])
        if len(gaps) == 0:
            errors.append("v711 gap index: expected at least one gap")
    except Exception as exc:
        errors.append(f"v711 gap index functional check failed: {exc}")
    return errors


def _functional_check_semantic_kernel_ir() -> list[str]:
    errors = []
    try:
        from odin.semantic_kernel_closure.ir import build_odin_work_ir
        ir = build_odin_work_ir()
        if ir.get("candidate_only") is not True:
            errors.append("semantic kernel IR: candidate_only must be True")
        ir_objects = ir.get("ir_objects", [])
        if len(ir_objects) < 16:
            errors.append(f"semantic kernel IR: expected >= 16 IR objects, got {len(ir_objects)}")
        required_ids = ["UniversalWorkIR", "ContextIR", "CriticIR", "FinalGateIR", "ProviderReceiptIR"]
        found_ids = {o["ir_id"] for o in ir_objects}
        for rid in required_ids:
            if rid not in found_ids:
                errors.append(f"semantic kernel IR: missing IR object: {rid}")
    except Exception as exc:
        errors.append(f"semantic kernel IR functional check failed: {exc}")
    return errors


def _functional_check_semantic_kernel_pipeline() -> list[str]:
    errors = []
    try:
        from odin.semantic_kernel_closure.pipeline import build_semantic_kernel_pipeline
        pipeline = build_semantic_kernel_pipeline()
        if pipeline.get("candidate_only") is not True:
            errors.append("semantic kernel pipeline: candidate_only must be True")
        stages = pipeline.get("stages", [])
        if len(stages) < 14:
            errors.append(f"semantic kernel pipeline: expected >= 14 stages, got {len(stages)}")
        stage_ids = {s["stage_id"] for s in stages}
        required = ["universal_work", "provider_receipt", "critic_runtime", "final_gate", "app_owned_apply_boundary"]
        for r in required:
            if r not in stage_ids:
                errors.append(f"semantic kernel pipeline: missing stage: {r}")
    except Exception as exc:
        errors.append(f"semantic kernel pipeline functional check failed: {exc}")
    return errors


def _functional_check_y_pattern_index() -> list[str]:
    errors = []
    try:
        from odin.y_pattern_operationalization_index.index_builder import build_y_pattern_operationalization_index
        idx = build_y_pattern_operationalization_index()
        if idx.get("candidate_only") is not True:
            errors.append("y pattern index: candidate_only must be True")
        mappings = idx.get("mappings", [])
        if len(mappings) < 14:
            errors.append(f"y pattern index: expected >= 14 mappings, got {len(mappings)}")
        # Check required mappings
        internal_patterns = {m["internal_pattern"] for m in mappings}
        required = ["Internal Semantic Bus", "AI without AI", "Thor", "app sovereignty"]
        for r in required:
            if r not in internal_patterns:
                errors.append(f"y pattern index: missing mapping for: {r}")
    except Exception as exc:
        errors.append(f"y pattern index functional check failed: {exc}")
    return errors


def _functional_check_claims_compiler() -> list[str]:
    errors = []
    try:
        from odin.claims_compiler.compiler import classify_claim, compile_safe_claim
        # Test allowed claim
        result = classify_claim("Odin returns candidates only.")
        if result.get("allowed") is not True:
            errors.append("claims compiler: expected allowed=True for safe claim")
        if "not_proven" not in result:
            errors.append("claims compiler: missing not_proven in classify_claim result")
        # Test forbidden claim
        result2 = classify_claim("Odin certifies production_readiness.")
        if result2.get("allowed") is not False:
            errors.append("claims compiler: expected allowed=False for forbidden claim")
        # Test compile_safe_claim
        compiled = compile_safe_claim(
            "Odin structural evidence exists.",
            evidence_class="structural_evidence",
            evidence_refs=["odin/execution_gate/"],
        )
        if compiled.get("allowed") is not True:
            errors.append("claims compiler: compile_safe_claim should allow structural_evidence claim")
    except Exception as exc:
        errors.append(f"claims compiler functional check failed: {exc}")
    return errors


def _functional_check_agent_operator_modes() -> list[str]:
    errors = []
    try:
        from odin.agent_operator_modes.modes import list_agent_operator_modes, get_agent_operator_mode
        modes = list_agent_operator_modes()
        if len(modes) < 9:
            errors.append(f"agent operator modes: expected >= 9 modes, got {len(modes)}")
        required_ids = [
            "claude_code_implementation_worker",
            "claude_code_runtime_integrator",
            "thor_handoff_compiler_mode",
            "pr_release_closure_worker",
        ]
        mode_ids = {m["mode_id"] for m in modes}
        for rid in required_ids:
            if rid not in mode_ids:
                errors.append(f"agent operator modes: missing mode: {rid}")
        # Test get
        m = get_agent_operator_mode("claude_code_implementation_worker")
        if m.get("agent_autonomy") is not False:
            errors.append("agent operator mode: agent_autonomy must be False")
        if m.get("app_apply") is not False:
            errors.append("agent operator mode: app_apply must be False")
        if m.get("candidate_only") is not True:
            errors.append("agent operator mode: candidate_only must be True")
        # Test KeyError
        try:
            get_agent_operator_mode("nonexistent_mode_xyz")
            errors.append("agent operator modes: should raise KeyError for unknown mode")
        except KeyError:
            pass
    except Exception as exc:
        errors.append(f"agent operator modes functional check failed: {exc}")
    return errors


def _functional_check_coverage_report() -> list[str]:
    errors = []
    try:
        from odin.v711_coverage_compiler.reports import build_v711_coverage_report
        report = build_v711_coverage_report()
        if report.get("candidate_only") is not True:
            errors.append("v711 coverage report: candidate_only must be True")
        if report.get("final_pr_13_remains_deferred") is not True:
            errors.append("v711 coverage report: final_pr_13_remains_deferred must be True")
        summary = report.get("summary", {})
        if summary.get("total_targets", 0) < 20:
            errors.append(f"v711 coverage report: expected >= 20 targets, got {summary.get('total_targets')}")
    except Exception as exc:
        errors.append(f"v711 coverage report functional check failed: {exc}")
    return errors


def run_checks(root: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    errors.extend(_check_required_files(root, _REQUIRED_MODULE_FILES, "module"))
    errors.extend(_check_required_files(root, _REQUIRED_EXAMPLES, "example"))
    errors.extend(_check_required_files(root, _REQUIRED_REPORTS, "report"))
    errors.extend(_check_required_files(root, _REQUIRED_REGISTRIES, "registry"))
    errors.extend(_check_required_files(root, _REQUIRED_SCHEMAS, "schema"))
    errors.extend(_check_required_files(root, _REQUIRED_DOCS, "doc"))
    errors.extend(_check_required_files(
        root,
        ["tests/test_final_pr_11_5_semantic_kernel_coverage.py",
         "tools/rebaseline/check_final_pr_11_5_semantic_kernel_coverage.py"],
        "test/validator"
    ))

    errors.extend(_check_json_files(root, _REQUIRED_EXAMPLES))
    errors.extend(_check_json_files(root, _REQUIRED_REPORTS))
    errors.extend(_check_json_files(root, _REQUIRED_REGISTRIES))
    errors.extend(_check_json_files(root, _REQUIRED_SCHEMAS))

    errors.extend(_check_no_eval_exec(root))
    errors.extend(_check_no_datetime_now(root))
    errors.extend(_check_cli_commands(root))
    errors.extend(_check_local_hub_endpoints(root))
    errors.extend(_check_ui_sections(root))
    errors.extend(_check_system_map(root))
    errors.extend(_check_file_manifest(root))

    # Functional checks
    try:
        errors.extend(_functional_check_v711_coverage())
        errors.extend(_functional_check_v711_gap_index())
        errors.extend(_functional_check_semantic_kernel_ir())
        errors.extend(_functional_check_semantic_kernel_pipeline())
        errors.extend(_functional_check_y_pattern_index())
        errors.extend(_functional_check_claims_compiler())
        errors.extend(_functional_check_agent_operator_modes())
        errors.extend(_functional_check_coverage_report())
    except Exception as exc:
        errors.append(f"functional check block failed: {exc}")

    status = "ok" if not errors else "error"
    return {
        "status": status,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "errors": errors,
        "warnings": warnings,
        "generated_at_utc": "2026-01-01T00:00:00Z",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check_final_pr_11_5_semantic_kernel_coverage",
        description="Validate FINAL-PR-11.5 Semantic Kernel Coverage + Claims Compiler + Y Pattern",
    )
    parser.add_argument("--repo-root", default=".", help="Path to repo root")
    parser.add_argument("--out", required=True, help="Output report JSON path")
    parser.add_argument("--generated-at-utc", default="2026-01-01T00:00:00Z")
    args = parser.parse_args(argv)

    root = Path(args.repo_root).resolve()
    report = run_checks(root)
    report["generated_at_utc"] = args.generated_at_utc

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    if report["errors"]:
        for err in report["errors"]:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
