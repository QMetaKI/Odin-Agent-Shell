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
