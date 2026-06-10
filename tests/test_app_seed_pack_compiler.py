from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_app_seed_pack_docs_and_registries_exist():
    for rel in [
        "docs/APP_SEED_PACK_COMPILER_V7_1.md",
        "docs/UNIVERSAL_SEED_PACK_FORMAT_V7_1.md",
        "docs/OPERATIONAL_SEED_FUNCTIONS_V7_1.md",
        "docs/SEED_PACK_SECURITY_BOUNDARY_V7_1.md",
        "docs/SEED_PACK_TO_RUNTIME_PACK_COMPILER_V7_1.md",
        "docs/SEED_PACK_CAPABILITY_SLICES_V7_1.md",
        "docs/SEED_PACK_COMPOSITION_AND_CONFLICTS_V7_1.md",
        "docs/SEED_PACK_USE_CASE_MATRIX_V7_1.md",
        "docs/SEED_PACK_WHY_TRACE_AND_EXPLAINABILITY_V7_1.md",
    ]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "No arbitrary seed-pack code execution" in text
        assert "Runtime Pack" in text
    for rel in [
        "registries/app_seed_pack_type_registry.json",
        "registries/operational_seed_function_registry.json",
        "registries/seed_pack_compiler_stage_registry.json",
        "registries/seed_pack_security_boundary_registry.json",
        "registries/seed_pack_capability_profile_registry.json",
    ]:
        data = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        assert data["registry_id"]
        assert data["version"] == "7.1"


def test_app_seed_pack_compiler_shadow_blocks_execution():
    from odin.shadow_runtime.app_seed_pack_compiler_shadow import compile_app_seed_pack_shadow
    blocked = compile_app_seed_pack_shadow({"artifact_kind": "seed_pack", "forbidden_actions": ["execute_code"]})
    assert blocked["status"] == "blocked"
    ok = compile_app_seed_pack_shadow({"artifact_kind": "seed_pack"})
    assert ok["candidate_only"] is True
    assert ok["no_app_mutation"] is True


def test_seed_pack_ladder_and_bundle_present():
    tasks = json.loads((ROOT / "registries/codex_task_registry.json").read_text(encoding="utf-8"))["tasks"]
    task_ids = {t["id"] for t in tasks}
    for tid in ["PR-87", "PR-88", "PR-89", "PR-90", "PR-91", "PR-92"]:
        assert tid in task_ids
    bundles = json.loads((ROOT / "registries/codex_pr_bundle_registry.json").read_text(encoding="utf-8"))["bundles"]
    bundle = next(b for b in bundles if b["id"] == "REAL-PR-22")
    assert bundle["internal_tasks"] == ["PR-87", "PR-88", "PR-89", "PR-90", "PR-91", "PR-92"]
