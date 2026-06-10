# Ring Radar / Resonance / Why Trace v7.1

## Purpose

Ring Radar and Resonance make Odin selective. Why Trace makes Odin explainable. Together they reduce black-box behavior and prevent unnecessary subsystem fan-out.

## Ring Activation Map

Each work item tracks activation for:

- R0 boundary
- R1 policy
- R2 universal_work
- R3 context
- R4 semantic_bus
- R5 slots
- R6 model_route
- R7 critics
- R8 candidate
- R9 app_response

Each ring has:

- activation_level
- pressure
- reason
- deviation_marker
- allowed_actions

## Resonance bands

Odin normalizes signals into bands:

- intent_fit
- context_fit
- artifact_fit
- seed_fit
- archetype_fit
- boundary_fit
- model_fit
- style_fit
- privacy_risk
- claim_risk
- genericness_risk

## Deviation triggers

Extra compute only activates if:

- ring pressure exceeds threshold
- boundary risk increases
- candidate drift detected
- genericness too high
- route score ambiguous
- seed conflict unresolved

## Why Trace

Why Trace answers:

- why this center
- why this route
- why this model ceiling
- why this candidate
- why these seeds
- why these archetype roles
- why a route was blocked
- why more context is needed

## Why Trace schema fields

- why_trace_id
- work_id
- centerline_packet_ref
- selected_center
- active_rings
- active_seeds
- active_archetype_roles
- selected_route
- blocked_routes
- qmath_score_ref
- risk_summary
- boundary_summary
- candidate_dna_ref
- user_safe_summary

## Redaction

Why Trace must never include secrets, raw private app state, credentials or hidden payloads. It may include digests, ids, scores, reasons and redacted summaries.

## Codex Rule

Every Response Packet from non-trivial work must have Why Trace or a reason why trace was suppressed by privacy policy.
