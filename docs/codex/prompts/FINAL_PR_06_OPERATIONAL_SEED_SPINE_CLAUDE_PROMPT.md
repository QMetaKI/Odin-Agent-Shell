# FINAL-PR-06: Operational Seed Spine + Role Profiles + Seed-to-Work-Capsule Compiler

## Purpose / Objective

Implement operational intent seeds, role profiles, seed packs, and a seed-to-work-capsule compiler. The implementation improves Handoff Context quality, Universal Work preparation, ModelWorkPacket preparation, Work Capsule generation, QIRC/event routing hints, and local worker token efficiency while preserving candidate-only boundaries.

## Base rule

Base: current main after prep PR merge. Do not base on open PR branches. If Y Pattern Spine is already merged, treat it as available baseline; if it is open, treat it as an expected precondition and do not depend on its branch.

## Allowed scope

Create the smallest deterministic, local-only implementation for the Operational Seed Spine. Add docs, neutral registries if needed, tests, validator, CLI hooks, proof packet, SYSTEM_MAP and FILE_MANIFEST updates. Keep all outputs candidate-only.

## Forbidden scope

No provider execution, model inference, API key reads, external network, public QIRC/network/federation, app apply, app state mutation, external send, production readiness claim, security certification claim, hidden authority, religious interpretation, persona injection, source-pattern runtime import, or Q-style new runtime artifact names.

## Files to create

- `odin/operational_seed_spine/__init__.py`
- `odin/operational_seed_spine/seeds.py`
- `odin/operational_seed_spine/role_profiles.py`
- `odin/operational_seed_spine/seed_packs.py`
- `odin/operational_seed_spine/compiler.py`
- `odin/operational_seed_spine/proof.py`
- `tools/rebaseline/check_operational_seed_spine.py`
- `tests/test_final_pr_06_operational_seed_spine.py`
- `reports/final_pr_06_operational_seed_spine_proof_packet.json`

## Required objects

- `OperationalSeed`
- `IntentSeed`
- `RoleProfile`
- `SeedPack`
- `SeedRoute`
- `SeedToWorkCapsuleResult`

## Seed families

- `repo_cognition`
- `document_drafting`
- `code_change`
- `code_review`
- `runtime_probe`
- `provider_probe`
- `qirc_event_trace`
- `proof_packet`
- `release_closure`
- `debug_triage`
- `local_hub_update`
- `validator_build`

## Role profiles

- `builder`
- `reviewer`
- `guard`
- `cartographer`
- `materializer`
- `scope_compressor`
- `proof_binder`
- `operator`

## CLI commands

- `python -m odin.cli validate-operational-seed-spine`
- `python -m odin.cli explain-seed-route --demo`
- `python -m odin.cli prove-operational-seed-spine`

## Validator requirement

Create `tools/rebaseline/check_operational_seed_spine.py`. It must verify files, neutral naming, seed families, role profiles, candidate-only/local-only/app-owned-apply flags, forbidden scope text, no provider/model execution, no app apply/state/external-send authority, no new forbidden Q-style runtime/schema/registry/CLI artifact names, and proof packet shape.

## Tests requirement

Create `tests/test_final_pr_06_operational_seed_spine.py` covering deterministic seed lookup, role profile posture, seed pack validation, seed-to-work-capsule compilation, invariant failures, CLI validator, proof packet generation, and `validate-all` integration.

## Proof packet requirement

Create `reports/final_pr_06_operational_seed_spine_proof_packet.json` via `prove-operational-seed-spine`. It must state `candidate_only: true`, `local_only: true`, `app_owned_apply: true`, no provider/model execution, no network, no app apply/state/external-send, and no truth authority.

## Required invariant

Seed routes work. Seeds do not decide truth. Role profiles guide posture. Role profiles are not personas.

## Senior review loop

Before finalizing, simulate a senior reviewer and a senior code reviewer. Confirm the implementation is bounded, neutral, deterministic, small, test-covered, and does not add hidden authority or runtime/model/app claims. Apply fixes before the final response.

## Final response format

Return summary, files changed, what remains scaffold, non-claims, and exact tests run. Each test/check command must be prefixed with pass/warn/fail status.
