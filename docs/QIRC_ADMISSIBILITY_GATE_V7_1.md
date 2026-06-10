# QIRC Admissibility Gate v7.1

## Objective

Prevent unnecessary or unsafe model calls. Every potential model route must pass QIRC admissibility after centerline, seed, archetype, QMath and ring checks.

## Decisions

- go
- hold
- ask_context
- split_work
- block

## Decision Contract

The gate returns reasons, blocked routes, next action, required receipts and why-trace hints. If the work is broad, expensive, risky, unsupported or missing context, the gate does not call a model.

## Model Dispatch Rule

No model dispatch before admissibility. This is a hard gate.


## Required Runtime Behavior

The real implementation must keep this component deterministic where possible, typed at the boundary, local-only by default and candidate-only at output. Any future implementation must include positive and negative fixtures, registry entries, system map references and Codex task mapping.

## Failure Behavior

On malformed input, missing trace_id, missing privacy_class, authority escalation, direct apply request, raw secret payload or unbounded event fanout, this component must fail closed and emit a blocked QIRC event or an admissibility hold record.

## Codex Conversion Rule

Codex must build this as a small typed module with no hidden agent autonomy. If a model provider would be required, Codex must instead create a candidate ModelWorkPacket or a hold/split/ask_context route unless the provider stage has already been implemented under the correct PR bundle.
