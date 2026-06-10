# CLAIM_BOUNDARY.md

## Current claim posture

Current handoff: `v0.8.7 CODEX_REAL_PR_HANDOFF_LADDER_LOCK`.
Runtime base: `v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK`.
Actual Codex/GitHub PR ladder: `REAL-GH-PR-01..08`.
Internal ladders `PR-00..PR-123` and `REAL-PR-01..28` are traceability only.

## Allowed Claims

This repository may claim only what current files and current workspace command receipts support:

- architecture specified
- repo scaffold prepared
- schemas present
- registries present
- tests included
- validation CLI present
- Candidate Artifact produced
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

Negated and proof-gap scoped language is allowed, for example: not production ready, no host validation proof, no live model inference proof.

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

Forbidden as Odin authority:

```text
applied_patch
sent_email
changed_project_state
executed_command
tests_passed
production_ready
```

## App Authority

Odin does candidate work. The caller/app does reality work. If something affects app reality, it must be done by the app through an app-owned apply gate. Apps own state, apply, external sends, storage, and domain truth.

## Provider, QIRC, and Windows Boundaries

Providers are workers, not authority. QIRC / Internal Semantic Bus is trace, receipt, and coordination infrastructure, not app-state authority. Windows service/tray/installer proof requires actual Windows receipts.
