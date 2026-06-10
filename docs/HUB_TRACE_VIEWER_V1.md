# Hub Trace Viewer V1

**Version:** 1.0
**Status:** Candidate specification — static viewer surfaces defined.
**Claim boundary:** trace_viewer_candidate_only_local_only_no_event_mutation_no_public_bus_no_raw_payload
**LRH PR:** LRH-PR-09 — Bus / Worklet / Atom Trace Viewer

---

## Purpose

The Hub Trace Viewer provides read-only, local-only inspection of bus events, worklet traces, work atom traces and runtime digests. It is a debugging and traceability surface for the Odin Local Runtime Hub, not a bus control panel.

---

## Surfaces

### Bus Event Timeline

Displays bus events fetched from `/v1/events` in a metadata-first, read-only timeline.

Shown per event:
- `event_id`
- `event_type`
- `timestamp` / `sequence` if available
- `source`
- `target`
- `status`
- `claim_boundary`
- `candidate_only` marker
- Redacted payload summary (raw payload never shown)
- Proof boundary / known gap marker

If no bus event list endpoint is available: renders a fixture-compatible placeholder and documents missing list endpoint as a proof gap.

### Worklet Trace View

Displays worklet metadata in read-only form.

Shown per worklet:
- `worklet_id`
- `worklet_type` / name
- `status` / state
- Input/output metadata (safe, redacted)
- `known_non_proofs` / proof boundaries

No execute, retry, apply, or delete controls exist.

### Work Atom Trace View

Displays work atom metadata in read-only form.

Shown per atom:
- `atom_id`
- `atom_kind`
- `status`
- `dependencies` (safe)
- `digest` / trace ID metadata
- Redacted preview

No mutate, delete, or apply controls exist.

### Runtime Digest View

Displays local runtime receipt information:
- `runtime_digest`
- `trace_digest`
- `event_count` (if available)
- `worklet_count` (if available)
- `atom_count` (if available)
- Local receipt status
- Not-production-certification warning

### Local-Only Trace Filters

Filters are applied in the browser — no remote search, no network fetch outside localhost.

Allowed filter fields:
- Event type
- Status
- Source
- Target

Forbidden filter/action:
- Remote search
- Network fetch outside localhost
- Upload trace
- Send trace externally
- Execute filtered worklets
- Mutate filtered events

---

## Metadata-First Trace Display

All trace surfaces display metadata only. Raw sensitive payloads are never shown by default:
- Any field with a name containing `secret`, `token`, `password`, `key`, `credential`, `auth`, `private`, `raw_payload`, `payload_raw`, `sensitive`, or `payload` is redacted as `[REDACTED — raw sensitive payload not displayed by default]`.
- Nested objects are shown as `[object — metadata-first display only]`.

---

## Redacted Payload Preview Policy

Raw sensitive payloads are not displayed by default. Redaction is enforced in the viewer's JavaScript before rendering. No button or toggle exists to reveal raw sensitive payloads. This does not certify full payload safety for all data paths.

---

## What This Proves

- `trace_viewer_static_files_exist`
- `trace_viewer_references_v1_events`
- `trace_viewer_references_v1_proof_gaps`
- `trace_viewer_references_v1_status`
- `trace_viewer_references_v1_health`
- `bus_event_timeline_surface_present`
- `worklet_trace_surface_present`
- `work_atom_trace_surface_present`
- `runtime_digest_surface_present`
- `local_only_trace_filters_present`
- `metadata_first_display_enforced`
- `redacted_payload_policy_present`
- `no_event_mutation_controls`
- `no_worklet_execution_controls`
- `no_atom_mutation_controls`
- `no_external_send_controls`
- `no_public_bus_controls`
- `raw_sensitive_payload_not_displayed_by_default`

---

## What This Does Not Prove

- **Not production readiness.** This viewer does not prove the runtime is production-ready.
- **Not security certification.** This viewer does not certify security.
- **Not live browser runtime E2E.** No live end-to-end browser test has been run.
- **Not full bus backend coverage.** The `/v1/events` endpoint may not expose the full bus.
- **Not full worklet backend coverage.** Worklet list APIs are not assumed complete.
- **Not full work atom backend coverage.** Atom list APIs are not assumed complete.
- **Not raw sensitive payload safety certification.** Redaction is client-side only; full payload safety requires backend redaction guarantees not proven here.
- **Not event mutation authority.** The viewer has no authority to mutate events.
- **Not worklet execution authority.** The viewer has no authority to execute worklets.
- **Not atom mutation authority.** The viewer has no authority to mutate atoms.
- **Not public bus exposure proof.** The bus is not publicly exposed by this viewer.
- **Not external send authority.** The viewer does not send data externally.
- **Not provider execution proof.** No model provider execution is claimed.
- **Not app state mutation proof.** No app state is mutated.
- **Not public network API proof.** No public network API is created by this viewer.

---

## Proof Boundaries

```
not_production_readiness_certification
not_security_certification
not_event_mutation_proof
not_bus_publish_replay_delete_ack_proof
not_public_bus_exposure_proof
not_lan_wan_trace_endpoint_proof
not_worklet_execution_proof
not_work_atom_mutation_proof
not_raw_sensitive_payload_safety_certification
not_live_browser_runtime_e2e
not_provider_execution_proof
not_public_network_api_proof
not_app_state_mutation_proof
not_external_send_authority_proof
not_live_model_inference_proof
not_model_quality_proof
not_full_bus_backend_coverage
not_full_worklet_backend_coverage
not_full_work_atom_backend_coverage
```

---

## Explicit Boundary Statements

This does not mutate bus events.
This does not publish, replay, delete or acknowledge bus events.
This does not execute worklets.
This does not mutate work atoms.
This does not expose a public bus.
This does not add LAN/WAN trace endpoints by default.
This does not display raw sensitive payloads by default.
This does not prove production readiness.
This does not prove security certification.
This is not a hosted cloud UI.
This is not a public network API.
This does not grant app apply authority.
This does not send externally.
This does not execute providers.
This viewer is local-only and read-only.

---

## Forbidden Scope

This document does not claim:
- Public bus exposure
- LAN/WAN trace endpoint
- Event mutation authority
- Worklet execution authority
- Atom mutation authority
- Production readiness
- Security certification
- External send authority
- Provider execution
- Hidden upload
- Full Universal Work Playground (LRH-PR-11)
- External App Bridge (LRH-PR-12)
- Live model integration

---

## Next Recommended PR

LRH-PR-10 — Provider / Worker / Pre-LLM Inspector
