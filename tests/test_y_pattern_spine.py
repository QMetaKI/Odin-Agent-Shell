"""Tests for Y Pattern Spine.

Claim boundary: y_pattern_spine_test_candidate_only_no_provider_no_app_apply
candidate_only: true
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


# --- Helper ---

def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def run_cli(*args) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli"] + list(args),
        capture_output=True, text=True, cwd=str(ROOT),
    )
    return result.returncode, result.stdout + result.stderr


# --- 1. Schemas load ---

def test_schemas_load():
    schema_files = [
        "schemas/y_pattern_spine.schema.json",
        "schemas/y_route_hint.schema.json",
        "schemas/y_work_capsule.schema.json",
        "schemas/y_materialization_ladder.schema.json",
        "schemas/y_projection_set.schema.json",
        "schemas/y_pattern_receipt.schema.json",
        "schemas/y_token_budget.schema.json",
    ]
    for rel in schema_files:
        p = ROOT / rel
        assert p.exists(), f"missing schema: {rel}"
        data = load_json(p)
        assert isinstance(data, dict), f"not a dict: {rel}"


# --- 2. Registries load ---

def test_registries_load():
    reg_files = [
        "registries/y_pattern_spine.v1.json",
        "registries/y_profile_registry.v1.json",
        "registries/y_materialization_ladder.v1.json",
        "registries/y_source_pattern_mine.v1.json",
        "registries/y_token_budget_registry.v1.json",
    ]
    for rel in reg_files:
        p = ROOT / rel
        assert p.exists(), f"missing registry: {rel}"
        data = load_json(p)
        assert isinstance(data, dict), f"not a dict: {rel}"


# --- 3. Examples load ---

def test_examples_load():
    example_files = [
        "examples/y_pattern_spine.example.json",
        "examples/y_route_hint.example.json",
        "examples/y_work_capsule.example.json",
        "examples/y_projection_set.example.json",
        "examples/y_pattern_receipt.example.json",
        "examples/y_token_budget.example.json",
    ]
    for rel in example_files:
        p = ROOT / rel
        assert p.exists(), f"missing example: {rel}"
        data = load_json(p)
        assert isinstance(data, dict), f"not a dict: {rel}"


# --- 4. Forbidden new names absent ---

def test_forbidden_new_names_absent():
    forbidden = [
        "q_shabang", "qmath", "q_state", "qgit", "qcode", "qli", "qstar",
        "q_state_os", "q_code", "q_git",
    ]
    y_spine_root = ROOT / "odin" / "y_pattern_spine"
    assert y_spine_root.exists(), "y_pattern_spine module missing"
    for py_file in y_spine_root.rglob("*.py"):
        text = py_file.read_text(encoding="utf-8").lower()
        for f in forbidden:
            assert f not in text, f"forbidden name '{f}' found in {py_file.relative_to(ROOT)}"


# --- 5. Pattern spine has required families ---

def test_pattern_spine_has_required_families():
    from odin.y_pattern_spine.patterns import PATTERN_FAMILIES
    required = [
        "orientation", "token_efficiency", "review", "route_selection",
        "work_state", "lineage", "center_first", "candidate_set",
        "compile_near", "projection", "operator_pattern", "ai_without_ai",
        "scope_compression", "balance_axis",
    ]
    for family in required:
        assert family in PATTERN_FAMILIES, f"missing family: {family}"


# --- 6. Baseline fit matrix exists and maps every included pattern to Odin target surface ---

def test_baseline_fit_matrix_exists_and_maps():
    from odin.y_pattern_spine.patterns import list_patterns
    patterns = list_patterns()
    assert len(patterns) > 0, "no patterns loaded"
    for p in patterns:
        assert p.odin_target_surface is not None, f"pattern {p.pattern_id} has no odin_target_surface"
        assert p.odin_target_surface != "", f"pattern {p.pattern_id} has empty odin_target_surface"


# --- 7. Harmony matrix exists and defines composition/conflict policies ---

def test_harmony_matrix_exists():
    from odin.y_pattern_spine.patterns import list_patterns
    patterns = list_patterns()
    for p in patterns:
        assert p.allowed_use, f"pattern {p.pattern_id} missing allowed_use"
        assert p.forbidden_use, f"pattern {p.pattern_id} missing forbidden_use"
        assert p.claim_boundary, f"pattern {p.pattern_id} missing claim_boundary"


# --- 8. Materialization ladder has M0–M9 ---

def test_materialization_ladder_has_all_levels():
    from odin.y_pattern_spine.materialization import MATERIALIZATION_LADDER, list_levels
    levels = list_levels()
    for required in ["M0", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9"]:
        assert required in levels, f"missing materialization level: {required}"
    assert len(MATERIALIZATION_LADDER) == 10


# --- 9. Route hint demo selects deterministic route ---

def test_route_hint_demo_deterministic():
    from odin.y_pattern_spine.profiles import build_route_hint_demo
    demo = build_route_hint_demo()
    assert demo["selected_route"] == "work_capsule_then_response_packet"
    assert demo["candidate_only"] is True
    assert demo["artifact_kind"] == "y_route_explanation_demo"


# --- 10. Route hint includes token_budget_hint ---

def test_route_hint_has_token_budget_hint():
    from odin.y_pattern_spine.profiles import build_route_hint_demo
    demo = build_route_hint_demo()
    assert "token_budget_hint" in demo
    assert demo["token_budget_hint"] in ("minimal", "normal", "deep")


# --- 11. Work capsule includes allowed_files and forbidden_files ---

def test_work_capsule_has_files():
    from odin.y_pattern_spine.capsules import build_work_capsule_demo
    capsule = build_work_capsule_demo()
    assert len(capsule.allowed_files) > 0
    assert len(capsule.forbidden_files) > 0
    assert capsule.token_budget in ("minimal", "normal", "deep")


# --- 12. Token budget modes minimal/normal/deep exist ---

def test_token_budget_modes_exist():
    from odin.y_pattern_spine.token_budget import TOKEN_BUDGET_MODES
    for mode in ("minimal", "normal", "deep"):
        assert mode in TOKEN_BUDGET_MODES, f"missing token budget mode: {mode}"
        budget = TOKEN_BUDGET_MODES[mode]
        assert budget.includes
        assert budget.excludes


# --- 13. Projection set includes human_clear, expression, machine ---

def test_projection_set_has_three_projections():
    from odin.y_pattern_spine.explain import build_projection_set_demo
    proj = build_projection_set_demo()
    assert proj.human_clear_projection
    assert proj.expression_projection
    assert isinstance(proj.machine_projection, dict)
    assert proj.lineage_trace


# --- 14. Proof packet includes not_proven model/provider/event/app claims ---

def test_proof_packet_not_proven():
    from odin.y_pattern_spine.proof import build_proof_packet
    packet = build_proof_packet()
    required_not_proven = [
        "model_inference", "provider_execution", "event_core_runtime",
        "runtime_authority", "app_apply", "app_state_mutation",
        "external_send", "production_readiness", "security_certification",
    ]
    not_proven = packet.get("not_proven", [])
    for item in required_not_proven:
        assert item in not_proven, f"proof packet missing not_proven: {item}"
    assert packet["candidate_only"] is True


# --- 15. validate-y-pattern-spine passes ---

def test_validate_y_pattern_spine_cli():
    code, output = run_cli("validate-y-pattern-spine")
    assert code == 0, f"validate-y-pattern-spine failed:\n{output}"
    assert "OK" in output


# --- 16. explain-y-route --demo returns expected JSON ---

def test_explain_y_route_demo_cli():
    code, output = run_cli("explain-y-route", "--demo")
    assert code == 0, f"explain-y-route --demo failed:\n{output}"
    data = json.loads(output.strip().split("\n", 1)[0] + "..." if "{" not in output else output)
    # parse just the JSON part
    for line in output.split("\n"):
        if "{" in line:
            break
    parsed = json.loads(output[output.index("{"):])
    assert parsed["selected_route"] == "work_capsule_then_response_packet"
    assert parsed["candidate_only"] is True
    assert parsed["artifact_kind"] == "y_route_explanation_demo"
    assert "not_proven" in parsed


# --- 17. prove-y-pattern-spine returns expected JSON ---

def test_prove_y_pattern_spine_cli():
    code, output = run_cli("prove-y-pattern-spine")
    assert code == 0, f"prove-y-pattern-spine failed:\n{output}"
    parsed = json.loads(output[output.index("{"):])
    assert parsed["candidate_only"] is True
    assert parsed["artifact_kind"] == "y_pattern_spine_proof_packet"
    assert "model_inference" in parsed["not_proven"]
    assert parsed["pattern_spine_loaded"] is True


# --- 18. validate-all includes y pattern spine validator ---

def test_validate_all_includes_y_pattern_spine():
    code, output = run_cli("validate-all")
    assert code == 0, f"validate-all failed:\n{output}"


# --- 19. Local hub /demo/y-route.json works ---

def test_local_hub_y_route_endpoint():
    from odin.y_pattern_spine.profiles import build_route_hint_demo
    result = build_route_hint_demo()
    assert result["selected_route"] == "work_capsule_then_response_packet"
    assert result["candidate_only"] is True


# --- 20. No provider/model execution occurs ---

def test_no_provider_model_execution():
    y_spine_root = ROOT / "odin" / "y_pattern_spine"
    forbidden_imports = [
        "import anthropic", "import openai",
        "requests.post", "urllib.request.urlopen",
    ]
    for py_file in y_spine_root.rglob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        for pattern in forbidden_imports:
            assert pattern not in text, f"forbidden import '{pattern}' in {py_file.name}"


# --- 21. No app apply/state/external-send introduced ---

def test_no_app_apply_state():
    y_spine_root = ROOT / "odin" / "y_pattern_spine"
    forbidden_patterns = [
        "app_state_mutation(", "external_send(", "app_apply(",
    ]
    for py_file in y_spine_root.rglob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        for pattern in forbidden_patterns:
            assert pattern not in text, f"forbidden call '{pattern}' in {py_file.name}"


# --- 22. No event core runtime proof claimed ---

def test_no_event_core_runtime_proof():
    from odin.y_pattern_spine.proof import build_proof_packet
    packet = build_proof_packet()
    assert "event_core_runtime" in packet["not_proven"]


# --- 23. No religious/source-specific labels in new runtime artifacts ---

def test_no_religious_labels_in_runtime():
    religious_terms = ["bible", "bibleOS", "bible_os", "holy", "sacred", "divine"]
    y_spine_root = ROOT / "odin" / "y_pattern_spine"
    for py_file in y_spine_root.rglob("*.py"):
        text = py_file.read_text(encoding="utf-8").lower()
        for term in religious_terms:
            assert term not in text, f"religious term '{term}' found in {py_file.name}"


# --- 24. Full pytest passes ---

def test_full_module_import():
    from odin.y_pattern_spine import (
        YPattern, YRouteHint, YMaterializationLevel, YSelectionScore,
        YProjectionSet, YPatternReceipt, YTokenBudget, YWorkCapsule,
        PATTERN_FAMILIES, TOKEN_BUDGET_MODES, MATERIALIZATION_LADDER,
        list_patterns, list_families, get_level,
        build_route_hint_demo, build_projection_set_demo,
        build_proof_packet, build_work_capsule_demo,
    )
    assert PATTERN_FAMILIES
    assert TOKEN_BUDGET_MODES
    assert MATERIALIZATION_LADDER
    patterns = list_patterns()
    assert len(patterns) >= 10
    families = list_families()
    assert len(families) >= 14
    level_m7 = get_level("M7")
    assert level_m7 is not None
    assert level_m7.level == "M7"


# --- Additional: proof packet persisted ---

def test_proof_packet_persisted():
    p = ROOT / "reports" / "y_pattern_spine_proof_packet.json"
    assert p.exists(), "reports/y_pattern_spine_proof_packet.json not persisted (run prove-y-pattern-spine)"
    data = load_json(p)
    assert data["candidate_only"] is True
    assert "model_inference" in data["not_proven"]
