"""Tests for LRH-PR-06 LRH Ladder Compiler v1 Hardened.

All tests are deterministic — no network, no browser, no model inference.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


# -----------------------------------------------------------------------
# Module-level imports
# -----------------------------------------------------------------------

def test_lrh_ladder_compiler_importable():
    from odin.agent_operator import lrh_ladder_compiler  # noqa: F401


def test_lrh_ladder_compiler_functions_exist():
    from odin.agent_operator.lrh_ladder_compiler import (
        load_lrh_ladder,
        find_lrh_pr,
        compile_lrh_pr_to_agent_task,
        compile_lrh_pr_to_allowed_files,
        compile_lrh_pr_to_forbidden_scope,
        compile_lrh_pr_to_required_commands,
        compile_lrh_pr_to_acceptance_gates,
        compile_lrh_pr_to_proof_boundaries,
        compile_lrh_pr_to_agent_work_packet,
    )


# -----------------------------------------------------------------------
# load_lrh_ladder
# -----------------------------------------------------------------------

def test_load_lrh_ladder_returns_dict():
    from odin.agent_operator.lrh_ladder_compiler import load_lrh_ladder
    data, missing = load_lrh_ladder()
    assert isinstance(data, dict), "load_lrh_ladder must return a dict"
    assert isinstance(missing, list), "missing keys must be a list"


# -----------------------------------------------------------------------
# find_lrh_pr
# -----------------------------------------------------------------------

def test_find_lrh_pr_06_by_short_id():
    from odin.agent_operator.lrh_ladder_compiler import find_lrh_pr
    entry, missing = find_lrh_pr("06")
    assert entry is not None, f"LRH-PR-06 not found; missing: {missing}"
    assert entry.get("id") == "LRH-PR-06"


def test_find_lrh_pr_06_by_canonical_id():
    from odin.agent_operator.lrh_ladder_compiler import find_lrh_pr
    entry, missing = find_lrh_pr("LRH-PR-06")
    assert entry is not None, f"LRH-PR-06 not found; missing: {missing}"


def test_find_lrh_pr_06_by_int_string():
    from odin.agent_operator.lrh_ladder_compiler import find_lrh_pr
    entry, missing = find_lrh_pr("6")
    assert entry is not None, f"LRH-PR-06 not found; missing: {missing}"


def test_find_lrh_pr_missing_returns_none():
    from odin.agent_operator.lrh_ladder_compiler import find_lrh_pr
    entry, missing = find_lrh_pr("99")
    assert entry is None
    assert any("not_found" in m or "missing" in m for m in missing)


# -----------------------------------------------------------------------
# compile_lrh_pr_to_agent_task
# -----------------------------------------------------------------------

def test_compile_lrh_pr_to_agent_task_06():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_agent_task
    objective, missing = compile_lrh_pr_to_agent_task("06")
    assert isinstance(objective, str)
    assert len(objective) > 10, "objective must be non-trivial"
    assert "Browser" in objective or "browser" in objective or "Hub" in objective or "hub" in objective, \
        f"objective should reference Browser Hub Shell; got: {objective!r}"


# -----------------------------------------------------------------------
# compile_lrh_pr_to_allowed_files
# -----------------------------------------------------------------------

def test_compile_lrh_pr_to_allowed_files_06_includes_hub():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_allowed_files
    files, missing = compile_lrh_pr_to_allowed_files("06")
    assert isinstance(files, list)
    assert any("odin/hub" in f for f in files), \
        f"allowed_files must include odin/hub/; got: {files}"


def test_compile_lrh_pr_to_allowed_files_06_includes_static():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_allowed_files
    files, _ = compile_lrh_pr_to_allowed_files("06")
    assert any("static" in f or "odin/hub/" in f for f in files), \
        f"allowed_files must include hub static path; got: {files}"


def test_compile_lrh_pr_to_allowed_files_06_includes_api_client():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_allowed_files
    files, _ = compile_lrh_pr_to_allowed_files("06")
    assert any("api_client" in f for f in files), \
        f"allowed_files must include api_client.js; got: {files}"


def test_compile_lrh_pr_to_allowed_files_06_includes_doc():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_allowed_files
    files, _ = compile_lrh_pr_to_allowed_files("06")
    assert any("BROWSER_ODIN_HUB_SHELL" in f or "docs/" in f for f in files), \
        f"allowed_files must include docs; got: {files}"


def test_compile_lrh_pr_to_allowed_files_06_includes_test():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_allowed_files
    files, _ = compile_lrh_pr_to_allowed_files("06")
    assert any("test" in f for f in files), \
        f"allowed_files must include test file; got: {files}"


# -----------------------------------------------------------------------
# compile_lrh_pr_to_forbidden_scope
# -----------------------------------------------------------------------

def test_compile_lrh_pr_to_forbidden_scope_06():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_forbidden_scope
    scope, missing = compile_lrh_pr_to_forbidden_scope("06")
    assert isinstance(scope, list)


# -----------------------------------------------------------------------
# compile_lrh_pr_to_proof_boundaries
# -----------------------------------------------------------------------

def test_compile_lrh_pr_to_proof_boundaries_06():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_proof_boundaries
    bounds, missing = compile_lrh_pr_to_proof_boundaries("06")
    assert isinstance(bounds, list)
    assert len(bounds) > 0


# -----------------------------------------------------------------------
# compile_lrh_pr_to_agent_work_packet
# -----------------------------------------------------------------------

def test_compile_lrh_pr_to_agent_work_packet_valid():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_agent_work_packet
    from odin.agent_operator.packets import validate_agent_work_packet
    packet = compile_lrh_pr_to_agent_work_packet("06", "claude-code")
    result = validate_agent_work_packet(packet)
    assert result["status"] == "ok", f"packet validation failed: {result['errors']}"


def test_compile_lrh_pr_to_agent_work_packet_06_agent_profile_id():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_agent_work_packet
    packet = compile_lrh_pr_to_agent_work_packet("06", "claude-code")
    assert packet["agent_profile_id"] == "claude-code"


def test_compile_lrh_pr_to_agent_work_packet_06_objective():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_agent_work_packet
    packet = compile_lrh_pr_to_agent_work_packet("06", "claude-code")
    obj = packet.get("objective", "")
    assert "Browser" in obj or "browser" in obj or "Hub" in obj or "hub" in obj, \
        f"packet objective should reference Browser Hub Shell; got: {obj!r}"


def test_compile_lrh_pr_to_agent_work_packet_06_allowed_files_hub():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_agent_work_packet
    packet = compile_lrh_pr_to_agent_work_packet("06", "claude-code")
    files = packet.get("allowed_files", [])
    assert any("odin/hub" in f for f in files), f"allowed_files: {files}"


def test_compile_lrh_pr_to_agent_work_packet_06_forbidden_app_state_apply():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_agent_work_packet
    packet = compile_lrh_pr_to_agent_work_packet("06", "claude-code")
    assert "app_state_apply" in packet.get("forbidden_actions", [])


def test_compile_lrh_pr_to_agent_work_packet_06_forbidden_external_send():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_agent_work_packet
    packet = compile_lrh_pr_to_agent_work_packet("06", "claude-code")
    assert "external_send" in packet.get("forbidden_actions", [])


def test_compile_lrh_pr_to_agent_work_packet_06_proof_boundaries():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_agent_work_packet
    packet = compile_lrh_pr_to_agent_work_packet("06", "claude-code")
    bounds = packet.get("proof_boundaries", [])
    # The ladder uses human-readable strings like "no public network API proof"
    assert any("public" in b.lower() and "network" in b.lower() for b in bounds), \
        f"missing no_public_network_api_proof boundary; got: {bounds}"
    assert any("app" in b.lower() and ("state" in b.lower() or "mutation" in b.lower()) for b in bounds), \
        f"missing no_app_state_mutation_proof boundary; got: {bounds}"


def test_compile_lrh_pr_to_agent_work_packet_06_candidate_only():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_agent_work_packet
    packet = compile_lrh_pr_to_agent_work_packet("06", "claude-code")
    assert packet.get("candidate_only") is True
    assert packet.get("app_owned_apply") is True
    assert packet.get("external_send_default") is False
    assert packet.get("hidden_tool_execution_allowed") is False


def test_compile_lrh_pr_to_agent_work_packet_06_compiler_metadata():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_agent_work_packet
    packet = compile_lrh_pr_to_agent_work_packet("06", "claude-code")
    meta = packet.get("compiler_metadata", {})
    assert "missing_optional_keys" in meta, "compiler_metadata must include missing_optional_keys"
    assert "source" in meta


# -----------------------------------------------------------------------
# Missing optional keys are recorded, not raised
# -----------------------------------------------------------------------

def test_compiler_handles_missing_optional_keys_gracefully():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_agent_work_packet
    # PR 99 doesn't exist — should not raise, should record missing keys
    packet = compile_lrh_pr_to_agent_work_packet("99", "claude-code")
    assert isinstance(packet, dict)
    meta = packet.get("compiler_metadata", {})
    assert len(meta.get("missing_optional_keys", [])) > 0


def test_compiler_records_missing_optional_keys_in_metadata():
    from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_agent_work_packet
    packet = compile_lrh_pr_to_agent_work_packet("06", "claude-code")
    meta = packet.get("compiler_metadata", {})
    # missing_optional_keys should always be present, even if empty
    assert "missing_optional_keys" in meta


# -----------------------------------------------------------------------
# CLI integration: agent-handoff --lrh-pr 06 --out writes valid packet
# -----------------------------------------------------------------------

def test_cli_agent_handoff_lrh_pr_06_writes_valid_packet():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        out_path = f.name
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "06", "--out", out_path],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 0, f"agent-handoff failed: {result.stderr}"
    packet = json.loads(Path(out_path).read_text(encoding="utf-8"))
    assert packet["artifact_kind"] == "odin_agent_work_packet"
    assert packet["agent_profile_id"] == "claude-code"
    assert packet.get("candidate_only") is True


def test_cli_agent_handoff_lrh_pr_06_objective_contains_browser():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        out_path = f.name
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "06", "--out", out_path],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 0
    packet = json.loads(Path(out_path).read_text(encoding="utf-8"))
    obj = packet.get("objective", "")
    assert "browser" in obj.lower() or "hub" in obj.lower() or "shell" in obj.lower(), \
        f"objective should reference browser/hub/shell; got: {obj!r}"


def test_cli_agent_guard_passes_on_compiled_packet():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        out_path = f.name
    subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "06", "--out", out_path],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-guard", "--packet", out_path],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 0, f"agent-guard failed: {result.stdout}\n{result.stderr}"


def test_cli_agent_check_passes_on_compiled_packet():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        out_path = f.name
    subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "06", "--out", out_path],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-check", "--packet", out_path],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 0, f"agent-check failed: {result.stdout}\n{result.stderr}"


def test_cli_agent_proof_passes_on_compiled_packet():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        out_path = f.name
    subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "06", "--out", out_path],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-proof", "--packet", out_path],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 0, f"agent-proof failed: {result.stdout}\n{result.stderr}"


# -----------------------------------------------------------------------
# Fallback markdown parsing
# -----------------------------------------------------------------------

def test_compiler_fallback_parsing_from_markdown():
    from odin.agent_operator.lrh_ladder_compiler import _parse_ladder_markdown
    md_path = ROOT / "docs" / "rebaseline" / "LOCAL_RUNTIME_HUB_BUILD_LADDER_V1.md"
    if not md_path.exists():
        pytest.skip("Markdown fallback path not present")
    data = _parse_ladder_markdown(md_path)
    assert isinstance(data, dict)
    # Markdown fallback may find 0 or more entries — it should not raise
