# Hub Candidate Store Viewer v1

**PR:** LRH-PR-08 — Sessions, Candidates, Store and Proof Gap Viewer
**Claim boundary:** `candidate_store_viewer_candidate_only_local_only_no_apply_no_external_send_no_store_mutation_no_raw_payload`

---

## Purpose

The Candidate Store Viewer is a read-only, local-only viewer for inspecting candidate artifacts, session metadata, store metadata, and proof gaps from the Odin Local Runtime Hub.

The viewer exposes four surfaces: Sessions view, Candidate Artifact view, Store Metadata view, and Proof Gap viewer. Every surface carries an explicit candidate-only boundary banner and a not-applied truth warning.

The viewer exists to let users inspect candidate-only output without treating it as applied truth.

---

## Sessions View

Shows:

- Session ID
- Status
- Created / updated metadata if available
- Candidate count if available
- `claim_boundary` marker
- `candidate_only` marker

Uses `/v1/sessions/{id}` where applicable.

If no session endpoint is available, the viewer renders a fixture-compatible placeholder and documents the missing session list backend as a proof gap.

**Proof gap:** full session list backend not proven.

---

## Candidate Artifact Viewer

Shows:

- `candidate_id`
- `session_id` if available
- Candidate status
- `artifact_kind`
- `claim_boundary`
- `candidate_only: true` marker
- `app_owned_apply: true` marker
- `proof_boundaries`
- Not-applied truth warning
- Safe summary / redacted preview only

Uses `/v1/candidates/{id}`.

Raw sensitive payloads are not displayed by default. Any field whose key contains `secret`, `token`, `password`, `key`, `credential`, `auth`, `private`, `raw_payload`, `payload_raw`, or `sensitive` is redacted.

**Proof gap:** full candidate backend coverage not proven.

---

## Store Metadata Viewer

Shows:

- Store status if available
- Record IDs or metadata if safe
- Counts / categories if safe
- Readonly badge
- No mutation controls

Store APIs are not assumed. If store APIs are absent, the viewer renders a static/fixture-compatible placeholder and documents the missing store endpoint as a proof gap.

**Proof gap:** full store backend coverage not proven.

---

## Proof Gap Viewer

Shows:

- Proof gaps list from `/v1/proof-gaps`
- Known non-proofs
- Missing capabilities
- Proof boundaries
- Next recommended PR

Displaying proof gaps does not close them. The viewer does not resolve, certify, or close any gap.

---

## Candidate-Only Boundary Banner

Every view in the Candidate Store Viewer includes a boundary banner with:

- Candidate-only
- Not applied truth
- App-owned apply
- No app apply
- No external send
- No store mutation
- No raw sensitive payload display

---

## Not-Applied Truth Warning

Every candidate surface includes an explicit warning:

> "Not applied truth — candidate artifacts are candidate-only. The app owns apply, state, external sends, and domain authority."

---

## Raw Sensitive Payload Protection

Raw sensitive payloads are never displayed by default.

The viewer automatically redacts any field whose key matches a known sensitive-key pattern.

No raw payload reveal button exists.
No unsafe payload toggle exists.
No raw payload download link exists.

---

## What This Proves

When `validate-candidate-store-viewer` passes:

- `candidate_store_viewer.js` exists and loads in index.html
- All required viewer surfaces are present
- The viewer references `/v1/candidates`, `/v1/sessions`, `/v1/proof-gaps`
- The candidate-only boundary banner is present
- The not-applied truth warning is present
- No forbidden interactive controls exist
- No apply, external-send, or store-mutation controls exist
- Raw sensitive payloads are not displayed by default
- Documentation includes required boundary phrases

---

## What This Does Not Prove

This does not apply candidate artifacts.

This does not show candidates as applied truth.

This does not mutate the runtime store.

This does not send externally.

This does not display raw sensitive payloads by default.

This does not close proof gaps by displaying them.

This does not prove production readiness.

This is not a hosted cloud UI.

This is not a public network API.

This does not grant app apply authority.

This does not execute model providers.

This is not a security certification.

This does not prove live browser runtime e2e.

This does not prove full session list backend.

This does not prove full candidate backend coverage.

This does not prove full store backend coverage.

---

## Proof Boundaries

```text
not_production_readiness_certification
not_candidate_application_proof
not_candidate_as_truth_proof
not_store_mutation_proof
not_raw_sensitive_payload_safety_certification
not_live_browser_runtime_e2e
not_provider_execution_proof
not_public_network_api_proof
not_app_state_mutation_proof
not_external_send_authority_proof
not_live_model_inference_proof
not_model_quality_proof
not_full_session_list_backend
not_full_candidate_backend_coverage
not_full_store_backend_coverage
```

---

## No Apply Action

No apply button exists. No apply form exists. No `applyCandidate()` or `apply()` JS function exists. The viewer cannot apply candidates.

## No Candidate Shown as Truth

All candidate surfaces carry explicit not-applied truth warnings. Candidates are presented as candidates, not as applied state.

## No Store Mutation

No store write, delete, or mutation controls exist. The store viewer is strictly metadata-first and read-only.

## No Raw Sensitive Payload Display

No raw payload reveal button exists. Sensitive fields are automatically redacted.

---

## CLI

```bash
python -m odin.cli validate-candidate-store-viewer
python -m odin.cli prove-browser-hub --candidates
```

`validate-candidate-store-viewer` is integrated into `validate-all`.

---

## Next Recommended PR

LRH-PR-09 — Bus / Worklet / Atom Trace Viewer
