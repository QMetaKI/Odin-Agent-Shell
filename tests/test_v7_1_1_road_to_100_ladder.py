import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "V7_1_1_ROAD_TO_100_BUILD_LADDER.md"
LADDER = ROOT / "registries" / "v7_1_1_road_to_100_ladder.json"
MATRIX = ROOT / "registries" / "v7_1_1_road_to_100_coverage_matrix.json"
REPORT = ROOT / "docs" / "codex" / "reports" / "V7_1_1_ROAD_TO_100_LADDER_RETURN_REPORT.md"
TARGET_REG = ROOT / "registries" / "v7_1_1_operational_target_registry.json"

FAMILIES = {
    "PR-25-COVERAGE-GAP-COMPILER",
    "PR-26-CANON-BOUNDARY-INTEGRITY",
    "PR-27-APP-BOUNDARY-UNIVERSAL-WORK",
    "PR-28-QIRC-SEMANTIC-BUS",
    "PR-29-CONTEXT-LENSES",
    "PR-30-WORKLETS-SLOTS-GAPTEXT",
    "PR-31-MODELWORKPACKET-SCALE-LADDER",
    "PR-32-SMALL-MODEL-HYBRID-DIRECTOR",
    "PR-33-MINICHECK-CRITICS-TOURNAMENT",
    "PR-34-CANDIDATE-FINAL-GATE",
    "PR-35-STORAGE-TRACE-RECEIPT",
    "PR-36-THOR-AGENT-HANDOFF",
    "PR-37-SDK-APP-BRIDGE",
    "PR-38-ACCEPTANCE-DOJO-SCOREBOARD",
    "PR-39-FULL-V711-OPERATIONAL-CLOSURE",
}
REQUIRED_KEYS = {
    "id", "phase_id", "title", "objective", "target_area_ids", "depends_on", "source_refs",
    "likely_future_files_or_modules", "forbidden_scope", "expected_artifacts", "required_tests",
    "required_proof_commands", "done_criteria", "claim_boundary", "non_claims",
    "recommended_future_pr_family", "evidence_required_later", "senior_reviewer_checks",
    "senior_code_reviewer_checks",
}


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_road_to_100_files_exist_and_json_valid():
    assert DOC.exists()
    assert LADDER.exists()
    assert MATRIX.exists()
    assert REPORT.exists()
    assert isinstance(_json(LADDER), dict)
    assert isinstance(_json(MATRIX), dict)


def test_ladder_top_level_counts_and_status():
    data = _json(LADDER)
    assert data["status"] == "road_to_100_target_ladder_not_runtime_completion"
    assert data["canonical_slice_count"] >= 190
    assert data["minimum_slice_count"] >= 190
    assert len(data["slices"]) >= 190
    assert data["phase_count"] == 13


def test_slice_ids_unique_and_sequential():
    slices = _json(LADDER)["slices"]
    ids = [s["id"] for s in slices]
    assert len(ids) == len(set(ids))
    assert ids == [f"V711-R100-{i:03d}" for i in range(len(ids))]


def test_phases_have_at_least_five_slices_and_dependencies_are_earlier():
    data = _json(LADDER)
    ids = [s["id"] for s in data["slices"]]
    id_index = {sid: i for i, sid in enumerate(ids)}
    for phase in data["phases"]:
        assert sum(1 for s in data["slices"] if s["phase_id"] == phase["id"]) >= 5
    for s in data["slices"]:
        for dep in s["depends_on"]:
            assert dep in id_index
            assert id_index[dep] < id_index[s["id"]]


def test_every_target_area_is_covered_by_ladder_slice():
    target_ids = {a["id"] for a in _json(TARGET_REG)["target_areas"]}
    covered = {tid for s in _json(LADDER)["slices"] for tid in s["target_area_ids"]}
    assert target_ids <= covered


def test_future_pr_families_are_present():
    data = _json(LADDER)
    assert FAMILIES <= set(data["future_pr_families"])
    used = {s["recommended_future_pr_family"] for s in data["slices"]}
    assert FAMILIES <= used


def test_every_slice_has_required_keys_and_non_empty_core_fields():
    for s in _json(LADDER)["slices"]:
        assert REQUIRED_KEYS <= set(s), s["id"]
        for key in ["objective", "forbidden_scope", "expected_artifacts", "done_criteria", "claim_boundary", "non_claims", "evidence_required_later"]:
            assert s[key], (s["id"], key)


def test_ladder_doc_required_phrases():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "Literal v7.1.1 operational completion",
        "Canon before implementation",
        "Coverage before runtime",
        "Slots before prompts",
        "ModelWorkPacket before provider execution",
        "Candidate before apply",
        "QIRC coordination before QIRC server/runtime claims",
        "PR-25 — v7.1.1 Operational Coverage / Gap Compiler",
    ]:
        assert phrase in text


def test_coverage_matrix_covers_each_target_area_once_and_is_non_proof():
    matrix = _json(MATRIX)
    target_ids = [a["id"] for a in _json(TARGET_REG)["target_areas"]]
    entries = matrix["target_area_coverage"]
    assert [e["target_area_id"] for e in entries] == target_ids
    assert len(entries) == len(target_ids)
    assert matrix["claim_boundary"] == "coverage_matrix_is_planning_not_implementation_proof"
    assert "not_runtime_proof" in matrix["status"]
    assert matrix["known_uncovered_items"] == []
    valid_slice_ids = {s["id"] for s in _json(LADDER)["slices"]}
    for entry in entries:
        assert entry["covered_by_slices"]
        assert set(entry["covered_by_slices"]) <= valid_slice_ids


def test_no_slice_contains_forbidden_placeholder_text():
    forbidden = ["TODO", "TBD", "placeholder", "later maybe", "as needed"]
    for s in _json(LADDER)["slices"]:
        payload = json.dumps(s)
        for term in forbidden:
            assert term not in payload, (s["id"], term)


def test_no_slice_contains_forbidden_positive_claims_outside_boundary_fields():
    forbidden = [
        "production" + " ready",
        "security certified",
        "live model proof",
        "QIRC server implemented",
        "target-host proof",
        "model quality proven",
        "release" + " ready",
    ]
    for s in _json(LADDER)["slices"]:
        scoped = {k: v for k, v in s.items() if k not in {"non_claims", "evidence_required_later", "forbidden_scope"}}
        payload = json.dumps(scoped).lower()
        for term in forbidden:
            assert term.lower() not in payload, (s["id"], term)
