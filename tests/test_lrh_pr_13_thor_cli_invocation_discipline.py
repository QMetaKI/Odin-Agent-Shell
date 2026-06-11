"""Tests for LRH-PR-13: Thor CLI Invocation Discipline.

These tests do NOT require Thor to be installed.
They validate the invocation discipline document and probe script structure.

Claim boundary: test_lrh_pr_13_thor_discipline_doc_only_no_runtime_proof
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Thor CLI invocation discipline document
# ---------------------------------------------------------------------------


def test_thor_discipline_doc_exists():
    assert (ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md").exists()


def test_thor_discipline_doc_has_advisory_boundary():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "thor is advisory" in text, "Must state 'Thor is advisory'"


def test_thor_discipline_doc_has_odin_validators_authority():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "odin" in text and "validator" in text


def test_thor_discipline_doc_has_claim_boundary():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "claim_boundary" in text or "claim boundary" in text


def test_thor_discipline_doc_has_classification_table():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "not_found_in_path" in text
    assert "entrypoint_missing_after_install" in text
    assert "clone_unavailable" in text
    assert "network_unavailable" in text


def test_thor_discipline_doc_has_preferred_invocation_order():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "preferred invocation order" in text or "invocation order" in text


def test_thor_discipline_doc_has_diagnostic_commands():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore")
    assert "command -v thor" in text


def test_thor_discipline_doc_has_path_check():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore")
    assert "PATH" in text


def test_thor_discipline_doc_has_python_module_check():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore")
    assert "importlib" in text or "find_spec" in text


def test_thor_discipline_doc_has_tmp_thor_agent_kit_section():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore")
    assert "/tmp/thor-agent-kit" in text


def test_thor_discipline_doc_has_fresh_clone_section():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "fresh clone" in text or "git clone" in text


def test_thor_discipline_doc_has_working_directory_section():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "working directory" in text


def test_thor_discipline_doc_has_blocking_vs_nonblocking():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "blocking" in text and "non-blocking" in text


def test_thor_discipline_doc_has_summary_artifact_pattern():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "thor summary" in text or "summary artifact" in text


def test_thor_discipline_doc_has_cite_in_return_reports_section():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "return report" in text or "cite thor" in text


def test_thor_discipline_doc_has_what_not_to_claim():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "what not to claim" in text


def test_thor_discipline_doc_has_known_command_set():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "known command set" in text or "thor start" in text


def test_thor_discipline_doc_no_overclaim():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "production-ready" not in text
    assert "fully proven" not in text
    assert "complete proof" not in text


# ---------------------------------------------------------------------------
# Thor probe script structure (does not execute Thor)
# ---------------------------------------------------------------------------


def test_thor_probe_script_exists():
    assert (ROOT / "tools" / "dev" / "thor_cli_probe.py").exists()


def test_thor_probe_script_has_main():
    probe = ROOT / "tools" / "dev" / "thor_cli_probe.py"
    text = probe.read_text(encoding="utf-8", errors="ignore")
    assert "def main(" in text


def test_thor_probe_script_has_probe_function():
    probe = ROOT / "tools" / "dev" / "thor_cli_probe.py"
    text = probe.read_text(encoding="utf-8", errors="ignore")
    assert "def probe(" in text


def test_thor_probe_script_has_classification():
    probe = ROOT / "tools" / "dev" / "thor_cli_probe.py"
    text = probe.read_text(encoding="utf-8", errors="ignore")
    assert "classify_failure" in text or "classification" in text


def test_thor_probe_script_has_json_output():
    probe = ROOT / "tools" / "dev" / "thor_cli_probe.py"
    text = probe.read_text(encoding="utf-8", errors="ignore")
    assert "--json" in text
    assert "json.dumps" in text


def test_thor_probe_script_has_attempt_install_flag():
    probe = ROOT / "tools" / "dev" / "thor_cli_probe.py"
    text = probe.read_text(encoding="utf-8", errors="ignore")
    assert "--attempt-install" in text


def test_thor_probe_script_claim_boundary():
    probe = ROOT / "tools" / "dev" / "thor_cli_probe.py"
    text = probe.read_text(encoding="utf-8", errors="ignore")
    assert "claim_boundary" in text


def test_thor_probe_script_advisory_note():
    probe = ROOT / "tools" / "dev" / "thor_cli_probe.py"
    text = probe.read_text(encoding="utf-8", errors="ignore").lower()
    assert "advisory" in text


def test_thor_probe_script_read_only_by_default():
    probe = ROOT / "tools" / "dev" / "thor_cli_probe.py"
    text = probe.read_text(encoding="utf-8", errors="ignore")
    assert "read-only" in text.lower() or "Read-only" in text or "read_only" in text.lower()


def test_thor_probe_script_no_network_by_default():
    probe = ROOT / "tools" / "dev" / "thor_cli_probe.py"
    text = probe.read_text(encoding="utf-8", errors="ignore").lower()
    assert "network" in text
    assert "attempt-install" in text or "attempt_install" in text


def test_thor_probe_script_can_be_imported():
    """Verify probe imports without executing main."""
    probe_path = ROOT / "tools" / "dev" / "thor_cli_probe.py"
    import importlib.util
    spec = importlib.util.spec_from_file_location("thor_cli_probe", probe_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "probe")
    assert hasattr(mod, "classify_failure")
    assert hasattr(mod, "main")
