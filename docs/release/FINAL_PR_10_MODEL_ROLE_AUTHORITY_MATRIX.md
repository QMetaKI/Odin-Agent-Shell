# FINAL-PR-10 Model Role Authority Matrix

**claim_boundary:** `final_pr_10_boundary_gated_release_operationalization_not_release_certification`
**candidate_only:** true
**app_owned_apply:** true

---

## Overview

FINAL-PR-10 defines the authority envelope for each model role in the Odin system. Model roles determine which ring a model may operate in, what candidate types it may emit, and what operations are forbidden regardless of capability claims.

This matrix is structural — it does not assert that any model currently has live inference capability. Authority envelopes are boundary constraints, not capability certifications.

---

## Model Role Authority Matrix

| Model Role | Ring Authority | Permitted Candidate Types | Forbidden Operations | Notes |
|------------|---------------|--------------------------|---------------------|-------|
| **3B (small local)** | Ring 2 max | work_atom, seed_candidate | app_state_apply, external_send, provider_call_unreceipted | Local inference only; no Ring 0 direct access |
| **7B (mid local)** | Ring 2 max | work_atom, seed_candidate, field_selection_candidate | app_state_apply, external_send | Can emit field selection candidates; still no Ring 0 |
| **Hybrid (local+remote)** | Ring 1 max | work_atom, seed_candidate, field_selection_candidate, projection_candidate | app_state_apply | Must present provider receipt for remote calls |
| **No-model (deterministic)** | Ring 0 | boundary_check_result, gate_result | Any model-dependent candidate | Deterministic logic only; no inference |
| **Local-provider** | Ring 1 max | provider_receipt, work_atom, seed_candidate | external_send, domain_state_write | Receipt-bearing provider calls only |

---

## Ring Authority Explanation

- **Ring 0:** Core boundary enforcement. Only deterministic, no-model components operate here. Boundary checks, gate results, and receipt validations.
- **Ring 1:** Candidate production with receipt. Local-provider and hybrid models may operate here with proper receipts.
- **Ring 2:** Small and mid local models. Seed and work-atom candidates. No external authority.
- **Ring 3:** Release evidence and preflight. No model operates directly at Ring 3 — only aggregated candidate packets.

---

## Candidate Type Definitions

| Candidate Type | Description | App-Owned Apply |
|---------------|-------------|-----------------|
| `work_atom` | Atomic unit of work output, candidate only | true |
| `seed_candidate` | Seed pack selection candidate | true |
| `field_selection_candidate` | Field selection from schema candidate | true |
| `projection_candidate` | Output projection candidate | true |
| `boundary_check_result` | Result of a boundary gate check | true |
| `gate_result` | Pass/fail/deferred gate resolution | true |
| `provider_receipt` | Receipt for a completed provider call | true |

---

## Authority Drift Prevention

Bug6 (authority_drift_scanner) monitors for model roles attempting to operate above their ring ceiling. If a 3B model emits a candidate that claims Ring 0 authority, the scanner flags it as authority_drift and the candidate is rejected at the candidate envelope check.

---

## FINAL-PR-11 Deferred Items

The following model role authority items are deferred to FINAL-PR-11:
- Live inference validation per role
- Dynamic ring ceiling adjustment based on observed quality
- Multi-model ensemble authority routing

---

## Not Proven

- `production_readiness`
- `live_model_inference`
- `app_state_mutation`
- `external_send_authority`
- `release_certification`
- Model capability claims beyond structural boundary assignment
