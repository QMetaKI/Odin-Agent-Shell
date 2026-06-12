"""Tests for FINAL-PR-06 Operational Seed Spine.

Claim boundary: operational_seed_spine_routes_work_not_authority
candidate_only: true

Tests are deterministic. No external network, providers, models, or non-deterministic clocks.
"""
from __future__ import annotations

import importlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

# ── 1. Imports ─────────────────────────────────────────────────────────────


def test_module_imports():
    mod = importlib.import_module("odin.operational_seed_spine")
    assert hasattr(mod, "CLAIM_BOUNDARY")
    assert hasattr(mod, "INTENT_SEEDS")
    assert hasattr(mod, "ROLE_PROFILES")
    assert hasattr(mod, "SEED_PACKS")
    assert hasattr(mod, "select_seed_route")
    assert hasattr(mod, "compile_work_capsule")
    assert hasattr(mod, "build_proof_packet")


# ── 2-4. Required collections defined ──────────────────────────────────────


def test_required_seed_packs_defined():
    from odin.operational_seed_spine.seed_packs import SEED_PACKS, REQUIRED_SEED_PACK_IDS
    pack_ids = {p.pack_id for p in SEED_PACKS}
    for required in REQUIRED_SEED_PACK_IDS:
        assert required in pack_ids, f"Missing seed pack: {required}"


def test_required_seed_ids_defined():
    from odin.operational_seed_spine.intent_seeds import INTENT_SEEDS, REQUIRED_SEED_IDS
    seed_ids = {s.seed_id for s in INTENT_SEEDS}
    for required in REQUIRED_SEED_IDS:
        assert required in seed_ids, f"Missing seed: {required}"


def test_required_role_profiles_defined():
    from odin.operational_seed_spine.role_profiles import ROLE_PROFILES, REQUIRED_ROLE_PROFILE_IDS
    profile_ids = {p.role_profile_id for p in ROLE_PROFILES}
    for required in REQUIRED_ROLE_PROFILE_IDS:
        assert required in profile_ids, f"Missing role profile: {required}"


# ── 5. Seeds have required fields ──────────────────────────────────────────


def test_seeds_have_required_fields():
    from odin.operational_seed_spine.intent_seeds import INTENT_SEEDS
    required_fields = [
        "seed_id", "family", "trigger_shapes", "input_requirements",
        "output_shape", "preferred_surfaces", "allowed_use", "forbidden_use",
        "qirc_event_hints", "validator_expectations", "proof_boundary",
        "token_budget_key", "fallback_behavior",
    ]
    for seed in INTENT_SEEDS:
        for f in required_fields:
            assert hasattr(seed, f), f"Seed {seed.seed_id!r} missing field {f!r}"
            val = getattr(seed, f)
            assert val is not None and val != "" and val != [], \
                f"Seed {seed.seed_id!r} field {f!r} is empty"


# ── 6. Role profiles have required fields ──────────────────────────────────


def test_role_profiles_have_required_fields():
    from odin.operational_seed_spine.role_profiles import ROLE_PROFILES
    required_fields = [
        "role_profile_id", "family", "allowed_use", "forbidden_use",
        "review_axes", "output_shape", "claim_boundary",
    ]
    for profile in ROLE_PROFILES:
        for f in required_fields:
            assert hasattr(profile, f), f"Profile {profile.role_profile_id!r} missing field {f!r}"


# ── 7. Selector exact trigger match ────────────────────────────────────────


def test_selector_exact_trigger_match():
    from odin.operational_seed_spine.selector import select_seed_route
    route = select_seed_route({"trigger_shape": "repo"})
    assert route.selected_seed_id == "repo_cognition"
    assert route.selection_priority == "exact_trigger_shape"
    assert route.fallback_used is False


def test_selector_exact_trigger_match_code():
    from odin.operational_seed_spine.selector import select_seed_route
    route = select_seed_route({"trigger_shape": "code_change"})
    assert route.selected_seed_id == "code_change"
    assert route.selection_priority == "exact_trigger_shape"
    assert route.fallback_used is False


# ── 8. Selector family/surface match ───────────────────────────────────────


def test_selector_family_match():
    from odin.operational_seed_spine.selector import select_seed_route
    route = select_seed_route({"family": "boundary"})
    assert route.selection_priority == "family_surface_match"
    assert route.fallback_used is False


def test_selector_surface_match():
    from odin.operational_seed_spine.selector import select_seed_route
    route = select_seed_route({"surface": "worker"})
    assert route.selection_priority == "family_surface_match"
    assert route.fallback_used is False


# ── 9. Selector deterministic fallback ─────────────────────────────────────


def test_selector_deterministic_fallback():
    from odin.operational_seed_spine.selector import select_seed_route, FALLBACK_SEED_ID
    route = select_seed_route({})
    assert route.fallback_used is True
    assert route.selected_seed_id == FALLBACK_SEED_ID
    assert route.selection_priority == "deterministic_fallback"


# ── 10. Selector stable across repeated calls ──────────────────────────────


def test_selector_stable():
    from odin.operational_seed_spine.selector import select_seed_route
    ctx = {"trigger_shape": "debug"}
    r1 = select_seed_route(ctx)
    r2 = select_seed_route(ctx)
    assert r1.selected_seed_id == r2.selected_seed_id
    assert r1.selected_role_profile_id == r2.selected_role_profile_id
    assert r1.fallback_used == r2.fallback_used
    assert r1.selection_priority == r2.selection_priority


# ── 11. Work capsule compiles from route ───────────────────────────────────


def test_work_capsule_compiles():
    from odin.operational_seed_spine.selector import select_seed_route
    from odin.operational_seed_spine.work_capsule import compile_work_capsule
    route = select_seed_route({"trigger_shape": "repo"})
    capsule = compile_work_capsule(route)
    assert capsule.seed_id == "repo_cognition"
    assert capsule.role_profile_id == route.selected_role_profile_id
    assert capsule.capsule_id.startswith("seed_capsule_")
    assert isinstance(capsule.qirc_hints, list)
    assert isinstance(capsule.token_budget, dict)


# ── 12. Capsule ID is deterministic ────────────────────────────────────────


def test_capsule_id_deterministic():
    from odin.operational_seed_spine.selector import select_seed_route
    from odin.operational_seed_spine.work_capsule import compile_work_capsule
    ctx = {"trigger_shape": "repo"}
    r1 = compile_work_capsule(select_seed_route(ctx))
    r2 = compile_work_capsule(select_seed_route(ctx))
    assert r1.capsule_id == r2.capsule_id


def test_capsule_id_no_uuid4():
    from odin.operational_seed_spine import work_capsule
    import inspect
    src = inspect.getsource(work_capsule)
    assert "uuid4" not in src
    assert "uuid.uuid4" not in src
    assert "time.time()" not in src
    assert "datetime.now()" not in src


# ── 13-15. Capsule boundary fields ─────────────────────────────────────────


def test_capsule_candidate_only_true():
    from odin.operational_seed_spine.selector import select_seed_route
    from odin.operational_seed_spine.work_capsule import compile_work_capsule
    capsule = compile_work_capsule(select_seed_route({"trigger_shape": "proof"}))
    assert capsule.candidate_only is True


def test_capsule_app_owned_apply_true():
    from odin.operational_seed_spine.selector import select_seed_route
    from odin.operational_seed_spine.work_capsule import compile_work_capsule
    capsule = compile_work_capsule(select_seed_route({"trigger_shape": "proof"}))
    assert capsule.app_owned_apply is True


def test_capsule_has_claim_boundary():
    from odin.operational_seed_spine.selector import select_seed_route
    from odin.operational_seed_spine.work_capsule import compile_work_capsule
    capsule = compile_work_capsule(select_seed_route({}))
    assert capsule.claim_boundary == "operational_seed_spine_routes_work_not_authority"


# ── 16. QIRC hints are hint_only ───────────────────────────────────────────


def test_qirc_hints_are_hint_only():
    from odin.operational_seed_spine.qirc_hints import build_qirc_hints
    hints = build_qirc_hints(["work_seed_selected", "repo_cognition_started"])
    assert len(hints) == 2
    for hint in hints:
        assert hint["authority"] == "hint_only"
        assert hint["candidate_only"] is True


# ── 17. Token budget is per seed ───────────────────────────────────────────


def test_token_budget_per_seed():
    from odin.operational_seed_spine.token_budget import get_token_budget, REQUIRED_BUDGET_KEYS
    for key in REQUIRED_BUDGET_KEYS:
        budget = get_token_budget(key)
        assert budget["budget_key"] == key
        assert budget["candidate_only"] is True
        assert "max_input_tokens_hint" in budget
        assert "max_output_tokens_hint" in budget


# ── 18-19. Proof packet ────────────────────────────────────────────────────


def test_proof_packet_proven_list():
    from odin.operational_seed_spine.proof import build_proof_packet, PROVEN
    packet = build_proof_packet()
    proven = set(packet["proven"])
    for p in ["seed_packs_defined", "role_profiles_defined",
               "selector_deterministic", "work_capsule_compiled"]:
        assert p in proven


def test_proof_packet_not_proven_list():
    from odin.operational_seed_spine.proof import build_proof_packet
    packet = build_proof_packet()
    not_proven = set(packet["not_proven"])
    for p in ["autonomous_reasoning", "model_inference", "provider_execution",
               "app_apply", "app_state_mutation", "external_send",
               "production_readiness", "security_certification"]:
        assert p in not_proven


# ── 20. Validator returns ok ───────────────────────────────────────────────


def test_validator_returns_ok():
    import importlib.util
    tool_path = ROOT / "tools/rebaseline/check_final_pr_06_operational_seed_spine.py"
    assert tool_path.exists()
    spec = importlib.util.spec_from_file_location("_check_pr06", tool_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "report.json"
        code = mod.main(["--repo-root", str(ROOT), "--out", str(out),
                         "--generated-at-utc", "2026-01-01T00:00:00Z"])
        assert code == 0, f"Validator returned {code}: {out.read_text()}"
        report = json.loads(out.read_text())
        assert report["status"] == "ok"
        assert report["error_count"] == 0


# ── 21. CLI validate-operational-seed-spine returns 0 ─────────────────────


def test_cli_validate_operational_seed_spine():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-operational-seed-spine"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 0, f"stderr: {result.stderr}\nstdout: {result.stdout}"


# ── 22. CLI explain-seed-route --demo returns valid JSON ──────────────────


def test_cli_explain_seed_route_demo():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "explain-seed-route", "--demo"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    data = json.loads(result.stdout)
    assert data.get("candidate_only") is True
    assert "selected_seed_id" in data or "seed_route" in data


# ── 23. CLI prove-operational-seed-spine returns 0 ────────────────────────


def test_cli_prove_operational_seed_spine():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "prove-operational-seed-spine"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    data = json.loads(result.stdout)
    assert data.get("candidate_only") is True


# ── 24. Local hub seed route payload returns valid JSON ───────────────────


def test_local_hub_seed_route_payload():
    from odin.operational_seed_spine.selector import select_seed_route
    from odin.operational_seed_spine.work_capsule import compile_work_capsule
    route = select_seed_route({"trigger_shape": "repo"})
    capsule = compile_work_capsule(route)
    payload = {
        "status": "ok",
        "candidate_only": True,
        "claim_boundary": "operational_seed_spine_routes_work_not_authority",
        "seed_route": route.to_dict(),
        "work_capsule": capsule.to_dict(),
        "not_proven": capsule.not_proven,
    }
    serialized = json.dumps(payload)
    parsed = json.loads(serialized)
    assert parsed["status"] == "ok"
    assert parsed["candidate_only"] is True
    assert parsed["seed_route"]["selected_seed_id"] == "repo_cognition"


# ── 25. No forbidden Q-style runtime names ────────────────────────────────


def test_no_forbidden_q_style_names():
    import re
    forbidden = ["q_shabang", "qmath", "q_state", "qgit", "qcode", "qli", "qstar"]
    module_dir = ROOT / "odin" / "operational_seed_spine"
    for py_file in module_dir.glob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        for name in forbidden:
            # Look for usage as runtime identifier (variable/function/class/import), not in guard lists
            identifier_pat = re.compile(
                r'(?:^|\s|=|,|\(|\[)' + re.escape(name) + r'(?:\s*=|\s*\(|$|\s|,|\)|\])',
                re.MULTILINE,
            )
            assert not identifier_pat.search(text), \
                f"Forbidden Q-style runtime identifier {name!r} found in {py_file.name}"


# ── 26. validate-all includes PR06 validator ──────────────────────────────


def test_validate_all_includes_pr06():
    cli_path = ROOT / "odin" / "cli.py"
    text = cli_path.read_text(encoding="utf-8")
    assert "validate_operational_seed_spine" in text, \
        "validate_all does not call validate_operational_seed_spine"
