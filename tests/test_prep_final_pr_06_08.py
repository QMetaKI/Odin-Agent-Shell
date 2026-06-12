"""Tests for Prep FINAL-PR-06..08 scaffold artifacts.

Claim boundary: prep_final_pr_06_08_prepares_future_prs_not_runtime_execution
candidate_only: true
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(rel: str) -> dict:
    p = ROOT / rel
    assert p.exists(), f"File not found: {rel}"
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


# ---------- Test 1: Required prompt files exist ----------

def test_required_prompt_files_exist():
    required = [
        "docs/codex/prompts/FINAL_PR_06_OPERATIONAL_SEED_SPINE.md",
        "docs/codex/prompts/FINAL_PR_07_FIELD_SELECTION_SPINE.md",
        "docs/codex/prompts/FINAL_PR_08_PROJECTION_CANDIDATE_SPINE.md",
        "docs/codex/prompts/FINAL_PR_09_RELEASE_CLOSURE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), f"Missing required prompt: {rel}"


# ---------- Test 2: Registry exists and parses ----------

def test_registry_exists_and_parses():
    data = load_json("registries/prep_final_pr_06_08_plan.v1.json")
    assert "registry_id" in data
    assert "version" in data
    assert "future_prs" in data
    assert isinstance(data["future_prs"], dict)
    assert data.get("candidate_only") is True
    assert "claim_boundary" in data


# ---------- Test 3: PR06 entry exists ----------

def test_pr06_entry_exists():
    data = load_json("registries/prep_final_pr_06_08_plan.v1.json")
    future_prs = data["future_prs"]
    assert "final_pr_06_operational_seed_spine" in future_prs
    pr06 = future_prs["final_pr_06_operational_seed_spine"]
    assert pr06["claim_boundary"] == "operational_seed_spine_routes_work_not_authority"
    assert len(pr06.get("expected_modules", [])) >= 5
    assert len(pr06.get("expected_cli", [])) >= 3


# ---------- Test 4: PR07 entry exists ----------

def test_pr07_entry_exists():
    data = load_json("registries/prep_final_pr_06_08_plan.v1.json")
    future_prs = data["future_prs"]
    assert "final_pr_07_field_selection_spine" in future_prs
    pr07 = future_prs["final_pr_07_field_selection_spine"]
    assert pr07["claim_boundary"] == "field_selection_scores_routes_not_truth"
    assert len(pr07.get("expected_modules", [])) >= 5
    assert "autonomous_decision_authority" in pr07.get("forbidden_scope", [])


# ---------- Test 5: PR08 entry exists ----------

def test_pr08_entry_exists():
    data = load_json("registries/prep_final_pr_06_08_plan.v1.json")
    future_prs = data["future_prs"]
    assert "final_pr_08_projection_candidate_spine" in future_prs
    pr08 = future_prs["final_pr_08_projection_candidate_spine"]
    assert pr08["claim_boundary"] == "projection_candidate_spine_prepares_candidates_not_runtime_execution"
    assert len(pr08.get("expected_modules", [])) >= 5
    assert "executing_models_or_generating_code_via_model_calls" in pr08.get("forbidden_scope", [])


# ---------- Test 6: PR09 release entry exists ----------

def test_pr09_release_entry_exists():
    data = load_json("registries/prep_final_pr_06_08_plan.v1.json")
    future_prs = data["future_prs"]
    assert "final_pr_09_release_closure" in future_prs
    pr09 = future_prs["final_pr_09_release_closure"]
    assert pr09["claim_boundary"] == "release_closure_records_evidence_not_production_certification"
    title = pr09.get("title", "")
    assert "Release" in title or "release" in title.lower()
    assert "Closure" in title or "closure" in title.lower()


# ---------- Test 7: PR09 depends on PR06, PR07, PR08 ----------

def test_pr09_depends_on_pr06_pr07_pr08():
    data = load_json("registries/prep_final_pr_06_08_plan.v1.json")
    pr09 = data["future_prs"]["final_pr_09_release_closure"]
    depends = pr09.get("depends_on", [])
    assert "final_pr_06_operational_seed_spine_merged" in depends, \
        "PR09 must depend on PR06"
    assert "final_pr_07_field_selection_spine_merged" in depends, \
        "PR09 must depend on PR07"
    assert "final_pr_08_projection_candidate_spine_merged" in depends, \
        "PR09 must depend on PR08"


# ---------- Test 8: Each future PR has forbidden scope ----------

def test_each_future_pr_has_forbidden_scope():
    data = load_json("registries/prep_final_pr_06_08_plan.v1.json")
    for pr_id, pr_entry in data["future_prs"].items():
        forbidden = pr_entry.get("forbidden_scope", [])
        assert isinstance(forbidden, list), f"PR {pr_id}: forbidden_scope must be a list"
        assert len(forbidden) >= 3, f"PR {pr_id}: forbidden_scope must have at least 3 entries"


# ---------- Test 9: Each future PR has claim boundary ----------

def test_each_future_pr_has_claim_boundary():
    data = load_json("registries/prep_final_pr_06_08_plan.v1.json")
    for pr_id, pr_entry in data["future_prs"].items():
        cb = pr_entry.get("claim_boundary", "")
        assert cb, f"PR {pr_id}: missing claim_boundary"
        assert isinstance(cb, str), f"PR {pr_id}: claim_boundary must be a string"
        assert len(cb) > 10, f"PR {pr_id}: claim_boundary too short: {cb!r}"


# ---------- Test 10: Validator returns ok ----------

def test_validator_returns_ok(tmp_path):
    import importlib.util
    validator_path = ROOT / "tools/rebaseline/check_prep_final_pr_06_08.py"
    assert validator_path.exists(), "Validator file not found"

    spec = importlib.util.spec_from_file_location("check_prep_final_pr_06_08", validator_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    out_file = tmp_path / "prep_check.json"
    result = mod.main([
        "--repo-root", str(ROOT),
        "--out", str(out_file),
        "--generated-at-utc", "2026-01-01T00:00:00Z",
    ])
    assert result == 0, f"Validator returned non-zero exit code: {result}"
    assert out_file.exists(), "Validator did not write output file"
    report = json.loads(out_file.read_text())
    assert report["status"] == "ok", f"Validator status not ok: {report.get('errors', [])}"
    assert isinstance(report["errors"], list)
    assert len(report["errors"]) == 0, f"Validator errors: {report['errors']}"


# ---------- Test 11: CLI command returns ok ----------

def test_cli_command_returns_ok():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-prep-final-pr-06-08"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, (
        f"CLI command failed.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    )
    assert "ok" in result.stdout.lower() or "validate-prep-final-pr-06-08" in result.stdout


# ---------- Test 12: validate-all includes prep validator ----------

def test_validate_all_includes_prep_validator():
    cli_path = ROOT / "odin" / "cli.py"
    content = cli_path.read_text(encoding="utf-8")
    assert "validate_prep_final_pr_06_08" in content, \
        "odin/cli.py must call validate_prep_final_pr_06_08 from validate_all()"
    assert "validate-prep-final-pr-06-08" in content, \
        "odin/cli.py must have validate-prep-final-pr-06-08 subparser"

    # Verify it's actually called in validate_all
    import ast
    tree = ast.parse(content)
    validate_all_func = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "validate_all":
            validate_all_func = node
            break
    assert validate_all_func is not None, "validate_all function not found in cli.py"
    func_src = ast.get_source_segment(content, validate_all_func) or ""
    assert "validate_prep_final_pr_06_08" in func_src, \
        "validate_prep_final_pr_06_08 must be called from validate_all()"


# ---------- Test 13: Pattern synthesis file contains source-to-neutral mapping ----------

def test_pattern_synthesis_contains_source_neutral_mapping():
    p = ROOT / "docs/codex/pattern_mines/PREP_FINAL_PR_06_08_SOURCE_PATTERN_SYNTHESIS.md"
    assert p.exists(), "Pattern synthesis file not found"
    content = p.read_text(encoding="utf-8")
    required_markers = [
        "Source Concept",
        "Neutral Odin Concept",
        "Target PR",
        "Target Surface",
    ]
    for marker in required_markers:
        assert marker in content, f"Pattern synthesis missing mapping table marker: {marker!r}"
    assert "IntentSeed" in content, "Pattern synthesis must mention IntentSeed"
    assert "RoleProfile" in content, "Pattern synthesis must mention RoleProfile"
    assert "FieldSelection" in content or "field_selection" in content, \
        "Pattern synthesis must mention field selection"
    assert "ProjectionSet" in content, "Pattern synthesis must mention ProjectionSet"


# ---------- Test 14: No forbidden new runtime Q-style names in runtime artifacts ----------

def test_no_forbidden_q_names_in_disallowed_sections():
    """Check that no forbidden Q-style names appear as new runtime identifiers.

    Only checks runtime artifact locations (future PR module dirs).
    Documentation, validator, and test files may reference these names
    in order to document what is forbidden.

    NOTE: odin/operational_seed_spine is skipped here because FINAL-PR-06 has
    been implemented. That PR's own tests verify its naming conventions.
    """
    import re
    forbidden = [
        "q_shabang", "qshabang", "qmath", "q_math",
        "q_state", "qstate", "qgit", "q_git", "qcode", "q_code",
        "qli", "q_li", "qstar", "q_star",
    ]
    # Modules now implemented by their respective PRs — checked by those PRs' own tests
    implemented_dirs = ["odin/operational_seed_spine", "odin/field_selection_spine"]
    future_runtime_dirs = [
        "odin/operational_seed_spine",
        "odin/field_selection_spine",
        "odin/projection_candidate_spine",
    ]
    violations = []
    for rel_dir in future_runtime_dirs:
        if rel_dir in implemented_dirs:
            continue  # Now implemented; naming checked by its own PR test
        d = ROOT / rel_dir
        if not d.exists():
            continue
        for py_file in d.glob("*.py"):
            content = py_file.read_text(encoding="utf-8").lower()
            for name in forbidden:
                if name in content:
                    violations.append(f"{py_file.relative_to(ROOT)}: forbidden name {name!r}")
    assert not violations, "Forbidden Q-style names found in runtime artifacts:\n" + "\n".join(violations)


# ---------- Test 15: Prep PR does not claim model/provider execution or app apply ----------

def test_prep_pr_no_execution_or_apply_claims():
    forbidden_phrases = [
        "model_inference: true",
        "provider_execution: true",
        "app_apply: true",
        "app_state_mutation: true",
        "allows public network by default",
    ]
    files_to_check = [
        "docs/codex/prompts/FINAL_PR_06_OPERATIONAL_SEED_SPINE.md",
        "docs/codex/prompts/FINAL_PR_07_FIELD_SELECTION_SPINE.md",
        "docs/codex/prompts/FINAL_PR_08_PROJECTION_CANDIDATE_SPINE.md",
        "docs/codex/prompts/FINAL_PR_09_RELEASE_CLOSURE.md",
        "registries/prep_final_pr_06_08_plan.v1.json",
        "reports/prep_final_pr_06_08_report.json",
    ]
    violations = []
    for rel in files_to_check:
        p = ROOT / rel
        if not p.exists():
            continue
        content = p.read_text(encoding="utf-8").lower()
        for phrase in forbidden_phrases:
            if phrase.lower() in content:
                violations.append(f"{rel}: found forbidden phrase: {phrase!r}")
    assert not violations, "Forbidden execution/apply claims found:\n" + "\n".join(violations)


# ---------- Test 16: Report JSON has correct structure ----------

def test_prep_report_json_structure():
    data = load_json("reports/prep_final_pr_06_08_report.json")
    assert "status" in data
    assert "errors" in data
    assert "not_proven" in data
    assert "claim_boundaries" in data
    assert "candidate_only" in data
    assert data.get("candidate_only") is True
    cb = data.get("claim_boundaries", {})
    assert "prep_pr" in cb
    assert cb["prep_pr"] == "prep_final_pr_06_08_prepares_future_prs_not_runtime_execution"


# ---------- Test 17: Prompt quality matrix has all four prompts ----------

def test_prompt_quality_matrix_coverage():
    data = load_json("reports/prep_final_pr_06_08_prompt_quality_matrix.json")
    scores = data.get("scores", {})
    assert "FINAL_PR_06_OPERATIONAL_SEED_SPINE" in scores
    assert "FINAL_PR_07_FIELD_SELECTION_SPINE" in scores
    assert "FINAL_PR_08_PROJECTION_CANDIDATE_SPINE" in scores
    assert "FINAL_PR_09_RELEASE_CLOSURE" in scores
    for key, score_entry in scores.items():
        assert "overall" in score_entry, f"Score entry {key!r} missing 'overall'"
        assert score_entry["overall"] >= 8.0, f"Score for {key!r} below threshold: {score_entry['overall']}"


# ---------- Test 18: Handoff file covers required existing surfaces ----------

def test_handoff_covers_existing_surfaces():
    p = ROOT / "docs/codex/handoffs/PREP_FINAL_PR_06_08_REPO_REALITY_INTAKE.md"
    assert p.exists()
    content = p.read_text(encoding="utf-8")
    required_surface_mentions = [
        "local_hub", "qirc", "y_pattern_spine", "execution_gate", "proof_chain"
    ]
    for surface in required_surface_mentions:
        assert surface in content.lower(), \
            f"Handoff file missing reference to existing surface: {surface!r}"


# ---------- Test 19: No runtime module dirs for future PRs exist in prep PR ----------

def test_no_future_pr_runtime_modules_exist():
    # Modules now legitimately implemented by their respective PRs — skip them
    implemented_dirs = ["odin/operational_seed_spine", "odin/field_selection_spine"]  # Implemented by FINAL-PR-06
    future_module_dirs = [
        "odin/operational_seed_spine",
        "odin/field_selection_spine",
        "odin/projection_candidate_spine",
    ]
    for rel in future_module_dirs:
        if rel in implemented_dirs:
            continue  # Legitimately implemented; no longer "future" leakage
        p = ROOT / rel
        if p.exists() and p.is_dir():
            py_files = list(p.glob("*.py"))
            assert not py_files, (
                f"Prep PR should NOT implement runtime module {rel!r}. "
                f"Found {len(py_files)} .py files. These belong in future PR implementations."
            )


# ---------- Test 20: Pattern synthesis has neutral neutralizations section ----------

def test_pattern_synthesis_has_neutralizations():
    p = ROOT / "docs/codex/pattern_mines/PREP_FINAL_PR_06_08_SOURCE_PATTERN_SYNTHESIS.md"
    assert p.exists()
    content = p.read_text(encoding="utf-8")
    assert "Operational Neutralizations" in content or "neutralization" in content.lower()
    assert "Seed System Extraction" in content or "seed system" in content.lower()
    assert "Archetype-to-Role-Profile" in content or "role profile" in content.lower()
    assert "DFAS" in content or "field selection" in content.lower()
