# CLAIM_BOUNDARY.md

## Allowed Claims

This repository may claim:

- architecture specified
- repo scaffold prepared
- schemas present
- registries present
- tests included
- validation CLI present
- local test receipt present only if generated in this repo state

## Forbidden Without Receipt

Never claim the following unless exact receipt exists:

```text
runtime_verified
host_validated
model_inference_verified
network_verified
security_verified
production_ready
deploy_verified
patch_applied
tests_passed
full_implementation_complete
```

## Candidate-Only Rule

Odin output is candidate-only by default.

Allowed:

```text
candidate_artifact
response_packet
patchplan_candidate
review_candidate
receipt_candidate
debug_hypothesis_candidate
```

Forbidden:

```text
applied_patch
sent_email
changed_project_state
executed_command
tests_passed
production_ready
```

## App Authority

If something affects app reality, it must be done by the app through an app-owned apply gate.

## v0.8.7 Codex hardening proof discipline

Current handoff is `v0.8.7 CODEX_REAL_PR_HANDOFF_LADDER_LOCK` for Odin Agent Shell v7.1. Current execution mode is Codex hardening from a running Runtime Candidate, not production certification.

Odin emits candidates only. App-owned apply is mandatory. Odin does not mutate caller/app state, does not silently send externally, and does not promote model/provider output to truth.

Required retained proof gaps: no production readiness proof; no live model inference proof; no model quality proof; no Windows service/tray/installer proof unless actually tested; no security certification proof; no external send proof; no app-state mutation proof; manual review remains required.

Current actual Codex PR path: `CODEX-PR-01`, `CODEX-PR-02`, `CODEX-PR-03`, `CODEX-PR-04`, `CODEX-PR-05`. Historical traceability retained: `PR-00..PR-123`, `REAL-PR-01..28`, `REAL-GH-PR-01..08`.

