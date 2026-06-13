"""Tests for FINAL-PR-08 Projection Candidate Spine."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CLAIM_BOUNDARY = "projection_candidate_spine_prepares_candidates_not_runtime_execution"
REQUIRED_MATERIALIZATION_LEVELS = [
    "M0_raw_input", "M1_handoff_context", "M2_universal_work", "M3_seed_route",
    "M4_field_selection", "M5_projection_set", "M6_candidate_artifact",
    "M7_response_packet", "M8_trace_receipt", "M9_release_evidence",
]


# ── 1. Import ──────────────────────────────────────────────────────────────────

def test_module_importable():
    import odin.projection_candidate_spine  # noqa: F401


# ── 2-3. Materialization levels ────────────────────────────────────────────────

def test_all_10_materialization_levels_defined():
    from odin.projection_candidate_spine.materialization import MATERIALIZATION_LEVELS
    assert len(MATERIALIZATION_LEVELS) == 10
    for level in REQUIRED_MATERIALIZATION_LEVELS:
        assert level in MATERIALIZATION_LEVELS


def test_materialization_levels_ordered():
    from odin.projection_candidate_spine.materialization import MATERIALIZATION_LEVELS
    assert MATERIALIZATION_LEVELS == REQUIRED_MATERIALIZATION_LEVELS


# ── 4-6. CandidateNode ─────────────────────────────────────────────────────────

def test_candidate_node_can_be_constructed():
    from odin.projection_candidate_spine.candidate_graph import CandidateNode
    node = CandidateNode(
        node_id="candidate_node_test001",
        label="test_node",
        materialization_level="M6_candidate_artifact",
        content_summary="Test candidate node",
        proof_boundary=CLAIM_BOUNDARY,
    )
    assert node.node_id == "candidate_node_test001"


def test_candidate_node_candidate_only_true():
    from odin.projection_candidate_spine.candidate_graph import CandidateNode
    node = CandidateNode(
        node_id="candidate_node_test002",
        label="test_node",
        materialization_level="M5_projection_set",
        content_summary="Test node",
        proof_boundary=CLAIM_BOUNDARY,
    )
    assert node.candidate_only is True


def test_candidate_node_materialization_level_validation():
    from odin.projection_candidate_spine.candidate_graph import CandidateNode
    with pytest.raises(ValueError):
        CandidateNode(
            node_id="bad_node",
            label="bad",
            materialization_level="M99_invalid",
            content_summary="Bad node",
            proof_boundary=CLAIM_BOUNDARY,
        )


# ── 7-9. ProjectionSet ─────────────────────────────────────────────────────────

def test_projection_set_can_be_constructed():
    from odin.projection_candidate_spine.candidate_graph import CandidateNode
    from odin.projection_candidate_spine.projection_set import build_projection_set
    node = CandidateNode(
        node_id="candidate_node_ps_test",
        label="ps_test",
        materialization_level="M6_candidate_artifact",
        content_summary="PS test node",
        proof_boundary=CLAIM_BOUNDARY,
    )
    ps = build_projection_set({"work_type": "repo"}, [node])
    assert ps.projection_id.startswith("projection_set_")
    assert len(ps.candidate_nodes) == 1


def test_projection_set_candidate_only_true():
    from odin.projection_candidate_spine.candidate_graph import CandidateNode
    from odin.projection_candidate_spine.projection_set import build_projection_set
    node = CandidateNode(
        node_id="candidate_node_co_test",
        label="co_test",
        materialization_level="M6_candidate_artifact",
        content_summary="Candidate only test",
        proof_boundary=CLAIM_BOUNDARY,
    )
    ps = build_projection_set({}, [node])
    assert ps.candidate_only is True


def test_projection_set_claim_boundary_correct():
    from odin.projection_candidate_spine.candidate_graph import CandidateNode
    from odin.projection_candidate_spine.projection_set import build_projection_set
    node = CandidateNode(
        node_id="candidate_node_cb_test",
        label="cb_test",
        materialization_level="M6_candidate_artifact",
        content_summary="Claim boundary test",
        proof_boundary=CLAIM_BOUNDARY,
    )
    ps = build_projection_set({}, [node])
    assert ps.claim_boundary == CLAIM_BOUNDARY


def test_projection_id_differs_for_different_candidate_nodes():
    from odin.projection_candidate_spine.candidate_graph import CandidateNode
    from odin.projection_candidate_spine.projection_set import build_projection_set
    ctx = {"work_type": "repo", "field_selection_available": True}
    node_a = CandidateNode("candidate_node_pida1", "a", "M6_candidate_artifact", "Node A", CLAIM_BOUNDARY)
    node_b = CandidateNode("candidate_node_pidb1", "b", "M6_candidate_artifact", "Node B", CLAIM_BOUNDARY)
    ps_a = build_projection_set(ctx, [node_a])
    ps_b = build_projection_set(ctx, [node_b])
    assert ps_a.projection_id != ps_b.projection_id, (
        "Same source_context with different candidate_nodes must produce different projection_id"
    )


# ── 10-12. CandidateGraph ──────────────────────────────────────────────────────

def test_candidate_graph_has_nodes_and_explicit_edges():
    from odin.projection_candidate_spine.candidate_graph import CandidateNode, build_candidate_graph
    node_a = CandidateNode("candidate_node_ga1", "a", "M4_field_selection", "Node A", CLAIM_BOUNDARY)
    node_b = CandidateNode("candidate_node_gb1", "b", "M6_candidate_artifact", "Node B", CLAIM_BOUNDARY)
    graph = build_candidate_graph([node_a, node_b])
    assert len(graph.nodes) == 2
    assert len(graph.edges) == 1
    assert graph.edges[0]["from_node_id"] == node_a.node_id
    assert graph.edges[0]["to_node_id"] == node_b.node_id
    assert graph.edges[0]["relation"] == "derived_from"


def test_candidate_graph_id_deterministic():
    from odin.projection_candidate_spine.candidate_graph import CandidateNode, build_candidate_graph
    node_a = CandidateNode("candidate_node_det1", "a", "M4_field_selection", "Node A", CLAIM_BOUNDARY)
    node_b = CandidateNode("candidate_node_det2", "b", "M6_candidate_artifact", "Node B", CLAIM_BOUNDARY)
    g1 = build_candidate_graph([node_a, node_b])
    g2 = build_candidate_graph([node_a, node_b])
    assert g1.graph_id == g2.graph_id


def test_candidate_graph_id_differs_for_different_explicit_edges():
    from odin.projection_candidate_spine.candidate_graph import CandidateNode, build_candidate_graph
    node_a = CandidateNode("candidate_node_ede1", "a", "M4_field_selection", "Node A", CLAIM_BOUNDARY)
    node_b = CandidateNode("candidate_node_ede2", "b", "M6_candidate_artifact", "Node B", CLAIM_BOUNDARY)
    edges_ab = [{"from_node_id": node_a.node_id, "to_node_id": node_b.node_id, "relation": "derived_from"}]
    edges_ba = [{"from_node_id": node_b.node_id, "to_node_id": node_a.node_id, "relation": "derived_from"}]
    g_ab = build_candidate_graph([node_a, node_b], edges=edges_ab)
    g_ba = build_candidate_graph([node_a, node_b], edges=edges_ba)
    assert g_ab.graph_id != g_ba.graph_id, "Different explicit edges must produce different graph_id"


def test_candidate_graph_is_not_execution_graph():
    from odin.projection_candidate_spine.candidate_graph import CandidateGraph, CandidateNode
    node = CandidateNode("candidate_node_exe1", "a", "M6_candidate_artifact", "Node A", CLAIM_BOUNDARY)
    graph = CandidateGraph(
        graph_id="candidate_graph_test",
        nodes=[node],
        edges=[],
        entry_node_id=node.node_id,
    )
    assert graph.candidate_only is True
    assert graph.claim_boundary == CLAIM_BOUNDARY


# ── 13-15. ExpressionPacket ────────────────────────────────────────────────────

def test_expression_packet_near_code_is_string_or_none():
    from odin.projection_candidate_spine.candidate_graph import CandidateNode
    from odin.projection_candidate_spine.expression_packet import build_expression_packet
    node = CandidateNode("candidate_node_ep1", "ep_test", "M6_candidate_artifact", "EP node", CLAIM_BOUNDARY)
    ep = build_expression_packet(node, near_code="def foo(): pass")
    assert isinstance(ep.near_code, (str, type(None)))
    ep2 = build_expression_packet(node, near_code=None)
    assert ep2.near_code is None


def test_expression_packet_near_code_not_executed():
    from odin.projection_candidate_spine.candidate_graph import CandidateNode
    from odin.projection_candidate_spine.expression_packet import build_expression_packet
    node = CandidateNode("candidate_node_ep2", "ep_test2", "M6_candidate_artifact", "EP node2", CLAIM_BOUNDARY)
    ep = build_expression_packet(node, near_code="def foo(): pass")
    assert ep.near_code_execution is False


def test_expression_packet_candidate_only_true():
    from odin.projection_candidate_spine.candidate_graph import CandidateNode
    from odin.projection_candidate_spine.expression_packet import build_expression_packet
    node = CandidateNode("candidate_node_ep3", "ep_test3", "M6_candidate_artifact", "EP node3", CLAIM_BOUNDARY)
    ep = build_expression_packet(node)
    assert ep.candidate_only is True


# ── 16-17. CandidateComparison ─────────────────────────────────────────────────

def test_candidate_comparison_has_not_proven_list():
    from odin.projection_candidate_spine.candidate_graph import CandidateNode
    from odin.projection_candidate_spine.compare import compare_candidate_nodes
    node_a = CandidateNode("candidate_node_cmp_a", "a", "M4_field_selection", "Node A", CLAIM_BOUNDARY)
    node_b = CandidateNode("candidate_node_cmp_b", "b", "M6_candidate_artifact", "Node B", CLAIM_BOUNDARY)
    comp = compare_candidate_nodes(node_a, node_b)
    assert isinstance(comp.not_proven, list)
    assert "generated_code_correctness_unless_tested" in comp.not_proven


def test_candidate_comparison_winner_id_is_recommendation_only():
    from odin.projection_candidate_spine.candidate_graph import CandidateNode
    from odin.projection_candidate_spine.compare import compare_candidate_nodes
    node_a = CandidateNode("candidate_node_win_a", "a", "M4_field_selection", "Short", CLAIM_BOUNDARY)
    node_b = CandidateNode("candidate_node_win_b", "b", "M6_candidate_artifact", "Also short", CLAIM_BOUNDARY)
    comp = compare_candidate_nodes(node_a, node_b)
    assert comp.winner_id is None or comp.winner_id in (node_a.node_id, node_b.node_id)
    assert comp.candidate_only is True


# ── 18-19. ReceiptLink ────────────────────────────────────────────────────────

def test_receipt_link_has_bound_at_utc():
    from odin.projection_candidate_spine.receipt_link import build_receipt_link
    rl = build_receipt_link("candidate_node_rl1", "trace_ref_001")
    assert rl.bound_at_utc == "2026-01-01T00:00:00Z"


def test_receipt_link_id_deterministic():
    from odin.projection_candidate_spine.receipt_link import build_receipt_link
    rl1 = build_receipt_link("candidate_node_rl2", "trace_ref_002")
    rl2 = build_receipt_link("candidate_node_rl2", "trace_ref_002")
    assert rl1.link_id == rl2.link_id
    assert rl1.link_id.startswith("receipt_link_")


# ── 20-22. Proof packet ────────────────────────────────────────────────────────

def test_proof_packet_includes_hidden_runtime():
    from odin.projection_candidate_spine.proof import build_proof_packet
    packet = build_proof_packet()
    assert "hidden_runtime" in packet["not_proven"]


def test_proof_packet_includes_model_inference():
    from odin.projection_candidate_spine.proof import build_proof_packet
    packet = build_proof_packet()
    assert "model_inference" in packet["not_proven"]


def test_proof_packet_includes_generated_code_correctness():
    from odin.projection_candidate_spine.proof import build_proof_packet
    packet = build_proof_packet()
    assert "generated_code_correctness" in packet["not_proven"]


# ── 23. PR07 integration ───────────────────────────────────────────────────────

def test_pr07_integration_field_selection_to_projection_set():
    from odin.field_selection_spine.selector import select_field_route
    from odin.projection_candidate_spine.projection_set import build_projection_set_from_field_selection
    fs = select_field_route({"work_type": "repo", "repo_evidence": "SYSTEM_MAP.json"})
    ps = build_projection_set_from_field_selection(fs)
    assert ps.candidate_only is True
    assert ps.claim_boundary == CLAIM_BOUNDARY
    assert "field_selection_available" in ps.source_context
    assert ps.source_context.get("field_selection_available") is True


# ── 24. PR06→PR07→PR08 chain ──────────────────────────────────────────────────

def test_pr06_pr07_pr08_chain_works():
    from odin.operational_seed_spine.selector import select_seed_route
    from odin.field_selection_spine.selector import select_field_route_from_seed_route
    from odin.projection_candidate_spine.projection_set import build_projection_set_from_field_selection
    seed = select_seed_route({"trigger_shape": "repo", "work_type": "repo"})
    fs = select_field_route_from_seed_route(seed)
    ps = build_projection_set_from_field_selection(fs)
    assert ps.candidate_only is True
    assert ps.claim_boundary == CLAIM_BOUNDARY
    assert len(ps.candidate_nodes) > 0


# ── 25-27. CLI commands ────────────────────────────────────────────────────────

def test_cli_validate_projection_candidate_spine_returns_0():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-projection-candidate-spine"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, f"validate-projection-candidate-spine failed:\n{result.stdout}\n{result.stderr}"


def test_cli_explain_projection_candidate_demo_returns_valid_json():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "explain-projection-candidate", "--demo"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, f"explain-projection-candidate --demo failed:\n{result.stderr}"
    data = json.loads(result.stdout)
    assert data.get("candidate_only") is True
    assert data.get("claim_boundary") == CLAIM_BOUNDARY


def test_cli_prove_projection_candidate_spine_returns_0():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "prove-projection-candidate-spine"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, f"prove-projection-candidate-spine failed:\n{result.stderr}"


# ── 28. Local hub payload ─────────────────────────────────────────────────────

def test_local_hub_projection_candidate_payload_is_valid_json():
    from odin.local_hub.server import build_projection_candidate_payload
    payload = build_projection_candidate_payload()
    assert payload.get("status") == "ok"
    assert payload.get("candidate_only") is True
    assert payload.get("claim_boundary") == CLAIM_BOUNDARY


# ── 29-31. No forbidden content ───────────────────────────────────────────────

def test_no_forbidden_runtime_names_in_pr08_modules():
    forbidden = ["dfas", "q_shabang", "qmath", "q_state", "qgit", "qcode", "qli", "qstar"]
    module_dir = REPO_ROOT / "odin/projection_candidate_spine"
    for py_file in module_dir.glob("*.py"):
        text = py_file.read_text(encoding="utf-8").lower()
        for name in forbidden:
            assert name not in text, f"Forbidden name {name!r} found in {py_file.name}"


def test_no_uuid_random_time_datetime_in_deterministic_modules():
    bad_tokens = ["uuid.uuid4()", "random.", "time.time()", "datetime.now()"]
    module_dir = REPO_ROOT / "odin/projection_candidate_spine"
    for py_file in module_dir.glob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        for token in bad_tokens:
            assert token not in text, f"Non-deterministic token {token!r} found in {py_file.name}"


def test_no_eval_exec_subprocess_in_pr08_modules():
    bad_tokens = ["eval(", "exec(", "subprocess."]
    module_dir = REPO_ROOT / "odin/projection_candidate_spine"
    for py_file in module_dir.glob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        for token in bad_tokens:
            assert token not in text, f"Forbidden token {token!r} found in {py_file.name}"


# ── 32-33. Validator and validate-all ─────────────────────────────────────────

def test_validator_returns_ok():
    import importlib.util
    tool_path = REPO_ROOT / "tools/rebaseline/check_final_pr_08_projection_candidate_spine.py"
    spec = importlib.util.spec_from_file_location("check_pr08", tool_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "report.json"
        code = module.main(["--repo-root", str(REPO_ROOT), "--out", str(out)])
    assert code == 0, "PR08 validator returned non-zero"


def test_validate_all_includes_pr08_validator():
    cli_text = (REPO_ROOT / "odin/cli.py").read_text(encoding="utf-8")
    assert "validate_projection_candidate_spine()" in cli_text


# ── 34-35. Prep validator ─────────────────────────────────────────────────────

def test_prep_validator_still_passes():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-prep-final-pr-06-08"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, f"prep validator failed:\n{result.stdout}\n{result.stderr}"


def test_prep_validator_keeps_pr09_deferred():
    prep_text = (REPO_ROOT / "tools/rebaseline/check_prep_final_pr_06_08.py").read_text(encoding="utf-8")
    assert "final_pr_09" in prep_text or "release_closure" in prep_text.lower()


# ── 36. REQUIRED_IDS ──────────────────────────────────────────────────────────

def test_required_ids_contains_projection_candidate_spine_section():
    from odin.local_hub.ui import REQUIRED_IDS
    assert "projection-candidate-spine-section" in REQUIRED_IDS


# ── 37. FILE_MANIFEST ─────────────────────────────────────────────────────────

def test_file_manifest_contains_every_pr08_required_file():
    required = [
        "odin/projection_candidate_spine/__init__.py",
        "odin/projection_candidate_spine/materialization.py",
        "odin/projection_candidate_spine/candidate_graph.py",
        "odin/projection_candidate_spine/projection_set.py",
        "odin/projection_candidate_spine/expression_packet.py",
        "odin/projection_candidate_spine/compare.py",
        "odin/projection_candidate_spine/receipt_link.py",
        "odin/projection_candidate_spine/proof.py",
        "registries/final_pr_08_projection_candidate_spine_registry.json",
        "schemas/final_pr_08_projection_candidate_spine_proof_packet.schema.json",
        "tools/rebaseline/check_final_pr_08_projection_candidate_spine.py",
        "tests/test_final_pr_08_projection_candidate_spine.py",
    ]
    manifest_text = (REPO_ROOT / "FILE_MANIFEST.json").read_text(encoding="utf-8")
    for rel in required:
        assert rel in manifest_text, f"FILE_MANIFEST missing: {rel}"


# ── 38. Return report self-contained ─────────────────────────────────────────

def test_return_report_exists_and_self_contained():
    rr_path = REPO_ROOT / "docs/codex/reports/FINAL_PR_08_PROJECTION_CANDIDATE_SPINE_RETURN_REPORT.md"
    assert rr_path.exists(), "Return report does not exist"
    text = rr_path.read_text(encoding="utf-8")
    assert "passed" in text.lower() or "pytest" in text.lower()


# ── 39-40. PR06/07 tests still pass ──────────────────────────────────────────

def test_pr07_tests_still_pass():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q",
         "tests/test_final_pr_07_field_selection_spine.py", "-p", "no:cacheprovider"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, f"PR07 tests failed:\n{result.stdout}\n{result.stderr}"


def test_pr06_tests_still_pass():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q",
         "tests/test_final_pr_06_operational_seed_spine.py", "-p", "no:cacheprovider"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, f"PR06 tests failed:\n{result.stdout}\n{result.stderr}"
