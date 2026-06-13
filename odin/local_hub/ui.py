"""Simple Local Hub browser UI generator — FINAL-PR-01/02.

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
    # FINAL-PR-02 additions
    "model-picker-section",
    "model-option-none",
    "model-option-mock",
    "model-option-local-candidate",
    "provider-status-panel",
    "connected-apps-section",
    "connected-app-slot-generic",
    "connected-app-slot-browser",
    "connected-app-slot-file",
    "app-bridge-status",
    "demo-universal-work-section",
    "demo-work-input",
    "demo-submit-placeholder",
    "demo-response-packet",
    "demo-candidate-artifact",
    "demo-handoff-context",
    "demo-universal-work-packet",
    "demo-proof-gap-status",
    # FINAL-PR-03 Dev Mode additions
    "qirc-channel-viewer",
    "qirc-event-viewer",
    "activity-timeline",
    "trace-viewer",
    "receipt-viewer",
    "handoff-chain-viewer",
    "surface-map-viewer",
    "proof-gap-viewer",
    # FINAL-PR-04 Provider Probe + Security Smoke additions
    "provider-policy-status",
    "provider-probe-panel",
    "provider-probe-results",
    "provider-execution-boundary",
    "runtime-security-smoke-status",
    "secret-scan-status",
    "network-boundary-status",
    "qirc-provider-events-status",
    # FINAL-PR-05 Execution Gate + Ladder Scaffold additions
    "execution-gate-status",
    "mock-execution-panel",
    "mock-execution-result",
    "local-candidate-policy-status",
    "execution-boundary-status",
    "proof-chain-status",
    "final-pr-ladder-scaffold-status",
    "model-execution-warning",
    # Y Pattern Spine
    "y-pattern-spine-status",
    # FINAL-PR-06 Operational Seed Spine
    "operational-seed-spine-status",
    # FINAL-PR-07 Field Selection Spine (already present in HTML)
    "field-selection-spine-section",
    # FINAL-PR-08 Projection Candidate Spine
    "projection-candidate-spine-section",
    # FINAL-PR-09++ Operational Spine
    "operational-spine-section",
]

REQUIRED_COPY = [
    "Odin is running locally.",
    "Odin returns candidates; apps decide what to apply.",
    "No model is active yet.",
    "No apps are connected yet.",
    "QIRC core is planned for a later final slice.",
    "Handoff-First prepares work before Universal Work.",
    "Dev Mode contains traces, receipts, proof gaps, validators, and handoff details.",
    # FINAL-PR-02 additions
    "Choose how Odin should prepare work.",
    "No model inference runs in this PR.",
    "Mock mode returns deterministic demo candidates.",
    "Local candidate provider is listed but not executed yet.",
    "Connected apps are demo slots only.",
    "Odin can accept a demo Universal Work request and return a candidate response packet.",
    "Apps still decide what to apply.",
    # FINAL-PR-03 additions
    "QIRC coordinates locally. Odin gates. Apps decide.",
    "Activity timeline shows local candidate events.",
    "Dev Mode: QIRC channels, events, traces, receipts, handoff chain.",
    # FINAL-PR-04 additions
    "Provider probe checks readiness only.",
    "No model is executed.",
    "No API keys are read.",
    "No external network is used.",
    "Provider execution remains disabled by default.",
    # FINAL-PR-05 additions
    "Mock execution is local and deterministic.",
    "Mock execution is not model inference.",
    "No real model is executed by default.",
    "Local candidate execution is disabled by default.",
    "Apps still decide what to apply.",
    "Remote providers and API keys are not used.",
    "Proof chain links receipts but does not prove production readiness.",
    "FINAL-PR Ladder scaffold is not a full Thor replacement.",
    # Y Pattern Spine
    "Odin prepares work with compact route hints.",
    "Y Pattern Spine explains why a route/capsule was selected.",
    # FINAL-PR-06 Operational Seed Spine
    "Operational Seed Spine explains why a seed route and work capsule were selected.",
    "Field Selection Spine scores work context against review axes and recommends a dominant routing field.",
    "Odin ranks candidate routes by coherence.",
    # FINAL-PR-08 Projection Candidate Spine
    "Projection Candidate Spine organizes candidate artifacts on the materialization ladder and links them to trace receipts.",
    "Odin organizes candidate work into structured sets.",
    # FINAL-PR-09++ Operational Spine
    "Operational Spine connects Universal Work, small-model route plans, ModelWorkPackets, candidate artifacts, Final Gate, and trace receipts without app apply or live model inference claims.",
    "Odin organizes local candidate work into a safe structured response.",
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

<!-- FINAL-PR-02: Model Picker -->
<div id="model-picker-section" class="section">
  <div class="label">Model Picker</div>
  <p>Choose how Odin should prepare work.</p>
  <p class="note">No model inference runs in this PR. All options are placeholder/candidate-only.</p>
  <div id="model-option-none" class="dev-row">
    <span class="chip ok">None</span> &#8212; No model selected. Odin returns deterministic candidates only.
  </div>
  <div id="model-option-mock" class="dev-row">
    <span class="chip pending">Mock</span> &#8212; Mock mode returns deterministic demo candidates. No model binary is called.
  </div>
  <div id="model-option-local-candidate" class="dev-row">
    <span class="chip deferred">Local candidate</span> &#8212; Local candidate provider is listed but not executed yet. Deferred to FINAL-PR-04.
  </div>
  <div id="provider-status-panel" class="dev-row">
    <span class="chip deferred">Provider status</span> &#8212; No provider active. No API key in use. No binary running.
  </div>
</div>

<!-- FINAL-PR-02: Connected Apps -->
<div id="connected-apps-section" class="section">
  <div class="label">Connected Apps</div>
  <p>Connected apps are demo slots only. No real app is connected.</p>
  <div id="connected-app-slot-generic" class="dev-row">
    <span class="chip deferred">Generic App Slot</span> &#8212; Placeholder. Not connected. No app apply. No external send.
  </div>
  <div id="connected-app-slot-browser" class="dev-row">
    <span class="chip deferred">Browser Slot</span> &#8212; Placeholder. Not connected.
  </div>
  <div id="connected-app-slot-file" class="dev-row">
    <span class="chip deferred">File Slot</span> &#8212; Placeholder. Not connected.
  </div>
  <div id="app-bridge-status" class="dev-row">
    <span class="chip deferred">App Bridge</span> &#8212; Demo placeholder only. No real app bridge runtime. Apps still decide what to apply.
  </div>
</div>

<!-- FINAL-PR-02: Demo Universal Work -->
<div id="demo-universal-work-section" class="section">
  <div class="label">Demo Universal Work</div>
  <p>Odin can accept a demo Universal Work request and return a candidate response packet.</p>
  <p class="note">This is a deterministic demo. No model is called. No provider is executed. No app apply.</p>
  <div id="demo-work-input" class="dev-row">
    <span class="chip ok">Input</span> &#8212; Raw demo input accepted (GET/POST /demo/universal-work.json).
  </div>
  <div id="demo-submit-placeholder" class="dev-row">
    <span class="chip pending">Submit</span> &#8212; POST to /demo/universal-work or GET /demo/universal-work.json for demo response.
  </div>
  <div id="demo-handoff-context" class="dev-row">
    <span class="chip ok">Handoff Context</span> &#8212; Profile: generic. Intent: demo_universal_work. Forbidden: provider, model, apply, send.
  </div>
  <div id="demo-universal-work-packet" class="dev-row">
    <span class="chip ok">Universal Work Packet</span> &#8212; Kind: demo. Status: compiled. No model execution.
  </div>
  <div id="demo-candidate-artifact" class="dev-row">
    <span class="chip ok">Candidate Artifact</span> &#8212; Deterministic demo candidate. App reviews and optionally applies.
  </div>
  <div id="demo-response-packet" class="dev-row">
    <span class="chip ok">Response Packet</span> &#8212; Status: ok_with_known_gaps. Candidate-only. Not final truth.
  </div>
  <div id="demo-proof-gap-status" class="dev-row">
    <span class="chip pending">Proof Gaps</span> &#8212; Not proven: model_inference, provider_execution, real_app_bridge_runtime, app_apply, external_send, qirc_core_runtime.
  </div>
</div>

<!-- FINAL-PR-03: QIRC Dev Mode viewers -->
<div id="qirc-channel-viewer" class="section">
  <div class="label">QIRC Channel Viewer</div>
  <p>QIRC coordinates locally. Odin gates. Apps decide.</p>
  <p class="note">Local-only channels: GET /qirc/channels.json. Candidate-only. No public network. No federation.</p>
</div>

<div id="qirc-event-viewer" class="section">
  <div class="label">QIRC Event Viewer</div>
  <p class="note">All local QIRC bus events: GET /qirc/events.json. Candidate-only. No app apply. No external send.</p>
</div>

<div id="activity-timeline" class="section">
  <div class="label">Activity Timeline</div>
  <p>Activity timeline shows local candidate events.</p>
  <p class="note">GET /activity.json returns local activity events from #odin.activity channel. Candidate-only.</p>
</div>

<div id="trace-viewer" class="section">
  <div class="label">Trace Viewer</div>
  <p class="note">GET /traces.json returns trace events from #odin.trace. Local-only. Candidate-only.</p>
</div>

<div id="receipt-viewer" class="section">
  <div class="label">Receipt Viewer</div>
  <p class="note">GET /receipts.json returns receipt events from #odin.receipt. Local-only. Candidate-only.</p>
</div>

<div id="handoff-chain-viewer" class="section">
  <div class="label">Handoff Chain Viewer</div>
  <p class="note">Handoff chain events from #odin.handoff. Local-only. Candidate-only.</p>
</div>

<div id="surface-map-viewer" class="section">
  <div class="label">Surface Map Viewer</div>
  <p class="note">Surface map: 8765 (canonical entry), 8877 (local API), 8878 (browser shell). GET /dev/status.json.</p>
</div>

<div id="proof-gap-viewer" class="section">
  <div class="label">Proof Gap Viewer</div>
  <p>Dev Mode: QIRC channels, events, traces, receipts, handoff chain.</p>
  <p class="note">Not proven: provider_execution, model_inference, public_qirc_network, qirc_federation, app_apply, app_state_mutation, external_send, production_readiness, security_certification.</p>
</div>

<!-- FINAL-PR-04: Provider Probe + Runtime Security Smoke -->
<div id="provider-policy-status" class="section">
  <div class="label">Provider Policy Status</div>
  <p>Provider probe checks readiness only.</p>
  <p class="note">Probe does not execute. Policy gates provider readiness. No model is executed. No API keys are read. No external network is used.</p>
</div>

<div id="provider-probe-panel" class="section">
  <div class="label">Provider Probe Panel</div>
  <p>No model is executed.</p>
  <p class="note">GET /providers.json for policy list. GET /providers/probe.json for readiness status. POST /providers/probe for safe local probe. Candidate-only results.</p>
</div>

<div id="provider-probe-results" class="section">
  <div class="label">Provider Probe Results</div>
  <p class="note">Probe results are candidate-only readiness signals. Provider status is not model quality proof. Local provider discovery does not imply inference.</p>
</div>

<div id="provider-execution-boundary" class="section">
  <div class="label">Provider Execution Boundary</div>
  <p>Provider execution remains disabled by default.</p>
  <p class="note">execution_allowed=false for all providers. No ollama run/chat/generate. No llama-cli model load. App-owned apply boundary intact.</p>
</div>

<div id="runtime-security-smoke-status" class="section">
  <div class="label">Runtime Security Smoke</div>
  <p class="note">GET /security/runtime-smoke.json. This is a smoke check, not a security certification. Checks provider/model/network/secrets/app-apply boundaries.</p>
</div>

<div id="secret-scan-status" class="section">
  <div class="label">Secret Scan Status</div>
  <p>No API keys are read.</p>
  <p class="note">No OPENAI_API_KEY. No ANTHROPIC_API_KEY. No provider credentials. Forbidden markers scanned in provider/security source files.</p>
</div>

<div id="network-boundary-status" class="section">
  <div class="label">Network Boundary Status</div>
  <p class="note">No external network. No public bind. No LAN/WAN QIRC. No federation. Localhost-only operation.</p>
</div>

<div id="qirc-provider-events-status" class="section">
  <div class="label">QIRC Provider Events</div>
  <p class="note">Provider probe emits local events on #odin.model channel. Local-only. Candidate-only. No public QIRC transport. No federation.</p>
</div>

<div id="execution-gate-status" class="section">
  <div class="label">Execution Gate Status</div>
  <p>No real model is executed by default.</p>
  <p class="note">GET /execution-gate/status.json. mock_execution_allowed=true. local_candidate_execution_allowed=false. remote_execution_allowed=false. api_key_reads_allowed=false.</p>
</div>

<div id="mock-execution-panel" class="section">
  <div class="label">Mock Execution Panel</div>
  <p>Mock execution is local and deterministic.</p>
  <p>Mock execution is not model inference.</p>
  <p class="note">POST /execution-gate/mock. Sends a deterministic candidate response. No model, no subprocess, no inference. Apps still decide what to apply.</p>
</div>

<div id="mock-execution-result" class="section">
  <div class="label">Mock Execution Result</div>
  <p class="note">Mock execution result is a candidate packet. artifact_kind: odin_mock_execution_response_packet. candidate_only: true. local_only: true. app_apply: false.</p>
</div>

<div id="local-candidate-policy-status" class="section">
  <div class="label">Local Candidate Policy Status</div>
  <p>Local candidate execution is disabled by default.</p>
  <p class="note">ollama_candidate and llama_cpp_candidate require explicit future gate. ci_must_not_require_binary: true. No Ollama generate/chat/embed/run. No llama.cpp model run.</p>
</div>

<div id="execution-boundary-status" class="section">
  <div class="label">Execution Boundary Status</div>
  <p>Remote providers and API keys are not used.</p>
  <p class="note">remote_execution_allowed=false. api_key_reads_allowed=false. external_network_allowed=false. external_send_allowed=false. app_apply_allowed=false.</p>
</div>

<div id="proof-chain-status" class="section">
  <div class="label">Proof Chain Status</div>
  <p>Proof chain links receipts but does not prove production readiness.</p>
  <p class="note">GET /execution-gate/proof-chain.json. References FINAL-PR-01 through FINAL-PR-05. candidate_only: true. not_proven includes production_readiness, live_model_inference.</p>
</div>

<div id="final-pr-ladder-scaffold-status" class="section">
  <div class="label">FINAL-PR Ladder Scaffold Status</div>
  <p>FINAL-PR Ladder scaffold is not a full Thor replacement.</p>
  <p class="note">GET /final-pr-ladder/scaffold.json. Scaffold only — does not generate full prompts. claim_boundary: final_pr_ladder_scaffold_not_full_prompt_compiler.</p>
</div>

<div id="model-execution-warning" class="section">
  <div class="label">Model Execution Warning</div>
  <p>No real model is executed by default.</p>
  <p>Mock execution is not model inference.</p>
  <p class="note">This hub does not perform real model inference. All execution is deterministic mock only. Real local model execution requires explicit future gate (FINAL-PR-06+). Remote providers are permanently forbidden in this PR.</p>
</div>

<div id="y-pattern-spine-status" class="section">
  <div class="label">Y Pattern Spine</div>
  <p>Odin prepares work with compact route hints.</p>
  <p><span class="chip ok">available</span> Y Pattern Spine: route hints, work capsules, token budgets, materialization levels.</p>
  <p class="note">GET /demo/y-route.json for demo route explanation. Dev Mode: Y Pattern Spine explains why a route/capsule was selected.</p>
</div>

<div id="operational-seed-spine-status" class="section">
  <div class="label">Operational Seed Spine</div>
  <p>Odin prepares work with compact route hints.</p>
  <p><span class="chip ok">available</span> Operational Seed Spine: available</p>
  <p>Operational Seed Spine explains why a seed route and work capsule were selected.</p>
  <p class="note">GET /demo/seed-route.json for deterministic seed route demo. Seeds are routing signals, not agents. Role profiles are contracts, not personas. QIRC hints are hint-only.</p>
</div>

<div id="dev-mode-entry" class="section dev">
  <div class="label">Dev Mode</div>
  <p>Dev Mode contains traces, receipts, proof gaps, validators, and handoff details.</p>
  <details>
    <summary>Expand Dev Mode</summary>
    <div class="dev-row" id="dev-qirc-status">QIRC status: placeholder &#8212; not running</div>
    <div class="dev-row" id="dev-handoff-first-status">Handoff-First status: placeholder &#8212; not running</div>
    <div class="dev-row" id="dev-trace-status">Trace/Receipt status: placeholder &#8212; viewer deferred to FINAL-PR-03</div>
    <div class="dev-row" id="dev-validator-status">Validator status: run <code>python -m odin.cli validate-simple-local-hub</code> or <code>python -m odin.cli validate-final-pr-02-model-apps-demo</code></div>
    <div class="dev-row" id="dev-proof-gaps">Proof gaps: provider_execution, model_inference, qirc_core_runtime, handoff_compiler_runtime, app_bridge_runtime, app_apply, app_state_mutation, external_send, public_network, production_readiness, security_certification</div>
    <div class="dev-row" id="dev-support-bundle">Support bundle: placeholder &#8212; run <code>python -m odin.cli emit-support-bundle</code></div>
    <div class="dev-row" id="dev-handoff-viewer">Handoff viewer: placeholder &#8212; deep viewer deferred to FINAL-PR-03</div>
    <div class="dev-row" id="dev-y-pattern-spine">Y Pattern Spine: available. <code>python -m odin.cli explain-y-route --demo</code> returns route hint. <code>python -m odin.cli validate-y-pattern-spine</code>. GET /demo/y-route.json. candidate_only: true. Pattern = hint/route/capsule, not authority.</div>
    <div class="dev-row" id="dev-operational-seed-spine">Operational Seed Spine: available. <code>python -m odin.cli explain-seed-route --demo</code> returns seed route. <code>python -m odin.cli validate-operational-seed-spine</code>. GET /demo/seed-route.json. candidate_only: true. Seeds are routing signals, not agents.</div>
    <div class="dev-row" id="dev-demo-flow">Demo flow: Raw demo input &#8594; Handoff Context &#8594; Universal Work &#8594; Candidate Artifact &#8594; Response Packet. No provider execution. No model inference. No app apply. No external send.</div>
  </details>
</div>

<div id="field-selection-spine-section" class="section">
  <div class="label">Field Selection Spine</div>
  <span class="chip ok">Available</span>
  <p>Odin ranks candidate routes by coherence.</p>
  <p class="note">Dev Mode: Field Selection Spine scores work context against review axes and recommends a dominant routing field.</p>
</div>

<div id="projection-candidate-spine-section" class="section">
  <div class="label">Projection Candidate Spine</div>
  <span class="chip ok">Available</span>
  <p>Odin organizes candidate work into structured sets.</p>
  <p class="note">Dev Mode: Projection Candidate Spine organizes candidate artifacts on the materialization ladder and links them to trace receipts. GET /demo/projection-candidate.json. candidate_only: true. No model inference. No app apply.</p>
</div>

<div id="operational-spine-section" class="section">
  <div class="label">Operational Spine (FINAL-PR-09++)</div>
  <span class="chip ok">Available</span>
  <p>Odin organizes local candidate work into a safe structured response.</p>
  <p class="note">Dev Mode: Operational Spine connects Universal Work, small-model route plans, ModelWorkPackets, candidate artifacts, Final Gate, and trace receipts without app apply or live model inference claims. GET /operational-spine/demo.json. candidate_only: true. No model inference. No app apply. Provider seam disabled by default.</p>
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
