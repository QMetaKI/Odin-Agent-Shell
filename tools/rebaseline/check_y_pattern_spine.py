"""Y Pattern Spine Validator.

Claim boundary: y_pattern_spine_validator_candidate_only_no_provider_no_app_apply
candidate_only: true
local_only: true
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CLAIM_BOUNDARY = "y_pattern_spine_validator_candidate_only_no_provider_no_app_apply"

FORBIDDEN_NEW_ARTIFACT_NAMES = [
    "q_shabang", "qmath", "q_state", "qgit", "qcode", "qli", "qstar",
    "q_state_os", "q_code", "q_git", "qshabang",
]

REQUIRED_MODULE_FILES = [
    "odin/y_pattern_spine/__init__.py",
    "odin/y_pattern_spine/patterns.py",
    "odin/y_pattern_spine/profiles.py",
    "odin/y_pattern_spine/materialization.py",
    "odin/y_pattern_spine/scoring.py",
    "odin/y_pattern_spine/explain.py",
    "odin/y_pattern_spine/proof.py",
    "odin/y_pattern_spine/token_budget.py",
    "odin/y_pattern_spine/capsules.py",
]

REQUIRED_SCHEMA_FILES = [
    "schemas/y_pattern_spine.schema.json",
    "schemas/y_route_hint.schema.json",
    "schemas/y_work_capsule.schema.json",
    "schemas/y_materialization_ladder.schema.json",
    "schemas/y_projection_set.schema.json",
    "schemas/y_pattern_receipt.schema.json",
    "schemas/y_token_budget.schema.json",
]

REQUIRED_REGISTRY_FILES = [
    "registries/y_pattern_spine.v1.json",
    "registries/y_profile_registry.v1.json",
    "registries/y_materialization_ladder.v1.json",
    "registries/y_source_pattern_mine.v1.json",
    "registries/y_token_budget_registry.v1.json",
]

REQUIRED_EXAMPLE_FILES = [
    "examples/y_pattern_spine.example.json",
    "examples/y_route_hint.example.json",
    "examples/y_work_capsule.example.json",
    "examples/y_projection_set.example.json",
    "examples/y_pattern_receipt.example.json",
    "examples/y_token_budget.example.json",
]

REQUIRED_DOC_FILES = [
    "docs/codex/handoffs/INSERT_Y_PATTERN_SPINE_REPO_REALITY_INTAKE.md",
    "docs/codex/pattern_mines/INSERT_Y_PATTERN_SPINE_SOURCE_PATTERN_MINE_INTAKE.md",
    "docs/codex/audits/INSERT_Y_PATTERN_SPINE_BASELINE_FIT_MATRIX.md",
    "docs/codex/audits/INSERT_Y_PATTERN_SPINE_PATTERN_HARMONY_MATRIX.md",
    "docs/codex/audits/INSERT_Y_PATTERN_SPINE_SENIOR_REVIEW.md",
    "docs/codex/reports/INSERT_Y_PATTERN_SPINE_RETURN_REPORT.md",
    "docs/rebaseline/INSERT_Y_PATTERN_SPINE.md",
]

REQUIRED_REPORT_FILES = [
    "reports/y_pattern_spine_proof_packet.json",
    "reports/insert_y_pattern_spine_report.json",
]

REQUIRED_PATTERN_FAMILIES = [
    "orientation",
    "token_efficiency",
    "review",
    "route_selection",
    "work_state",
    "lineage",
    "center_first",
    "candidate_set",
    "compile_near",
    "projection",
    "operator_pattern",
    "ai_without_ai",
    "scope_compression",
    "balance_axis",
]

REQUIRED_MATERIALIZATION_LEVELS = ["M0", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9"]

NOT_PROVEN_REQUIRED = [
    "model_inference",
    "provider_execution",
    "event_core_runtime",
    "runtime_authority",
    "app_apply",
    "app_state_mutation",
    "external_send",
    "production_readiness",
    "security_certification",
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check_files_exist(repo_root: Path, file_list: list[str]) -> list[str]:
    errors = []
    for rel in file_list:
        p = repo_root / rel
        if not p.exists():
            errors.append(f"missing required file: {rel}")
    return errors


def check_json_valid(repo_root: Path, file_list: list[str]) -> list[str]:
    errors = []
    for rel in file_list:
        p = repo_root / rel
        if not p.exists():
            continue
        try:
            load_json(p)
        except Exception as exc:
            errors.append(f"invalid JSON in {rel}: {exc}")
    return errors


def check_forbidden_names_in_new_artifacts(repo_root: Path) -> list[str]:
    errors = []
    y_spine_root = repo_root / "odin" / "y_pattern_spine"
    if not y_spine_root.exists():
        return errors
    for py_file in y_spine_root.rglob("*.py"):
        text = py_file.read_text(encoding="utf-8").lower()
        for forbidden in FORBIDDEN_NEW_ARTIFACT_NAMES:
            if forbidden in text:
                rel = py_file.relative_to(repo_root)
                errors.append(f"forbidden name '{forbidden}' found in new artifact {rel}")
    for json_file in list((repo_root / "registries").glob("y_*.json")) + \
                     list((repo_root / "schemas").glob("y_*.json")) + \
                     list((repo_root / "examples").glob("y_*.json")):
        text = json_file.read_text(encoding="utf-8").lower()
        for forbidden in FORBIDDEN_NEW_ARTIFACT_NAMES:
            if f'"{forbidden}"' in text or f"'_{forbidden}_'" in text:
                rel = json_file.relative_to(repo_root)
                errors.append(f"forbidden name '{forbidden}' as JSON key in {rel}")
    return errors


def check_pattern_registry(repo_root: Path) -> list[str]:
    errors = []
    reg_path = repo_root / "registries" / "y_pattern_spine.v1.json"
    if not reg_path.exists():
        return ["registries/y_pattern_spine.v1.json missing"]
    try:
        data = load_json(reg_path)
    except Exception as exc:
        return [f"registries/y_pattern_spine.v1.json invalid JSON: {exc}"]
    for family in REQUIRED_PATTERN_FAMILIES:
        if family not in data.get("families", []):
            errors.append(f"y_pattern_spine.v1.json missing required family: {family}")
    if data.get("candidate_only") is not True:
        errors.append("y_pattern_spine.v1.json: candidate_only must be true")
    if not data.get("claim_boundary"):
        errors.append("y_pattern_spine.v1.json: missing claim_boundary")
    return errors


def check_materialization_ladder(repo_root: Path) -> list[str]:
    errors = []
    reg_path = repo_root / "registries" / "y_materialization_ladder.v1.json"
    if not reg_path.exists():
        return ["registries/y_materialization_ladder.v1.json missing"]
    try:
        data = load_json(reg_path)
    except Exception as exc:
        return [f"materialization ladder invalid JSON: {exc}"]
    levels = [lv.get("level") for lv in data.get("levels", [])]
    for required_level in REQUIRED_MATERIALIZATION_LEVELS:
        if required_level not in levels:
            errors.append(f"materialization ladder missing level: {required_level}")
    return errors


def check_route_hint_example(repo_root: Path) -> list[str]:
    errors = []
    p = repo_root / "examples" / "y_route_hint.example.json"
    if not p.exists():
        return ["examples/y_route_hint.example.json missing"]
    try:
        data = load_json(p)
    except Exception as exc:
        return [f"y_route_hint.example.json invalid JSON: {exc}"]
    if not data.get("candidate_routes"):
        errors.append("y_route_hint.example.json: missing candidate_routes")
    if not data.get("evidence_required") and data.get("evidence_required") != []:
        errors.append("y_route_hint.example.json: missing evidence_required")
    if not data.get("selected_route"):
        errors.append("y_route_hint.example.json: missing selected_route")
    if not data.get("token_budget_hint"):
        errors.append("y_route_hint.example.json: missing token_budget_hint")
    return errors


def check_work_capsule_example(repo_root: Path) -> list[str]:
    errors = []
    p = repo_root / "examples" / "y_work_capsule.example.json"
    if not p.exists():
        return ["examples/y_work_capsule.example.json missing"]
    try:
        data = load_json(p)
    except Exception as exc:
        return [f"y_work_capsule.example.json invalid JSON: {exc}"]
    if not data.get("allowed_files"):
        errors.append("y_work_capsule.example.json: missing allowed_files")
    if "forbidden_files" not in data:
        errors.append("y_work_capsule.example.json: missing forbidden_files")
    if not data.get("validators"):
        errors.append("y_work_capsule.example.json: missing validators")
    if not data.get("proof_commands"):
        errors.append("y_work_capsule.example.json: missing proof_commands")
    return errors


def check_token_budget_modes(repo_root: Path) -> list[str]:
    errors = []
    p = repo_root / "registries" / "y_token_budget_registry.v1.json"
    if not p.exists():
        return ["registries/y_token_budget_registry.v1.json missing"]
    try:
        data = load_json(p)
    except Exception as exc:
        return [f"y_token_budget_registry.v1.json invalid: {exc}"]
    modes = data.get("modes", {})
    for required_mode in ["minimal", "normal", "deep"]:
        if required_mode not in modes:
            errors.append(f"y_token_budget_registry.v1.json missing mode: {required_mode}")
    return errors


def check_projection_set_example(repo_root: Path) -> list[str]:
    errors = []
    p = repo_root / "examples" / "y_projection_set.example.json"
    if not p.exists():
        return ["examples/y_projection_set.example.json missing"]
    try:
        data = load_json(p)
    except Exception as exc:
        return [f"y_projection_set.example.json invalid: {exc}"]
    if not data.get("human_clear_projection"):
        errors.append("y_projection_set.example.json: missing human_clear_projection")
    if not data.get("expression_projection"):
        errors.append("y_projection_set.example.json: missing expression_projection")
    if not data.get("machine_projection"):
        errors.append("y_projection_set.example.json: missing machine_projection")
    return errors


def check_proof_packet(repo_root: Path) -> list[str]:
    errors = []
    p = repo_root / "reports" / "y_pattern_spine_proof_packet.json"
    if not p.exists():
        return ["reports/y_pattern_spine_proof_packet.json missing (run prove-y-pattern-spine first)"]
    try:
        data = load_json(p)
    except Exception as exc:
        return [f"y_pattern_spine_proof_packet.json invalid: {exc}"]
    for field in NOT_PROVEN_REQUIRED:
        not_proven = data.get("not_proven", [])
        if field not in not_proven:
            errors.append(f"proof packet missing not_proven entry: {field}")
    if data.get("candidate_only") is not True:
        errors.append("proof packet: candidate_only must be true")
    return errors


def check_patterns_have_required_fields(repo_root: Path) -> list[str]:
    errors = []
    try:
        sys.path.insert(0, str(repo_root))
        from odin.y_pattern_spine.patterns import list_patterns
        for pattern in list_patterns():
            if not pattern.allowed_use:
                errors.append(f"pattern {pattern.pattern_id}: missing allowed_use")
            if not pattern.forbidden_use:
                errors.append(f"pattern {pattern.pattern_id}: missing forbidden_use")
            if not pattern.claim_boundary:
                errors.append(f"pattern {pattern.pattern_id}: missing claim_boundary")
    except Exception as exc:
        errors.append(f"could not load patterns module: {exc}")
    return errors


def check_demo_route_command(repo_root: Path) -> list[str]:
    errors = []
    try:
        sys.path.insert(0, str(repo_root))
        from odin.y_pattern_spine.profiles import build_route_hint_demo, DEMO_ROUTE_HINT
        demo = build_route_hint_demo()
        if demo.get("selected_route") != "work_capsule_then_response_packet":
            errors.append("demo route hint: selected_route is not deterministic expected value")
        if demo.get("candidate_only") is not True:
            errors.append("demo route hint: candidate_only must be true")
        if not demo.get("not_proven"):
            errors.append("demo route hint: missing not_proven")
    except Exception as exc:
        errors.append(f"could not load route hint demo: {exc}")
    return errors


def check_no_provider_model_execution(repo_root: Path) -> list[str]:
    errors = []
    y_spine_root = repo_root / "odin" / "y_pattern_spine"
    if not y_spine_root.exists():
        return errors
    forbidden_imports = [
        "import anthropic",
        "import openai",
        "requests.post",
        "http.client.HTTPSConnection",
        "urllib.request.urlopen",
    ]
    for py_file in y_spine_root.rglob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        for pattern in forbidden_imports:
            if pattern in text:
                rel = py_file.relative_to(repo_root)
                errors.append(f"forbidden pattern '{pattern}' in {rel}")
    return errors


def run_all_checks(repo_root: Path) -> list[str]:
    errors = []
    errors.extend(check_files_exist(repo_root, REQUIRED_MODULE_FILES))
    errors.extend(check_files_exist(repo_root, REQUIRED_SCHEMA_FILES))
    errors.extend(check_files_exist(repo_root, REQUIRED_REGISTRY_FILES))
    errors.extend(check_files_exist(repo_root, REQUIRED_EXAMPLE_FILES))
    errors.extend(check_json_valid(repo_root, REQUIRED_SCHEMA_FILES))
    errors.extend(check_json_valid(repo_root, REQUIRED_REGISTRY_FILES))
    errors.extend(check_json_valid(repo_root, REQUIRED_EXAMPLE_FILES))
    errors.extend(check_forbidden_names_in_new_artifacts(repo_root))
    errors.extend(check_pattern_registry(repo_root))
    errors.extend(check_materialization_ladder(repo_root))
    errors.extend(check_route_hint_example(repo_root))
    errors.extend(check_work_capsule_example(repo_root))
    errors.extend(check_token_budget_modes(repo_root))
    errors.extend(check_projection_set_example(repo_root))
    errors.extend(check_patterns_have_required_fields(repo_root))
    errors.extend(check_demo_route_command(repo_root))
    errors.extend(check_no_provider_model_execution(repo_root))
    errors.extend(check_proof_packet(repo_root))
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Check Y Pattern Spine validator")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument("--out", default=None, help="Output JSON report path")
    parser.add_argument("--generated-at-utc", default="2026-01-01T00:00:00Z")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    errors = run_all_checks(repo_root)

    report = {
        "report_id": "odin.y_pattern_spine_check",
        "status": "ok" if not errors else "error",
        "generated_at_utc": args.generated_at_utc,
        "repo_root": str(repo_root),
        "error_count": len(errors),
        "errors": errors,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
    }

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))

    print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
