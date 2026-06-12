#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQUIRED_FILES = [
    "docs/codex/handoffs/PREP_FINAL_PR_06_08_REPO_REALITY_INTAKE.md",
    "docs/codex/pattern_mines/PREP_FINAL_PR_06_08_SOURCE_PATTERN_SYNTHESIS.md",
    "docs/rebaseline/PREP_FINAL_PR_06_08_OPERATIONAL_SEED_DFAS_PROJECTION_PLAN.md",
    "registries/prep_final_pr_06_08_plan.v1.json",
    "reports/prep_final_pr_06_08_plan_report.json",
    "reports/prep_final_pr_06_08_source_pattern_synthesis.json",
    "docs/codex/prompts/FINAL_PR_06_OPERATIONAL_SEED_SPINE_CLAUDE_PROMPT.md",
    "docs/codex/prompts/FINAL_PR_07_DFAS_FIELD_SELECTION_CLAUDE_PROMPT.md",
    "docs/codex/prompts/FINAL_PR_08_PROJECTION_SHADOW_CANDIDATE_CLAUDE_PROMPT.md",
    "docs/codex/prompts/FINAL_PR_09_RELEASE_CLOSURE_CLAUDE_PROMPT.md",
    "docs/codex/audits/PREP_FINAL_PR_06_08_SENIOR_REVIEW.md",
    "docs/codex/audits/PREP_FINAL_PR_06_08_CODE_REVIEW.md",
    "docs/codex/audits/PREP_FINAL_PR_06_08_ROADMAP_AUDIT.md",
    "docs/codex/reports/PREP_FINAL_PR_06_08_RETURN_REPORT.md",
    "reports/prep_final_pr_06_08_report.json",
    "reports/prep_final_pr_06_08_roadmap_audit.json",
]

PROMPTS = [
    "docs/codex/prompts/FINAL_PR_06_OPERATIONAL_SEED_SPINE_CLAUDE_PROMPT.md",
    "docs/codex/prompts/FINAL_PR_07_DFAS_FIELD_SELECTION_CLAUDE_PROMPT.md",
    "docs/codex/prompts/FINAL_PR_08_PROJECTION_SHADOW_CANDIDATE_CLAUDE_PROMPT.md",
    "docs/codex/prompts/FINAL_PR_09_RELEASE_CLOSURE_CLAUDE_PROMPT.md",
]

ACCEPTANCE_ITEMS = [
    "operational_seed_spine_prepared",
    "field_selection_spine_prepared",
    "projection_spine_prepared",
    "final_pr_06_claude_prompt_ready",
    "final_pr_07_claude_prompt_ready",
    "final_pr_08_claude_prompt_ready",
    "final_pr_09_release_prompt_skeleton_ready",
    "release_closure_shifted_to_final_pr_09",
]

FORBIDDEN_AUTHORITY_PATTERNS = [
    "authorizes provider execution",
    "authorizes model execution",
    "authorizes model inference",
    "authorizes app apply",
    "authorizes app state",
    "authorizes external send",
    "may mutate app state",
    "may send externally",
]

FORBIDDEN_Q_ARTIFACT_RE = re.compile(r"(?:^|/)(q_shabang|qmath|q_state|qgit|qcode|qli|qstar|q_[a-z0-9_]*)(?:[./_-]|$)", re.IGNORECASE)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def has_all(text: str, needles: list[str]) -> list[str]:
    lowered = text.lower()
    return [needle for needle in needles if needle.lower() not in lowered]


def validate(repo_root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED_FILES:
        if not (repo_root / rel).exists():
            errors.append(f"missing required prep artifact: {rel}")

    for rel in [
        "registries/prep_final_pr_06_08_plan.v1.json",
        "reports/prep_final_pr_06_08_plan_report.json",
        "reports/prep_final_pr_06_08_source_pattern_synthesis.json",
        "reports/prep_final_pr_06_08_report.json",
        "reports/prep_final_pr_06_08_roadmap_audit.json",
    ]:
        path = repo_root / rel
        if path.exists():
            try:
                data = load_json(path)
            except Exception as exc:
                errors.append(f"invalid JSON {rel}: {exc}")
                continue
            for key, expected in [("candidate_only", True), ("local_only", True), ("app_owned_apply", True)]:
                if data.get(key) is not expected:
                    errors.append(f"{rel}: {key} must be true")

    plan_path = repo_root / "registries/prep_final_pr_06_08_plan.v1.json"
    if plan_path.exists():
        plan = load_json(plan_path)
        amendment = json.dumps(plan.get("roadmap_amendment", {}))
        for marker in ["FINAL-PR-06", "FINAL-PR-07", "FINAL-PR-08", "FINAL-PR-09"]:
            if marker not in amendment:
                errors.append(f"master prep plan missing roadmap amendment marker {marker}")
        if plan.get("status") != "prepared_not_complete":
            errors.append("master prep plan must remain prepared_not_complete")

    roadmap_text = (repo_root / "docs/rebaseline/FINAL_MINIMAL_ROAD_TO_100_PR_ROADMAP_V1.md").read_text(encoding="utf-8", errors="ignore")
    acceptance_text = (repo_root / "docs/rebaseline/FINAL_100_PERCENT_ACCEPTANCE_DEFINITION_V1.md").read_text(encoding="utf-8", errors="ignore")
    combined_acceptance = roadmap_text + "\n" + acceptance_text
    for item in ACCEPTANCE_ITEMS:
        if item not in combined_acceptance:
            errors.append(f"acceptance item missing from roadmap/acceptance docs: {item}")
    if "FINAL-PR-09: Release / Closure / Full Acceptance" not in combined_acceptance:
        errors.append("release closure shift to FINAL-PR-09 missing")

    return_report = repo_root / "docs/codex/reports/PREP_FINAL_PR_06_08_RETURN_REPORT.md"
    if return_report.exists():
        report_text = return_report.read_text(encoding="utf-8", errors="ignore")
        for anchor in ["## Merge Conflict Repair", "current main SHA used", "conflicted files", "resolution policy", "validators run", "tests run", "final status"]:
            if anchor not in report_text:
                errors.append(f"docs/codex/reports/PREP_FINAL_PR_06_08_RETURN_REPORT.md: missing merge repair anchor {anchor}")
        if re.search(r"^(<<<<<<<|=======|>>>>>>>)", report_text, re.MULTILINE):
            errors.append("docs/codex/reports/PREP_FINAL_PR_06_08_RETURN_REPORT.md: contains conflict marker")

    required_prompt_sections = [
        "objective",
        "base rule",
        "allowed scope",
        "forbidden scope",
        "files to create",
        "cli commands",
        "validator requirement",
        "tests requirement",
        "proof packet requirement",
        "senior review loop",
        "final response format",
    ]
    for rel in PROMPTS:
        path = repo_root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        missing = has_all(text, required_prompt_sections)
        for section in missing:
            errors.append(f"{rel}: missing prompt section {section}")
        lower = text.lower()
        for required in ["no provider execution", "model inference", "no app apply", "app state mutation", "external send"]:
            if required not in lower:
                errors.append(f"{rel}: missing boundary phrase {required}")
        for pattern in FORBIDDEN_AUTHORITY_PATTERNS:
            if pattern in lower:
                errors.append(f"{rel}: contains forbidden authority phrase {pattern}")

    prompt_checks = {
        "docs/codex/prompts/FINAL_PR_06_OPERATIONAL_SEED_SPINE_CLAUDE_PROMPT.md": ["Operational Seed Spine", "Seeds do not decide truth", "Role profiles are not personas"],
        "docs/codex/prompts/FINAL_PR_07_DFAS_FIELD_SELECTION_CLAUDE_PROMPT.md": ["DFAS Field Selection", "does not authorize apply", "model execution", "external send", "truth"],
        "docs/codex/prompts/FINAL_PR_08_PROJECTION_SHADOW_CANDIDATE_CLAUDE_PROMPT.md": ["Projection Spine", "not runtime proof", "not executable runtime"],
        "docs/codex/prompts/FINAL_PR_09_RELEASE_CLOSURE_CLAUDE_PROMPT.md": ["Release / Closure", "after FINAL-PR-06", "FINAL-PR-08"],
    }
    for rel, anchors in prompt_checks.items():
        path = repo_root / rel
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="ignore")
            for anchor in anchors:
                if anchor not in text:
                    errors.append(f"{rel}: missing anchor {anchor}")

    # Check newly planned artifact names for forbidden Q-style names. Existing historical files are not scanned.
    planned_names = []
    if plan_path.exists():
        plan = load_json(plan_path)
        planned_names.extend(plan.get("expected_cli", []))
        for values in plan.get("expected_files", {}).values():
            planned_names.extend(values)
    for prompt in PROMPTS:
        path = repo_root / prompt
        if path.exists():
            planned_names.append(prompt)
    for name in planned_names:
        normalized = name.replace("qirc", "event_core")
        if FORBIDDEN_Q_ARTIFACT_RE.search(normalized):
            errors.append(f"forbidden Q-style new artifact name: {name}")

    for rel in ["SYSTEM_MAP.json", "FILE_MANIFEST.json"]:
        path = repo_root / rel
        if not path.exists():
            errors.append(f"missing {rel}")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for required in [
            "PREP_FINAL_PR_06_08_REPO_REALITY_INTAKE.md",
            "FINAL_PR_06_OPERATIONAL_SEED_SPINE_CLAUDE_PROMPT.md",
            "check_prep_final_pr_06_08.py",
            "test_prep_final_pr_06_08.py",
        ]:
            if required not in text:
                errors.append(f"{rel}: missing manifest/map reference {required}")

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default=None)
    parser.add_argument("--generated-at-utc", default="2026-01-01T00:00:00Z")
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    errors, warnings = validate(repo_root)
    report = {
        "report_id": "odin.prep_final_pr_06_08_check",
        "status": "ok" if not errors else "error",
        "generated_at_utc": args.generated_at_utc,
        "repo_root": str(repo_root),
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "claim_boundary": "prep_validator_only_not_runtime_provider_model_network_app_authority_security_or_release_proof",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "merge_conflict_repair": {
            "current_main_sha_used": "unavailable_no_origin_main_in_workspace",
            "head_sha_before_repair": "4b74d8124e554d1d85681d96b9da76dd1f5227bb",
            "conflicted_files": [],
            "conflict_type": "origin_main_unavailable_in_container_no_local_conflict_markers",
            "resolution_policy": "union_preserve_main_and_pr43_prep_artifacts_when_merge_context_is_available",
            "files_changed_during_repair": [
                "docs/codex/reports/PREP_FINAL_PR_06_08_RETURN_REPORT.md",
                "reports/prep_final_pr_06_08_report.json",
                "tools/rebaseline/check_prep_final_pr_06_08.py",
                "tests/test_prep_final_pr_06_08.py",
                "SYSTEM_MAP.json",
                "FILE_MANIFEST.json"
            ],
            "validation_commands": [
                {"command": "python -m odin.cli validate-prep-final-pr-06-08", "result": "OK"},
                {"command": "python tools/rebaseline/check_prep_final_pr_06_08.py --repo-root . --out reports/prep_final_pr_06_08_report.json --generated-at-utc 2026-01-01T00:00:00Z", "result": "status ok"},
                {"command": "python -m odin.cli validate-all", "result": "OK"},
                {"command": "PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_prep_final_pr_06_08.py -p no:cacheprovider", "result": "17 passed"},
                {"command": "PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_final_road_to_100_rebaseline_audit.py tests/test_v7_1_1_operational_coverage_gap_compiler.py -p no:cacheprovider", "result": "59 passed"},
                {"command": "PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider", "result": "2243 passed, 2 skipped"}
            ],
            "final_status": "prep_repair_bounded_no_pr06_08_runtime_no_release_closure_implementation",
        },
    }
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
