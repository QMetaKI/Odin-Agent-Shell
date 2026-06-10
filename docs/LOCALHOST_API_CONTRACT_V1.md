# Odin Localhost API Contract v1

**Version:** 7.1 / LRH-PR-05
**Claim boundary:** local_api_candidate_only_no_app_apply_no_external_send_no_wan_lan_claim

---

## Purpose

This document defines the hardened v1 localhost-only API contract for Odin.
It describes what host apps can safely call, what each endpoint returns,
and what no endpoint ever does.

This is not a public network API.
This does not grant app apply authority.
This does not send externally.
This does not send raw app state to models.
This does not provide provider credentials.
This does not prove live model inference.
This does not prove production readiness.

---

## Base URL and Binding

**Default base URL:** `http://127.0.0.1:8877`

Odin binds to localhost-only by default.
`0.0.0.0` and `::` are blocked by default.
Only `127.0.0.1`, `localhost`, and `::1` are permitted.
WAN/LAN network access is not enabled by default.

---

## Endpoint List

| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/health | Runtime health status |
| GET | /v1/status | Runtime store status |
| GET | /v1/providers | Available provider cards |
| POST | /v1/universal-work | Submit Universal Work (candidate-only) |
| GET | /v1/sessions/{id} | Read session record |
| GET | /v1/candidates/{id} | Read candidate artifact |
| GET | /v1/events | Read local bus events |
| GET | /v1/proof-gaps | Read proof gap summary |

---

## Endpoint Specifications

### GET /v1/health

Returns runtime health status.

```json
{
  "artifact_kind": "odin_localhost_api_health",
  "protocol_version": "7.1",
  "status": "ok",
  "runtime": "candidate",
  "network_scope": "localhost_only",
  "version": "0.8.7",
  "candidate_only": true,
  "app_owned_apply": true,
  "external_send_default": false,
  "claim_boundary": "local_api_candidate_only_no_app_apply_no_external_send_no_wan_lan_claim"
}
```

### GET /v1/status

Returns runtime store status including candidate, session, and event counts.

```json
{
  "artifact_kind": "odin_localhost_api_status",
  "candidate_count": 0,
  "session_count": 0,
  "bus_event_count": 0,
  "candidate_only": true,
  "app_owned_apply": true,
  "external_send_default": false,
  "claim_boundary": "..."
}
```

### GET /v1/providers

Returns provider cards. Provider cards are metadata, not live inference proof.

```json
{
  "artifact_kind": "odin_localhost_api_providers",
  "providers": [...],
  "candidate_only": true,
  "claim_boundary": "provider_cards_not_live_provider_proof"
}
```

### POST /v1/universal-work

Submit Universal Work. Returns a candidate-only result.

Request body:

```json
{
  "work": { "work_id": "...", "work_intent": {...}, "output_contract": {...} },
  "caller_manifest": {...},
  "seed_pack": {...},
  "pattern_mine": {...}
}
```

Response:

```json
{
  "runtime_status": "ok",
  "session_id": "...",
  "selected_candidate_id": "...",
  "candidates": [...],
  "candidate_only": true,
  "app_owned_apply": true,
  "external_send_default": false,
  "proof_boundaries": ["not_production_readiness_certification", ...],
  "claim_boundary": "..."
}
```

**Invariants:**
- Does NOT apply app state
- Does NOT send externally
- Does NOT call live model/provider unless deterministic local behavior exists
- Returns `candidate_only: true`
- Returns `app_owned_apply: true`

### GET /v1/sessions/{id}

Read a session record by session ID. Returns 404 with structured error if not found.

### GET /v1/candidates/{id}

Read a candidate artifact by candidate ID. Returns 404 with structured error if not found.
App owns apply. The candidate is not applied by Odin.

### GET /v1/events

Returns local semantic bus events. Local-only, candidate-only.

```json
{
  "artifact_kind": "odin_localhost_api_events",
  "events": [...],
  "candidate_only": true,
  "local_only": true,
  "claim_boundary": "..."
}
```

### GET /v1/proof-gaps

Returns known proof gaps and proof boundary declarations.

```json
{
  "artifact_kind": "odin_localhost_api_proof_gaps",
  "proof_boundaries": ["not_production_readiness_certification", ...],
  "known_gaps": ["no_live_model_inference_proof", ...],
  "candidate_only": true,
  "note": "..."
}
```

---

## Request/Response Schema

All schemas are in `schemas/v7_1/`:

- `localhost_api_health.schema.json`
- `localhost_api_status.schema.json`
- `localhost_api_providers.schema.json`
- `localhost_api_universal_work_request.schema.json`
- `localhost_api_universal_work_response.schema.json`
- `localhost_api_session.schema.json`
- `localhost_api_candidate.schema.json`
- `localhost_api_events.schema.json`
- `localhost_api_proof_gaps.schema.json`
- `localhost_api_error.schema.json`

---

## Structured Errors

All errors use this shape:

```json
{
  "error": true,
  "artifact_kind": "odin_local_api_error",
  "protocol_version": "7.1",
  "status": "blocked",
  "code": "not_found",
  "message": "human-readable message",
  "details": {},
  "candidate_only": true,
  "claim_boundary": "..."
}
```

- No tracebacks in public API responses
- No secret values in errors

---

## Proof Gaps

The API exposes its own proof gaps via `/v1/proof-gaps`. Known gaps:

| Gap | Notes |
|-----|-------|
| no_live_model_inference_proof | Local API uses deterministic scaffold, not live model |
| no_production_readiness_proof | This is not a production API certification |
| no_public_network_api_proof | Localhost-only; no WAN/LAN access |
| no_app_state_mutation_proof | Odin never mutates app state |
| no_external_send_authority_proof | Odin never sends externally |
| no_provider_credential_proof | No provider credentials in API |
| no_windows_host_proof | Not a Windows service/installer |
| no_security_certification | Not a security audit certificate |

---

## Candidate Artifacts

Candidate artifacts are read-only outputs from Odin.
They are not applied by Odin.
App owns apply, state, and external sends.

---

## Forbidden Endpoints

The following routes return 404 and are permanently blocked:

- POST /v1/apply
- POST /v1/app-apply
- POST /v1/external-send
- GET/POST /v1/app/state
- POST /v1/network-enable
- POST /v1/provider-credentials
- POST /v1/raw-app-state-to-model

---

## What This Proves

- The API contract is localhost-only by default
- All responses include `candidate_only: true` where relevant
- All responses include `claim_boundary`
- Structured errors follow a consistent shape
- Forbidden endpoints return 404
- Universal Work returns `app_owned_apply: true`

## What This Does Not Prove

- Not production readiness certification
- Not Windows service, tray, or installer proof
- Not signed installer proof
- Not live model inference proof
- Not model quality proof
- Not security certification
- Not public network API proof
- Not app-state mutation proof
- Not external send authority proof
- Not provider credential proof

---

## Proof Boundaries

```
not_production_readiness_certification
not_windows_service_tray_installer_proof
not_signed_installer_proof
not_live_model_inference_proof
not_model_quality_proof
not_security_certification
not_public_network_api_proof
not_app_state_mutation_proof
not_external_send_authority_proof
not_provider_credential_proof
```
