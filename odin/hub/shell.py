"""Odin Browser Hub Shell — local static asset server scaffold.

Claim boundary: browser_hub_shell_candidate_only_local_only_no_apply_no_external_send

This module provides:
- validate_browser_hub_shell(): deterministic static validator for the shell (LRH-PR-06)
- build_browser_hub_proof_packet(): emit a proof packet for the shell
- validate_hub_runtime_dashboard(): deterministic static validator for the dashboard (LRH-PR-07)
- build_dashboard_proof_packet(): emit a dashboard proof packet
- BROWSER_HUB_SHELL_CLAIM_BOUNDARY: canonical boundary string
- BROWSER_HUB_PROOF_BOUNDARIES: list of not-proven items
- DASHBOARD_CLAIM_BOUNDARY: dashboard-specific boundary string
- DASHBOARD_PROOF_BOUNDARIES: dashboard-specific not-proven list

Runtime serve is scaffold only — no live listen loop is claimed in LRH-PR-06.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[2]
_HUB_DIR = Path(__file__).resolve().parent
_STATIC_DIR = _HUB_DIR / "static"
_API_CLIENT_PATH = _HUB_DIR / "api_client.js"

BROWSER_HUB_SHELL_CLAIM_BOUNDARY = (
    "browser_hub_shell_candidate_only_local_only_no_apply_no_external_send_no_provider_execution"
)

BROWSER_HUB_PROOF_BOUNDARIES = [
    "not_production_readiness_certification",
    "not_hosted_cloud_ui_proof",
    "not_auth_security_certification",
    "not_live_browser_runtime_e2e",
    "not_provider_execution_proof",
    "not_public_network_api_proof",
    "not_app_state_mutation_proof",
    "not_external_send_authority_proof",
    "not_live_model_inference_proof",
    "not_model_quality_proof",
]

# Patterns that must NOT appear as interactive controls
_FORBIDDEN_CONTROL_PATTERNS = [
    "onclick=\"apply(",
    'onclick="apply(',
    "id=\"apply-btn",
    'id="apply-btn',
    "id=\"external-send",
    'id="external-send',
    "function apply()",
    "function externalSend()",
    "function sendExternally()",
    "providerCredential",
    "enablePublicNetwork()",
]

# Patterns that must be present in index.html
_REQUIRED_BOUNDARY_PATTERNS = [
    "Localhost only",
    "Candidate-only",
    "No app apply",
    "No external send",
    "No provider execution",
]

_REQUIRED_NAV_ITEMS = [
    "health",
    "status",
    "proof-gap",
]

_DEFAULT_API_BASE = "http://127.0.0.1:8877"


def validate_browser_hub_shell() -> list[str]:
    """Deterministic static validator for the browser hub shell.

    Returns a list of error strings (empty = ok).
    """
    errors: list[str] = []

    # File existence checks
    required_files = [
        _STATIC_DIR / "index.html",
        _STATIC_DIR / "styles.css",
        _STATIC_DIR / "app.js",
        _API_CLIENT_PATH,
        _HUB_DIR / "shell.py",
        _ROOT / "docs" / "BROWSER_ODIN_HUB_SHELL_V1.md",
        _ROOT / "tests" / "test_lrh_pr_06_browser_hub_shell.py",
    ]
    for p in required_files:
        if not p.exists():
            errors.append(f"browser hub shell file missing: {p.relative_to(_ROOT)}")

    index = _STATIC_DIR / "index.html"
    if index.exists():
        html = index.read_text(encoding="utf-8", errors="ignore")

        # Boundary banner required patterns
        for pattern in _REQUIRED_BOUNDARY_PATTERNS:
            if pattern not in html:
                errors.append(f"index.html: missing required boundary text: {pattern!r}")

        # Navigation items
        for nav in _REQUIRED_NAV_ITEMS:
            if nav not in html.lower():
                errors.append(f"index.html: missing navigation item: {nav!r}")

        # Universal Work Playground placeholder must be present
        if "universal" not in html.lower() and "playground" not in html.lower():
            errors.append("index.html: missing Universal Work Playground placeholder")

        # Forbidden interactive controls
        html_lower = html.lower()
        forbidden_found = [p for p in _FORBIDDEN_CONTROL_PATTERNS if p.lower() in html_lower]
        if forbidden_found:
            errors.append(f"index.html: forbidden interactive controls found: {forbidden_found}")

    api_client = _API_CLIENT_PATH
    if api_client.exists():
        js = api_client.read_text(encoding="utf-8", errors="ignore")

        # Must reference localhost default
        if "127.0.0.1" not in js:
            errors.append("api_client.js: missing 127.0.0.1 default base URL")

        # Must reference /v1 paths
        for path in ["/v1/health", "/v1/status", "/v1/proof-gaps"]:
            if path not in js:
                errors.append(f"api_client.js: missing required path reference: {path!r}")

        # Must NOT have apply or externalSend as callable methods
        if "function apply(" in js or ".prototype.apply = function" in js:
            errors.append("api_client.js: must not have apply() method")
        if "function externalSend(" in js or "prototype.externalSend" in js or "prototype.external_send" in js:
            errors.append("api_client.js: must not have externalSend() method")

        # Must NOT default to non-localhost URL
        if "0.0.0.0" in js:
            errors.append("api_client.js: must not reference 0.0.0.0")

    # Docs boundary checks
    doc = _ROOT / "docs" / "BROWSER_ODIN_HUB_SHELL_V1.md"
    if doc.exists():
        doc_text = doc.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in [
            "not a hosted cloud ui",
            "not a public network api",
            "does not grant app apply",
            "does not send externally",
            "does not execute provider",
            "proof boundaries",
            "not_production_readiness",
        ]:
            if phrase not in doc_text:
                errors.append(f"BROWSER_ODIN_HUB_SHELL_V1.md: missing required phrase: {phrase!r}")

    return errors


DASHBOARD_CLAIM_BOUNDARY = (
    "hub_runtime_dashboard_candidate_only_local_only_no_apply_no_external_send_no_production_health_claim"
)

DASHBOARD_PROOF_BOUNDARIES = [
    "not_production_readiness_certification",
    "not_production_health_certification",
    "not_hosted_cloud_dashboard_proof",
    "not_hidden_diagnostic_upload_proof",
    "not_live_browser_runtime_e2e",
    "not_provider_execution_proof",
    "not_public_network_api_proof",
    "not_app_state_mutation_proof",
    "not_external_send_authority_proof",
    "not_live_model_inference_proof",
    "not_model_quality_proof",
]

_DASHBOARD_REQUIRED_FILES = [
    "odin/hub/static/dashboard.js",
    "odin/hub/static/index.html",
    "docs/HUB_RUNTIME_DASHBOARD_V1.md",
    "tests/test_lrh_pr_07_hub_runtime_dashboard.py",
]

_DASHBOARD_FORBIDDEN_CONTROL_PATTERNS = [
    "function apply(",
    "function externalSend(",
    "function sendExternally(",
    'onclick="apply(',
    "onclick=\"apply(",
    'id="apply-btn',
    "id=\"apply-btn",
    'id="external-send',
    "id=\"external-send",
    "providerCredential",
    "enablePublicNetwork(",
    "hiddenUpload(",
    "remoteUpload(",
    "diagnosticUpload(",
]

_DASHBOARD_REQUIRED_BOUNDARY_PATTERNS = [
    "candidate_only",
    "claim_boundary",
    "no_apply",
    "local",
]

_DASHBOARD_REQUIRED_API_REFS = [
    "/v1/health",
    "/v1/status",
    "/v1/proof-gaps",
]

_DASHBOARD_REQUIRED_SURFACE_IDS = [
    "runtime-status",
    "validation-status",
    "doctor",
    "support-bundle",
    "proof-gap-summary",
    "dashboard-health",
    "missing-capabilities",
]

_DASHBOARD_REQUIRED_DOC_PHRASES = [
    "not a production health certification",
    "not a hosted cloud dashboard",
    "does not upload diagnostics",
    "does not grant app apply",
    "does not send externally",
    "does not execute provider",
    "proof boundaries",
    "not_production_readiness",
]


def validate_hub_runtime_dashboard() -> list[str]:
    """Deterministic static validator for the Hub Runtime Dashboard (LRH-PR-07).

    Returns a list of error strings (empty = ok).
    """
    errors: list[str] = []

    for rel in _DASHBOARD_REQUIRED_FILES:
        p = _ROOT / rel
        if not p.exists():
            errors.append(f"dashboard required file missing: {rel}")

    dashboard_js = _STATIC_DIR / "dashboard.js"
    if dashboard_js.exists():
        js = dashboard_js.read_text(encoding="utf-8", errors="ignore")
        for api_ref in _DASHBOARD_REQUIRED_API_REFS:
            if api_ref not in js:
                errors.append(f"dashboard.js: missing required API reference: {api_ref!r}")
        for pattern in ["candidate_only", "claim_boundary"]:
            if pattern not in js:
                errors.append(f"dashboard.js: missing required boundary token: {pattern!r}")
        js_lower = js.lower()
        forbidden_found = [p for p in _DASHBOARD_FORBIDDEN_CONTROL_PATTERNS if p.lower() in js_lower]
        if forbidden_found:
            errors.append(f"dashboard.js: forbidden interactive controls found: {forbidden_found}")
        if "127.0.0.1" not in js and "ODIN_API_BASE" not in js:
            errors.append("dashboard.js: missing localhost default reference")
        if "function apply(" in js or "prototype.apply = function" in js:
            errors.append("dashboard.js: must not have apply() function definition")
        if "function externalSend(" in js or "prototype.externalSend" in js:
            errors.append("dashboard.js: must not have externalSend() function definition")

    index = _STATIC_DIR / "index.html"
    if index.exists():
        html = index.read_text(encoding="utf-8", errors="ignore")
        if "dashboard.js" not in html:
            errors.append("index.html: must load dashboard.js")
        for surface_id in _DASHBOARD_REQUIRED_SURFACE_IDS:
            if surface_id not in html:
                errors.append(f"index.html: missing required dashboard surface id: {surface_id!r}")
        html_lower = html.lower()
        forbidden_found = [p for p in _DASHBOARD_FORBIDDEN_CONTROL_PATTERNS if p.lower() in html_lower]
        if forbidden_found:
            errors.append(f"index.html: forbidden interactive controls found in dashboard section: {forbidden_found}")
        if "support-bundle" not in html.lower():
            errors.append("index.html: missing support-bundle surface")
        for phrase in ["local-only", "diagnostics-only", "no hidden upload"]:
            if phrase.lower() not in html.lower():
                errors.append(f"index.html: support bundle surface missing phrase: {phrase!r}")

    doc = _ROOT / "docs" / "HUB_RUNTIME_DASHBOARD_V1.md"
    if doc.exists():
        doc_text = doc.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in _DASHBOARD_REQUIRED_DOC_PHRASES:
            if phrase.lower() not in doc_text:
                errors.append(f"HUB_RUNTIME_DASHBOARD_V1.md: missing required phrase: {phrase!r}")

    return errors


def build_dashboard_proof_packet() -> dict[str, Any]:
    """Emit a bounded proof packet for the Hub Runtime Dashboard (LRH-PR-07)."""
    dashboard_errors = validate_hub_runtime_dashboard()
    all_ok = not bool(dashboard_errors)

    return {
        "artifact_kind": "hub_runtime_dashboard_proof_packet",
        "candidate_only": True,
        "local_only": True,
        "dashboard_only": True,
        "status": "ok" if all_ok else "partial",
        "validation_errors": dashboard_errors,
        "proven": [
            "dashboard_static_files_exist",
            "dashboard_references_v1_health",
            "dashboard_references_v1_status",
            "dashboard_references_v1_proof_gaps",
            "no_apply_controls",
            "no_external_send_controls",
            "support_bundle_surface_is_local_only",
            "no_hidden_diagnostic_upload_controls",
            "runtime_status_surface_present",
            "validation_status_surface_present",
            "doctor_surface_present",
            "proof_gap_summary_surface_present",
            "missing_capabilities_surface_present",
        ] if all_ok else [],
        "not_proven": [
            "production_readiness",
            "production_health_certification",
            "hosted_cloud_dashboard",
            "live_browser_runtime_e2e",
            "provider_execution",
            "app_state_mutation",
            "external_send_authority",
            "hidden_diagnostic_upload_absence_beyond_static_scan",
            "live_model_inference",
            "model_quality",
        ],
        "proof_boundaries": DASHBOARD_PROOF_BOUNDARIES,
        "claim_boundary": DASHBOARD_CLAIM_BOUNDARY,
    }


CANDIDATE_STORE_VIEWER_CLAIM_BOUNDARY = (
    "candidate_store_viewer_candidate_only_local_only_no_apply_no_external_send_no_store_mutation_no_raw_payload"
)

CANDIDATE_STORE_VIEWER_PROOF_BOUNDARIES = [
    "not_production_readiness_certification",
    "not_candidate_application_proof",
    "not_candidate_as_truth_proof",
    "not_store_mutation_proof",
    "not_raw_sensitive_payload_safety_certification",
    "not_live_browser_runtime_e2e",
    "not_provider_execution_proof",
    "not_public_network_api_proof",
    "not_app_state_mutation_proof",
    "not_external_send_authority_proof",
    "not_live_model_inference_proof",
    "not_model_quality_proof",
    "not_full_session_list_backend",
    "not_full_candidate_backend_coverage",
    "not_full_store_backend_coverage",
]

_CSV_REQUIRED_FILES = [
    "odin/hub/static/candidate_store_viewer.js",
    "odin/hub/static/index.html",
    "docs/HUB_CANDIDATE_STORE_VIEWER_V1.md",
    "tests/test_lrh_pr_08_candidate_store_viewer.py",
]

_CSV_REQUIRED_JS_API_REFS = [
    "/v1/candidates",
    "/v1/sessions",
    "/v1/proof-gaps",
]

_CSV_REQUIRED_JS_BOUNDARY_TOKENS = [
    "candidate_only",
    "claim_boundary",
    "not_applied_truth",
    "no_apply",
]

_CSV_FORBIDDEN_CONTROL_PATTERNS = [
    "function apply(",
    "function applyCandidate(",
    "function externalSend(",
    "function sendExternally(",
    "function storeWrite(",
    "function storeDelete(",
    "function rawPayloadReveal(",
    "function unsafePayloadToggle(",
    'onclick="apply(',
    "onclick=\"apply(",
    'id="apply-btn',
    "id=\"apply-btn",
    'id="external-send',
    "id=\"external-send",
    "providerCredential",
    "enablePublicNetwork(",
    "hiddenUpload(",
    "remoteUpload(",
]

_CSV_REQUIRED_SURFACE_IDS = [
    "csv-sessions-content",
    "csv-candidate-content",
    "csv-store-content",
    "csv-proof-gaps-content",
]

_CSV_REQUIRED_BOUNDARY_PHRASES = [
    "Candidate-only",
    "not applied truth",
    "app-owned apply",
    "No app apply",
    "No external send",
    "No store mutation",
    "No raw sensitive payload",
]

_CSV_REQUIRED_DOC_PHRASES = [
    "does not apply candidate artifacts",
    "does not show candidates as applied truth",
    "does not mutate the runtime store",
    "does not send externally",
    "does not display raw sensitive payloads by default",
    "does not close proof gaps by displaying them",
    "does not prove production readiness",
    "proof boundaries",
]


def validate_candidate_store_viewer() -> list[str]:
    """Deterministic static validator for the Candidate Store Viewer (LRH-PR-08).

    Returns a list of error strings (empty = ok).
    """
    errors: list[str] = []

    for rel in _CSV_REQUIRED_FILES:
        p = _ROOT / rel
        if not p.exists():
            errors.append(f"candidate store viewer required file missing: {rel}")

    csv_js = _STATIC_DIR / "candidate_store_viewer.js"
    if csv_js.exists():
        js = csv_js.read_text(encoding="utf-8", errors="ignore")

        for api_ref in _CSV_REQUIRED_JS_API_REFS:
            if api_ref not in js:
                errors.append(f"candidate_store_viewer.js: missing required API reference: {api_ref!r}")

        for token in _CSV_REQUIRED_JS_BOUNDARY_TOKENS:
            if token not in js:
                errors.append(f"candidate_store_viewer.js: missing required boundary token: {token!r}")

        js_lower = js.lower()
        forbidden_found = [p for p in _CSV_FORBIDDEN_CONTROL_PATTERNS if p.lower() in js_lower]
        if forbidden_found:
            errors.append(f"candidate_store_viewer.js: forbidden interactive controls found: {forbidden_found}")

        if "127.0.0.1" not in js and "ODIN_API_BASE" not in js:
            errors.append("candidate_store_viewer.js: missing localhost default reference")

        if "function apply(" in js:
            errors.append("candidate_store_viewer.js: must not define apply() function")
        if "function externalSend(" in js:
            errors.append("candidate_store_viewer.js: must not define externalSend() function")

    index = _STATIC_DIR / "index.html"
    if index.exists():
        html = index.read_text(encoding="utf-8", errors="ignore")

        if "candidate_store_viewer.js" not in html:
            errors.append("index.html: must load candidate_store_viewer.js")

        for surface_id in _CSV_REQUIRED_SURFACE_IDS:
            if surface_id not in html:
                errors.append(f"index.html: missing required candidate store viewer surface id: {surface_id!r}")

        html_lower = html.lower()
        for phrase in _CSV_REQUIRED_BOUNDARY_PHRASES:
            if phrase.lower() not in html_lower:
                errors.append(f"index.html: missing required boundary phrase: {phrase!r}")

        forbidden_found = [p for p in _CSV_FORBIDDEN_CONTROL_PATTERNS if p.lower() in html_lower]
        if forbidden_found:
            errors.append(f"index.html: forbidden interactive controls found in candidate viewer: {forbidden_found}")

    doc = _ROOT / "docs" / "HUB_CANDIDATE_STORE_VIEWER_V1.md"
    if doc.exists():
        doc_text = doc.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in _CSV_REQUIRED_DOC_PHRASES:
            if phrase.lower() not in doc_text:
                errors.append(f"HUB_CANDIDATE_STORE_VIEWER_V1.md: missing required phrase: {phrase!r}")

    return errors


def build_candidate_store_viewer_proof_packet() -> dict[str, Any]:
    """Emit a bounded proof packet for the Candidate Store Viewer (LRH-PR-08)."""
    csv_errors = validate_candidate_store_viewer()
    all_ok = not bool(csv_errors)

    return {
        "artifact_kind": "hub_candidate_store_viewer_proof_packet",
        "candidate_only": True,
        "local_only": True,
        "read_only": True,
        "viewer_only": True,
        "status": "ok" if all_ok else "partial",
        "validation_errors": csv_errors,
        "proven": [
            "candidate_store_viewer_static_files_exist",
            "candidate_viewer_references_v1_candidates",
            "candidate_viewer_references_v1_sessions",
            "proof_gap_viewer_references_v1_proof_gaps",
            "candidate_boundary_banner_present",
            "not_applied_truth_warning_present",
            "no_apply_controls",
            "no_external_send_controls",
            "no_store_mutation_controls",
            "raw_sensitive_payload_not_displayed_by_default",
        ] if all_ok else [],
        "not_proven": [
            "production_readiness",
            "live_browser_runtime_e2e",
            "full_session_list_backend",
            "full_candidate_backend_coverage",
            "full_store_backend_coverage",
            "raw_sensitive_payload_safety_certification",
            "candidate_application",
            "external_send_authority",
            "store_mutation",
            "live_model_inference",
            "model_quality",
        ],
        "proof_boundaries": CANDIDATE_STORE_VIEWER_PROOF_BOUNDARIES,
        "claim_boundary": CANDIDATE_STORE_VIEWER_CLAIM_BOUNDARY,
    }


TRACE_VIEWER_CLAIM_BOUNDARY = (
    "trace_viewer_candidate_only_local_only_no_event_mutation_no_public_bus_no_raw_payload"
)

TRACE_VIEWER_PROOF_BOUNDARIES = [
    "not_production_readiness_certification",
    "not_security_certification",
    "not_event_mutation_proof",
    "not_bus_publish_replay_delete_ack_proof",
    "not_public_bus_exposure_proof",
    "not_lan_wan_trace_endpoint_proof",
    "not_worklet_execution_proof",
    "not_work_atom_mutation_proof",
    "not_raw_sensitive_payload_safety_certification",
    "not_live_browser_runtime_e2e",
    "not_provider_execution_proof",
    "not_public_network_api_proof",
    "not_app_state_mutation_proof",
    "not_external_send_authority_proof",
    "not_live_model_inference_proof",
    "not_model_quality_proof",
    "not_full_bus_backend_coverage",
    "not_full_worklet_backend_coverage",
    "not_full_work_atom_backend_coverage",
]

_TV_REQUIRED_FILES = [
    "odin/hub/static/trace_viewer.js",
    "odin/hub/static/index.html",
    "docs/HUB_TRACE_VIEWER_V1.md",
    "tests/test_lrh_pr_09_trace_viewer.py",
]

_TV_REQUIRED_JS_API_REFS = [
    "/v1/events",
    "/v1/proof-gaps",
]

_TV_REQUIRED_JS_HEALTH_REFS = [
    "/v1/health",
    "/v1/status",
]

_TV_REQUIRED_JS_BOUNDARY_TOKENS = [
    "candidate_only",
    "claim_boundary",
    "local_only",
    "read_only",
    "no_event_mutation",
    "no_raw_payload",
    "metadata_first",
]

_TV_FORBIDDEN_CONTROL_PATTERNS = [
    "function publishEvent(",
    "function replayEvent(",
    "function deleteEvent(",
    "function ackEvent(",
    "function mutateEvent(",
    "function executeWorklet(",
    "function retryWorklet(",
    "function mutateAtom(",
    "function deleteAtom(",
    "function applyTrace(",
    "function externalSend(",
    "function uploadTrace(",
    "function hiddenUpload(",
    "function rawPayloadReveal(",
    "function unsafePayloadToggle(",
    'id="public-bus-toggle',
    'id="network-enable',
    'id="raw-payload-reveal',
    "providerCredential",
    "enablePublicNetwork(",
    "enablePublicBus(",
]

_TV_REQUIRED_SURFACE_IDS = [
    "tv-bus-events-content",
    "tv-worklet-trace-content",
    "tv-work-atom-trace-content",
    "tv-runtime-digest-content",
    "tv-proof-gaps-content",
]

_TV_REQUIRED_BOUNDARY_PHRASES = [
    "No event mutation",
    "No bus publish",
    "No worklet execution",
    "No atom mutation",
    "No raw sensitive payload",
    "local-only",
    "read-only",
    "not-certification",
]

_TV_REQUIRED_DOC_PHRASES = [
    "this does not mutate bus events",
    "this does not publish, replay, delete or acknowledge bus events",
    "this does not execute worklets",
    "this does not mutate work atoms",
    "this does not expose a public bus",
    "this does not add lan/wan trace endpoints by default",
    "this does not display raw sensitive payloads by default",
    "this does not prove production readiness",
    "this does not prove security certification",
    "proof boundaries",
    "not_production_readiness_certification",
]


def validate_trace_viewer() -> list[str]:
    """Deterministic static validator for the Trace Viewer (LRH-PR-09).

    Returns a list of error strings (empty = ok).
    """
    errors: list[str] = []

    for rel in _TV_REQUIRED_FILES:
        p = _ROOT / rel
        if not p.exists():
            errors.append(f"trace viewer required file missing: {rel}")

    tv_js = _STATIC_DIR / "trace_viewer.js"
    if tv_js.exists():
        js = tv_js.read_text(encoding="utf-8", errors="ignore")

        for api_ref in _TV_REQUIRED_JS_API_REFS:
            if api_ref not in js:
                errors.append(f"trace_viewer.js: missing required API reference: {api_ref!r}")

        for health_ref in _TV_REQUIRED_JS_HEALTH_REFS:
            if health_ref not in js:
                errors.append(f"trace_viewer.js: missing required health/status reference: {health_ref!r}")

        for token in _TV_REQUIRED_JS_BOUNDARY_TOKENS:
            if token not in js:
                errors.append(f"trace_viewer.js: missing required boundary token: {token!r}")

        js_lower = js.lower()
        forbidden_found = [p for p in _TV_FORBIDDEN_CONTROL_PATTERNS if p.lower() in js_lower]
        if forbidden_found:
            errors.append(f"trace_viewer.js: forbidden interactive controls found: {forbidden_found}")

        if "127.0.0.1" not in js and "ODIN_API_BASE" not in js:
            errors.append("trace_viewer.js: missing localhost default reference")

        if "function publishEvent(" in js:
            errors.append("trace_viewer.js: must not define publishEvent() function")
        if "function externalSend(" in js:
            errors.append("trace_viewer.js: must not define externalSend() function")
        if "function executeWorklet(" in js:
            errors.append("trace_viewer.js: must not define executeWorklet() function")
        if "function mutateAtom(" in js:
            errors.append("trace_viewer.js: must not define mutateAtom() function")

    index = _STATIC_DIR / "index.html"
    if index.exists():
        html = index.read_text(encoding="utf-8", errors="ignore")

        if "trace_viewer.js" not in html:
            errors.append("index.html: must load trace_viewer.js")

        for surface_id in _TV_REQUIRED_SURFACE_IDS:
            if surface_id not in html:
                errors.append(f"index.html: missing required trace viewer surface id: {surface_id!r}")

        html_lower = html.lower()
        for phrase in _TV_REQUIRED_BOUNDARY_PHRASES:
            if phrase.lower() not in html_lower:
                errors.append(f"index.html: missing required trace viewer boundary phrase: {phrase!r}")

        forbidden_found = [p for p in _TV_FORBIDDEN_CONTROL_PATTERNS if p.lower() in html_lower]
        if forbidden_found:
            errors.append(f"index.html: forbidden interactive controls found in trace viewer: {forbidden_found}")

        if "not-certification" not in html.lower() and "not a production" not in html.lower():
            errors.append("index.html: runtime digest surface missing not-certification boundary phrase")

    doc = _ROOT / "docs" / "HUB_TRACE_VIEWER_V1.md"
    if doc.exists():
        doc_text = doc.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in _TV_REQUIRED_DOC_PHRASES:
            if phrase.lower() not in doc_text:
                errors.append(f"HUB_TRACE_VIEWER_V1.md: missing required phrase: {phrase!r}")

    return errors


def build_trace_viewer_proof_packet() -> dict[str, Any]:
    """Emit a bounded proof packet for the Trace Viewer (LRH-PR-09)."""
    tv_errors = validate_trace_viewer()
    all_ok = not bool(tv_errors)

    return {
        "artifact_kind": "hub_trace_viewer_proof_packet",
        "candidate_only": True,
        "local_only": True,
        "read_only": True,
        "trace_viewer_only": True,
        "status": "ok" if all_ok else "partial",
        "validation_errors": tv_errors,
        "proven": [
            "trace_viewer_static_files_exist",
            "trace_viewer_references_v1_events",
            "trace_viewer_references_v1_proof_gaps",
            "trace_viewer_references_v1_status",
            "trace_viewer_references_v1_health",
            "bus_event_timeline_surface_present",
            "worklet_trace_surface_present",
            "work_atom_trace_surface_present",
            "runtime_digest_surface_present",
            "local_only_trace_filters_present",
            "metadata_first_display_enforced",
            "redacted_payload_policy_present",
            "no_event_mutation_controls",
            "no_worklet_execution_controls",
            "no_atom_mutation_controls",
            "no_external_send_controls",
            "no_public_bus_controls",
            "raw_sensitive_payload_not_displayed_by_default",
        ] if all_ok else [],
        "not_proven": [
            "production_readiness",
            "security_certification",
            "live_browser_runtime_e2e",
            "full_bus_backend_coverage",
            "full_worklet_backend_coverage",
            "full_work_atom_backend_coverage",
            "raw_sensitive_payload_safety_certification",
            "event_mutation_authority",
            "worklet_execution_authority",
            "atom_mutation_authority",
            "public_bus_exposure",
            "external_send_authority",
            "live_model_inference",
            "model_quality",
            "app_state_mutation",
        ],
        "proof_boundaries": TRACE_VIEWER_PROOF_BOUNDARIES,
        "claim_boundary": TRACE_VIEWER_CLAIM_BOUNDARY,
    }


PROVIDER_WORKER_INSPECTOR_CLAIM_BOUNDARY = (
    "provider_worker_inspector_candidate_only_local_only_no_provider_execution_no_credentials_no_worker_mutation"
)

PROVIDER_WORKER_INSPECTOR_PROOF_BOUNDARIES = [
    "not_production_readiness_certification",
    "not_security_certification",
    "not_live_model_inference_proof",
    "not_model_quality_proof",
    "not_provider_authority_proof",
    "not_provider_execution_proof",
    "not_provider_credential_storage_proof",
    "not_worker_mutation_proof",
    "not_worker_permission_mutation_proof",
    "not_route_mutation_proof",
    "not_redaction_safety_certification",
    "not_redaction_bypass_proof",
    "not_full_pre_llm_runtime_coverage",
    "not_public_network_api_proof",
    "not_app_state_mutation_proof",
    "not_external_send_authority_proof",
]

_PWI_REQUIRED_FILES = [
    "odin/hub/static/provider_worker_inspector.js",
    "odin/hub/static/index.html",
    "docs/PROVIDER_WORKER_INSPECTOR_V1.md",
    "tests/test_lrh_pr_10_provider_worker_inspector.py",
]

_PWI_REQUIRED_JS_API_REFS = [
    "/v1/providers",
    "/v1/proof-gaps",
]

_PWI_REQUIRED_JS_HEALTH_REFS = [
    "/v1/status",
]

_PWI_REQUIRED_JS_BOUNDARY_TOKENS = [
    "candidate_only",
    "claim_boundary",
    "local_only",
    "read_only",
    "no_provider_execution",
    "no_credentials",
    "no_worker_mutation",
    "metadata_first",
    "provider_as_worker",
]

_PWI_FORBIDDEN_CONTROL_PATTERNS = [
    "function runProvider(",
    "function executeProvider(",
    "function callModel(",
    "function runModel(",
    "function testInference(",
    "function saveCredential(",
    "function setApiKey(",
    "function enableProvider(",
    "function disableProvider(",
    "function mutateWorker(",
    "function editPermission(",
    "function changeRoute(",
    "function mutateRoute(",
    "function bypassRedaction(",
    "function rawPayloadReveal(",
    "function externalSend(",
    "function uploadDiagnostics(",
    "function hiddenUpload(",
    'id="provider-credential',
    'id="api-key',
    'type="password"',
    "providerCredential",
    "apiKey",
    "enablePublicNetwork(",
]

_PWI_REQUIRED_SURFACE_IDS = [
    "pwi-provider-cards-content",
    "pwi-worker-permission-content",
    "pwi-pre-llm-route-content",
    "pwi-model-avoidance-content",
    "pwi-redaction-status-content",
    "pwi-disabled-by-default-content",
    "pwi-proof-gaps-content",
]

_PWI_REQUIRED_BOUNDARY_PHRASES = [
    "Provider is worker, not authority",
    "No live inference without receipt",
    "No credentials by default",
    "Disabled by default",
    "No provider execution",
    "No worker mutation",
    "No route mutation",
    "Redaction status is not safety certification",
]

_PWI_REQUIRED_DOC_PHRASES = [
    "this does not execute providers",
    "this does not call live models",
    "this does not store or request provider credentials",
    "this does not treat providers as authority",
    "this does not mutate worker permissions",
    "this does not mutate routing policy",
    "this does not bypass redaction",
    "this does not prove model quality",
    "this does not prove production readiness",
    "this does not prove security certification",
    "proof boundaries",
    "not_production_readiness_certification",
]


def validate_provider_worker_inspector() -> list[str]:
    """Deterministic static validator for the Provider/Worker Inspector (LRH-PR-10).

    Returns a list of error strings (empty = ok).
    """
    errors: list[str] = []

    for rel in _PWI_REQUIRED_FILES:
        p = _ROOT / rel
        if not p.exists():
            errors.append(f"provider worker inspector required file missing: {rel}")

    pwi_js = _STATIC_DIR / "provider_worker_inspector.js"
    if pwi_js.exists():
        js = pwi_js.read_text(encoding="utf-8", errors="ignore")

        for api_ref in _PWI_REQUIRED_JS_API_REFS:
            if api_ref not in js:
                errors.append(f"provider_worker_inspector.js: missing required API reference: {api_ref!r}")

        for health_ref in _PWI_REQUIRED_JS_HEALTH_REFS:
            if health_ref not in js:
                errors.append(f"provider_worker_inspector.js: missing required status reference: {health_ref!r}")

        for token in _PWI_REQUIRED_JS_BOUNDARY_TOKENS:
            if token not in js:
                errors.append(f"provider_worker_inspector.js: missing required boundary token: {token!r}")

        js_lower = js.lower()
        forbidden_found = [p for p in _PWI_FORBIDDEN_CONTROL_PATTERNS if p.lower() in js_lower]
        if forbidden_found:
            errors.append(f"provider_worker_inspector.js: forbidden interactive controls found: {forbidden_found}")

        if "127.0.0.1" not in js and "ODIN_API_BASE" not in js:
            errors.append("provider_worker_inspector.js: missing localhost default reference")

        if "function runProvider(" in js:
            errors.append("provider_worker_inspector.js: must not define runProvider() function")
        if "function executeProvider(" in js:
            errors.append("provider_worker_inspector.js: must not define executeProvider() function")
        if "function callModel(" in js:
            errors.append("provider_worker_inspector.js: must not define callModel() function")
        if "function externalSend(" in js:
            errors.append("provider_worker_inspector.js: must not define externalSend() function")

    index = _STATIC_DIR / "index.html"
    if index.exists():
        html = index.read_text(encoding="utf-8", errors="ignore")

        if "provider_worker_inspector.js" not in html:
            errors.append("index.html: must load provider_worker_inspector.js")

        for surface_id in _PWI_REQUIRED_SURFACE_IDS:
            if surface_id not in html:
                errors.append(f"index.html: missing required provider worker inspector surface id: {surface_id!r}")

        html_lower = html.lower()
        for phrase in _PWI_REQUIRED_BOUNDARY_PHRASES:
            if phrase.lower() not in html_lower:
                errors.append(f"index.html: missing required provider worker inspector boundary phrase: {phrase!r}")

        forbidden_found = [p for p in _PWI_FORBIDDEN_CONTROL_PATTERNS if p.lower() in html_lower]
        if forbidden_found:
            errors.append(f"index.html: forbidden interactive controls found in provider worker inspector: {forbidden_found}")

        if "redaction status is not safety certification" not in html.lower() and "not-certification" not in html.lower():
            errors.append("index.html: provider worker inspector missing redaction status not-certification phrase")

    doc = _ROOT / "docs" / "PROVIDER_WORKER_INSPECTOR_V1.md"
    if doc.exists():
        doc_text = doc.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in _PWI_REQUIRED_DOC_PHRASES:
            if phrase.lower() not in doc_text:
                errors.append(f"PROVIDER_WORKER_INSPECTOR_V1.md: missing required phrase: {phrase!r}")

    return errors


def build_provider_worker_inspector_proof_packet() -> dict[str, Any]:
    """Emit a bounded proof packet for the Provider/Worker Inspector (LRH-PR-10)."""
    pwi_errors = validate_provider_worker_inspector()
    all_ok = not bool(pwi_errors)

    return {
        "artifact_kind": "hub_provider_worker_inspector_proof_packet",
        "candidate_only": True,
        "local_only": True,
        "read_only": True,
        "provider_worker_inspector_only": True,
        "status": "ok" if all_ok else "partial",
        "validation_errors": pwi_errors,
        "proven": [
            "provider_worker_inspector_static_files_exist",
            "provider_viewer_references_v1_providers",
            "provider_cards_surface_present",
            "worker_permission_cards_surface_present",
            "pre_llm_route_decision_surface_present",
            "model_work_avoidance_surface_present",
            "redaction_status_surface_present",
            "disabled_by_default_surface_present",
            "no_provider_execution_controls",
            "no_live_model_call_controls",
            "no_credential_controls",
            "no_worker_mutation_controls",
            "no_route_mutation_controls",
            "no_redaction_bypass_controls",
            "no_external_send_controls",
        ] if all_ok else [],
        "not_proven": [
            "production_readiness",
            "security_certification",
            "live_model_inference",
            "model_quality",
            "provider_authority",
            "provider_credential_storage",
            "full_pre_llm_runtime_coverage",
            "full_redaction_safety_certification",
            "worker_mutation_authority",
            "external_send_authority",
        ],
        "proof_boundaries": PROVIDER_WORKER_INSPECTOR_PROOF_BOUNDARIES,
        "claim_boundary": PROVIDER_WORKER_INSPECTOR_CLAIM_BOUNDARY,
    }


UNIVERSAL_WORK_PLAYGROUND_CLAIM_BOUNDARY = (
    "uwp_candidate_only_local_only_no_apply_no_external_send_no_shell_no_provider_no_credentials"
)

UNIVERSAL_WORK_PLAYGROUND_PROOF_BOUNDARIES = [
    "not_production_readiness_certification",
    "not_security_certification",
    "not_live_model_inference_proof",
    "not_model_quality_proof",
    "not_app_apply_proof",
    "not_app_state_mutation_proof",
    "not_external_send_authority_proof",
    "not_arbitrary_shell_execution_proof",
    "not_provider_execution_proof",
    "not_credential_handling_proof",
    "not_full_live_universal_work_backend_coverage",
    "not_external_app_bridge_proof",
    "candidate_result_not_applied_truth",
]

_UWP_REQUIRED_FILES = [
    "odin/hub/static/universal_work_playground.js",
    "odin/hub/static/index.html",
    "docs/UNIVERSAL_WORK_PLAYGROUND_V1.md",
    "tests/test_lrh_pr_11_universal_work_playground.py",
    "examples/universal_work_playground/safe_demo_work_packet.valid.json",
    "examples/universal_work_playground/safe_demo_candidate_result.valid.json",
]

_UWP_REQUIRED_JS_API_REFS = [
    "/v1/universal-work",
    "/v1/proof-gaps",
]

_UWP_REQUIRED_JS_BOUNDARY_TOKENS = [
    "candidate_only",
    "claim_boundary",
    "local_only",
    "read_only",
    "no_app_apply",
    "no_external_send",
    "no_arbitrary_shell_execution",
    "no_provider_execution",
    "no_credentials",
    "safe_demo_only",
    "playground_only",
    "not_applied_truth",
    "proof_boundaries",
    "known_non_proofs",
    "metadata_first",
    "provider_as_worker_not_authority",
    "disabled_by_default",
]

_UWP_FORBIDDEN_CONTROL_PATTERNS = [
    "function applyCandidate(",
    "function externalSend(",
    "function sendExternally(",
    "function uploadResult(",
    "function publishResult(",
    "function runShell(",
    "function executeShell(",
    "function runCommand(",
    "function executeCommand(",
    "function runScript(",
    "function executeScript(",
    "function runProvider(",
    "function executeProvider(",
    "function callModel(",
    "function runModel(",
    "function testInference(",
    "function saveCredential(",
    "function setApiKey(",
    'id="apply-btn',
    'id="external-send',
    'name="shell_command"',
    'name="command"',
    'name="script"',
    'name="exec"',
    'name="provider_credential"',
    'name="api_key"',
    'name="token"',
    'name="secret"',
    'name="remote_url"',
    'name="callback_url"',
    'name="webhook_url"',
    'name="app_apply_target"',
    'type="password"',
    "providerCredential",
    "apiKey",
    "enablePublicNetwork(",
]

_UWP_REQUIRED_SURFACE_IDS = [
    "uwp-work-form-content",
    "uwp-candidate-result-content",
    "uwp-proof-boundary-content",
    "uwp-validation-status-content",
    "uwp-provider-worker-context-content",
]

_UWP_REQUIRED_BOUNDARY_PHRASES = [
    "Candidate-only",
    "not applied truth",
    "No app apply",
    "No external send",
    "No arbitrary shell execution",
    "No provider execution",
    "No credentials by default",
    "safe demo only",
    "candidate result is not applied truth",
]

_UWP_REQUIRED_DOC_PHRASES = [
    "this does not apply candidate artifacts",
    "this does not mutate app state",
    "this does not send externally",
    "this does not execute arbitrary shell commands",
    "this does not execute providers",
    "this does not call live models",
    "this does not store or request credentials",
    "this does not prove model quality",
    "this does not prove production readiness",
    "this does not prove security certification",
    "proof boundaries",
    "not_production_readiness_certification",
    "candidate result is not applied truth",
]


def validate_universal_work_playground() -> list[str]:
    """Deterministic static validator for the Universal Work Playground (LRH-PR-11).

    Returns a list of error strings (empty = ok).
    """
    errors: list[str] = []

    for rel in _UWP_REQUIRED_FILES:
        p = _ROOT / rel
        if not p.exists():
            errors.append(f"universal work playground required file missing: {rel}")

    uwp_js = _STATIC_DIR / "universal_work_playground.js"
    if uwp_js.exists():
        js = uwp_js.read_text(encoding="utf-8", errors="ignore")

        for api_ref in _UWP_REQUIRED_JS_API_REFS:
            if api_ref not in js:
                errors.append(f"universal_work_playground.js: missing required API reference: {api_ref!r}")

        for token in _UWP_REQUIRED_JS_BOUNDARY_TOKENS:
            if token not in js:
                errors.append(f"universal_work_playground.js: missing required boundary token: {token!r}")

        js_lower = js.lower()
        forbidden_found = [p for p in _UWP_FORBIDDEN_CONTROL_PATTERNS if p.lower() in js_lower]
        if forbidden_found:
            errors.append(f"universal_work_playground.js: forbidden interactive controls found: {forbidden_found}")

        if "127.0.0.1" not in js and "ODIN_API_BASE" not in js:
            errors.append("universal_work_playground.js: missing localhost default reference")

        for fn_name in ["function applyCandidate(", "function externalSend(", "function runShell(",
                         "function executeShell(", "function runProvider(", "function callModel("]:
            if fn_name in js:
                errors.append(f"universal_work_playground.js: must not define forbidden function: {fn_name!r}")

    index = _STATIC_DIR / "index.html"
    if index.exists():
        html = index.read_text(encoding="utf-8", errors="ignore")

        if "universal_work_playground.js" not in html:
            errors.append("index.html: must load universal_work_playground.js")

        for surface_id in _UWP_REQUIRED_SURFACE_IDS:
            if surface_id not in html:
                errors.append(f"index.html: missing required UWP surface id: {surface_id!r}")

        html_lower = html.lower()
        for phrase in _UWP_REQUIRED_BOUNDARY_PHRASES:
            if phrase.lower() not in html_lower:
                errors.append(f"index.html: missing required UWP boundary phrase: {phrase!r}")

        forbidden_found = [p for p in _UWP_FORBIDDEN_CONTROL_PATTERNS if p.lower() in html_lower]
        if forbidden_found:
            errors.append(f"index.html: forbidden interactive controls found in UWP section: {forbidden_found}")

    _uwp_examples = _ROOT / "examples" / "universal_work_playground"
    work_packet = _uwp_examples / "safe_demo_work_packet.valid.json"
    if work_packet.exists():
        try:
            wp_data = json.loads(work_packet.read_text(encoding="utf-8"))
            if wp_data.get("candidate_only") is not True:
                errors.append("safe_demo_work_packet.valid.json: candidate_only must be true")
            if wp_data.get("local_only") is not True:
                errors.append("safe_demo_work_packet.valid.json: local_only must be true")
            if wp_data.get("app_apply") is not False:
                errors.append("safe_demo_work_packet.valid.json: app_apply must be false")
            if wp_data.get("external_send") is not False:
                errors.append("safe_demo_work_packet.valid.json: external_send must be false")
            if wp_data.get("arbitrary_shell_execution") is not False:
                errors.append("safe_demo_work_packet.valid.json: arbitrary_shell_execution must be false")
            if wp_data.get("provider_execution") is not False:
                errors.append("safe_demo_work_packet.valid.json: provider_execution must be false")
            if wp_data.get("credential_required") is not False:
                errors.append("safe_demo_work_packet.valid.json: credential_required must be false")
            if "claim_boundary" not in wp_data:
                errors.append("safe_demo_work_packet.valid.json: missing claim_boundary")
            if "proof_boundaries" not in wp_data:
                errors.append("safe_demo_work_packet.valid.json: missing proof_boundaries")
            if "known_non_proofs" not in wp_data:
                errors.append("safe_demo_work_packet.valid.json: missing known_non_proofs")
        except Exception as exc:
            errors.append(f"safe_demo_work_packet.valid.json: parse error: {exc}")

    candidate_result = _uwp_examples / "safe_demo_candidate_result.valid.json"
    if candidate_result.exists():
        try:
            cr_data = json.loads(candidate_result.read_text(encoding="utf-8"))
            if cr_data.get("candidate_only") is not True:
                errors.append("safe_demo_candidate_result.valid.json: candidate_only must be true")
            if cr_data.get("applied_truth") is not False:
                errors.append("safe_demo_candidate_result.valid.json: applied_truth must be false")
            if cr_data.get("app_state_mutated") is not False:
                errors.append("safe_demo_candidate_result.valid.json: app_state_mutated must be false")
            if cr_data.get("external_send") is not False:
                errors.append("safe_demo_candidate_result.valid.json: external_send must be false")
            if "claim_boundary" not in cr_data:
                errors.append("safe_demo_candidate_result.valid.json: missing claim_boundary")
            if "proof_boundaries" not in cr_data:
                errors.append("safe_demo_candidate_result.valid.json: missing proof_boundaries")
        except Exception as exc:
            errors.append(f"safe_demo_candidate_result.valid.json: parse error: {exc}")

    doc = _ROOT / "docs" / "UNIVERSAL_WORK_PLAYGROUND_V1.md"
    if doc.exists():
        doc_text = doc.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in _UWP_REQUIRED_DOC_PHRASES:
            if phrase.lower() not in doc_text:
                errors.append(f"UNIVERSAL_WORK_PLAYGROUND_V1.md: missing required phrase: {phrase!r}")

    return errors


def build_universal_work_playground_proof_packet() -> dict[str, Any]:
    """Emit a bounded proof packet for the Universal Work Playground (LRH-PR-11)."""
    uwp_errors = validate_universal_work_playground()
    all_ok = not bool(uwp_errors)

    return {
        "artifact_kind": "hub_universal_work_playground_proof_packet",
        "candidate_only": True,
        "local_only": True,
        "playground_only": True,
        "safe_demo_only": True,
        "status": "ok" if all_ok else "partial",
        "validation_errors": uwp_errors,
        "proven": [
            "universal_work_playground_static_files_exist",
            "local_only_form_present",
            "safe_demo_work_fixture_present",
            "safe_demo_candidate_result_fixture_present",
            "candidate_result_panel_present",
            "proof_boundary_panel_present",
            "validation_status_panel_present",
            "provider_worker_boundary_context_present",
            "no_app_apply_controls",
            "no_external_send_controls",
            "no_arbitrary_shell_execution_controls",
            "no_provider_execution_controls",
            "no_credential_controls",
            "candidate_result_not_applied_truth",
        ] if all_ok else [],
        "not_proven": [
            "production_readiness",
            "security_certification",
            "live_model_inference",
            "model_quality",
            "app_apply_authority",
            "external_send_authority",
            "arbitrary_shell_execution_safety",
            "provider_execution",
            "credential_handling",
            "full_live_universal_work_backend_coverage",
            "external_app_bridge",
        ],
        "proof_boundaries": UNIVERSAL_WORK_PLAYGROUND_PROOF_BOUNDARIES,
        "claim_boundary": UNIVERSAL_WORK_PLAYGROUND_CLAIM_BOUNDARY,
    }


def build_browser_hub_proof_packet(shell_only: bool = True, dashboard: bool = False, candidates: bool = False, traces: bool = False, providers: bool = False, playground: bool = False) -> dict[str, Any]:
    """Emit a bounded proof packet for the browser hub shell.

    If candidates=True, runs the candidate store viewer validator.
    If dashboard=True, runs both shell and dashboard validators and returns a combined packet.
    If shell_only=True (default), runs only shell validator.
    """
    if playground:
        return build_universal_work_playground_proof_packet()

    if providers:
        return build_provider_worker_inspector_proof_packet()

    if traces:
        return build_trace_viewer_proof_packet()

    if candidates:
        return build_candidate_store_viewer_proof_packet()

    if dashboard:
        return build_dashboard_proof_packet()

    errors = validate_browser_hub_shell()
    all_ok = not bool(errors)

    return {
        "artifact_kind": "browser_hub_shell_proof_packet",
        "candidate_only": True,
        "local_only": True,
        "shell_only": shell_only,
        "status": "ok" if all_ok else "partial",
        "validation_errors": errors,
        "proven": [
            "static_shell_files_exist",
            "local_api_client_references_v1_contract",
            "no_apply_controls",
            "no_external_send_controls",
            "boundary_banner_present",
            "navigation_shell_present",
            "localhost_default_enforced",
        ] if all_ok else [],
        "not_proven": [
            "production_readiness",
            "hosted_cloud_ui",
            "auth_security_certification",
            "live_browser_runtime_e2e",
            "provider_execution",
            "app_state_mutation",
            "external_send_authority",
            "live_model_inference",
            "model_quality",
        ],
        "proof_boundaries": BROWSER_HUB_PROOF_BOUNDARIES,
        "claim_boundary": BROWSER_HUB_SHELL_CLAIM_BOUNDARY,
    }


# ---------------------------------------------------------------------------
# LRH-PR-12 — Neutral External App Bridge Pack
# ---------------------------------------------------------------------------

NEUTRAL_EXTERNAL_APP_BRIDGE_CLAIM_BOUNDARY = (
    "neutral_external_app_bridge_pack_candidate_only_no_app_apply_"
    "no_external_send_no_credentials_no_hosted_bridge_no_public_gateway"
)

NEUTRAL_EXTERNAL_APP_BRIDGE_PROOF_BOUNDARIES = [
    "not_production_readiness_certification",
    "not_security_certification",
    "not_hosted_bridge_proof",
    "not_public_gateway_proof",
    "not_real_external_app_integration_proof",
    "not_app_apply_proof",
    "not_host_state_mutation_proof",
    "not_external_send_authority_proof",
    "not_provider_execution_proof",
    "not_provider_credential_storage_proof",
    "not_live_model_inference_proof",
    "not_model_quality_proof",
    "candidate_artifact_not_applied_truth",
    "host_app_owns_apply_state_external_send",
]

_NEAB_ROOT = _ROOT / "examples" / "external_app_bridge"
_NEAB_DOC = _ROOT / "docs" / "NEUTRAL_EXTERNAL_APP_BRIDGE_PACK_V1.md"

_NEAB_REQUIRED_FILES = [
    "docs/NEUTRAL_EXTERNAL_APP_BRIDGE_PACK_V1.md",
    "examples/external_app_bridge/neutral_host_health_check.py",
    "examples/external_app_bridge/neutral_host_submit_universal_work.py",
    "examples/external_app_bridge/neutral_host_read_candidate.py",
    "examples/external_app_bridge/neutral_host_read_proof_gaps.py",
    "examples/external_app_bridge/neutral_bridge_config.example.json",
    "examples/external_app_bridge/neutral_universal_work_request.valid.json",
    "examples/external_app_bridge/neutral_candidate_artifact_response.valid.json",
    "tests/test_lrh_pr_12_neutral_external_app_bridge.py",
]

_NEAB_REQUIRED_DOC_PHRASES = [
    "host app owns apply",
    "host app owns state",
    "host app owns external send",
    "odin does not apply",
    "odin does not send externally",
    "candidate artifact",
    "not applied truth",
    "localhost",
    "not_production_readiness_certification",
    "not a hosted bridge",
    "not a public",
]

_NEAB_FORBIDDEN_BRIDGE_CONFIG_KEYS = [
    "token", "secret", "api_key", "password", "credential", "webhook_url",
    "callback_url", "remote_url",
]

_NEAB_FORBIDDEN_HELPER_NAMES = [
    "applyCandidate", "apply_candidate", "sendExternally", "send_external",
    "uploadResult", "upload_result", "publishResult", "publish_result",
    "mutateAppState", "mutate_app_state", "storeCredential", "store_credential",
    "saveCredential", "save_credential", "setApiKey", "set_api_key",
    "setToken", "set_token", "runProvider", "run_provider",
    "executeProvider", "execute_provider", "callModel", "call_model",
    "runModel", "run_model",
]

_NEAB_FORBIDDEN_DOC_CLAIMS = [
    "production bridge complete",
    "security certified",
    "is a hosted bridge",
    "is a public gateway",
    "production-ready bridge",
    "this is a hosted",
    "this is a public gateway",
]

_NEAB_REQUIRED_CONFIG_KEYS = {
    "odin_base_url": "http://127.0.0.1:8877",
    "localhost_only": True,
    "host_app_owns_apply": True,
    "host_app_owns_state": True,
    "host_app_owns_external_send": True,
    "odin_external_send": False,
    "odin_app_apply": False,
    "credential_required": False,
}

_NEAB_REQUIRED_WORK_REQUEST_KEYS = {
    "candidate_only": True,
    "local_only": True,
    "external_send": False,
    "app_apply": False,
    "host_app_owns_apply": True,
    "host_app_owns_state": True,
    "host_app_owns_external_send": True,
}

_NEAB_REQUIRED_CANDIDATE_KEYS = {
    "candidate_only": True,
    "applied_truth": False,
    "app_state_mutated": False,
    "external_send": False,
}


def validate_neutral_external_app_bridge() -> list[str]:
    """Deterministic static validator for the Neutral External App Bridge Pack (LRH-PR-12).

    Returns a list of error strings (empty = ok).
    """
    errors: list[str] = []

    # Required files
    for rel in _NEAB_REQUIRED_FILES:
        if not (_ROOT / rel).exists():
            errors.append(f"neutral external app bridge required file missing: {rel}")

    # Bridge config fixture
    config_path = _NEAB_ROOT / "neutral_bridge_config.example.json"
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
            for key, expected in _NEAB_REQUIRED_CONFIG_KEYS.items():
                if config.get(key) != expected:
                    errors.append(
                        f"neutral_bridge_config.example.json: {key} must be {expected!r} (got {config.get(key)!r})"
                    )
            for forbidden in _NEAB_FORBIDDEN_BRIDGE_CONFIG_KEYS:
                if forbidden in config:
                    errors.append(
                        f"neutral_bridge_config.example.json: must not contain forbidden key: {forbidden!r}"
                    )
        except Exception as exc:
            errors.append(f"neutral_bridge_config.example.json: parse error: {exc}")

    # Universal Work request fixture
    work_path = _NEAB_ROOT / "neutral_universal_work_request.valid.json"
    if work_path.exists():
        try:
            work = json.loads(work_path.read_text(encoding="utf-8"))
            for key, expected in _NEAB_REQUIRED_WORK_REQUEST_KEYS.items():
                if work.get(key) != expected:
                    errors.append(
                        f"neutral_universal_work_request.valid.json: {key} must be {expected!r} (got {work.get(key)!r})"
                    )
            if "claim_boundary" not in work:
                errors.append("neutral_universal_work_request.valid.json: missing claim_boundary")
            if "proof_boundaries" not in work:
                errors.append("neutral_universal_work_request.valid.json: missing proof_boundaries")
            if "known_non_proofs" not in work:
                errors.append("neutral_universal_work_request.valid.json: missing known_non_proofs")
        except Exception as exc:
            errors.append(f"neutral_universal_work_request.valid.json: parse error: {exc}")

    # Candidate artifact fixture
    artifact_path = _NEAB_ROOT / "neutral_candidate_artifact_response.valid.json"
    if artifact_path.exists():
        try:
            artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
            for key, expected in _NEAB_REQUIRED_CANDIDATE_KEYS.items():
                if artifact.get(key) != expected:
                    errors.append(
                        f"neutral_candidate_artifact_response.valid.json: {key} must be {expected!r} (got {artifact.get(key)!r})"
                    )
            if "claim_boundary" not in artifact:
                errors.append("neutral_candidate_artifact_response.valid.json: missing claim_boundary")
            if "proof_boundaries" not in artifact:
                errors.append("neutral_candidate_artifact_response.valid.json: missing proof_boundaries")
        except Exception as exc:
            errors.append(f"neutral_candidate_artifact_response.valid.json: parse error: {exc}")

    # Doc phrase checks
    if _NEAB_DOC.exists():
        doc_text = _NEAB_DOC.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in _NEAB_REQUIRED_DOC_PHRASES:
            if phrase.lower() not in doc_text:
                errors.append(
                    f"NEUTRAL_EXTERNAL_APP_BRIDGE_PACK_V1.md: missing required phrase: {phrase!r}"
                )
        for claim in _NEAB_FORBIDDEN_DOC_CLAIMS:
            if claim.lower() in doc_text:
                errors.append(
                    f"NEUTRAL_EXTERNAL_APP_BRIDGE_PACK_V1.md: forbidden overclaim phrase found: {claim!r}"
                )

    # SDK helper forbidden name check
    sdk_files = [
        _ROOT / "sdk" / "python" / "odin_client.py",
        _ROOT / "odin_app_sdk" / "client.py",
    ]
    for sdk_file in sdk_files:
        if sdk_file.exists():
            sdk_text = sdk_file.read_text(encoding="utf-8", errors="ignore")
            for name in _NEAB_FORBIDDEN_HELPER_NAMES:
                if f"def {name}(" in sdk_text:
                    errors.append(
                        f"{sdk_file.name}: must not define forbidden helper: def {name}()"
                    )

    # Example files: check localhost guard and no forbidden patterns
    example_files = [
        "neutral_host_health_check.py",
        "neutral_host_submit_universal_work.py",
        "neutral_host_read_candidate.py",
        "neutral_host_read_proof_gaps.py",
    ]
    for fname in example_files:
        fpath = _NEAB_ROOT / fname
        if fpath.exists():
            src = fpath.read_text(encoding="utf-8", errors="ignore")
            if "127.0.0.1" not in src and "localhost" not in src:
                errors.append(f"{fname}: missing localhost reference / guard")
            if "candidate_only" not in src:
                errors.append(f"{fname}: missing candidate_only boundary reference")
            if "host_app_owns_apply" not in src:
                errors.append(f"{fname}: missing host_app_owns_apply boundary reference")

    return errors


def build_neutral_external_app_bridge_proof_packet() -> dict[str, Any]:
    """Emit a bounded proof packet for the Neutral External App Bridge Pack (LRH-PR-12)."""
    errors = validate_neutral_external_app_bridge()
    all_ok = not bool(errors)

    return {
        "artifact_kind": "neutral_external_app_bridge_pack_proof_packet",
        "candidate_only": True,
        "local_only_default": True,
        "bridge_pack_only": True,
        "neutral_app_only": True,
        "status": "ok" if all_ok else "partial",
        "validation_errors": errors,
        "proven": [
            "neutral_bridge_doc_exists",
            "neutral_examples_exist",
            "neutral_fixtures_exist",
            "health_check_example_exists",
            "universal_work_submit_example_exists",
            "candidate_read_example_exists",
            "proof_gap_read_example_exists",
            "host_app_owns_apply_declared",
            "host_app_owns_state_declared",
            "host_app_owns_external_send_declared",
            "odin_does_not_apply_declared",
            "odin_does_not_external_send_declared",
            "no_concrete_app_names",
            "no_credentials_in_fixtures",
            "no_external_send_controls",
            "no_app_apply_helpers",
            "candidate_result_not_applied_truth",
            "localhost_only_default",
        ] if all_ok else [],
        "not_proven": [
            "production_readiness",
            "security_certification",
            "hosted_bridge",
            "public_gateway",
            "real_external_app_integration",
            "app_apply_authority",
            "external_send_authority",
            "credential_handling",
            "provider_execution",
            "live_model_inference",
            "model_quality",
            "app_state_mutation",
        ],
        "proof_boundaries": NEUTRAL_EXTERNAL_APP_BRIDGE_PROOF_BOUNDARIES,
        "claim_boundary": NEUTRAL_EXTERNAL_APP_BRIDGE_CLAIM_BOUNDARY,
    }


# ---------------------------------------------------------------------------
# LRH-PR-13 — Generic App Bridge Golden Harness
# ---------------------------------------------------------------------------

GENERIC_APP_BRIDGE_GOLDEN_HARNESS_CLAIM_BOUNDARY = (
    "generic_app_bridge_golden_harness_candidate_only_local_only_no_apply_no_external_send"
)

GENERIC_APP_BRIDGE_GOLDEN_HARNESS_PROOF_BOUNDARIES = [
    "not_production_readiness_certification",
    "not_security_certification",
    "not_hosted_bridge_proof",
    "not_public_gateway_proof",
    "not_specific_external_app_integration_proof",
    "not_signed_distribution_proof",
    "not_windows_service_tray_installer_proof",
    "not_app_apply_proof",
    "not_host_state_mutation_proof",
    "not_external_send_authority_proof",
    "not_provider_execution_proof",
    "not_live_model_inference_proof",
    "not_model_quality_proof",
    "candidate_artifact_not_applied_truth",
    "host_app_owns_apply_state_external_send",
]

_GABGH_ROOT = _ROOT / "examples" / "generic_app_bridge"
_GABGH_REF_HOST = _ROOT / "examples" / "reference_host_app"
_GABGH_DOC = _ROOT / "docs" / "GENERIC_APP_BRIDGE_GOLDEN_HARNESS_V1.md"
_THOR_DISCIPLINE_DOC = _ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"

_GABGH_REQUIRED_FILES = [
    "docs/GENERIC_APP_BRIDGE_GOLDEN_HARNESS_V1.md",
    "docs/THOR_CLI_INVOCATION_DISCIPLINE_V1.md",
    "examples/generic_app_bridge/generic_bridge_flow_one.py",
    "examples/generic_app_bridge/generic_bridge_flow_two.py",
    "examples/generic_app_bridge/generic_bridge_harness.py",
    "examples/generic_app_bridge/fixtures/generic_bridge_flow_one_request.valid.json",
    "examples/generic_app_bridge/fixtures/generic_bridge_flow_one_candidate.valid.json",
    "examples/generic_app_bridge/fixtures/generic_bridge_flow_two_request.valid.json",
    "examples/generic_app_bridge/fixtures/generic_bridge_flow_two_candidate.valid.json",
    "examples/reference_host_app/reference_host_app.py",
    "examples/reference_host_app/reference_host_policy.json",
    "tests/test_lrh_pr_13_generic_app_bridge_golden_harness.py",
]

_GABGH_REQUIRED_REQUEST_KEYS = {
    "candidate_only": True,
    "local_only": True,
    "host_app_owns_apply": True,
    "applied_truth": False,
}

_GABGH_REQUIRED_CANDIDATE_KEYS = {
    "candidate_only": True,
    "applied_truth": False,
    "host_app_owns_apply": True,
    "app_state_mutated": False,
    "external_send": False,
}

_GABGH_REQUIRED_POLICY_KEYS = {
    "host_app_owns_apply": True,
    "host_app_owns_state": True,
    "host_app_owns_external_send": True,
    "app_state_mutated": False,
    "external_send_performed": False,
}

_GABGH_REQUIRED_DOC_PHRASES = [
    "host app owns apply",
    "host app owns state",
    "host app owns external send",
    "candidate artifact",
    "not applied truth",
    "candidate_only",
    "local_only",
    "golden harness",
    "known non-proofs",
    "proof boundaries",
]

_GABGH_FORBIDDEN_DOC_CLAIMS = [
    "production-ready release",
    "fully proven",
    "complete proof",
    "real integration complete",
    "hosted bridge ready",
    "public gateway ready",
    "signed release ready",
]

_GABGH_FORBIDDEN_HELPER_NAMES = [
    "apply_candidate",
    "send_external",
    "mutate_app_state",
    "store_credential",
    "save_credential",
    "set_api_key",
    "run_provider",
    "execute_provider",
    "call_model",
    "run_model",
]

_GABGH_FORBIDDEN_CONCRETE_NAMES = [
    "github_copilot",
    "jira_integration",
    "slack_bot",
    "salesforce",
    "notion_plugin",
    "linear_integration",
]

_GABGH_REQUIRED_NEUTRAL_EXAMPLE_FILES = [
    "examples/generic_app_bridge/generic_bridge_flow_one.py",
    "examples/generic_app_bridge/generic_bridge_flow_two.py",
]


def validate_generic_app_bridge_golden_harness() -> list[str]:
    """Deterministic static validator for the Generic App Bridge Golden Harness (LRH-PR-13).

    Returns a list of error strings (empty = ok).
    """
    errors: list[str] = []

    # Required files
    for rel in _GABGH_REQUIRED_FILES:
        if not (_ROOT / rel).exists():
            errors.append(f"generic app bridge golden harness required file missing: {rel}")

    # Neutral example count
    neutral_count = sum(
        1 for rel in _GABGH_REQUIRED_NEUTRAL_EXAMPLE_FILES if (_ROOT / rel).exists()
    )
    if neutral_count < 2:
        errors.append(
            f"generic app bridge: at least two neutral examples required; found {neutral_count}"
        )

    # Flow one request fixture
    req_one = _GABGH_ROOT / "fixtures" / "generic_bridge_flow_one_request.valid.json"
    if req_one.exists():
        try:
            data = json.loads(req_one.read_text(encoding="utf-8"))
            for key, expected in _GABGH_REQUIRED_REQUEST_KEYS.items():
                if data.get(key) != expected:
                    errors.append(
                        f"generic_bridge_flow_one_request.valid.json: {key} must be {expected}"
                    )
            if "claim_boundary" not in data:
                errors.append("generic_bridge_flow_one_request.valid.json: missing claim_boundary")
        except Exception as exc:
            errors.append(f"generic_bridge_flow_one_request.valid.json: parse error: {exc}")

    # Flow one candidate fixture
    cand_one = _GABGH_ROOT / "fixtures" / "generic_bridge_flow_one_candidate.valid.json"
    if cand_one.exists():
        try:
            data = json.loads(cand_one.read_text(encoding="utf-8"))
            for key, expected in _GABGH_REQUIRED_CANDIDATE_KEYS.items():
                if data.get(key) != expected:
                    errors.append(
                        f"generic_bridge_flow_one_candidate.valid.json: {key} must be {expected}"
                    )
            if "claim_boundary" not in data:
                errors.append("generic_bridge_flow_one_candidate.valid.json: missing claim_boundary")
        except Exception as exc:
            errors.append(f"generic_bridge_flow_one_candidate.valid.json: parse error: {exc}")

    # Flow two request fixture
    req_two = _GABGH_ROOT / "fixtures" / "generic_bridge_flow_two_request.valid.json"
    if req_two.exists():
        try:
            data = json.loads(req_two.read_text(encoding="utf-8"))
            for key, expected in _GABGH_REQUIRED_REQUEST_KEYS.items():
                if data.get(key) != expected:
                    errors.append(
                        f"generic_bridge_flow_two_request.valid.json: {key} must be {expected}"
                    )
        except Exception as exc:
            errors.append(f"generic_bridge_flow_two_request.valid.json: parse error: {exc}")

    # Flow two candidate fixture
    cand_two = _GABGH_ROOT / "fixtures" / "generic_bridge_flow_two_candidate.valid.json"
    if cand_two.exists():
        try:
            data = json.loads(cand_two.read_text(encoding="utf-8"))
            for key, expected in _GABGH_REQUIRED_CANDIDATE_KEYS.items():
                if data.get(key) != expected:
                    errors.append(
                        f"generic_bridge_flow_two_candidate.valid.json: {key} must be {expected}"
                    )
        except Exception as exc:
            errors.append(f"generic_bridge_flow_two_candidate.valid.json: parse error: {exc}")

    # Reference host policy fixture
    policy = _GABGH_REF_HOST / "reference_host_policy.json"
    if policy.exists():
        try:
            data = json.loads(policy.read_text(encoding="utf-8"))
            for key, expected in _GABGH_REQUIRED_POLICY_KEYS.items():
                if data.get(key) != expected:
                    errors.append(
                        f"reference_host_policy.json: {key} must be {expected}"
                    )
        except Exception as exc:
            errors.append(f"reference_host_policy.json: parse error: {exc}")

    # Doc phrase checks
    if _GABGH_DOC.exists():
        doc_text = _GABGH_DOC.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in _GABGH_REQUIRED_DOC_PHRASES:
            if phrase.lower() not in doc_text:
                errors.append(
                    f"GENERIC_APP_BRIDGE_GOLDEN_HARNESS_V1.md: missing required phrase: {phrase!r}"
                )
        for claim in _GABGH_FORBIDDEN_DOC_CLAIMS:
            if claim.lower() in doc_text:
                errors.append(
                    f"GENERIC_APP_BRIDGE_GOLDEN_HARNESS_V1.md: forbidden overclaim phrase: {claim!r}"
                )

    # Thor discipline doc phrase check
    if _THOR_DISCIPLINE_DOC.exists():
        thor_text = _THOR_DISCIPLINE_DOC.read_text(encoding="utf-8", errors="ignore").lower()
        if "thor is advisory" not in thor_text:
            errors.append(
                "THOR_CLI_INVOCATION_DISCIPLINE_V1.md: missing 'Thor is advisory' statement"
            )
        if "classification" not in thor_text:
            errors.append(
                "THOR_CLI_INVOCATION_DISCIPLINE_V1.md: missing classification section"
            )

    # Neutral naming guard — no concrete app names in examples/fixtures
    scan_paths: list[Path] = []
    for rel in _GABGH_REQUIRED_NEUTRAL_EXAMPLE_FILES:
        p = _ROOT / rel
        if p.exists():
            scan_paths.append(p)
    for fixture_dir in [_GABGH_ROOT / "fixtures", _GABGH_REF_HOST]:
        if fixture_dir.exists():
            scan_paths.extend(fixture_dir.glob("*.json"))

    for scan_path in scan_paths:
        text = scan_path.read_text(encoding="utf-8", errors="ignore").lower()
        for name in _GABGH_FORBIDDEN_CONCRETE_NAMES:
            if name in text:
                errors.append(
                    f"{scan_path.name}: forbidden concrete app name found: {name!r}"
                )

    # Forbidden helper function names in example files
    for rel in _GABGH_REQUIRED_NEUTRAL_EXAMPLE_FILES:
        p = _ROOT / rel
        if p.exists():
            src = p.read_text(encoding="utf-8", errors="ignore")
            for fname in _GABGH_FORBIDDEN_HELPER_NAMES:
                if f"def {fname}(" in src:
                    errors.append(
                        f"{p.name}: must not define forbidden helper: def {fname}()"
                    )

    return errors


def build_generic_app_bridge_golden_harness_proof_packet() -> dict[str, Any]:
    """Emit a bounded proof packet for the Generic App Bridge Golden Harness (LRH-PR-13)."""
    errors = validate_generic_app_bridge_golden_harness()
    all_ok = not bool(errors)

    return {
        "artifact_kind": "generic_app_bridge_golden_harness_proof_packet",
        "candidate_only": True,
        "local_only": True,
        "neutral_examples_count": 2,
        "host_app_owns_apply": True,
        "host_app_owns_state": True,
        "host_app_owns_external_send": True,
        "odin_app_apply": False,
        "odin_external_send": False,
        "host_state_mutation_by_odin": False,
        "concrete_app_names_present": False,
        "status": "ok" if all_ok else "partial",
        "validation_errors": errors,
        "proven": [
            "generic_examples_exist",
            "reference_host_app_exists",
            "golden_harness_exists",
            "two_neutral_examples_present",
            "golden_harness_receipt_ok",
            "host_app_owns_apply_declared",
            "host_app_owns_state_declared",
            "host_app_owns_external_send_declared",
            "odin_app_apply_false",
            "odin_external_send_false",
            "host_state_mutation_by_odin_false",
            "candidate_artifact_not_applied_truth",
            "neutral_naming_guard_passed",
            "local_only_examples",
            "thor_invocation_discipline_doc_exists",
        ] if all_ok else [],
        "not_proven": [
            "production_readiness",
            "security_certification",
            "signed_distribution",
            "windows_service_tray_installer",
            "hosted_bridge",
            "public_network_api",
            "specific_external_app_integration",
            "live_model_inference",
            "model_quality",
            "provider_execution",
            "real_app_state_mutation",
            "external_send_authority",
        ],
        "proof_boundaries": GENERIC_APP_BRIDGE_GOLDEN_HARNESS_PROOF_BOUNDARIES,
        "claim_boundary": GENERIC_APP_BRIDGE_GOLDEN_HARNESS_CLAIM_BOUNDARY,
    }
