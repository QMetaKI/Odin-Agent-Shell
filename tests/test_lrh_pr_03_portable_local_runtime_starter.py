"""LRH-PR-03 — Portable Local Runtime Starter tests.

Deterministic, no network beyond localhost, no live model, no provider API.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------------------
# Config tests
# ---------------------------------------------------------------------------

class TestPortableRuntimeConfig:
    def test_valid_config_127_no_errors(self):
        from odin.local_runtime.config import validate_config
        errors = validate_config({"host": "127.0.0.1", "port": 8877})
        assert errors == []

    def test_valid_config_localhost_no_errors(self):
        from odin.local_runtime.config import validate_config
        errors = validate_config({"host": "localhost", "port": 8877})
        assert errors == []

    def test_valid_config_ipv6_loopback_no_errors(self):
        from odin.local_runtime.config import validate_config
        errors = validate_config({"host": "::1", "port": 8877})
        assert errors == []

    def test_default_host_is_127_0_0_1(self):
        from odin.local_runtime.config import DEFAULT_HOST
        assert DEFAULT_HOST == "127.0.0.1"

    def test_public_bind_0_0_0_0_is_blocked(self):
        from odin.local_runtime.config import validate_config
        errors = validate_config({"host": "0.0.0.0", "port": 8877})
        assert any("blocked" in e or "0.0.0.0" in e for e in errors)

    def test_public_bind_double_colon_is_blocked(self):
        from odin.local_runtime.config import validate_config
        errors = validate_config({"host": "::", "port": 8877})
        assert any("blocked" in e or "::" in e for e in errors)

    def test_empty_host_is_blocked(self):
        from odin.local_runtime.config import validate_config
        errors = validate_config({"host": "", "port": 8877})
        assert len(errors) > 0

    def test_unknown_host_is_rejected(self):
        from odin.local_runtime.config import validate_config
        errors = validate_config({"host": "192.168.1.1", "port": 8877})
        assert len(errors) > 0

    def test_candidate_only_false_is_rejected(self):
        from odin.local_runtime.config import validate_config
        errors = validate_config({"host": "127.0.0.1", "port": 8877, "candidate_only": False})
        assert any("candidate_only" in e for e in errors)

    def test_app_owned_apply_false_is_rejected(self):
        from odin.local_runtime.config import validate_config
        errors = validate_config({"host": "127.0.0.1", "port": 8877, "app_owned_apply": False})
        assert any("app_owned_apply" in e for e in errors)

    def test_external_send_true_is_rejected(self):
        from odin.local_runtime.config import validate_config
        errors = validate_config({"host": "127.0.0.1", "port": 8877, "external_send_default": True})
        assert any("external_send" in e for e in errors)

    def test_invalid_port_is_rejected(self):
        from odin.local_runtime.config import validate_config
        errors = validate_config({"host": "127.0.0.1", "port": 80})
        assert len(errors) > 0

    def test_load_config_from_dict_valid(self):
        from odin.local_runtime.config import load_config_from_dict
        cfg, errors = load_config_from_dict({"host": "127.0.0.1", "port": 8877})
        assert errors == []
        assert cfg is not None
        assert cfg.host == "127.0.0.1"
        assert cfg.port == 8877
        assert cfg.candidate_only is True
        assert cfg.app_owned_apply is True

    def test_load_config_from_dict_invalid(self):
        from odin.local_runtime.config import load_config_from_dict
        cfg, errors = load_config_from_dict({"host": "0.0.0.0", "port": 8877})
        assert cfg is None
        assert len(errors) > 0


# ---------------------------------------------------------------------------
# Fixture file tests
# ---------------------------------------------------------------------------

class TestConfigFixtures:
    def test_valid_fixture_validates(self):
        from odin.local_runtime.config import validate_config
        fixture = ROOT / "examples/local_runtime/portable_runtime_config.valid.json"
        assert fixture.exists(), f"missing fixture: {fixture}"
        data = json.loads(fixture.read_text())
        errors = validate_config(data)
        assert errors == [], f"valid fixture should have no errors: {errors}"

    def test_invalid_public_bind_fixture_fails(self):
        from odin.local_runtime.config import validate_config
        fixture = ROOT / "examples/local_runtime/portable_runtime_config.invalid.public_bind.json"
        assert fixture.exists(), f"missing fixture: {fixture}"
        data = json.loads(fixture.read_text())
        errors = validate_config(data)
        assert len(errors) > 0, "invalid public_bind fixture should fail validation"

    def test_valid_fixture_host_is_localhost(self):
        fixture = ROOT / "examples/local_runtime/portable_runtime_config.valid.json"
        data = json.loads(fixture.read_text())
        assert data["host"] in {"127.0.0.1", "localhost", "::1"}

    def test_valid_fixture_candidate_only_is_true(self):
        fixture = ROOT / "examples/local_runtime/portable_runtime_config.valid.json"
        data = json.loads(fixture.read_text())
        assert data.get("candidate_only") is True

    def test_invalid_fixture_host_is_blocked(self):
        fixture = ROOT / "examples/local_runtime/portable_runtime_config.invalid.public_bind.json"
        data = json.loads(fixture.read_text())
        from odin.local_runtime.config import BLOCKED_HOSTS
        assert data["host"] in BLOCKED_HOSTS


# ---------------------------------------------------------------------------
# Lockfile tests
# ---------------------------------------------------------------------------

class TestLockfile:
    def test_write_read_remove_deterministic(self, tmp_path):
        from odin.local_runtime import lockfile as lf_module
        orig_path = lf_module.LOCKFILE_PATH
        test_lock = tmp_path / "test.lock"
        lf_module.LOCKFILE_PATH = test_lock
        try:
            lf_module.write_lockfile(pid=12345, host="127.0.0.1", port=8877)
            assert test_lock.exists()
            data = lf_module.read_lockfile()
            assert data is not None
            assert data["pid"] == 12345
            assert data["host"] == "127.0.0.1"
            assert data["port"] == 8877
            assert data["candidate_only"] is True
            assert "claim_boundary" in data
            removed = lf_module.remove_lockfile()
            assert removed is True
            assert not test_lock.exists()
            assert lf_module.read_lockfile() is None
        finally:
            lf_module.LOCKFILE_PATH = orig_path

    def test_lockfile_fields_present(self, tmp_path):
        from odin.local_runtime import lockfile as lf_module
        orig_path = lf_module.LOCKFILE_PATH
        test_lock = tmp_path / "test.lock"
        lf_module.LOCKFILE_PATH = test_lock
        try:
            lf_module.write_lockfile(pid=99, host="127.0.0.1", port=8877)
            data = lf_module.read_lockfile()
            for field in ["pid", "host", "port", "started_by", "runtime_mode", "created_at_policy", "claim_boundary"]:
                assert field in data, f"lockfile missing field: {field}"
        finally:
            lf_module.LOCKFILE_PATH = orig_path

    def test_lockfile_exists_false_when_missing(self, tmp_path):
        from odin.local_runtime import lockfile as lf_module
        orig_path = lf_module.LOCKFILE_PATH
        lf_module.LOCKFILE_PATH = tmp_path / "no.lock"
        try:
            assert lf_module.lockfile_exists() is False
        finally:
            lf_module.LOCKFILE_PATH = orig_path

    def test_lockfile_exists_true_when_present(self, tmp_path):
        from odin.local_runtime import lockfile as lf_module
        orig_path = lf_module.LOCKFILE_PATH
        test_lock = tmp_path / "test.lock"
        lf_module.LOCKFILE_PATH = test_lock
        try:
            lf_module.write_lockfile(pid=1, host="127.0.0.1", port=8877)
            assert lf_module.lockfile_exists() is True
        finally:
            lf_module.LOCKFILE_PATH = orig_path

    def test_remove_lockfile_returns_false_when_missing(self, tmp_path):
        from odin.local_runtime import lockfile as lf_module
        orig_path = lf_module.LOCKFILE_PATH
        lf_module.LOCKFILE_PATH = tmp_path / "no.lock"
        try:
            assert lf_module.remove_lockfile() is False
        finally:
            lf_module.LOCKFILE_PATH = orig_path

    def test_lockfile_under_odin_runtime_dir(self):
        from odin.local_runtime.lockfile import LOCKFILE_PATH
        assert ".odin_runtime" in str(LOCKFILE_PATH)


# ---------------------------------------------------------------------------
# Port detection tests
# ---------------------------------------------------------------------------

class TestPortDetection:
    def test_check_port_available_returns_structured_status(self):
        from odin.local_runtime.ports import check_port_in_use
        result = check_port_in_use("127.0.0.1", 18877)
        assert "status" in result
        assert result["status"] in {"available", "in_use"}
        assert "host" in result
        assert "port" in result
        assert "claim_boundary" in result

    def test_is_port_available_returns_bool(self):
        from odin.local_runtime.ports import is_port_available
        result = is_port_available("127.0.0.1", 18877)
        assert isinstance(result, bool)

    def test_port_in_use_returns_guidance(self):
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", 18878))
            sock.listen(1)
            from odin.local_runtime.ports import check_port_in_use
            result = check_port_in_use("127.0.0.1", 18878)
            assert result["status"] == "in_use"
            assert "guidance" in result
        finally:
            sock.close()


# ---------------------------------------------------------------------------
# Check portable runtime tests
# ---------------------------------------------------------------------------

class TestCheckPortableRuntime:
    def test_check_returns_structured_status(self, tmp_path):
        from odin.local_runtime import starter, lockfile as lf_module
        orig_path = lf_module.LOCKFILE_PATH
        lf_module.LOCKFILE_PATH = tmp_path / "test.lock"
        try:
            result = starter.check_portable_runtime(host="127.0.0.1", port=18879)
            assert "artifact_kind" in result
            assert result["artifact_kind"] == "odin_local_runtime_check"
            assert "status" in result
            assert "candidate_only" in result
            assert result["candidate_only"] is True
            assert "claim_boundary" in result
        finally:
            lf_module.LOCKFILE_PATH = orig_path

    def test_check_not_running_when_no_lockfile(self, tmp_path):
        from odin.local_runtime import starter, lockfile as lf_module
        orig_path = lf_module.LOCKFILE_PATH
        lf_module.LOCKFILE_PATH = tmp_path / "no.lock"
        try:
            result = starter.check_portable_runtime(host="127.0.0.1", port=18880)
            assert result["status"] in {"not_running", "stale_lockfile"}
            assert result["lockfile_present"] is False
        finally:
            lf_module.LOCKFILE_PATH = orig_path

    def test_check_config_invalid_when_public_host(self, tmp_path):
        from odin.local_runtime import starter, lockfile as lf_module
        orig_path = lf_module.LOCKFILE_PATH
        lf_module.LOCKFILE_PATH = tmp_path / "no.lock"
        try:
            result = starter.check_portable_runtime(host="0.0.0.0", port=18881)
            assert result["config_valid"] is False
            assert "config_errors" in result
        finally:
            lf_module.LOCKFILE_PATH = orig_path


# ---------------------------------------------------------------------------
# Proof packet tests
# ---------------------------------------------------------------------------

class TestOnceSmoke:
    def test_once_smoke_emits_proof_packet(self):
        from odin.local_runtime.proof import run_once_smoke_proof
        result = run_once_smoke_proof(host="127.0.0.1", port=18882)
        assert result["artifact_kind"] == "local_runtime_proof_packet"
        assert result["status"] in {"ok", "partial"}
        assert result["candidate_only"] is True
        assert "claim_boundary" in result
        assert "proven" in result
        assert "not_proven" in result
        assert "steps" in result

    def test_once_smoke_not_proven_includes_production_readiness(self):
        from odin.local_runtime.proof import run_once_smoke_proof
        result = run_once_smoke_proof(host="127.0.0.1", port=18883)
        assert "production_readiness" in result["not_proven"]

    def test_once_smoke_not_proven_includes_windows_service(self):
        from odin.local_runtime.proof import run_once_smoke_proof
        result = run_once_smoke_proof(host="127.0.0.1", port=18884)
        assert any("windows" in s.lower() for s in result["not_proven"])

    def test_once_smoke_not_proven_includes_live_model(self):
        from odin.local_runtime.proof import run_once_smoke_proof
        result = run_once_smoke_proof(host="127.0.0.1", port=18885)
        assert any("live_model" in s or "model" in s for s in result["not_proven"])

    def test_once_smoke_has_note_about_no_production_claim(self):
        from odin.local_runtime.proof import run_once_smoke_proof
        result = run_once_smoke_proof(host="127.0.0.1", port=18886)
        assert "note" in result
        note = result["note"].lower()
        assert "not" in note or "does not" in note


# ---------------------------------------------------------------------------
# Scripts existence tests
# ---------------------------------------------------------------------------

class TestScripts:
    @pytest.mark.parametrize("script", [
        "scripts/start_odin.sh",
        "scripts/stop_odin.sh",
        "scripts/check_odin.sh",
        "scripts/start_odin.bat",
        "scripts/stop_odin.bat",
        "scripts/check_odin.bat",
    ])
    def test_script_exists(self, script):
        p = ROOT / script
        assert p.exists(), f"Script missing: {script}"

    @pytest.mark.parametrize("script", [
        "scripts/start_odin.sh",
        "scripts/stop_odin.sh",
        "scripts/check_odin.sh",
        "scripts/start_odin.bat",
        "scripts/stop_odin.bat",
        "scripts/check_odin.bat",
    ])
    def test_script_calls_odin_cli(self, script):
        p = ROOT / script
        assert p.exists()
        text = p.read_text(encoding="utf-8")
        assert "python -m odin.cli" in text, f"{script}: must call 'python -m odin.cli'"

    @pytest.mark.parametrize("script", [
        "scripts/start_odin.sh",
        "scripts/stop_odin.sh",
        "scripts/check_odin.sh",
        "scripts/start_odin.bat",
        "scripts/stop_odin.bat",
        "scripts/check_odin.bat",
    ])
    def test_script_has_no_secrets(self, script):
        p = ROOT / script
        assert p.exists()
        text = p.read_text(encoding="utf-8").lower()
        for secret_word in ("password", "secret", "api_key", "token", "bearer"):
            assert secret_word not in text, f"{script}: must not contain secret word '{secret_word}'"


# ---------------------------------------------------------------------------
# Documentation tests
# ---------------------------------------------------------------------------

class TestDocs:
    def test_local_runtime_starter_doc_exists(self):
        assert (ROOT / "docs/LOCAL_RUNTIME_STARTER_V1.md").exists()

    def test_doc_states_not_windows_service(self):
        doc = (ROOT / "docs/LOCAL_RUNTIME_STARTER_V1.md").read_text(encoding="utf-8").lower()
        assert "not a windows service" in doc or "not a service" in doc

    def test_doc_states_not_tray_app(self):
        doc = (ROOT / "docs/LOCAL_RUNTIME_STARTER_V1.md").read_text(encoding="utf-8").lower()
        assert "not a tray" in doc

    def test_doc_states_not_signed_installer(self):
        doc = (ROOT / "docs/LOCAL_RUNTIME_STARTER_V1.md").read_text(encoding="utf-8").lower()
        assert "not a signed installer" in doc or "not production readiness" in doc

    def test_doc_states_no_public_network(self):
        doc = (ROOT / "docs/LOCAL_RUNTIME_STARTER_V1.md").read_text(encoding="utf-8").lower()
        assert "public network" in doc

    def test_doc_mentions_127_0_0_1(self):
        doc = (ROOT / "docs/LOCAL_RUNTIME_STARTER_V1.md").read_text(encoding="utf-8")
        assert "127.0.0.1" in doc


# ---------------------------------------------------------------------------
# Claim boundary tests
# ---------------------------------------------------------------------------

class TestClaimBoundaries:
    def test_check_result_has_candidate_only(self, tmp_path):
        from odin.local_runtime import starter, lockfile as lf_module
        orig_path = lf_module.LOCKFILE_PATH
        lf_module.LOCKFILE_PATH = tmp_path / "no.lock"
        try:
            result = starter.check_portable_runtime(host="127.0.0.1", port=18887)
            assert result.get("candidate_only") is True
        finally:
            lf_module.LOCKFILE_PATH = orig_path

    def test_proof_packet_has_candidate_only(self):
        from odin.local_runtime.proof import run_once_smoke_proof
        result = run_once_smoke_proof(host="127.0.0.1", port=18888)
        assert result.get("candidate_only") is True

    def test_proof_claim_boundary_contains_no_app_apply(self):
        from odin.local_runtime.proof import PROOF_CLAIM_BOUNDARY
        assert "no_app_apply" in PROOF_CLAIM_BOUNDARY or "candidate_only" in PROOF_CLAIM_BOUNDARY

    def test_lockfile_claim_boundary_present(self, tmp_path):
        from odin.local_runtime import lockfile as lf_module
        orig_path = lf_module.LOCKFILE_PATH
        lf_module.LOCKFILE_PATH = tmp_path / "test.lock"
        try:
            lf_module.write_lockfile(pid=1, host="127.0.0.1", port=8877)
            data = lf_module.read_lockfile()
            assert "claim_boundary" in data
        finally:
            lf_module.LOCKFILE_PATH = orig_path


# ---------------------------------------------------------------------------
# validate-local-runtime-starter CLI validator test
# ---------------------------------------------------------------------------

class TestValidateLocalRuntimeStarter:
    def test_validator_passes(self):
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "odin.cli", "validate-local-runtime-starter"],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        assert result.returncode == 0, f"validate-local-runtime-starter failed:\n{result.stdout}\n{result.stderr}"

    def test_prove_local_runtime_once_smoke(self):
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "odin.cli", "prove-local-runtime", "--once-smoke",
             "--host", "127.0.0.1", "--port", "18889"],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        assert result.returncode == 0, f"prove-local-runtime failed:\n{result.stdout}\n{result.stderr}"
        output = json.loads(result.stdout)
        assert output["artifact_kind"] == "local_runtime_proof_packet"
        assert output["candidate_only"] is True
