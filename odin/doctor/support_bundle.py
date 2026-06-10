from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from odin.doctor.redaction import redact_recursive, DOCTOR_REDACTION_CLAIM

SUPPORT_BUNDLE_CLAIM = (
    "support_bundle_diagnostics_only_local_redacted_no_external_send_no_secret_values"
)

BUNDLE_KNOWN_NON_PROOFS = [
    "not_production_security_certification",
    "not_windows_service_tray_installer_proof",
    "not_provider_live_model_proof",
    "not_public_network_api_proof",
    "not_external_send_authority",
    "not_app_state_mutation_authority",
]


def _make_bundle_id() -> str:
    return f"BUNDLE-{uuid.uuid4().hex[:12].upper()}"


def emit_diagnostics_support_bundle(
    doctor_report: dict[str, Any] | None = None,
    bootstrap_report: dict[str, Any] | None = None,
    *,
    out_dir: Path | None = None,
) -> dict[str, Any]:
    bundle_id = _make_bundle_id()

    included_reports: list[str] = []
    redacted_contents: dict[str, Any] = {}

    if doctor_report is not None:
        redacted_contents["doctor_report"] = redact_recursive(doctor_report)
        included_reports.append("doctor_report")

    if bootstrap_report is not None:
        redacted_contents["bootstrap_report"] = redact_recursive(bootstrap_report)
        included_reports.append("bootstrap_report")

    bundle: dict[str, Any] = {
        "artifact_kind": "odin_diagnostics_support_bundle",
        "schema_version": "1.0",
        "bundle_id": bundle_id,
        "included_reports": included_reports,
        "redaction_applied": True,
        "redaction_policy": DOCTOR_REDACTION_CLAIM,
        "created_by": "odin.doctor.support_bundle",
        "candidate_only": True,
        "external_send": False,
        "claim_boundary": SUPPORT_BUNDLE_CLAIM,
        "known_non_proofs": BUNDLE_KNOWN_NON_PROOFS,
        "contents": redacted_contents,
    }

    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{bundle_id}.json"
        out_path.write_text(
            json.dumps(bundle, indent=2, ensure_ascii=False, sort_keys=True),
            encoding="utf-8",
        )
        bundle["written_to"] = str(out_path)

    return bundle
