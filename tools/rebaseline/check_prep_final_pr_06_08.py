"""Prep FINAL-PR-06..08 Validator.

Claim boundary: prep_final_pr_06_08_prepares_future_prs_not_runtime_execution
candidate_only: true
local_only: true
stdlib_only: true
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

CLAIM_BOUNDARY = "prep_final_pr_06_08_prepares_future_prs_not_runtime_execution"

FORBIDDEN_RUNTIME_NAMES = [
    "q_shabang", "qshabang", "q_shebang", "qmath", "q_math",
    "q_state", "qstate", "qgit", "q_git", "qcode", "q_code",
    "qli", "q_li", "qstar", "q_star",
]

REQUIRED_PROMPT_FILES = [
    "docs/codex/prompts/FINAL_PR_06_OPERATIONAL_SEED_SPINE.md",
    "docs/codex/prompts/FINAL_PR_07_FIELD_SELECTION_SPINE.md",
    "docs/codex/prompts/FINAL_PR_08_PROJECTION_CANDIDATE_SPINE.md",
    "docs/codex/prompts/FINAL_PR_09_RELEASE_CLOSURE.md",
]

REQUIRED_HANDOFF_FILES = [
    "docs/codex/handoffs/PREP_FINAL_PR_06_08_REPO_REALITY_INTAKE.md",
]

REQUIRED_PATTERN_MINE_FILES = [
    "docs/codex/pattern_mines/PREP_FINAL_PR_06_08_SOURCE_PATTERN_SYNTHESIS.md",
]

REQUIRED_PLAN_FILES = [
    "docs/rebaseline/PREP_FINAL_PR_06_08_OPERATIONAL_SEED_DFAS_PROJECTION_PLAN.md",
]

REQUIRED_AUDIT_FILES = [
    "docs/codex/audits/PREP_FINAL_PR_06_08_SENIOR_REVIEW.md",
    "docs/codex/audits/PREP_FINAL_PR_06_08_CODE_REVIEW.md",
    "docs/codex/audits/PREP_FINAL_PR_06_08_ROADMAP_AUDIT.md",
]

REQUIRED_REPORT_FILES = [
    "docs/codex/reports/PREP_FINAL_PR_06_08_RETURN_REPORT.md",
    "reports/prep_final_pr_06_08_report.json",
    "reports/prep_final_pr_06_08_prompt_quality_matrix.json",
]

REQUIRED_REGISTRY_FILE = "registries/prep_final_pr_06_08_plan.v1.json"
REQUIRED_VALIDATOR_FILE = "tools/rebaseline/check_prep_final_pr_06_08.py"
REQUIRED_TEST_FILE = "tests/test_prep_final_pr_06_08.py"

REQUIRED_FUTURE_PR_IDS = [
    "final_pr_06_operational_seed_spine",
    "final_pr_07_field_selection_spine",
    "final_pr_08_projection_candidate_spine",
    "final_pr_09_release_closure",
]

PROMPT_REQUIRED_SECTIONS = [
    "Claim boundary",
    "candidate_only",
    "Scope",
    "Non-Scope",
    "Allowed Files",
    "Forbidden Changes",
    "Claim Boundary",
    "Not-Proven",
    "Acceptance Gates",
]

PROMPT_FORBIDDEN_CLAIM_PHRASES = [
    "provider_execution: true",
    "model_inference: true",
    "app_apply: true",
    "app_state_mutation: true",
    "public_network: true",
    "allows public network by default",
    "allows app apply",
    "allows external send",
]

RUNTIME_MODULE_DIRS_FOR_FUTURE_PRS = [
    "odin/operational_seed_spine",
    "odin/field_selection_spine",
    "odin/projection_candidate_spine",
]

# When a future PR has been implemented, its module dir is no longer "leakage".
# Track implemented PR modules here so the prep validator skips them gracefully.
IMPLEMENTED_PR_MODULE_DIRS = [
    "odin/operational_seed_spine",  # FINAL-PR-06 implemented
]

# JSON artifacts that are expected to exist once the corresponding PR is implemented.
IMPLEMENTED_PR_JSON_ARTIFACTS = [
    "schemas/final_pr_06_operational_seed_spine_proof_packet.schema.json",
    "registries/final_pr_06_operational_seed_spine_registry.json",
]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check_files_exist(repo_root: Path, file_list: list[str]) -> list[str]:
    errors = []
    for rel in file_list:
        p = repo_root / rel
        if not p.exists():
            errors.append(f"missing required file: {rel}")
    return errors


def check_registry(repo_root: Path) -> list[str]:
    errors = []
    p = repo_root / REQUIRED_REGISTRY_FILE
    if not p.exists():
        return [f"missing registry: {REQUIRED_REGISTRY_FILE}"]
    try:
        data = load_json(p)
    except Exception as exc:
        return [f"registry parse error: {exc}"]

    future_prs = data.get("future_prs", {})
    if not isinstance(future_prs, dict):
        return ["registry: future_prs must be a dict"]

    for pr_id in REQUIRED_FUTURE_PR_IDS:
        if pr_id not in future_prs:
            errors.append(f"registry: missing future PR entry: {pr_id}")

    for pr_id, pr_entry in future_prs.items():
        if not isinstance(pr_entry, dict):
            errors.append(f"registry: PR entry {pr_id!r} must be a dict")
            continue
        if "forbidden_scope" not in pr_entry or not pr_entry["forbidden_scope"]:
            errors.append(f"registry: PR {pr_id!r} missing or empty forbidden_scope")
        if "claim_boundary" not in pr_entry or not pr_entry["claim_boundary"]:
            errors.append(f"registry: PR {pr_id!r} missing or empty claim_boundary")
        if "depends_on" not in pr_entry:
            errors.append(f"registry: PR {pr_id!r} missing depends_on")
        if "not_proven" not in pr_entry or not pr_entry["not_proven"]:
            errors.append(f"registry: PR {pr_id!r} missing or empty not_proven")

    pr09 = future_prs.get("final_pr_09_release_closure", {})
    if isinstance(pr09, dict):
        depends = pr09.get("depends_on", [])
        for req_dep in [
            "final_pr_06_operational_seed_spine_merged",
            "final_pr_07_field_selection_spine_merged",
            "final_pr_08_projection_candidate_spine_merged",
        ]:
            if req_dep not in depends:
                errors.append(
                    f"registry: PR09 depends_on missing required dependency: {req_dep}"
                )
        not_proven = pr09.get("not_proven", [])
        for req_np in ["production_readiness", "security_certification"]:
            if req_np not in not_proven:
                errors.append(
                    f"registry: PR09 not_proven must include: {req_np}"
                )

    return errors


def check_prompt_sections(repo_root: Path) -> list[str]:
    errors = []
    for rel in REQUIRED_PROMPT_FILES:
        p = repo_root / rel
        if not p.exists():
            continue
        try:
            content = p.read_text(encoding="utf-8")
        except Exception as exc:
            errors.append(f"prompt read error {rel}: {exc}")
            continue
        for section in PROMPT_REQUIRED_SECTIONS:
            if section.lower() not in content.lower():
                errors.append(f"prompt {rel!r} missing required section: {section!r}")
        for phrase in PROMPT_FORBIDDEN_CLAIM_PHRASES:
            if phrase.lower() in content.lower():
                errors.append(
                    f"prompt {rel!r} contains forbidden claim phrase: {phrase!r}"
                )
    return errors


def check_no_forbidden_names(repo_root: Path) -> list[str]:
    """Check that no forbidden Q-style names appear as new runtime identifiers.

    Only checks actual runtime artifact locations:
    - New Python modules under odin/ (if they exist from future PRs)
    - New JSON schema/registry/example files for future PRs

    Documentation, validator, and test files may legitimately reference
    forbidden names in order to document what is forbidden.
    """
    errors = []

    # Only check runtime artifact locations — not docs, validators, or tests
    # These directories would only have content if a future PR was incorrectly
    # implemented in this prep PR.
    runtime_artifact_patterns = [
        ("odin/operational_seed_spine", "*.py"),
        ("odin/field_selection_spine", "*.py"),
        ("odin/projection_candidate_spine", "*.py"),
    ]

    for dir_rel, glob_pattern in runtime_artifact_patterns:
        # Skip dirs that are now implemented by their respective PR
        if dir_rel in IMPLEMENTED_PR_MODULE_DIRS:
            continue
        d = repo_root / dir_rel
        if not d.exists():
            continue
        for py_file in d.glob(glob_pattern):
            try:
                content = py_file.read_text(encoding="utf-8").lower()
            except Exception:
                continue
            for forbidden in FORBIDDEN_RUNTIME_NAMES:
                if forbidden in content:
                    rel_str = str(py_file.relative_to(repo_root))
                    errors.append(
                        f"forbidden runtime name {forbidden!r} found in new runtime artifact {rel_str!r}"
                    )

    # Check new JSON artifacts for future PRs (schemas, registries, examples)
    for json_rel in [
        "schemas/final_pr_07_field_selection_spine_proof_packet.schema.json",
        "schemas/final_pr_08_projection_candidate_spine_proof_packet.schema.json",
        "registries/final_pr_07_field_selection_spine_registry.json",
        "registries/final_pr_08_projection_candidate_spine_registry.json",
    ]:
        # Skip JSON artifacts from implemented PRs
        if json_rel in IMPLEMENTED_PR_JSON_ARTIFACTS:
            continue
        p = repo_root / json_rel
        if not p.exists():
            continue
        try:
            content = p.read_text(encoding="utf-8").lower()
        except Exception:
            continue
        for forbidden in FORBIDDEN_RUNTIME_NAMES:
            if f'"{forbidden}"' in content:
                errors.append(
                    f"forbidden runtime name {forbidden!r} as JSON key in {json_rel!r}"
                )

    return errors


def check_no_runtime_module_leakage(repo_root: Path) -> list[str]:
    errors = []
    for module_dir in RUNTIME_MODULE_DIRS_FOR_FUTURE_PRS:
        # Skip dirs that are legitimately implemented by their PR
        if module_dir in IMPLEMENTED_PR_MODULE_DIRS:
            continue
        p = repo_root / module_dir
        if p.exists() and p.is_dir():
            py_files = list(p.glob("*.py"))
            if py_files:
                errors.append(
                    f"prep PR should not implement runtime module: {module_dir}/ "
                    f"(found {len(py_files)} .py files — future PR only)"
                )
    return errors


def check_validate_all_integration(repo_root: Path) -> list[str]:
    errors = []
    cli_path = repo_root / "odin" / "cli.py"
    if not cli_path.exists():
        return ["odin/cli.py not found"]
    try:
        content = cli_path.read_text(encoding="utf-8")
    except Exception as exc:
        return [f"cli.py read error: {exc}"]
    if "validate-prep-final-pr-06-08" not in content:
        errors.append("odin/cli.py: missing 'validate-prep-final-pr-06-08' command")
    if "validate_prep_final_pr_06_08" not in content:
        errors.append("odin/cli.py: missing validate_prep_final_pr_06_08 function reference")
    return errors


def check_system_map_file_manifest(repo_root: Path) -> list[str]:
    errors = []
    sm_path = repo_root / "SYSTEM_MAP.json"
    if not sm_path.exists():
        errors.append("SYSTEM_MAP.json missing")
    else:
        try:
            sm = load_json(sm_path)
            if "prep_final_pr_06_08" not in sm:
                errors.append("SYSTEM_MAP.json: missing prep_final_pr_06_08 entry")
        except Exception as exc:
            errors.append(f"SYSTEM_MAP.json parse error: {exc}")

    fm_path = repo_root / "FILE_MANIFEST.json"
    if not fm_path.exists():
        errors.append("FILE_MANIFEST.json missing")
    else:
        try:
            fm = load_json(fm_path)
            files_list = fm.get("files", [])
            if not isinstance(files_list, list):
                errors.append("FILE_MANIFEST.json: 'files' must be a list")
            else:
                all_paths: list[str] = []
                for entry in files_list:
                    if isinstance(entry, str):
                        all_paths.append(entry)
                    elif isinstance(entry, dict):
                        p_val = entry.get("path", "")
                        if p_val:
                            all_paths.append(p_val)
                files_str = " ".join(all_paths)
                if "prep_final_pr_06_08" not in files_str:
                    errors.append(
                        "FILE_MANIFEST.json: missing prep_final_pr_06_08 file references"
                    )
        except Exception as exc:
            errors.append(f"FILE_MANIFEST.json parse error: {exc}")

    return errors


def check_pattern_synthesis_has_mapping(repo_root: Path) -> list[str]:
    errors = []
    p = repo_root / "docs/codex/pattern_mines/PREP_FINAL_PR_06_08_SOURCE_PATTERN_SYNTHESIS.md"
    if not p.exists():
        return ["missing pattern synthesis file"]
    content = p.read_text(encoding="utf-8")
    required_markers = [
        "Source Concept",
        "Neutral Odin Concept",
        "Target PR",
        "Target Surface",
    ]
    for marker in required_markers:
        if marker not in content:
            errors.append(
                f"pattern synthesis file missing mapping table marker: {marker!r}"
            )
    return errors


def run_all_checks(repo_root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    checked_files: list[str] = []

    all_required = (
        REQUIRED_PROMPT_FILES
        + REQUIRED_HANDOFF_FILES
        + REQUIRED_PATTERN_MINE_FILES
        + REQUIRED_PLAN_FILES
        + REQUIRED_AUDIT_FILES
        + REQUIRED_REPORT_FILES
        + [REQUIRED_REGISTRY_FILE, REQUIRED_VALIDATOR_FILE, REQUIRED_TEST_FILE]
    )
    errors.extend(check_files_exist(repo_root, all_required))
    checked_files.extend(all_required)

    errors.extend(check_registry(repo_root))
    errors.extend(check_prompt_sections(repo_root))
    errors.extend(check_no_forbidden_names(repo_root))
    errors.extend(check_no_runtime_module_leakage(repo_root))
    errors.extend(check_validate_all_integration(repo_root))
    errors.extend(check_system_map_file_manifest(repo_root))
    errors.extend(check_pattern_synthesis_has_mapping(repo_root))

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate Prep FINAL-PR-06..08 scaffold artifacts"
    )
    parser.add_argument("--repo-root", default=".", help="Path to repo root")
    parser.add_argument("--out", default=None, help="Write JSON report to this path")
    parser.add_argument(
        "--generated-at-utc",
        default=None,
        help="Override generated_at_utc timestamp",
    )
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    errors, warnings = run_all_checks(repo_root)

    generated_at = args.generated_at_utc or datetime.datetime.utcnow().strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    all_required = (
        REQUIRED_PROMPT_FILES
        + REQUIRED_HANDOFF_FILES
        + REQUIRED_PATTERN_MINE_FILES
        + REQUIRED_PLAN_FILES
        + REQUIRED_AUDIT_FILES
        + REQUIRED_REPORT_FILES
        + [REQUIRED_REGISTRY_FILE, REQUIRED_VALIDATOR_FILE, REQUIRED_TEST_FILE]
    )

    report = {
        "status": "ok" if not errors else "fail",
        "errors": errors,
        "warnings": warnings,
        "checked_files": all_required,
        "candidate_only": True,
        "future_prs": REQUIRED_FUTURE_PR_IDS,
        "roadmap_shift": {
            "release_closure_moved_to": "final_pr_09",
            "historical_prs_renumbered": False,
            "pr06_08_required_before_release": True,
        },
        "claim_boundaries": {
            "prep_pr": CLAIM_BOUNDARY,
            "final_pr_06": "operational_seed_spine_routes_work_not_authority",
            "final_pr_07": "field_selection_scores_routes_not_truth",
            "final_pr_08": "projection_candidate_spine_prepares_candidates_not_runtime_execution",
            "final_pr_09": "release_closure_records_evidence_not_production_certification",
        },
        "not_proven": [
            "final_pr_06_runtime_implemented",
            "final_pr_07_runtime_implemented",
            "final_pr_08_runtime_implemented",
            "final_pr_09_release_closure_complete",
            "model_inference",
            "provider_execution",
            "app_apply",
            "app_state_mutation",
            "external_send_authority",
            "production_readiness",
            "security_certification",
            "live_model_inference",
        ],
        "generated_at_utc": generated_at,
    }

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False, sort_keys=True)

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        print(f"\ncheck_prep_final_pr_06_08: FAIL ({len(errors)} errors)", file=sys.stderr)
        return 1

    if warnings:
        for w in warnings:
            print(f"WARNING: {w}")
    print("check_prep_final_pr_06_08: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
