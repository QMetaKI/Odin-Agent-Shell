# Redaction Policy Test Matrix V1

**Claim boundary:** `redaction_policy_test_matrix_not_security_certification`

**LRH-PR:** LRH-PR-18  
**Status:** policy and test matrix defined  
**Candidate-only:** true  
**Local-only:** true

---

## What This Is

Redaction policy test matrix for Odin Local Runtime Hub. Documents redaction policy categories, test fixture categories, and boundaries.

This is a policy and test matrix receipt only.

---

## What This Is Not

- Not a redaction guarantee
- Not security certification
- Not secret leakage impossibility proof
- Not production security proof
- Not complete secret detection

---

## Redaction Categories

| Category | Policy | Status |
|----------|--------|--------|
| `api_keys` | always_redact | covered |
| `passwords` | always_redact | covered |
| `private_keys` | always_redact | covered |
| `tokens` | always_redact | covered |
| `connection_strings` | always_redact | covered |
| `local_paths` | redact_on_external_send | covered |

---

## Support Bundle Redaction Policy

Applied to `emit-support-bundle --diagnostics-only`:
- Redact keys: `api_key`, `password`, `private_key`, `token`, `connection_string`, `secret`
- Redact values matching: `-----BEGIN`, `sk-`, `pk-`, `xox`
- Output claim: `redacted_support_bundle_local_diagnostics_only`

---

## Not Proven

- `redaction_guarantee`
- `security_certification`
- `secret_leakage_impossible`
- `production_security_proof`
- `complete_secret_detection`

---

## Proof Boundaries

- `not_redaction_guarantee`
- `not_security_certification`
- `not_secret_leakage_impossibility_proof`
- `policy_and_test_matrix_only`
- `best_effort_redaction`

---

## Registry Location

`registries/redaction_policy_test_matrix_v1.json`
