# Generic App Bridge Golden Harness V1

**Claim boundary:** `generic_app_bridge_golden_harness_candidate_only_local_only_no_apply_no_external_send`

**Version:** 1.0
**PR:** LRH-PR-13

---

## Purpose

This document describes the Generic App Bridge Golden Harness — a deterministic, local-only, fixture-based demonstration of the Odin / host app bridge boundary.

It provides neutral reference examples and a repeatable golden harness for any host app wanting to understand how to integrate with a local Odin instance.

---

## Scope

This document covers:

- Neutral reference app examples (flow one, flow two)
- Reference host app fixture
- Golden harness
- Host-owned apply boundary
- Host-owned state boundary
- Host-owned external send boundary
- Candidate Artifact not applied truth
- Proof boundaries
- Known non-proofs
- Commands and fixtures

---

## Core Architecture Formula

```
Neutral Host App Example
  → local health-check
  → construct Universal Work
  → submit/read candidate through local fixture or local Odin path
  → receive/read Candidate Artifact
  → inspect proof boundaries / proof gaps
  → host app decides whether to apply
  → host app owns apply/state/external send
```

**Odin:**
- local health/status/proof surface
- Universal Work receiver
- Candidate Artifact producer
- proof boundary / proof gap provider
- candidate-only output

**Host App:**
- host app owns apply
- host app owns state
- host app owns external send
- owns user-facing effects
- owns deployment
- owns credentials
- decides what to do with Candidate Artifacts

---

## Neutral Examples

### Flow One — Minimal Candidate Flow

`examples/generic_app_bridge/generic_bridge_flow_one.py`

Demonstrates:
- Load request fixture
- Construct Universal Work request
- Produce/read Candidate Artifact fixture
- Display proof boundaries
- Host app owns apply/state/external send
- Candidate artifact is not applied truth

Does not:
- Apply candidate
- Mutate host app state
- Send externally
- Use concrete app names
- Call provider or model
- Use credentials

### Flow Two — Proof-Gap-Aware Flow

`examples/generic_app_bridge/generic_bridge_flow_two.py`

Demonstrates:
- Read proof gaps from candidate artifact
- Construct Universal Work request
- Read Candidate Artifact
- Show known non-proofs
- Show app-owned apply boundary
- Show no external send by Odin

Does not:
- Close proof gaps by display
- Claim production readiness
- Claim security certification
- Claim specific external app integration

---

## Reference Host App

`examples/reference_host_app/reference_host_app.py`

Neutral fake host app:
- `neutral_host_state_fixture` — not real state, not mutated
- `candidate_inbox` — receives candidates without applying
- `host_owned_apply_policy` — plan-only demonstration
- `host_owned_external_send_policy` — no external send performed

```json
{
  "host_owned_apply_demo": "plan_only",
  "app_state_mutated": false,
  "external_send_performed": false
}
```

---

## Golden Harness

`examples/generic_app_bridge/generic_bridge_harness.py`

Runs both flow one and flow two as pure local fixture flows.

**Properties:**
- deterministic
- local-only
- fixture-safe
- neutral
- claim-bound
- repeatable
- non-production
- non-hosted
- non-public-gateway
- non-signed-distribution

**Output receipt:**
```json
{
  "artifact_kind": "generic_app_bridge_golden_harness_receipt",
  "status": "ok",
  "candidate_only": true,
  "local_only": true,
  "neutral_examples": 2,
  "host_app_owns_apply": true,
  "host_app_owns_state": true,
  "host_app_owns_external_send": true,
  "odin_app_apply": false,
  "odin_external_send": false,
  "host_state_mutated": false,
  "external_send_performed": false,
  "concrete_app_names_present": false,
  "proof_boundaries": [...],
  "known_non_proofs": [...]
}
```

---

## Host App / Odin Boundary

The boundary is enforced by design — not by runtime guard:

| Authority          | Owner    |
|--------------------|----------|
| Apply Candidate    | Host App |
| Mutate State       | Host App |
| External Send      | Host App |
| User-facing Effect | Host App |
| Deployment         | Host App |
| Credentials        | Host App |
| Candidate Output   | Odin     |
| Proof Gaps         | Odin     |
| Health Status      | Odin     |

---

## Fixtures

| File | Purpose |
|------|---------|
| `examples/generic_app_bridge/fixtures/generic_bridge_flow_one_request.valid.json` | Flow one request fixture |
| `examples/generic_app_bridge/fixtures/generic_bridge_flow_one_candidate.valid.json` | Flow one candidate fixture |
| `examples/generic_app_bridge/fixtures/generic_bridge_flow_two_request.valid.json` | Flow two request fixture |
| `examples/generic_app_bridge/fixtures/generic_bridge_flow_two_candidate.valid.json` | Flow two candidate fixture |
| `examples/reference_host_app/reference_host_policy.json` | Host-owned apply policy |

All fixtures include:
- `candidate_only: true`
- `applied_truth: false`
- `host_app_owns_apply: true`
- `claim_boundary`
- `proof_boundaries`
- `known_non_proofs`

---

## Commands

```bash
# Validate
python -m odin.cli validate-generic-app-bridge-golden-harness

# Prove
python -m odin.cli prove-generic-app-bridge-golden-harness

# Run harness directly
python examples/generic_app_bridge/generic_bridge_harness.py

# Run individual flows
python examples/generic_app_bridge/generic_bridge_flow_one.py
python examples/generic_app_bridge/generic_bridge_flow_two.py

# Run reference host app
python examples/reference_host_app/reference_host_app.py

# Run tests
python -m pytest tests/test_lrh_pr_13_generic_app_bridge_golden_harness.py -q
```

---

## What This Proves

- `generic_examples_exist` — at least two neutral generic examples exist
- `reference_host_app_exists` — reference host app fixture exists
- `golden_harness_exists` — golden harness file exists
- `two_neutral_examples_present` — exactly two neutral flows
- `golden_harness_receipt_ok` — harness produces ok receipt locally
- `host_app_owns_apply_declared` — apply boundary documented and code-visible
- `host_app_owns_state_declared` — state boundary documented and code-visible
- `host_app_owns_external_send_declared` — external send boundary documented and code-visible
- `odin_app_apply_false` — Odin does not apply in any example
- `odin_external_send_false` — Odin does not send externally in any example
- `host_state_mutation_by_odin_false` — Odin does not mutate host state
- `candidate_artifact_not_applied_truth` — candidate artifacts are not applied truth
- `neutral_naming_guard_passed` — no concrete app/product names in examples
- `local_only_examples` — all examples are local-only
- `thor_invocation_discipline_doc_exists` — Thor discipline doc created

---

## What This Does Not Prove

This does not integrate a concrete app.
This does not prove production readiness.
This does not prove security certification.
This does not prove public network API readiness.
This does not prove hosted bridge readiness.
This does not prove signed distribution readiness.
This does not apply Candidate Artifacts.
This does not mutate host app state.
This does not send externally.
This does not call live models.
This does not execute providers.

**Known non-proofs:**
- `production_readiness`
- `security_certification`
- `signed_distribution`
- `windows_service_tray_installer`
- `hosted_bridge`
- `public_network_api`
- `specific_external_app_integration`
- `live_model_inference`
- `model_quality`
- `provider_execution`
- `real_app_state_mutation`
- `external_send_authority`

---

## Proof Boundaries

- `not_production_readiness_certification`
- `not_security_certification`
- `not_hosted_bridge_proof`
- `not_public_gateway_proof`
- `not_specific_external_app_integration_proof`
- `not_signed_distribution_proof`
- `not_windows_service_tray_installer_proof`
- `not_app_apply_proof`
- `not_host_state_mutation_proof`
- `not_external_send_authority_proof`
- `not_provider_execution_proof`
- `not_live_model_inference_proof`
- `not_model_quality_proof`
- `candidate_artifact_not_applied_truth`
- `host_app_owns_apply_state_external_send`
