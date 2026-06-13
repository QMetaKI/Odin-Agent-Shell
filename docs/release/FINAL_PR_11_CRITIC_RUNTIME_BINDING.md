# FINAL-PR-11 Critic Runtime Binding

**Claim boundary:** `critic_runtime_binding_scores_candidates_not_truth_not_apply`
**candidate_only:** true

## How Critic Runtime Binding Works

The critic runtime binding provides a deterministic check on candidates.
It is advisory. It is not final authority. It cannot apply. It cannot send.

## Deterministic Critic Checks

- `candidate_only_present` — must be present
- `claim_boundary_present` — must be present and non-empty
- `not_proven_present` — must be present as list
- `candidate_only_true` — must be True
- `forbidden_actions_clean` — app_apply, external_send, public_network must not be True
- `model_projection_not_truth` — model output is not treated as truth

## Why Critic Is Not Authority

- Critic is advisory only
- Final gate is required (separate from critic)
- App owns apply authority
- Critic output must not be used to bypass final gate

## Critic Cascade

1. Always runs deterministic critic
2. Optionally runs model critic (requires `include_model_critic=True` AND `allow_local_provider_execution=True`)
3. If model critic unavailable, cascade continues with deterministic only
4. Cascade result is advisory, not authority

## Evidence Class

Critic results are always `structural_evidence`.
Model critic results, if available, are `host_scoped_local_receipt` via provider receipt harness.

## Not Proven

- final_authority
- production_readiness
- model_quality_superiority
- app_apply
- external_send
