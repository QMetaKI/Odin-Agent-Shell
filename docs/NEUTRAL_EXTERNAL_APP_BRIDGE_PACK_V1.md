# Neutral External App Bridge Pack V1

**Claim boundary:** `neutral_external_app_bridge_pack_candidate_only_no_app_apply_no_external_send_no_credentials_no_hosted_bridge_no_public_gateway`

LRH-PR-12 — Local Runtime Hub ladder.

---

## Purpose

This pack shows how any host app can integrate with a locally running Odin instance without giving Odin app authority. The bridge is a contract and example set — not a concrete third-party integration, not a hosted bridge, not a public gateway.

The fundamental boundary:

- Odin returns **Candidate Artifacts** only.
- The host app owns **apply**, **state**, and **external send**.
- Odin does not mutate host app state.
- Odin does not send externally.
- Odin does not hold or manage host app credentials.

---

## Architecture

```
Host App
  ↓  health-check Odin (localhost only)
  ↓  submit Universal Work (candidate-only input)
  ↓  read Candidate Artifact (candidate-only output)
  ↓  inspect proof boundaries / proof gaps
  ↓  host app decides whether to use the candidate
  ↓  host app owns apply / state / external send
```

Odin is a **read surface and work submission target** only. It does not cross the host app boundary.

---

## Host App / Odin Boundary

| Authority | Owner |
|---|---|
| App state | Host app |
| Apply / persist | Host app |
| External send | Host app |
| User-facing production effects | Host app |
| Deployment | Host app |
| Credentials | Host app |
| Health / status surface | Odin (read-only, localhost) |
| Universal Work receive | Odin (candidate-only) |
| Candidate Artifact produce | Odin (candidate-only, not applied truth) |
| Proof boundaries / proof gaps | Odin (informational, gaps not closed by read) |

---

## Neutrality Policy

This pack is app-agnostic and vendor-agnostic:

- No concrete third-party app names.
- No third-party product references.
- No project-specific workflows.
- No hosted or cloud bridge claim.
- No real external app dependency.
- No app-specific auth flow.
- No concrete customer or product reference.

Use terms: `host_app`, `neutral_host`, `example_host`, `external_app_client`, `host_owned_apply`, `candidate_artifact`.

---

## Health Check Flow

The host app:
1. Reads `neutral_bridge_config.example.json` for the local Odin base URL.
2. Issues a GET to `http://127.0.0.1:8877/v1/health` (localhost only).
3. Reads the candidate-only health response.
4. Decides its own next action based on the health status.

Odin returns health status as a candidate-only observation. Odin does not apply host state. Odin does not send externally.

See: `examples/external_app_bridge/neutral_host_health_check.py`

---

## Universal Work Submit Flow

The host app:
1. Constructs a Universal Work request (see `neutral_universal_work_request.valid.json`).
2. Issues a POST to `http://127.0.0.1:8877/v1/universal-work` (localhost only).
3. Receives a Candidate Artifact in the response.
4. The candidate is **not applied truth**. The host app decides what to do.

Odin accepts the work, produces a candidate, and returns it. Odin does not apply the result to the host app. Odin does not send the result externally.

See: `examples/external_app_bridge/neutral_host_submit_universal_work.py`

---

## Candidate Artifact Read Flow

The host app:
1. Obtains a candidate artifact ID (from a previous submission or by listing).
2. Issues a GET to `http://127.0.0.1:8877/v1/candidates/{id}` (localhost only).
3. Reads the candidate artifact.
4. The candidate is **not applied truth**. Displaying it does not apply it.
5. The host app decides what to do with the candidate.

See: `examples/external_app_bridge/neutral_host_read_candidate.py`

---

## Proof Gaps Read Flow

The host app:
1. Issues a GET to `http://127.0.0.1:8877/v1/proof-gaps` (localhost only).
2. Reads the proof gap summary.
3. Displaying gaps does **not close them**. Known non-proofs remain non-proofs.
4. The host app uses gap information to form its own risk posture.

See: `examples/external_app_bridge/neutral_host_read_proof_gaps.py`

---

## Host-Owned Apply / State / External Send Policy

**Odin does not apply candidate artifacts.**

Host app owns apply. Host app owns state. Host app owns external send.

The host app is the sole authority for:
- Deciding to use a candidate result.
- Writing to its own data store.
- Sending results externally (email, API, webhook, etc.).
- Persisting state changes.
- Triggering user-visible production effects.

Every example in this pack reflects this policy. No example causes Odin to apply, send, or mutate host state.

---

## SDK Helper Usage

The SDK helpers in `sdk/python/odin_client.py` and `odin_app_sdk/client.py` provide:

- `health()` — read Odin health (candidate-only).
- `status()` — read Odin status (candidate-only).
- `submit_universal_work()` — submit work, receive candidate artifact.
- `get_candidate()` — read candidate artifact by ID.
- `proof_gaps()` — read proof gaps (informational, not closed by read).

**Forbidden SDK helpers (must not exist):** `apply()`, `apply_candidate()`, `mutate_app_state()`, `send_external()`, `upload_result()`, `publish_result()`, `deploy()`, `run_provider()`, `execute_provider()`, `call_model()`, `store_credentials()`, `set_api_key()`, `set_token()`.

---

## Fixture Descriptions

### `neutral_bridge_config.example.json`

Example bridge configuration. Declares:
- `odin_base_url`: `http://127.0.0.1:8877` (localhost only).
- `localhost_only: true`.
- `host_app_owns_apply: true`, `host_app_owns_state: true`, `host_app_owns_external_send: true`.
- `odin_app_apply: false`, `odin_external_send: false`.
- `credential_required: false`.

### `neutral_universal_work_request.valid.json`

Example Universal Work request fixture. Declares:
- `candidate_only: true`, `local_only: true`.
- `external_send: false`, `app_apply: false`.
- `host_app_owns_apply: true`, `host_app_owns_state: true`, `host_app_owns_external_send: true`.

### `neutral_candidate_artifact_response.valid.json`

Example Candidate Artifact response fixture. Declares:
- `candidate_only: true`.
- `applied_truth: false`.
- `app_state_mutated: false`.
- `external_send: false`.
- `host_app_owns_apply: true`.

---

## What This Proves

- Neutral bridge documentation exists and is claim-bound.
- Neutral example files exist and enforce localhost-only target.
- Neutral fixture files exist and parse correctly.
- Health check example connects only to localhost.
- Universal Work submit example does not apply the candidate.
- Candidate read example does not mutate host state.
- Proof gap read example states gaps are not closed by display.
- SDK helpers do not expose apply, send, mutate, or credential authority.
- No concrete third-party app names appear in the pack.
- No credentials appear in fixtures.
- No hosted bridge or public gateway claim is made.
- Host-owned apply/state/external-send policy is declared throughout.

---

## What This Does Not Prove

- Production readiness.
- Security certification.
- Hosted bridge operation.
- Public network gateway operation.
- Real external app integration.
- App apply authority.
- External send authority.
- Credential handling.
- Provider execution.
- Live model inference.
- Model quality.
- App state mutation authority.

---

## Proof Boundaries

```
not_production_readiness_certification
not_security_certification
not_hosted_bridge_proof
not_public_gateway_proof
not_real_external_app_integration_proof
not_app_apply_proof
not_host_state_mutation_proof
not_external_send_authority_proof
not_provider_execution_proof
not_provider_credential_storage_proof
not_live_model_inference_proof
not_model_quality_proof
candidate_artifact_not_applied_truth
host_app_owns_apply_state_external_send
```

---

## Implementation Notes

- Default Odin base URL: `http://127.0.0.1:8877`.
- All examples enforce localhost-only with a `_assert_localhost()` guard.
- All examples include a prominent boundary notice in output.
- Examples fall back to fixture data when Odin is not reachable — this is by design for demonstration.
- No browser automation. No npm. No external network. No real credentials.
- Validate: `python -m odin.cli validate-neutral-external-app-bridge`.
- Prove: `python -m odin.cli prove-neutral-external-app-bridge`.

---

## Forbidden Scope

This pack does not and must not implement:

- A concrete external app.
- A third-party app integration.
- A hosted bridge.
- A public API gateway.
- OAuth or any auth provider.
- A credential manager.
- Provider execution.
- Live model calls.
- App apply from Odin.
- External send from Odin.
- Host app state mutation from Odin.
- Remote transport by default.
- Webhook or callback delivery.
- Public network exposure.
- Production bridge claim.
- Security certification claim.
- Model quality claim.
