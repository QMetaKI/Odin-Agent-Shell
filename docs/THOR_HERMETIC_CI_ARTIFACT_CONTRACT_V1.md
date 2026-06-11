# Thor Hermetic CI Artifact Contract V1

**Claim boundary:** `thor_hermetic_contract_schema_only_not_thor_execution_proof`

**LRH-PR:** LRH-PR-18  
**Status:** contract_defined_not_execution_proven  
**Candidate-only:** true  
**Local-only:** true

---

## What This Is

Thor governance contract schema. Defines diagnostic classes, boundary requirements, and required future receipts for Thor hermetic CI artifact integration. Does not claim Thor is available.

---

## What This Is Not

- Not Thor execution proof
- Not hermetic CI execution proof
- Not release validation by Thor
- Thor is advisory only — Odin validators remain authority

---

## Current Classification

**`not_found_in_PATH`** — Thor CLI not found in system PATH. Thor probe result: `thor_in_path: false`, `module_found: false`.

---

## Diagnostic Classes

| Class | Description |
|-------|-------------|
| `thor_available` | Thor found in PATH and importable |
| `not_found_in_PATH` | Thor CLI not found in system PATH (current) |
| `entrypoint_missing_after_install` | Thor installed but CLI entrypoint missing |
| `module_not_importable_after_install` | Thor installed but Python module not importable |
| `clone_unavailable` | Thor repository clone failed |
| `network_unavailable` | Network not available for Thor clone/install |
| `permission_issue` | Permission error during Thor install |
| `working_directory_issue` | Working directory issue during Thor operations |
| `unknown_invocation_regression` | Thor invocation produced unexpected output |

---

## Hermetic CI Artifact Schema

Required fields for a valid Thor hermetic CI artifact:
- `artifact_kind`
- `thor_classification`
- `advisory_only`
- `candidate_only`
- `local_only`
- `claim_boundary`

---

## Not Proven

- `thor_available_in_environment`
- `hermetic_ci_execution`
- `thor_validates_odin_release`
- `production_readiness`
- `release_certification`

---

## Proof Boundaries

- `not_thor_execution_proof`
- `not_hermetic_ci_execution_proof`
- `not_release_validation_by_thor`
- `thor_advisory_only`
- `odin_validators_remain_authority`
