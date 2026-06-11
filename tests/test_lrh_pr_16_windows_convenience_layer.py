"""Tests for LRH-PR-16 Windows Convenience Layer without Full Windows App.

Deterministic, local-only, no Windows host requirement, no network, no npm,
no browser automation.

Claim boundary: windows_convenience_candidate_only_not_service_not_tray_not_installer_not_signed
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# 9.1 Required file existence
# ---------------------------------------------------------------------------

def test_windows_convenience_doc_exists():
    assert (ROOT / "docs" / "WINDOWS_CONVENIENCE_LAYER_V1.md").exists()


def test_test_file_itself_exists():
    assert (ROOT / "tests" / "test_lrh_pr_16_windows_convenience_layer.py").exists()


def test_start_bat_exists():
    assert (ROOT / "scripts" / "start_odin.bat").exists()


def test_check_bat_exists():
    assert (ROOT / "scripts" / "check_odin.bat").exists()


def test_stop_bat_exists():
    assert (ROOT / "scripts" / "stop_odin.bat").exists()


def test_windows_readme_exists():
    assert (ROOT / "windows" / "README.md").exists()


def test_windows_helper_manifest_exists():
    assert (ROOT / "windows" / "helper_manifest_v1.json").exists()


def test_windows_no_service_tray_proof_doc_exists():
    assert (ROOT / "windows" / "NO_SERVICE_TRAY_INSTALLER_PROOF.md").exists()


def test_windows_manual_start_doc_exists():
    assert (ROOT / "windows" / "manual_start.md").exists()


def test_windows_shortcut_notes_exists():
    assert (ROOT / "windows" / "shortcut_notes.md").exists()


def test_windows_convenience_smoke_notes_exists():
    assert (ROOT / "windows" / "convenience_smoke_notes.md").exists()


# ---------------------------------------------------------------------------
# 9.2 Ladder tests
# ---------------------------------------------------------------------------

def _load_ladder() -> dict:
    return json.loads((ROOT / "registries" / "local_runtime_hub_build_ladder_v1.json").read_text(encoding="utf-8"))


def test_ladder_pr16_exists():
    ladder = _load_ladder()
    ids = [e["id"] for e in ladder["ladder"]]
    assert "LRH-PR-16" in ids


def test_ladder_pr16_title():
    ladder = _load_ladder()
    entry = next(e for e in ladder["ladder"] if e["id"] == "LRH-PR-16")
    assert entry["title"] == "Windows Convenience Layer without Full Windows App"


def test_ladder_pr16_depends_on_lrh_pr_03():
    ladder = _load_ladder()
    entry = next(e for e in ladder["ladder"] if e["id"] == "LRH-PR-16")
    assert "LRH-PR-03" in entry["depends_on"]


def test_ladder_pr16_depends_on_lrh_pr_15():
    ladder = _load_ladder()
    entry = next(e for e in ladder["ladder"] if e["id"] == "LRH-PR-16")
    assert "LRH-PR-15" in entry["depends_on"]


def test_ladder_pr16_target_files_include_windows_dir():
    ladder = _load_ladder()
    entry = next(e for e in ladder["ladder"] if e["id"] == "LRH-PR-16")
    assert "windows/" in entry["target_files"]


def test_ladder_pr16_target_files_include_start_bat():
    ladder = _load_ladder()
    entry = next(e for e in ladder["ladder"] if e["id"] == "LRH-PR-16")
    assert "scripts/start_odin.bat" in entry["target_files"]


def test_ladder_pr16_target_files_include_check_bat():
    ladder = _load_ladder()
    entry = next(e for e in ladder["ladder"] if e["id"] == "LRH-PR-16")
    assert "scripts/check_odin.bat" in entry["target_files"]


def test_ladder_pr16_target_files_include_doc():
    ladder = _load_ladder()
    entry = next(e for e in ladder["ladder"] if e["id"] == "LRH-PR-16")
    assert "docs/WINDOWS_CONVENIENCE_LAYER_V1.md" in entry["target_files"]


def test_ladder_pr16_target_files_include_test():
    ladder = _load_ladder()
    entry = next(e for e in ladder["ladder"] if e["id"] == "LRH-PR-16")
    assert "tests/test_lrh_pr_16_windows_convenience_layer.py" in entry["target_files"]


def test_ladder_pr16_forbidden_scope_no_service():
    ladder = _load_ladder()
    entry = next(e for e in ladder["ladder"] if e["id"] == "LRH-PR-16")
    forbidden_text = " ".join(entry["forbidden_scope"]).lower()
    assert "no windows service proof" in forbidden_text


def test_ladder_pr16_forbidden_scope_no_tray():
    ladder = _load_ladder()
    entry = next(e for e in ladder["ladder"] if e["id"] == "LRH-PR-16")
    forbidden_text = " ".join(entry["forbidden_scope"]).lower()
    assert "no tray proof" in forbidden_text


def test_ladder_pr16_forbidden_scope_no_signed_installer():
    ladder = _load_ladder()
    entry = next(e for e in ladder["ladder"] if e["id"] == "LRH-PR-16")
    forbidden_text = " ".join(entry["forbidden_scope"]).lower()
    assert "no signed installer proof" in forbidden_text


def test_ladder_pr16_forbidden_scope_no_full_windows_app():
    ladder = _load_ladder()
    entry = next(e for e in ladder["ladder"] if e["id"] == "LRH-PR-16")
    forbidden_text = " ".join(entry["forbidden_scope"]).lower()
    assert "no full windows app claim" in forbidden_text


def test_ladder_pr16_forbidden_scope_no_microsoft_store():
    ladder = _load_ladder()
    entry = next(e for e in ladder["ladder"] if e["id"] == "LRH-PR-16")
    forbidden_text = " ".join(entry["forbidden_scope"]).lower()
    assert "no microsoft store claim" in forbidden_text


# ---------------------------------------------------------------------------
# 9.3 Batch script shape tests
# ---------------------------------------------------------------------------

_FORBIDDEN_SCRIPT_PATTERNS = [
    "sc create",
    "sc.exe create",
    "sc start",
    "sc stop",
    "schtasks",
    "reg add",
    "reg delete",
    "start-process -verb runas",
    "new-service",
    "set-service",
    "installutil",
    "signtool",
    "makeappx",
    "winget",
    "msix",
    "--host 0.0.0.0",
    "0.0.0.0",
    "external_send",
    "applycandidate",
    "runprovider",
    "callmodel",
]


def _read_bat(name: str) -> str:
    return (ROOT / "scripts" / name).read_text(encoding="utf-8", errors="ignore")


def test_start_bat_has_echo_off():
    assert "@echo off" in _read_bat("start_odin.bat").lower()


def test_start_bat_has_python_invocation():
    assert "python" in _read_bat("start_odin.bat").lower()


def test_start_bat_has_odin_cli():
    assert "odin.cli" in _read_bat("start_odin.bat").lower()


def test_start_bat_no_forbidden_patterns():
    text = _read_bat("start_odin.bat").lower()
    for pattern in _FORBIDDEN_SCRIPT_PATTERNS:
        assert pattern.lower() not in text, f"start_odin.bat: forbidden pattern found: {pattern!r}"


def test_check_bat_has_echo_off():
    assert "@echo off" in _read_bat("check_odin.bat").lower()


def test_check_bat_has_python_invocation():
    assert "python" in _read_bat("check_odin.bat").lower()


def test_check_bat_has_odin_cli():
    assert "odin.cli" in _read_bat("check_odin.bat").lower()


def test_check_bat_no_forbidden_patterns():
    text = _read_bat("check_odin.bat").lower()
    for pattern in _FORBIDDEN_SCRIPT_PATTERNS:
        assert pattern.lower() not in text, f"check_odin.bat: forbidden pattern found: {pattern!r}"


def test_stop_bat_has_echo_off():
    assert "@echo off" in _read_bat("stop_odin.bat").lower()


def test_stop_bat_has_python_invocation():
    assert "python" in _read_bat("stop_odin.bat").lower()


def test_stop_bat_has_odin_cli():
    assert "odin.cli" in _read_bat("stop_odin.bat").lower()


def test_stop_bat_no_forbidden_patterns():
    text = _read_bat("stop_odin.bat").lower()
    for pattern in _FORBIDDEN_SCRIPT_PATTERNS:
        assert pattern.lower() not in text, f"stop_odin.bat: forbidden pattern found: {pattern!r}"


# ---------------------------------------------------------------------------
# 9.4 Documentation phrase tests
# ---------------------------------------------------------------------------

_REQUIRED_DOC_PHRASES = [
    "windows convenience layer",
    "manual start",
    "manual check",
    "manual stop",
    "candidate-only",
    "local-only",
    "not a full windows app",
    "not windows service proof",
    "not tray proof",
    "not signed installer proof",
    "not installer proof",
    "not target-host proof",
    "not microsoft store readiness",
    "not production readiness",
    "not security certification",
    "no app apply",
    "no external send",
    "no live model inference",
    "no model quality proof",
    "service/tray/signing/installer remains a proof gap",
]

_FORBIDDEN_DOC_CLAIMS = [
    "is fully proven",
    "complete proof of",
    "this is a full windows app",
    "windows service is proven",
    "tray is proven",
    "installer is proven",
    "signed distribution is proven",
    "microsoft store ready",
    "is production-ready",
    "is security certified",
]


def _read_doc() -> str:
    return (ROOT / "docs" / "WINDOWS_CONVENIENCE_LAYER_V1.md").read_text(encoding="utf-8", errors="ignore").lower()


def test_doc_has_all_required_phrases():
    text = _read_doc()
    for phrase in _REQUIRED_DOC_PHRASES:
        assert phrase.lower() in text, f"WINDOWS_CONVENIENCE_LAYER_V1.md: missing phrase: {phrase!r}"


def test_doc_has_no_forbidden_overclaim():
    text = _read_doc()
    for claim in _FORBIDDEN_DOC_CLAIMS:
        assert claim.lower() not in text, f"WINDOWS_CONVENIENCE_LAYER_V1.md: forbidden claim found: {claim!r}"


# ---------------------------------------------------------------------------
# 9.5 Helper manifest tests
# ---------------------------------------------------------------------------

def _load_manifest() -> dict:
    return json.loads((ROOT / "windows" / "helper_manifest_v1.json").read_text(encoding="utf-8"))


def test_manifest_valid_json():
    m = _load_manifest()
    assert isinstance(m, dict)


def test_manifest_artifact_kind():
    m = _load_manifest()
    assert m["artifact_kind"] == "odin_windows_convenience_helper_manifest"


def test_manifest_lrh_pr():
    m = _load_manifest()
    assert m["lrh_pr"] == "LRH-PR-16"


def test_manifest_candidate_only():
    m = _load_manifest()
    assert m["candidate_only"] is True


def test_manifest_local_only():
    m = _load_manifest()
    assert m["local_only"] is True


def test_manifest_windows_convenience_only():
    m = _load_manifest()
    assert m["windows_convenience_only"] is True


def test_manifest_manual_start_helper():
    m = _load_manifest()
    assert m.get("manual_start_helper") == "scripts/start_odin.bat"


def test_manifest_manual_check_helper():
    m = _load_manifest()
    assert m.get("manual_check_helper") == "scripts/check_odin.bat"


def test_manifest_manual_stop_helper():
    m = _load_manifest()
    assert m.get("manual_stop_helper") == "scripts/stop_odin.bat"


_REQUIRED_MANIFEST_NOT_PROVEN = [
    "windows_service",
    "windows_tray",
    "windows_installer",
    "signed_distribution",
    "target_host_validation",
    "microsoft_store_readiness",
    "production_readiness",
    "security_certification",
    "app_apply_authority",
    "app_state_mutation",
    "external_send_authority",
]


def test_manifest_not_proven_completeness():
    m = _load_manifest()
    not_proven = m.get("not_proven", [])
    for entry in _REQUIRED_MANIFEST_NOT_PROVEN:
        assert entry in not_proven, f"helper_manifest_v1.json: not_proven missing {entry!r}"


# ---------------------------------------------------------------------------
# 9.6 CLI tests
# ---------------------------------------------------------------------------

def test_cli_validate_windows_convenience_layer():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-windows-convenience-layer"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert result.returncode == 0, f"validate-windows-convenience-layer failed:\n{result.stdout}\n{result.stderr}"
    assert "OK" in result.stdout


def test_cli_prove_windows_convenience_layer():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "prove-windows-convenience-layer"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert result.returncode == 0, f"prove-windows-convenience-layer failed:\n{result.stdout}\n{result.stderr}"
    packet = json.loads(result.stdout)
    assert packet["candidate_only"] is True
    assert packet["local_only"] is True
    assert packet["windows_convenience_only"] is True
    assert packet["status"] in ("ok", "partial")
    assert "not_proven" in packet
    assert "proof_boundaries" in packet


def test_cli_prove_packet_not_proven_entries():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "prove-windows-convenience-layer"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert result.returncode == 0
    packet = json.loads(result.stdout)
    not_proven = packet["not_proven"]
    for entry in [
        "windows_service", "windows_tray", "windows_installer", "signed_distribution",
        "target_host_validation", "microsoft_store_readiness", "full_windows_app",
        "production_readiness", "security_certification", "public_network_api",
        "live_model_inference", "model_quality", "app_apply_authority",
        "app_state_mutation", "external_send_authority",
    ]:
        assert entry in not_proven, f"prove packet missing not_proven entry: {entry!r}"


def test_cli_prove_packet_proof_boundaries():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "prove-windows-convenience-layer"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert result.returncode == 0
    packet = json.loads(result.stdout)
    boundaries = packet["proof_boundaries"]
    for boundary in [
        "not_windows_service_proof", "not_tray_proof", "not_installer_proof",
        "not_signed_installer_proof", "not_full_windows_app_proof", "not_target_host_proof",
        "not_microsoft_store_readiness", "not_production_readiness_certification",
        "not_security_certification",
    ]:
        assert boundary in boundaries, f"prove packet missing proof_boundary: {boundary!r}"


# ---------------------------------------------------------------------------
# 9.7 Agent operator smoke
# ---------------------------------------------------------------------------

def test_agent_handoff_packet_shape():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff",
         "--agent", "claude-code", "--lrh-pr", "16"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert result.returncode == 0, f"agent-handoff failed:\n{result.stdout}\n{result.stderr}"
    packet = json.loads(result.stdout)
    assert packet["candidate_only"] is True
    assert packet["app_owned_apply"] is True
    assert packet["external_send_default"] is False
    assert packet["hidden_tool_execution_allowed"] is False


def test_agent_guard_ok():
    import tempfile, os
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        packet_path = f.name
    try:
        subprocess.run(
            [sys.executable, "-m", "odin.cli", "agent-handoff",
             "--agent", "claude-code", "--lrh-pr", "16", "--out", packet_path],
            capture_output=True, text=True, cwd=str(ROOT), check=True,
        )
        result = subprocess.run(
            [sys.executable, "-m", "odin.cli", "agent-guard", "--packet", packet_path],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        assert result.returncode == 0, f"agent-guard failed:\n{result.stdout}\n{result.stderr}"
        guard = json.loads(result.stdout)
        assert guard["status"] == "ok"
        assert guard["violations"] == []
    finally:
        os.unlink(packet_path)


# ---------------------------------------------------------------------------
# 9.8 Validate-all integration
# ---------------------------------------------------------------------------

def test_validate_all_includes_windows_convenience_layer():
    """validate-all must not error on windows convenience layer files."""
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-all"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert result.returncode == 0, f"validate-all failed:\n{result.stdout}\n{result.stderr}"
    assert "OK" in result.stdout
