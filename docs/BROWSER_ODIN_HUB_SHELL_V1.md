# Browser Odin Hub Shell v1

**Claim boundary:** `browser_hub_shell_candidate_only_local_only_no_apply_no_external_send_no_provider_execution`

**LRH-PR-06 deliverable.**

---

## Purpose

This document specifies the Browser Odin Hub Shell — a local static web shell that surfaces
the Odin Local Runtime Hub API in a browser without adding write/apply controls, external-send
controls, remote networking defaults, or provider execution.

---

## Local-Only Browser Shell

The Browser Odin Hub Shell is a set of static HTML/CSS/JS files served locally.

- Served from `odin/hub/static/` by the local runtime HTTP server
- No CDN, no external fonts, no remote asset references
- Defaults to `http://127.0.0.1:8877` as API base URL
- Warns visibly on non-localhost API base URLs
- No WebSocket or long-poll to remote endpoints by default

---

## Static Asset Serving

The shell consists of:

| File | Purpose |
|------|---------|
| `odin/hub/static/index.html` | Main HTML shell with boundary banner, nav, panels |
| `odin/hub/static/styles.css` | Local stylesheet (no external fonts or CDN) |
| `odin/hub/static/app.js` | Browser JS that polls local API endpoints |
| `odin/hub/api_client.js` | Reusable JS API client against `/v1/*` |

The `serve-browser-hub` CLI command serves these static files locally on `127.0.0.1` only.

---

## JS API Client

`odin/hub/api_client.js` provides:

| Method | Endpoint |
|--------|----------|
| `getHealth()` | `GET /v1/health` |
| `getStatus()` | `GET /v1/status` |
| `getProviders()` | `GET /v1/providers` |
| `getProofGaps()` | `GET /v1/proof-gaps` |
| `getEvents()` | `GET /v1/events` |
| `getSession(id)` | `GET /v1/sessions/:id` |
| `getCandidate(id)` | `GET /v1/candidates/:id` |

The client rejects or warns on non-localhost base URLs.
Default base URL: `http://127.0.0.1:8877`.

---

## Health Panel

Displays `/v1/health` response. Shows `candidate_only: true` when set.

---

## Status Panel

Displays `/v1/status` response.

---

## Providers Read-Only Panel

Displays `/v1/providers` response. Shows enabled/disabled status per provider.
Read-only — no credential entry, no provider activation controls.

---

## Proof Gaps Surface

Displays `/v1/proof-gaps` response. Shows each named proof gap.

---

## Navigation Shell

Navigation links to all active and placeholder panels:

- Health
- Status
- Providers (read-only)
- Candidates (placeholder → LRH-PR-08)
- Proof Gaps
- Events (placeholder → LRH-PR-09)
- Universal Work Playground (placeholder → LRH-PR-11)

---

## Universal Work Playground Placeholder

**The Universal Work Playground is a navigation entry / disabled placeholder only in LRH-PR-06.**

The actual Universal Work Playground implementation is in LRH-PR-11.

In this PR the placeholder is present as a navigation item and section with a clear note that
full implementation is in a later ladder slice.

---

## What This Proves

- Static shell files exist and are local-only
- JS API client defaults to `127.0.0.1:8877`
- JS API client references `/v1/health`, `/v1/status`, `/v1/proof-gaps`
- No apply controls, no external-send controls
- Boundary banner is present in `index.html`
- Navigation shell includes health, status, proof-gaps, candidates, events navigation items

---

## What This Does Not Prove

This is not a hosted cloud UI.

This is not a public network API.

This does not grant app apply authority.

This does not send externally.

This does not execute providers.

This does not prove auth/security certification.

This does not prove production readiness.

The Universal Work Playground is placeholder/entry only in LRH-PR-06.

---

## Proof Boundaries

```
not_production_readiness_certification
not_hosted_cloud_ui_proof
not_auth_security_certification
not_live_browser_runtime_e2e
not_provider_execution_proof
not_public_network_api_proof
not_app_state_mutation_proof
not_external_send_authority_proof
not_live_model_inference_proof
not_model_quality_proof
```

---

## No Apply Controls

The shell has no apply button, no apply form, no apply JS function that submits changes
to the app. All app state changes remain app-owned.

---

## No External Send Controls

The shell has no external-send button, no external-send form, no external-send JS function.
All external sends remain app-owned.

---

## No Remote Network Default

The API client defaults to `http://127.0.0.1:8877`. A non-localhost URL triggers an
explicit warning/error. No remote network calls are made by default.

---

## No Provider Execution

The shell reads provider cards from the API (read-only). It does not execute, invoke,
or credential providers. Providers remain workers with disabled-by-default posture.

---

## CLI Commands

```bash
python -m odin.cli serve-browser-hub --host 127.0.0.1 --port 8878
python -m odin.cli validate-browser-hub-shell
python -m odin.cli prove-browser-hub --shell-only
```

---

## Dependencies on Prior PRs

- LRH-PR-04: Doctor/bootstrap for runtime health context
- LRH-PR-05: Localhost API contract (`/v1/*` endpoints)
