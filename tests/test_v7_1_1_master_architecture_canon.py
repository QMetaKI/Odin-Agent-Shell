import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "docs" / "MASTER_ARCHITECTURE_V7_1_1.md"
SYNTH = ROOT / "docs" / "V7_1_1_OPERATIONAL_TARGET_SYNTHESIS.md"
TARGET_REG = ROOT / "registries" / "v7_1_1_operational_target_registry.json"
SLICE_MAP = ROOT / "registries" / "v7_1_1_slice_absorption_map.json"
REPORT = ROOT / "docs" / "codex" / "reports" / "V7_1_1_MASTER_ARCHITECTURE_CANON_RETURN_REPORT.md"
SYSTEM_MAP = ROOT / "SYSTEM_MAP.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict:
    return json.loads(_read(path))


def test_v7_1_1_files_exist_and_json_is_valid():
    assert ARCH.exists()
    assert SYNTH.exists()
    assert TARGET_REG.exists()
    assert SLICE_MAP.exists()
    assert REPORT.exists()
    assert isinstance(_json(TARGET_REG), dict)
    assert isinstance(_json(SLICE_MAP), dict)


def test_master_architecture_required_identity_and_boundary_phrases():
    text = _read(ARCH)
    assert "v7.1 remains baseline" in text
    assert "Odin is not a direct app" in text
    assert "QIRC is important but not Odin’s whole identity" in text or "QIRC is not the whole identity of Odin" in text
    assert "Small-Model Performance OS" in text
    for token in ["3B", "7B/8B", "3B+7B/8B", "Universal Work", "Candidate Artifact"]:
        assert token in text
    for token in ["Candidate DNA", "ModelWorkPacket", "Slot Forge", "Gaptext"]:
        assert token in text
    for token in ["Critic Cascade", "Candidate Tournament", "Thor"]:
        assert token in text


def test_master_architecture_contains_non_claims():
    text = _read(ARCH)
    for phrase in [
        "not runtime completion",
        "not production readiness",
        "not release certification",
        "not security certification",
        "not target-host proof",
        "not QIRC server implementation proof",
        "not live model inference proof",
        "not model quality proof",
    ]:
        assert phrase in text


def test_slice_absorption_map_traceability_counts_and_ladder():
    data = _json(SLICE_MAP)
    assert "micro-task" in data["rule"]
    assert "legacy bundle" in data["rule"]
    assert data["actual_execution_ladder"] == "REAL-GH-PR-01..08"
    assert data["micro_task_count"] == len(_json(ROOT / "registries" / "codex_task_registry.json")["tasks"])
    assert data["legacy_bundle_count"] == len(_json(ROOT / "registries" / "codex_pr_bundle_registry.json")["bundles"])
    assert data["actual_execution_pr_count"] == len(_json(ROOT / "registries" / "real_pr_execution_registry.json")["execution_prs"])
    group_ids = {group["id"] for group in data["groups"]}
    for expected in [
        "canon_and_boundary",
        "universal_work_and_candidate_core",
        "qirc_semantic_bus_and_replay",
        "small_model_power_and_hybrid_director",
        "thor_agent_handoff_and_bounded_code",
    ]:
        assert expected in group_ids


def test_operational_target_registry_required_areas_and_boundary():
    data = _json(TARGET_REG)
    assert data["status"] == "target_canon_not_runtime_completion"
    assert data["primary_identity"] == "small_model_performance_os_and_universal_semantic_work_kernel"
    area_ids = {area["id"] for area in data["target_areas"]}
    for expected in [
        "V711-SMALL-MODEL-POWER",
        "V711-QIRC",
        "V711-MODELWORKPACKET",
        "V711-THOR-HANDOFF",
    ]:
        assert expected in area_ids
    small_model = next(area for area in data["target_areas"] if area["id"] == "V711-SMALL-MODEL-POWER")
    assert small_model["small_model_power_relevance"] == "critical"
    qirc = next(area for area in data["target_areas"] if area["id"] == "V711-QIRC")
    assert qirc["qirc_relevance"] == "core_support"
    registry_text = json.dumps(data)
    assert "target_canon_not_runtime_completion" in registry_text
    assert "no live model inference proof" in registry_text


def test_system_map_contains_v7_1_1_entries():
    data = _json(SYSTEM_MAP)
    for key in [
        "master_architecture_v7_1_1",
        "v7_1_1_operational_target_synthesis",
        "v7_1_1_operational_target_registry",
        "v7_1_1_slice_absorption_map",
        "v7_1_1_master_architecture_return_report",
    ]:
        assert key in data
        assert (ROOT / data[key]).exists()
