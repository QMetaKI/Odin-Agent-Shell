#!/usr/bin/env python3
"""Validate FINAL-PR-07 Field Selection Spine artifacts."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CLAIM_BOUNDARY = "field_selection_scores_routes_not_truth"
REQUIRED_FILES = [
    "odin/field_selection_spine/__init__.py", "odin/field_selection_spine/fields.py", "odin/field_selection_spine/review_axes.py",
    "odin/field_selection_spine/coherence.py", "odin/field_selection_spine/hole_density.py", "odin/field_selection_spine/selector.py",
    "odin/field_selection_spine/why_trace.py", "odin/field_selection_spine/proof.py",
    "registries/final_pr_07_field_selection_spine_registry.json",
    "schemas/final_pr_07_field_selection_spine_proof_packet.schema.json",
    "examples/final_pr_07/field_signal.example.json", "examples/final_pr_07/field_selection.example.json",
    "examples/final_pr_07/coherence_score.example.json", "examples/final_pr_07/field_why_trace.example.json",
    "tools/rebaseline/check_final_pr_07_field_selection_spine.py", "tests/test_final_pr_07_field_selection_spine.py",
    "reports/final_pr_07_field_selection_spine_proof_packet.json",
    "reports/final_pr_07_field_selection_spine_report.json",
    "docs/rebaseline/FINAL_PR_07_FIELD_SELECTION_SPINE.md",
    "docs/codex/handoffs/FINAL_PR_07_REPO_COGNITION_SUMMARY.md",
    "docs/codex/handoffs/FINAL_PR_07_THOR_STYLE_REPO_FIELD_HANDOFF.md",
    "docs/codex/handoffs/FINAL_PR_07_ODIN_AGENT_OPERATOR_WORK_PACKET.md",
    "docs/codex/audits/FINAL_PR_07_FIELD_SELECTION_SPINE_AUDIT.md",
    "docs/codex/audits/FINAL_PR_07_SENIOR_REVIEW.md",
    "docs/codex/audits/FINAL_PR_07_CODE_REVIEW.md",
    "docs/codex/audits/FINAL_PR_07_THOR_ODIN_Y_EFFECTIVENESS_AUDIT.md",
    "docs/codex/reports/FINAL_PR_07_FIELD_SELECTION_SPINE_RETURN_REPORT.md",
]
REQUIRED_FIELD_IDS = ["scope_control", "claim_boundary_integrity", "repo_reality_alignment", "runtime_truth_alignment", "locality_preservation", "candidate_integrity", "evidence_sufficiency", "token_efficiency", "app_authority_boundary", "release_readiness_boundary"]
REQUIRED_AXES = ["scope", "claim_boundary", "repo_reality", "runtime_truth", "locality", "candidate_integrity", "evidence", "token_efficiency", "app_authority", "release_readiness"]
REQUIRED_PROVEN = ["review_axes_defined", "coherence_scorer_deterministic", "field_selection_candidate_only", "why_trace_recorded"]
REQUIRED_NOT_PROVEN = ["autonomous_decision_authority", "final_truth_claim", "model_inference", "provider_execution", "app_apply", "app_state_mutation", "external_send", "production_readiness", "security_certification"]
FORBIDDEN_NAMES = ["dfas", "q_shabang", "qmath", "q_state", "qgit", "qcode", "qli", "qstar"]
FORBIDDEN_CALL_TOKENS = ["openai.", "anthropic.", "requests.", "urllib.request.urlopen", "http.client", "socket.", "subprocess.", "os.system"]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def validate(repo_root: Path) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    checked: list[str] = []
    for rel in REQUIRED_FILES:
        p = repo_root / rel
        checked.append(rel)
        add(errors, p.exists(), f"missing required file: {rel}")
    registry_path = repo_root / "registries/final_pr_07_field_selection_spine_registry.json"
    if registry_path.exists():
        reg = load_json(registry_path)
        add(errors, reg.get("candidate_only") is True, "registry candidate_only must be true")
        add(errors, reg.get("claim_boundary") == CLAIM_BOUNDARY, "registry claim_boundary mismatch")
        for field_id in REQUIRED_FIELD_IDS:
            add(errors, field_id in reg.get("field_ids", []), f"registry missing field_id: {field_id}")
        for axis_id in REQUIRED_AXES:
            add(errors, axis_id in reg.get("review_axis_ids", []), f"registry missing axis_id: {axis_id}")
        add(errors, reg.get("coherence_score_bounds") == [0.0, 1.0], "coherence score bounds must be [0.0, 1.0]")
        add(errors, reg.get("hole_density_bounds") == [0.0, 1.0], "hole density bounds must be [0.0, 1.0]")
    schema_path = repo_root / "schemas/final_pr_07_field_selection_spine_proof_packet.schema.json"
    if schema_path.exists():
        load_json(schema_path)
    for rel in ["examples/final_pr_07/field_signal.example.json", "examples/final_pr_07/field_selection.example.json", "examples/final_pr_07/coherence_score.example.json", "examples/final_pr_07/field_why_trace.example.json"]:
        p = repo_root / rel
        if p.exists():
            data = load_json(p)
            if rel.endswith("field_selection.example.json"):
                add(errors, data.get("candidate_only") is True, "field_selection example candidate_only must be true")
    proof_path = repo_root / "reports/final_pr_07_field_selection_spine_proof_packet.json"
    if proof_path.exists():
        proof = load_json(proof_path)
        for item in REQUIRED_PROVEN:
            add(errors, item in proof.get("proven", []), f"proof packet missing proven: {item}")
        for item in REQUIRED_NOT_PROVEN:
            add(errors, item in proof.get("not_proven", []), f"proof packet missing not_proven: {item}")
    for py in sorted((repo_root / "odin/field_selection_spine").glob("*.py")):
        rel = py.relative_to(repo_root).as_posix()
        checked.append(rel)
        text = py.read_text(encoding="utf-8").lower()
        for forbidden in FORBIDDEN_NAMES:
            add(errors, forbidden not in text, f"forbidden runtime name {forbidden!r} in {rel}")
        for token in FORBIDDEN_CALL_TOKENS:
            add(errors, token not in text, f"forbidden provider/model/network/apply call token {token!r} in {rel}")
    cli = (repo_root / "odin/cli.py").read_text(encoding="utf-8")
    for cmd in ["validate-field-selection-spine", "explain-field-selection", "prove-field-selection-spine"]:
        add(errors, cmd in cli, f"CLI command not registered: {cmd}")
    add(errors, "validate_field_selection_spine()" in cli, "validate_all must call PR07 validator")
    system_map = load_json(repo_root / "SYSTEM_MAP.json")
    add(errors, "final_pr_07_field_selection_spine" in json.dumps(system_map), "SYSTEM_MAP missing final_pr_07_field_selection_spine")
    manifest_text = (repo_root / "FILE_MANIFEST.json").read_text(encoding="utf-8")
    for rel in REQUIRED_FILES:
        add(errors, rel in manifest_text, f"FILE_MANIFEST missing PR07 file: {rel}")
    prep = (repo_root / "tools/rebaseline/check_prep_final_pr_06_08.py").read_text(encoding="utf-8")
    add(errors, '"odin/field_selection_spine"' in prep and "IMPLEMENTED_PR_MODULE_DIRS" in prep, "prep validator does not recognize PR07 implementation")
    add(errors, "odin/projection_candidate_spine" in prep, "prep validator no longer protects PR08 leakage")
    return errors, warnings, sorted(set(checked))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default="reports/final_pr_07_field_selection_spine_report.json")
    parser.add_argument("--generated-at-utc", default="2026-01-01T00:00:00Z")
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    errors, warnings, checked = validate(repo_root)
    report = {"status": "ok" if not errors else "error", "error_count": len(errors), "warning_count": len(warnings), "candidate_only": True, "claim_boundary": CLAIM_BOUNDARY, "checked_files": checked, "errors": errors, "warnings": warnings, "generated_at_utc": args.generated_at_utc}
    out = Path(args.out)
    if not out.is_absolute():
        out = repo_root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
