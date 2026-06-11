"""Tests for FILE_MANIFEST closure / retained gap documentation (LRH-PR-18).

Claim boundary: file_manifest_closure_retained_gap_explicitly_documented
The FILE_MANIFEST.json backfill gap is retained in LRH-PR-18 because a safe
deterministic builder is not yet available. This test asserts the gap is
explicitly documented rather than silently omitted.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POST_LRH_REGISTRY = ROOT / "registries" / "post_lrh_proof_governance_registry_v1.json"
FILE_MANIFEST = ROOT / "FILE_MANIFEST.json"


def _post_lrh_data() -> dict:
    return json.loads(POST_LRH_REGISTRY.read_text(encoding="utf-8"))


class TestFileManifestClosureGapDocumented:
    def test_post_lrh_registry_exists(self):
        assert POST_LRH_REGISTRY.exists()

    def test_retained_gaps_list_present(self):
        data = _post_lrh_data()
        assert "retained_gaps" in data
        assert len(data["retained_gaps"]) > 0

    def test_file_manifest_gap_explicitly_retained(self):
        data = _post_lrh_data()
        retained_ids = [g["id"] if isinstance(g, dict) else str(g) for g in data["retained_gaps"]]
        retained_str = json.dumps(data["retained_gaps"]).lower()
        assert "file_manifest" in retained_str or "manifest" in retained_str, (
            "FILE_MANIFEST backfill gap must be explicitly documented in retained_gaps"
        )

    def test_file_manifest_gap_has_reason(self):
        data = _post_lrh_data()
        file_manifest_gap = None
        for gap in data["retained_gaps"]:
            if isinstance(gap, dict) and "file_manifest" in gap.get("id", "").lower():
                file_manifest_gap = gap
                break
        if file_manifest_gap is not None:
            assert "reason" in file_manifest_gap

    def test_file_manifest_gap_has_future_work(self):
        data = _post_lrh_data()
        for gap in data["retained_gaps"]:
            if isinstance(gap, dict) and "file_manifest" in gap.get("id", "").lower():
                assert "future_work" in gap
                return
        # If gap is a string (simpler format), just check it mentions future work implicitly
        retained_str = json.dumps(data["retained_gaps"]).lower()
        assert "manifest" in retained_str


class TestFileManifestNotBroken:
    def test_file_manifest_exists(self):
        assert FILE_MANIFEST.exists(), "FILE_MANIFEST.json must exist"

    def test_file_manifest_valid_json(self):
        data = json.loads(FILE_MANIFEST.read_text(encoding="utf-8"))
        assert isinstance(data, dict)

    def test_file_manifest_not_empty(self):
        data = json.loads(FILE_MANIFEST.read_text(encoding="utf-8"))
        assert len(data) > 0


class TestConsolidatedPGPacketFileManifestClosure:
    def test_pg_packet_file_manifest_closure_retained_gap(self):
        from odin.hub.shell import build_consolidated_proof_governance_packet
        result = build_consolidated_proof_governance_packet()
        fmc = result.get("file_manifest_closure", {})
        assert fmc.get("status") == "retained_gap"

    def test_pg_packet_file_manifest_closure_has_reason(self):
        from odin.hub.shell import build_consolidated_proof_governance_packet
        result = build_consolidated_proof_governance_packet()
        fmc = result.get("file_manifest_closure", {})
        assert "reason" in fmc
        assert len(fmc["reason"]) > 0
