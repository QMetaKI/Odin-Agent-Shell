# PR-32 B6 Thor Acceptance Review Prompts

claim_boundary: thor_reference_is_external_candidate_handoff_guidance_not_runtime_or_release_proof

## Senior reviewer prompt
Review B6 artifacts for static evidence boundaries, known gaps, B7+ recommendations, and absence of release/runtime/security overclaims.

## Senior code reviewer prompt
Review B6 validator and tests for fail-closed behavior, deterministic report generation, and no provider/runtime/network/API-key handling.

## Thor review mapping
THOR_REVIEW claim_findings become Acceptance Harness finding entries. THOR_REVIEW required_fixes become blocking_conditions or improvement_actions. THOR_RECEIPT accepted/denied/pending becomes closure readiness rows.
