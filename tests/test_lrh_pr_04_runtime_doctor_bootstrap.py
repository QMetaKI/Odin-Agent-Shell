"""LRH-PR-04: Runtime Doctor, First-Run Bootstrap and Self-Healing tests."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Redaction tests
# ---------------------------------------------------------------------------

class TestRedaction:
    def test_secret_key_token_redacted(self):
        from odin.doctor.redaction import redact_recursive
        result = redact_recursive({"token": "abc123", "name": "odin"})
        assert result["token"] == "[REDACTED]"
        assert result["name"] == "odin"

    def test_secret_key_api_key_redacted(self):
        from odin.doctor.redaction import redact_recursive
        result = redact_recursive({"api_key": "secret-val", "host": "127.0.0.1"})
        assert result["api_key"] == "[REDACTED]"
        assert result["host"] == "127.0.0.1"

    def test_secret_key_password_redacted(self):
        from odin.doctor.redaction import redact_recursive
        result = redact_recursive({"password": "hunter2"})
        assert result["password"] == "[REDACTED]"

    def test_secret_key_authorization_redacted(self):
        from odin.doctor.redaction import redact_recursive
        result = redact_recursive({"authorization": "Bearer xyz"})
        assert result["authorization"] == "[REDACTED]"

    def test_bearer_string_redacted(self):
        from odin.doctor.redaction import redact_recursive
        result = redact_recursive({"value": "Bearer secrettoken"})
        assert result["value"] == "[REDACTED]"

    def test_nested_secret_redacted(self):
        from odin.doctor.redaction import redact_recursive
        result = redact_recursive({"outer": {"access_token": "hidden"}})
        assert result["outer"]["access_token"] == "[REDACTED]"

    def test_list_with_dicts_redacted(self):
        from odin.doctor.redaction import redact_recursive
        result = redact_recursive([{"client_secret": "x"}, {"name": "y"}])
        assert result[0]["client_secret"] == "[REDACTED]"
        assert result[1]["name"] == "y"

    def test_non_secret_keys_not_redacted(self):
        from odin.doctor.redaction import redact_recursive
        result = redact_recursive({"host": "127.0.0.1", "port": 8877, "status": "ok"})
        assert result["host"] == "127.0.0.1"
        assert result["port"] == 8877
        assert result["status"] == "ok"

    def test_is_secret_key_true_for_token(self):
        from odin.doctor.redaction import is_secret_key
        assert is_secret_key("token") is True
        assert is_secret_key("my_token") is True
        assert is_secret_key("ACCESS_TOKEN") is True

    def test_is_secret_key_false_for_host(self):
        from odin.doctor.redaction import is_secret_key
        assert is_secret_key("host") is False
        assert is_secret_key("port") is False
        assert is_secret_key("status") is False

    def test_credential_key_redacted(self):
        from odin.doctor.redaction import redact_recursive
        result = redact_recursive({"credential": "abc"})
        assert result["credential"] == "[REDACTED]"

    def test_refresh_token_redacted(self):
        from odin.doctor.redaction import redact_recursive
        result = redact_recursive({"refresh_token": "tok"})
        assert result["refresh_token"] == "[REDACTED]"


# ---------------------------------------------------------------------------
# Doctor checks tests
# ---------------------------------------------------------------------------

class TestDoctorChecks:
    def test_python_version_check_returns_ok(self):
        from odin.doctor.checks import check_python_version
        result = check_python_version()
        assert result["check"] == "python_version"
        assert result["status"] == "ok"
        assert "detail" in result

    def test_package_imports_check_returns_ok(self):
        from odin.doctor.checks import check_package_imports
        result = check_package_imports()
        assert result["check"] == "package_imports"
        assert result["status"] == "ok"

    def test_host_safety_localhost_ok(self):
        from odin.doctor.checks import check_host_safety
        result = check_host_safety("127.0.0.1")
        assert result["status"] == "ok"

    def test_host_safety_blocked_host_fails(self):
        from odin.doctor.checks import check_host_safety
        result = check_host_safety("0.0.0.0")
        assert result["status"] == "fail"
        assert "failure_reason" in result

    def test_host_safety_public_host_fails(self):
        from odin.doctor.checks import check_host_safety
        result = check_host_safety("192.168.1.100")
        assert result["status"] == "fail"

    def test_lockfile_check_no_lockfile(self):
        from odin.doctor.checks import check_lockfile
        result = check_lockfile()
        assert result["check"] == "lockfile"
        assert result["status"] in {"ok", "warn", "fail"}

    def test_runtime_dir_check(self):
        from odin.doctor.checks import check_runtime_dir
        result = check_runtime_dir()
        assert result["check"] == "runtime_dir"
        assert result["status"] in {"ok", "warn"}

    def test_config_file_check_absent(self, tmp_path):
        from odin.doctor import checks as c
        orig = c._REPO_ROOT
        c._REPO_ROOT = tmp_path
        try:
            result = c.check_config_file()
            assert result["check"] == "config_file"
            assert result["status"] == "warn"
            assert "failure_reason" in result
        finally:
            c._REPO_ROOT = orig

    def test_config_file_check_valid(self, tmp_path):
        from odin.doctor import checks as c
        orig = c._REPO_ROOT = tmp_path
        rt_dir = tmp_path / ".odin_runtime"
        rt_dir.mkdir()
        cfg = {
            "host": "127.0.0.1",
            "port": 8877,
            "candidate_only": True,
            "app_owned_apply": True,
            "external_send_default": False,
        }
        (rt_dir / "local_runtime_config.json").write_text(json.dumps(cfg), encoding="utf-8")
        try:
            result = c.check_config_file()
            assert result["status"] == "ok"
        finally:
            c._REPO_ROOT = orig

    def test_config_file_check_blocked_host(self, tmp_path):
        from odin.doctor import checks as c
        orig = c._REPO_ROOT = tmp_path
        rt_dir = tmp_path / ".odin_runtime"
        rt_dir.mkdir()
        cfg = {
            "host": "0.0.0.0",
            "port": 8877,
            "candidate_only": True,
            "app_owned_apply": True,
            "external_send_default": False,
        }
        (rt_dir / "local_runtime_config.json").write_text(json.dumps(cfg), encoding="utf-8")
        try:
            result = c.check_config_file()
            assert result["status"] == "fail"
            assert "blocked" in result.get("failure_reason", "").lower()
        finally:
            c._REPO_ROOT = orig

    def test_check_result_has_required_fields(self):
        from odin.doctor.checks import check_python_version
        result = check_python_version()
        assert "check" in result
        assert "status" in result
        assert "detail" in result


# ---------------------------------------------------------------------------
# Doctor diagnostics tests
# ---------------------------------------------------------------------------

class TestDoctorDiagnostics:
    def test_run_doctor_returns_report(self):
        from odin.doctor.diagnostics import run_doctor
        report = run_doctor()
        assert report["artifact_kind"] == "odin_doctor_report"
        assert "status" in report
        assert "checks" in report
        assert "failure_count" in report
        assert "failure_reasons" in report
        assert "candidate_only" in report
        assert report["candidate_only"] is True

    def test_run_doctor_read_only_flag(self):
        from odin.doctor.diagnostics import run_doctor
        report = run_doctor()
        assert report["read_only"] is True
        assert report["state_mutated"] is False

    def test_run_doctor_has_claim_boundary(self):
        from odin.doctor.diagnostics import run_doctor
        report = run_doctor()
        assert "claim_boundary" in report
        assert "not_production_readiness_proof" in report["claim_boundary"] or \
               "candidate" in report["claim_boundary"]

    def test_run_doctor_has_known_non_proofs(self):
        from odin.doctor.diagnostics import run_doctor, KNOWN_NON_PROOFS
        report = run_doctor()
        assert "known_non_proofs" in report
        assert len(report["known_non_proofs"]) > 0
        for np in KNOWN_NON_PROOFS:
            assert np in report["known_non_proofs"]

    def test_run_doctor_does_not_create_config(self, tmp_path):
        from odin.doctor import checks as c
        orig = c._REPO_ROOT = tmp_path
        try:
            from odin.doctor.diagnostics import run_doctor
            run_doctor()
            config_path = tmp_path / ".odin_runtime" / "local_runtime_config.json"
            assert not config_path.exists(), "doctor must not create config"
        finally:
            c._REPO_ROOT = orig

    def test_run_doctor_does_not_delete_lockfile(self, tmp_path):
        from odin.local_runtime.lockfile import LOCKFILE_PATH
        lockfile = LOCKFILE_PATH
        had_lockfile = lockfile.exists()
        from odin.doctor.diagnostics import run_doctor
        run_doctor()
        if had_lockfile:
            assert lockfile.exists(), "doctor must not delete existing lockfile"

    def test_run_doctor_success_fixture_structure(self):
        fixture = ROOT / "examples/doctor/doctor_success.valid.json"
        assert fixture.exists()
        data = json.loads(fixture.read_text(encoding="utf-8"))
        assert data["artifact_kind"] == "odin_doctor_report"
        assert data["status"] == "ok"
        assert data["candidate_only"] is True
        assert data["read_only"] is True
        assert data["state_mutated"] is False
        assert "claim_boundary" in data
        assert "known_non_proofs" in data

    def test_run_doctor_failure_fixture_structure(self):
        fixture = ROOT / "examples/doctor/doctor_failure.valid.json"
        assert fixture.exists()
        data = json.loads(fixture.read_text(encoding="utf-8"))
        assert data["artifact_kind"] == "odin_doctor_report"
        assert data["status"] == "fail"
        assert data["failure_count"] > 0
        assert len(data["failure_reasons"]) > 0
        assert data["state_mutated"] is False

    def test_run_doctor_failure_fixture_has_clear_failure_reasons(self):
        fixture = ROOT / "examples/doctor/doctor_failure.valid.json"
        data = json.loads(fixture.read_text(encoding="utf-8"))
        for reason in data["failure_reasons"]:
            assert len(reason) > 10, "failure reasons must be descriptive"

    def test_run_doctor_success_fixture_no_windows_service_claim(self):
        fixture = ROOT / "examples/doctor/doctor_success.valid.json"
        data = json.loads(fixture.read_text(encoding="utf-8"))
        non_proofs = data.get("known_non_proofs", [])
        assert "not_windows_service_tray_installer_proof" in non_proofs
        bundle_str = json.dumps(data).lower()
        assert "windows service" not in bundle_str or "not_windows_service" in bundle_str

    def test_run_doctor_success_fixture_no_provider_claim(self):
        fixture = ROOT / "examples/doctor/doctor_success.valid.json"
        text = fixture.read_text(encoding="utf-8").lower()
        assert "provider_live_model_proof" not in text or "not_provider_live_model_proof" in text


# ---------------------------------------------------------------------------
# Bootstrap first-run tests
# ---------------------------------------------------------------------------

class TestFirstRunBootstrap:
    def test_creates_config_when_absent(self, tmp_path):
        from odin.bootstrap.first_run import run_first_run_bootstrap
        cfg_path = tmp_path / "local_runtime_config.json"
        result = run_first_run_bootstrap(config_path=cfg_path)
        assert result["status"] == "created"
        assert cfg_path.exists()
        assert result["state_mutated"] is True

    def test_skips_when_config_exists(self, tmp_path):
        from odin.bootstrap.first_run import run_first_run_bootstrap
        cfg_path = tmp_path / "local_runtime_config.json"
        cfg_path.write_text('{"host": "127.0.0.1"}', encoding="utf-8")
        result = run_first_run_bootstrap(config_path=cfg_path)
        assert result["status"] == "skipped"
        assert result["state_mutated"] is False

    def test_idempotent_double_run(self, tmp_path):
        from odin.bootstrap.first_run import run_first_run_bootstrap
        cfg_path = tmp_path / "local_runtime_config.json"
        r1 = run_first_run_bootstrap(config_path=cfg_path)
        r2 = run_first_run_bootstrap(config_path=cfg_path)
        assert r1["status"] == "created"
        assert r2["status"] == "skipped"

    def test_default_host_is_localhost(self, tmp_path):
        from odin.bootstrap.first_run import run_first_run_bootstrap
        cfg_path = tmp_path / "local_runtime_config.json"
        result = run_first_run_bootstrap(config_path=cfg_path)
        assert result["status"] == "created"
        written = json.loads(cfg_path.read_text(encoding="utf-8"))
        assert written["host"] == "127.0.0.1"

    def test_no_public_bind_in_default(self, tmp_path):
        from odin.bootstrap.first_run import run_first_run_bootstrap
        cfg_path = tmp_path / "local_runtime_config.json"
        run_first_run_bootstrap(config_path=cfg_path)
        written = json.loads(cfg_path.read_text(encoding="utf-8"))
        assert written.get("public_bind") is False

    def test_no_external_send_in_default(self, tmp_path):
        from odin.bootstrap.first_run import run_first_run_bootstrap
        cfg_path = tmp_path / "local_runtime_config.json"
        run_first_run_bootstrap(config_path=cfg_path)
        written = json.loads(cfg_path.read_text(encoding="utf-8"))
        assert written.get("external_send_default") is False

    def test_no_provider_live_in_default(self, tmp_path):
        from odin.bootstrap.first_run import run_first_run_bootstrap
        cfg_path = tmp_path / "local_runtime_config.json"
        run_first_run_bootstrap(config_path=cfg_path)
        written = json.loads(cfg_path.read_text(encoding="utf-8"))
        assert written.get("provider_live_default") is False

    def test_candidate_only_in_default(self, tmp_path):
        from odin.bootstrap.first_run import run_first_run_bootstrap
        cfg_path = tmp_path / "local_runtime_config.json"
        run_first_run_bootstrap(config_path=cfg_path)
        written = json.loads(cfg_path.read_text(encoding="utf-8"))
        assert written["candidate_only"] is True
        assert written["app_owned_apply"] is True

    def test_result_has_claim_boundary(self, tmp_path):
        from odin.bootstrap.first_run import run_first_run_bootstrap
        cfg_path = tmp_path / "local_runtime_config.json"
        result = run_first_run_bootstrap(config_path=cfg_path)
        assert "claim_boundary" in result
        assert "not_production_readiness_proof" in result["claim_boundary"]

    def test_result_has_known_non_proofs(self, tmp_path):
        from odin.bootstrap.first_run import run_first_run_bootstrap
        cfg_path = tmp_path / "local_runtime_config.json"
        result = run_first_run_bootstrap(config_path=cfg_path)
        assert "known_non_proofs" in result
        assert len(result["known_non_proofs"]) > 0

    def test_first_run_config_fixture_exists(self):
        fixture = ROOT / "examples/bootstrap/first_run_config.valid.json"
        assert fixture.exists()
        data = json.loads(fixture.read_text(encoding="utf-8"))
        assert data["artifact_kind"] == "odin_bootstrap_report"
        assert data["status"] == "created"
        assert data["state_mutated"] is True
        assert data["config_written"]["host"] == "127.0.0.1"
        assert data["config_written"]["public_bind"] is False

    def test_first_run_config_fixture_no_external_app_names(self):
        fixture = ROOT / "examples/bootstrap/first_run_config.valid.json"
        data = json.loads(fixture.read_text(encoding="utf-8"))
        non_proofs = data.get("known_non_proofs", [])
        assert "not_windows_service_tray_installer_proof" in non_proofs
        bundle_str = json.dumps(data).lower()
        assert "windows service" not in bundle_str or "not_windows_service" in bundle_str


# ---------------------------------------------------------------------------
# Repair plan tests
# ---------------------------------------------------------------------------

class TestRepairPlan:
    def _make_doctor_report(self, status: str, failures: list[str], warnings: list[str]) -> dict:
        checks = []
        for f in failures:
            checks.append({"check": f, "status": "fail", "detail": "", "failure_reason": f"fail: {f}"})
        for w in warnings:
            checks.append({"check": w, "status": "warn", "detail": "", "failure_reason": f"warn: {w}"})
        return {
            "artifact_kind": "odin_doctor_report",
            "status": status,
            "checks": checks,
            "failure_count": len(failures),
            "warning_count": len(warnings),
            "failure_reasons": [f"fail: {f}" for f in failures],
        }

    def test_repair_plan_emitted_for_failures(self):
        from odin.bootstrap.repair_plan import build_repair_plan
        report = self._make_doctor_report("fail", ["config_file"], [])
        plan = build_repair_plan(report)
        assert plan["artifact_kind"] == "odin_repair_plan"
        assert plan["plan_item_count"] > 0
        assert plan["status"] == "repairs_suggested"

    def test_repair_plan_does_not_apply_changes(self):
        from odin.bootstrap.repair_plan import build_repair_plan
        report = self._make_doctor_report("fail", ["config_file"], [])
        plan = build_repair_plan(report)
        assert plan["applied"] is False
        assert plan["state_mutated"] is False
        assert plan["plan_only"] is True

    def test_repair_plan_has_apply_gate(self):
        from odin.bootstrap.repair_plan import build_repair_plan
        report = self._make_doctor_report("fail", ["config_file"], [])
        plan = build_repair_plan(report)
        assert plan["apply_gate_required"] is True
        for item in plan["plan_items"]:
            assert item["apply_gate_required"] is True
            assert item["plan_only"] is True

    def test_repair_plan_no_repairs_when_healthy(self):
        from odin.bootstrap.repair_plan import build_repair_plan
        report = self._make_doctor_report("ok", [], [])
        plan = build_repair_plan(report)
        assert plan["status"] == "no_repairs_needed"
        assert plan["plan_item_count"] == 0

    def test_repair_plan_has_claim_boundary(self):
        from odin.bootstrap.repair_plan import build_repair_plan
        report = self._make_doctor_report("ok", [], [])
        plan = build_repair_plan(report)
        assert "claim_boundary" in plan
        assert "plan_only" in plan["claim_boundary"]

    def test_repair_plan_has_known_non_proofs(self):
        from odin.bootstrap.repair_plan import build_repair_plan
        report = self._make_doctor_report("ok", [], [])
        plan = build_repair_plan(report)
        assert "known_non_proofs" in plan
        assert "not_applied" in plan["known_non_proofs"]

    def test_repair_plan_includes_suggestions(self):
        from odin.bootstrap.repair_plan import build_repair_plan
        report = self._make_doctor_report("fail", ["config_file"], [])
        plan = build_repair_plan(report)
        for item in plan["plan_items"]:
            assert "suggested_fix" in item
            assert len(item["suggested_fix"]) > 5

    def test_repair_plan_fixture_exists(self):
        fixture = ROOT / "examples/bootstrap/repair_plan.valid.json"
        assert fixture.exists()
        data = json.loads(fixture.read_text(encoding="utf-8"))
        assert data["artifact_kind"] == "odin_repair_plan"
        assert data["applied"] is False
        assert data["plan_only"] is True
        assert data["apply_gate_required"] is True
        assert data["state_mutated"] is False

    def test_repair_plan_fixture_items_plan_only(self):
        fixture = ROOT / "examples/bootstrap/repair_plan.valid.json"
        data = json.loads(fixture.read_text(encoding="utf-8"))
        for item in data["plan_items"]:
            assert item["plan_only"] is True
            assert item["apply_gate_required"] is True


# ---------------------------------------------------------------------------
# Support bundle tests
# ---------------------------------------------------------------------------

class TestSupportBundle:
    def test_support_bundle_manifest_created(self):
        from odin.doctor.support_bundle import emit_diagnostics_support_bundle
        doctor_report = {"artifact_kind": "odin_doctor_report", "status": "ok", "checks": []}
        bundle = emit_diagnostics_support_bundle(doctor_report=doctor_report)
        assert bundle["artifact_kind"] == "odin_diagnostics_support_bundle"
        assert "bundle_id" in bundle
        assert "doctor_report" in bundle["included_reports"]

    def test_support_bundle_redacts_secrets(self):
        from odin.doctor.support_bundle import emit_diagnostics_support_bundle
        doctor_report = {
            "artifact_kind": "odin_doctor_report",
            "status": "ok",
            "token": "supersecret",
            "api_key": "also_secret",
            "host": "127.0.0.1",
        }
        bundle = emit_diagnostics_support_bundle(doctor_report=doctor_report)
        contents = bundle["contents"]["doctor_report"]
        assert contents["token"] == "[REDACTED]"
        assert contents["api_key"] == "[REDACTED]"
        assert contents["host"] == "127.0.0.1"

    def test_support_bundle_no_external_send(self):
        from odin.doctor.support_bundle import emit_diagnostics_support_bundle
        bundle = emit_diagnostics_support_bundle()
        assert bundle["external_send"] is False

    def test_support_bundle_redaction_flag(self):
        from odin.doctor.support_bundle import emit_diagnostics_support_bundle
        bundle = emit_diagnostics_support_bundle()
        assert bundle["redaction_applied"] is True

    def test_support_bundle_has_claim_boundary(self):
        from odin.doctor.support_bundle import emit_diagnostics_support_bundle
        bundle = emit_diagnostics_support_bundle()
        assert "claim_boundary" in bundle
        assert "local" in bundle["claim_boundary"]
        assert "redacted" in bundle["claim_boundary"]

    def test_support_bundle_has_known_non_proofs(self):
        from odin.doctor.support_bundle import emit_diagnostics_support_bundle
        bundle = emit_diagnostics_support_bundle()
        assert "known_non_proofs" in bundle
        assert len(bundle["known_non_proofs"]) > 0

    def test_support_bundle_does_not_contain_secret_fixture_values(self):
        from odin.doctor.support_bundle import emit_diagnostics_support_bundle
        doctor_report = {
            "status": "ok",
            "token": "MY_SECRET_TOKEN_VALUE",
            "password": "MY_SECRET_PASSWORD",
        }
        bundle = emit_diagnostics_support_bundle(doctor_report=doctor_report)
        bundle_str = json.dumps(bundle)
        assert "MY_SECRET_TOKEN_VALUE" not in bundle_str
        assert "MY_SECRET_PASSWORD" not in bundle_str

    def test_support_bundle_fixture_exists(self):
        fixture = ROOT / "examples/doctor/support_bundle_redacted.valid.json"
        assert fixture.exists()
        data = json.loads(fixture.read_text(encoding="utf-8"))
        assert data["artifact_kind"] == "odin_diagnostics_support_bundle"
        assert data["redaction_applied"] is True
        assert data["external_send"] is False

    def test_support_bundle_fixture_redacted_values(self):
        fixture = ROOT / "examples/doctor/support_bundle_redacted.valid.json"
        data = json.loads(fixture.read_text(encoding="utf-8"))
        bundle_str = json.dumps(data)
        assert "[REDACTED]" in bundle_str

    def test_support_bundle_written_to_disk(self, tmp_path):
        from odin.doctor.support_bundle import emit_diagnostics_support_bundle
        bundle = emit_diagnostics_support_bundle(out_dir=tmp_path)
        assert "written_to" in bundle
        assert Path(bundle["written_to"]).exists()


# ---------------------------------------------------------------------------
# CLI command tests
# ---------------------------------------------------------------------------

class TestCLICommands:
    def _run_cli(self, args: list[str]) -> tuple[int, str]:
        import io
        import sys
        from odin.cli import main
        buf = io.StringIO()
        old_out = sys.stdout
        sys.stdout = buf
        try:
            rc = main(args)
        except SystemExit as e:
            rc = int(e.code) if e.code is not None else 0
        finally:
            sys.stdout = old_out
        return rc, buf.getvalue()

    def test_doctor_command_runs(self):
        rc, out = self._run_cli(["doctor"])
        assert rc == 0
        data = json.loads(out)
        assert "artifact_kind" in data or "status" in data

    def test_doctor_command_has_claim_boundary(self):
        rc, out = self._run_cli(["doctor"])
        assert rc == 0
        data = json.loads(out)
        assert "claim_boundary" in data

    def test_doctor_command_candidate_only(self):
        rc, out = self._run_cli(["doctor"])
        assert rc == 0
        data = json.loads(out)
        assert data.get("candidate_only") is True

    def test_first_run_bootstrap_command_runs(self, tmp_path):
        import io, sys
        from odin.bootstrap import first_run as fr
        orig = fr.CONFIG_PATH
        fr.CONFIG_PATH = tmp_path / "local_runtime_config.json"
        from odin.cli import main
        buf = io.StringIO()
        old_out = sys.stdout
        sys.stdout = buf
        try:
            rc = main(["first-run-bootstrap"])
        except SystemExit as e:
            rc = int(e.code) if e.code is not None else 0
        finally:
            sys.stdout = old_out
            fr.CONFIG_PATH = orig
        out = buf.getvalue()
        assert rc == 0
        data = json.loads(out)
        assert data["status"] in {"created", "skipped"}

    def test_repair_local_runtime_plan_only_runs(self):
        rc, out = self._run_cli(["repair-local-runtime", "--plan-only"])
        assert rc == 0
        data = json.loads(out)
        assert data["artifact_kind"] == "odin_repair_plan"
        assert data["plan_only"] is True
        assert data["applied"] is False

    def test_repair_local_runtime_fails_without_plan_only(self):
        rc, out = self._run_cli(["repair-local-runtime"])
        assert rc == 1
        data = json.loads(out)
        assert data["status"] == "blocked"

    def test_emit_support_bundle_diagnostics_only(self, tmp_path):
        rc, out = self._run_cli(["emit-support-bundle", "--diagnostics-only", "--out", str(tmp_path)])
        assert rc == 0
        data = json.loads(out)
        assert "bundle_id" in data or "support_bundle" in data

    def test_validate_runtime_doctor_bootstrap(self):
        rc, out = self._run_cli(["validate-runtime-doctor-bootstrap"])
        assert rc == 0
        assert "OK" in out or "ok" in out.lower()


# ---------------------------------------------------------------------------
# Validate function tests
# ---------------------------------------------------------------------------

class TestValidateRuntimeDoctorBootstrap:
    def test_validate_function_returns_no_errors(self):
        from odin.cli import validate_runtime_doctor_bootstrap
        errors = validate_runtime_doctor_bootstrap()
        assert errors == [], f"validate_runtime_doctor_bootstrap had errors: {errors}"

    def test_validate_all_includes_runtime_doctor_bootstrap(self):
        from odin.cli import validate_all
        errors = validate_all()
        assert errors == [], f"validate_all had errors: {errors}"


# ---------------------------------------------------------------------------
# Documentation tests
# ---------------------------------------------------------------------------

class TestDocumentation:
    def test_runtime_doctor_bootstrap_doc_exists(self):
        doc = ROOT / "docs/RUNTIME_DOCTOR_BOOTSTRAP_V1.md"
        assert doc.exists(), "docs/RUNTIME_DOCTOR_BOOTSTRAP_V1.md must exist"

    def test_doc_has_not_proven_language(self):
        doc = ROOT / "docs/RUNTIME_DOCTOR_BOOTSTRAP_V1.md"
        text = doc.read_text(encoding="utf-8").lower()
        assert "not production" in text or "not a production" in text or "not_production" in text

    def test_doc_has_plan_only_language(self):
        doc = ROOT / "docs/RUNTIME_DOCTOR_BOOTSTRAP_V1.md"
        text = doc.read_text(encoding="utf-8").lower()
        assert "plan-only" in text or "plan only" in text

    def test_doc_has_no_external_send_language(self):
        doc = ROOT / "docs/RUNTIME_DOCTOR_BOOTSTRAP_V1.md"
        text = doc.read_text(encoding="utf-8").lower()
        assert "no external send" in text or "external send" in text

    def test_doc_has_no_windows_service_claim(self):
        doc = ROOT / "docs/RUNTIME_DOCTOR_BOOTSTRAP_V1.md"
        text = doc.read_text(encoding="utf-8").lower()
        assert "not a windows service" in text or "not windows service" in text or \
               "windows service" not in text or "not_windows_service" in text

    def test_doc_has_no_provider_live_model_claim(self):
        doc = ROOT / "docs/RUNTIME_DOCTOR_BOOTSTRAP_V1.md"
        text = doc.read_text(encoding="utf-8").lower()
        assert "not a provider" in text or "not_provider" in text or \
               "not provider" in text or "provider_live_model" not in text

    def test_doc_has_no_automatic_repair_claim(self):
        doc = ROOT / "docs/RUNTIME_DOCTOR_BOOTSTRAP_V1.md"
        text = doc.read_text(encoding="utf-8").lower()
        assert "no automatic repair" in text or "not automatic" in text or \
               "plan-only" in text

    def test_doc_has_localhost_language(self):
        doc = ROOT / "docs/RUNTIME_DOCTOR_BOOTSTRAP_V1.md"
        text = doc.read_text(encoding="utf-8")
        assert "127.0.0.1" in text or "localhost" in text

    def test_return_report_exists(self):
        report = ROOT / "docs/codex/reports/LRH-PR-04_RETURN_REPORT.md"
        assert report.exists(), "docs/codex/reports/LRH-PR-04_RETURN_REPORT.md must exist"


# ---------------------------------------------------------------------------
# Module structure tests
# ---------------------------------------------------------------------------

class TestModuleStructure:
    def test_doctor_module_importable(self):
        import odin.doctor
        assert hasattr(odin.doctor, "run_doctor")
        assert hasattr(odin.doctor, "emit_diagnostics_support_bundle")

    def test_bootstrap_module_importable(self):
        import odin.bootstrap
        assert hasattr(odin.bootstrap, "run_first_run_bootstrap")
        assert hasattr(odin.bootstrap, "build_repair_plan")

    def test_doctor_claim_boundary_constant(self):
        from odin.doctor.checks import DOCTOR_CLAIM_BOUNDARY
        assert "read_only" in DOCTOR_CLAIM_BOUNDARY or "candidate" in DOCTOR_CLAIM_BOUNDARY

    def test_bootstrap_claim_boundary_constant(self):
        from odin.bootstrap.first_run import BOOTSTRAP_CLAIM_BOUNDARY
        assert "not_production_readiness_proof" in BOOTSTRAP_CLAIM_BOUNDARY

    def test_repair_claim_boundary_constant(self):
        from odin.bootstrap.repair_plan import REPAIR_CLAIM_BOUNDARY
        assert "plan_only" in REPAIR_CLAIM_BOUNDARY

    def test_failure_reason_catalog_non_empty(self):
        from odin.bootstrap.repair_plan import FAILURE_REASON_CATALOG
        assert len(FAILURE_REASON_CATALOG) > 0

    def test_safe_default_config_no_blocked_hosts(self):
        from odin.bootstrap.first_run import SAFE_DEFAULT_CONFIG, BLOCKED_HOSTS
        assert SAFE_DEFAULT_CONFIG["host"] not in BLOCKED_HOSTS
        assert SAFE_DEFAULT_CONFIG.get("public_bind") is False
        assert SAFE_DEFAULT_CONFIG.get("external_send_default") is False
        assert SAFE_DEFAULT_CONFIG.get("provider_live_default") is False
