# Hub Runtime Dashboard v1

**Claim boundary:** `hub_runtime_dashboard_candidate_only_local_only_no_apply_no_external_send_no_production_health_claim`

**LRH-PR-07 deliverable.**

---

## Purpose

This document specifies the Hub Runtime Dashboard — read-only, local-only dashboard surfaces
added to the Browser Odin Hub Shell in LRH-PR-07. The dashboard surfaces let users see
whether Odin is running, what runtime health says, what validation status says, what doctor
says, what is missing, what proof gaps remain, and how to export local diagnostics.

---

## Runtime Dashboard

The dashboard is read-only and local-only.

- Served from `odin/hub/static/dashboard.js` (loaded by `odin/hub/static/index.html`)
- No CDN, no external fonts, no remote asset references
- Defaults to `http://127.0.0.1:8877` as API base URL
- All data fetched from local `/v1/*` API endpoints
- No mutation through dashboard
- No apply controls
- No external-send controls
- No provider credential input

---

## Runtime Status Surface

Shows:

- `running` / `not-running` / `unknown` state
- API base URL (localhost only)
- Last health check status
- `candidate_only: true` when set
- `claim_boundary` when set

Does not claim the runtime is live unless there is a local API receipt.
Does not claim production readiness.

---

## Health Surface

Displays `/v1/health` response. Shows:

- `candidate_only: true` when set
- `claim_boundary` when set
- `known_non_proofs` when present
- Full JSON health response

Not a production health certification.
Localhost only.

---

## Validation Status Surface

Shows fixture-compatible or local-receipt-compatible status from `/v1/status`.
Renders validation keys and pass/fail state in a read-only table.

Does not claim live validation unless the UI has actual local receipts.

Expected surface IDs that tests must see:

- `validation-status` — validation status surface
- `validation-status-content` — content element

---

## Doctor Result Surface

Shows read-only doctor result rendered from local API data:

- Doctor status (ok / warn / error)
- Warnings
- Errors
- Failure reasons
- Recommended plan-only repair hint

Does not execute repair.
Does not mutate config.
Does not apply patches.

Expected surface IDs:

- `doctor-surface` — doctor surface container
- `doctor-content` — content element

---

## Support Bundle Surface

Shows:

- Support bundle is diagnostics-only
- Redaction applied — no secrets
- Local export only — not uploaded
- No hidden upload
- No remote send
- No diagnostic transport

Export command: `python -m odin.cli emit-support-bundle --out .odin_runtime/support --diagnostics-only`

Expected surface IDs:

- `support-bundle-surface` — support bundle surface container
- `support-bundle-content` — content element

The support bundle surface must include the phrases:
- `local-only`
- `diagnostics-only`
- `No hidden upload`

---

## Proof-Gap Summary

Shows:

- Known proof gaps from `/v1/proof-gaps`
- Known proof boundaries
- Explanation that displaying gaps does not close them

Does not claim proof gaps are closed.
Does not claim production readiness.

Expected surface IDs:

- `proof-gap-summary-surface` — surface container
- `proof-gap-summary-content` — content element

---

## Missing Capabilities / Not Proven

Explains what is not proven by this dashboard:

- `production_readiness`
- `production_health_certification`
- `hosted_cloud_dashboard`
- `live_browser_runtime_e2e`
- `provider_execution`
- `app_state_mutation`
- `external_send_authority`
- `hidden_diagnostic_upload_absence_beyond_static_scan`
- `live_model_inference`
- `model_quality`

Expected surface IDs:

- `missing-capabilities-surface` — surface container
- `missing-capabilities-content` — content element

---

## Local-Only Diagnostic Export

Export is local filesystem only.

- `python -m odin.cli emit-support-bundle --out .odin_runtime/support --diagnostics-only`
- Output: local `.odin_runtime/support/` directory
- No upload. No remote send. No hidden diagnostic transport.
- Redaction applied.

---

## What This Proves

- `dashboard_static_files_exist` — static dashboard files exist locally
- `dashboard_references_v1_health` — dashboard.js references `/v1/health`
- `dashboard_references_v1_status` — dashboard.js references `/v1/status`
- `dashboard_references_v1_proof_gaps` — dashboard.js references `/v1/proof-gaps`
- `no_apply_controls` — no apply button, no apply form, no apply JS function
- `no_external_send_controls` — no external-send button, no external-send JS function
- `support_bundle_surface_is_local_only` — support bundle panel is local-only/diagnostics-only
- `no_hidden_diagnostic_upload_controls` — no hidden upload endpoint or control

---

## What This Does Not Prove

**This is not a production health certification.**

**This is not a hosted cloud dashboard.**

**This does not upload diagnostics.**

**This does not grant app apply authority.**

**This does not send externally.**

**This does not execute providers.**

**This does not close proof gaps by displaying them.**

---

## Proof Boundaries

```
not_production_readiness_certification
not_production_health_certification
not_hosted_cloud_dashboard_proof
not_hidden_diagnostic_upload_proof
not_live_browser_runtime_e2e
not_provider_execution_proof
not_public_network_api_proof
not_app_state_mutation_proof
not_external_send_authority_proof
not_live_model_inference_proof
not_model_quality_proof
```

---

## No Mutation Controls

The dashboard has no apply button, no apply form, no apply JS function, no externalSend()
JS function, no provider credential input, no network enable toggle, no repair apply button,
no hidden upload, no remote upload, and no diagnostic upload endpoint or control.

All app state changes remain app-owned.

---

## No Hidden Upload

The support bundle export is local filesystem only.
No data is uploaded to any remote server.
No hidden diagnostic transport is present.

---

## No Production Health Claim

This dashboard does not certify that Odin is production-ready.
Health status shown is a local API receipt, not a deployment certification.

---

## CLI Commands

```bash
python -m odin.cli validate-hub-runtime-dashboard
python -m odin.cli prove-browser-hub --dashboard
```

---

## Dependencies on Prior PRs

- LRH-PR-05: Localhost API contract (`/v1/*` endpoints)
- LRH-PR-06: Browser Odin Hub Shell (static shell base)
