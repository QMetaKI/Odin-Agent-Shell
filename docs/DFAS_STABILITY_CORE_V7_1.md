# DFAS Stability Core v7.1

## Purpose

The DFAS Stability Core is Odin's deterministic focus and admissibility spine. It decides whether the system should proceed, hold, ask context, split work, route deterministic, route small model, route hybrid or block.

## Inputs

- Centerline Packet
- Universal Work
- Output Contract
- Resource Profile
- Privacy Class
- Event Digest
- Seed Activation Packet
- Archetype Role Packet
- QMath Route Score
- Claim Boundary
- Work Memory

## Decision outputs

- continue
- hold
- ask_context
- split_work
- deterministic_only
- route_1b_2b
- route_3b_micro
- route_7b_8b
- route_hybrid
- route_quality_model
- route_heavy_batch
- block

## Hold / simulate posture

The stability core must prefer hold/simulate over expensive exploration when:

- center is unclear
- privacy risk is high
- output contract is non-candidate
- app apply boundary is unclear
- claim risk exceeds threshold
- seed conflicts are unresolved
- route score is below threshold
- context capsule is overbroad

## Stop-early rule

If deterministic or 3B micro work can answer safely, Odin must not escalate merely because a bigger model is available.

## Stability score

A work item is stable if:

- center is clear
- boundary is clear
- output is candidate-only
- context is sufficient
- model route is justified
- no forbidden claim path exists
- app authority is preserved

## Shadow Runtime behavior

The shadow module must expose the decision without side effects. It may return a plan but must not call models.

## Codex Rule

Implement this as a required pre-model gate. No provider adapter may be called before stability/admissibility returns a permitted route.
