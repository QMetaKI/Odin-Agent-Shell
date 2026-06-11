# Provider / Worker / Pre-LLM Inspector — v1

**Claim boundary:** `provider_worker_inspector_candidate_only_local_only_no_provider_execution_no_credentials_no_worker_mutation`

**LRH ladder entry:** LRH-PR-10

---

## Purpose

The Provider / Worker / Pre-LLM Inspector exposes bounded, read-only, local-only Hub visibility for:

- Provider capability cards (provider metadata, readiness, disabled/enabled posture)
- Worker permission boundaries (candidate_only, forbidden roles, app_owned_apply)
- Pre-LLM route decisions (route metadata, avoidance rationale — not live execution)
- Model-work avoidance rationale (why model work was not invoked)
- Redaction status (policy/warnings — not safety certification)
- Disabled-by-default posture (credential and execution defaults)
- Provider/worker proof gaps

This inspector is visibility-only. It does not execute providers, call live models, or mutate any system state.

---

## Surfaces

### Provider Card Viewer

Shows provider capability cards from `/v1/providers`:

- `provider_id`
- `provider_kind`
- `status`: disabled / enabled / unavailable / unknown
- `enabled_by_default`: shows disabled-by-default posture
- `configured`: credential/config status (no credential values shown)
- `live_inference_supported` / `live_inference_verified`
- `candidate_only`: always true
- `claim_boundary`
- `forbidden_roles`: worker boundary enforcement
- Provider-as-worker-not-authority banner on every card

### Worker Permission Card Viewer

Shows worker permission boundaries from `/v1/status`:

- `candidate_only`: true
- `app_owned_apply`: true
- `external_send_default`: false
- `hidden_tool_execution_allowed`: false
- `may_apply`: false
- `may_send_external`: false
- `may_mutate_app_state`: false
- `may_issue_receipt`: false
- `may_accept_claim`: false
- Forbidden worker roles listed: `app_authority`, `apply_executor`, `claim_acceptor`, `receipt_issuer`, `external_sender`, `state_mutator`

### Pre-LLM Route Decision Viewer

Shows route decision metadata from `/v1/status`:

- Route status (always `not_live_model_inference` unless receipted)
- Decision reason
- Avoidance rationale
- Redaction status before model work
- Proof boundaries

Route decisions are inspection-only. No route policy mutation is possible.

### Model-Work Avoidance Panel

Shows why model work was avoided:

- `candidate_only_mode`: true
- `disabled_provider`: all providers disabled by default
- `missing_credential`: no credentials configured
- `local_only_mode`: true
- `no_receipt`: no live inference receipt issued
- `proof_gap_reason`: `not_live_model_inference_proof`

### Redaction Status Panel

Shows redaction policy and known gaps:

- `redaction_policy`: active
- `metadata_first_display`: true
- `redaction_status_is_not_certification`: true
- `known_redaction_gaps`: `not_full_redaction_safety_certification`
- `safe_unsafe_policy`: safe by default; sensitive values redacted

**Redaction status is not safety certification and does not prove perfect redaction.**

### Disabled-by-Default Visibility

Shows the default posture for providers and credentials:

- `provider_execution_default`: disabled
- `credential_default`: none configured
- `external_send_default`: false
- `live_inference_receipt`: not issued

Per-provider `enabled_by_default` status shown from `/v1/providers` when available.

### Provider/Worker Proof Gaps

Shows known proof gaps from `/v1/proof-gaps`. Displaying gaps does not close them.

---

## What This Proves

When `validate-provider-worker-inspector` passes and `prove-browser-hub --providers` emits an `ok` packet, the following is proven:

- `provider_worker_inspector_static_files_exist`
- `provider_viewer_references_v1_providers`
- `provider_cards_surface_present`
- `worker_permission_cards_surface_present`
- `pre_llm_route_decision_surface_present`
- `model_work_avoidance_surface_present`
- `redaction_status_surface_present`
- `disabled_by_default_surface_present`
- `no_provider_execution_controls`
- `no_live_model_call_controls`
- `no_credential_controls`
- `no_worker_mutation_controls`
- `no_route_mutation_controls`
- `no_redaction_bypass_controls`
- `no_external_send_controls`

---

## What This Does Not Prove

**Proof Boundaries — explicitly not proven by this inspector:**

- `not_production_readiness_certification`
- `not_security_certification`
- `not_live_model_inference_proof`
- `not_model_quality_proof`
- `not_provider_authority_proof`
- `not_provider_execution_proof`
- `not_provider_credential_storage_proof`
- `not_worker_mutation_proof`
- `not_worker_permission_mutation_proof`
- `not_route_mutation_proof`
- `not_redaction_safety_certification`
- `not_redaction_bypass_proof`
- `not_full_pre_llm_runtime_coverage`
- `not_public_network_api_proof`
- `not_app_state_mutation_proof`
- `not_external_send_authority_proof`

---

## Explicit Boundary Statements

**This does not execute providers.**

**This does not call live models.**

**This does not store or request provider credentials.**

**This does not treat providers as authority.**

**This does not mutate worker permissions.**

**This does not mutate routing policy.**

**This does not bypass redaction.**

**This does not prove model quality.**

**This does not prove production readiness.**

**This does not prove security certification.**

---

## Forbidden Controls

The following are forbidden in all inspector UI surfaces:

- `runProvider()` / `executeProvider()` — no provider execution
- `callModel()` / `runModel()` / `testInference()` — no live inference
- `saveCredential()` / `setApiKey()` — no credential input
- `enableProvider()` / `disableProvider()` — no enable/disable controls
- `mutateWorker()` / `editPermission()` — no worker mutation
- `changeRoute()` / `mutateRoute()` — no route mutation
- `bypassRedaction()` — no redaction bypass
- `rawPayloadReveal()` — no raw sensitive payload display
- `externalSend()` / `uploadDiagnostics()` / `hiddenUpload()` — no external send

---

## CLI

```bash
python -m odin.cli validate-provider-worker-inspector
python -m odin.cli prove-browser-hub --providers
python -m odin.cli list-providers
```

---

## Proof Packet

`prove-browser-hub --providers` emits:

```json
{
  "artifact_kind": "hub_provider_worker_inspector_proof_packet",
  "candidate_only": true,
  "local_only": true,
  "read_only": true,
  "provider_worker_inspector_only": true
}
```

---

## Provider-as-Worker-Not-Authority Boundary

Providers are bounded workers in Odin. They produce candidate artifacts only. They are not decision authority, cannot apply app state, cannot send externally, and are disabled by default.

Worker permission cards enforce:
- `candidate_only: true`
- `app_owned_apply: true`
- `external_send_default: false`
- `may_apply: false`
- `may_mutate_app_state: false`
- `may_send_external: false`

This inspector surfaces that boundary for visibility — it does not change it.

---

## Local-Only / Read-Only Posture

- All API requests go to `http://127.0.0.1:8877` by default
- No WAN/LAN endpoints are exposed
- No data leaves the local machine
- No credentials are accepted or displayed
- No mutations are possible through this UI

---

_Claim boundary: `provider_worker_inspector_candidate_only_local_only_no_provider_execution_no_credentials_no_worker_mutation`_
