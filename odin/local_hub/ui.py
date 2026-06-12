"""Simple Local Hub browser UI generator — FINAL-PR-01.

Claim boundary: simple_local_hub_ui_candidate_only_no_provider_execution_no_app_apply
"""
from __future__ import annotations

import json

REQUIRED_IDS = [
    "hub-title",
    "runtime-status",
    "local-api-status",
    "model-status",
    "connected-apps-status",
    "activity-status",
    "warnings-proof-gaps",
    "qirc-status",
    "handoff-first-status",
    "dev-mode-entry",
    "normal-user-help",
]

REQUIRED_COPY = [
    "Odin is running locally.",
    "Odin returns candidates; apps decide what to apply.",
    "No model is active yet.",
    "No apps are connected yet.",
    "QIRC core is planned for a later final slice.",
    "Handoff-First prepares work before Universal Work.",
    "Dev Mode contains traces, receipts, proof gaps, validators, and handoff details.",
]


def generate_hub_html() -> str:
    """Generate the Simple Local Hub HTML page with all required stable IDs."""
    return """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Odin Local Hub</title>
  <style>
    body{font-family:system-ui,sans-serif;max-width:820px;margin:40px auto;padding:0 20px;color:#333}
    h1{border-bottom:2px solid #e0e0e0;padding-bottom:8px}
    .section{background:#f8f9fa;border:1px solid #e0e0e0;border-radius:4px;padding:12px 16px;margin:10px 0}
    .label{font-weight:600;color:#555;font-size:.9em;margin-bottom:4px}
    .chip{display:inline-block;padding:2px 8px;border-radius:3px;font-size:.85em}
    .ok{background:#d4edda;color:#155724}
    .pending{background:#fff3cd;color:#856404}
    .deferred{background:#e2e3e5;color:#383d41}
    .dev{background:#cce5ff;border-color:#b8daff}
    .note{font-size:.8em;color:#888;margin-top:6px;font-style:italic}
    details>summary{cursor:pointer;font-weight:600;margin-bottom:6px}
    .dev-row{margin:4px 0;font-size:.9em;color:#444}
  </style>
</head>
<body>

<h1 id="hub-title">Odin Local Hub</h1>

<div id="normal-user-help" class="section">
  <p>Odin is running locally.</p>
  <p>Odin returns candidates; apps decide what to apply.</p>
</div>

<div id="runtime-status" class="section">
  <div class="label">Runtime Status</div>
  <span class="chip ok">Running &#8212; localhost only</span>
  <p class="note">Localhost only. Candidate-only. No app apply. No external send. No provider execution.</p>
</div>

<div id="local-api-status" class="section">
  <div class="label">Local API</div>
  <span class="chip ok">Available at 127.0.0.1:8765</span>
  <p class="note">Simple Local Hub &#8212; FINAL-PR-01. GET /healthz, GET /status.json, GET /</p>
</div>

<div id="model-status" class="section">
  <div class="label">Model</div>
  <span class="chip pending">No model is active yet.</span>
  <p class="note">Model picker deferred to FINAL-PR-02.</p>
</div>

<div id="connected-apps-status" class="section">
  <div class="label">Connected Apps</div>
  <span class="chip pending">No apps are connected yet.</span>
  <p class="note">Connected apps runtime deferred to FINAL-PR-02.</p>
</div>

<div id="activity-status" class="section">
  <div class="label">Activity</div>
  <span class="chip deferred">No recent activity.</span>
  <p class="note">Activity / trace / receipt viewer deferred to FINAL-PR-03.</p>
</div>

<div id="warnings-proof-gaps" class="section">
  <div class="label">Warnings / Proof Gaps</div>
  <span class="chip pending">Known gaps &#8212; see Dev Mode for details.</span>
  <p class="note">No provider execution proof. No model inference proof. No production readiness. No security certification.</p>
</div>

<div id="qirc-status" class="section">
  <div class="label">QIRC</div>
  <span class="chip deferred">QIRC core is planned for a later final slice.</span>
  <p class="note">QIRC Core runtime deferred to FINAL-PR-03. This is a non-authoritative placeholder.</p>
</div>

<div id="handoff-first-status" class="section">
  <div class="label">Handoff-First</div>
  <span class="chip deferred">Handoff-First prepares work before Universal Work.</span>
  <p class="note">Deep handoff viewer deferred to FINAL-PR-03. This is a non-authoritative placeholder.</p>
</div>

<div id="dev-mode-entry" class="section dev">
  <div class="label">Dev Mode</div>
  <p>Dev Mode contains traces, receipts, proof gaps, validators, and handoff details.</p>
  <details>
    <summary>Expand Dev Mode</summary>
    <div class="dev-row" id="dev-qirc-status">QIRC status: placeholder &#8212; not running</div>
    <div class="dev-row" id="dev-handoff-first-status">Handoff-First status: placeholder &#8212; not running</div>
    <div class="dev-row" id="dev-trace-status">Trace/Receipt status: placeholder &#8212; viewer deferred to FINAL-PR-03</div>
    <div class="dev-row" id="dev-validator-status">Validator status: run <code>python -m odin.cli validate-simple-local-hub</code></div>
    <div class="dev-row" id="dev-proof-gaps">Proof gaps: provider_execution, model_inference, qirc_core_runtime, handoff_compiler_runtime, app_bridge_runtime, app_apply, app_state_mutation, external_send, public_network, production_readiness, security_certification</div>
    <div class="dev-row" id="dev-support-bundle">Support bundle: placeholder &#8212; run <code>python -m odin.cli emit-support-bundle</code></div>
    <div class="dev-row" id="dev-handoff-viewer">Handoff viewer: placeholder &#8212; deep viewer deferred to FINAL-PR-03</div>
  </details>
</div>

</body>
</html>
"""


def generate_status_json() -> str:
    return json.dumps({
        "status": "ok",
        "hub": "simple_local_hub",
        "version": "final_pr_01",
        "candidate_only": True,
        "local_only": True,
        "host": "127.0.0.1",
        "model": "none",
        "connected_apps": 0,
        "qirc": "deferred_to_final_pr_03",
        "handoff_first": "placeholder_not_running",
        "claim_boundary": "simple_local_hub_local_receipt_not_runtime_completion_not_production",
        "not_proven": [
            "provider_execution",
            "model_inference",
            "qirc_core_runtime",
            "handoff_compiler_runtime",
            "app_bridge_runtime",
            "app_apply",
            "app_state_mutation",
            "external_send",
            "public_network",
            "production_readiness",
            "security_certification",
        ],
    }, indent=2)
