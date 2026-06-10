# QIRC Hot Window Memory v7.1

## Objective

Define how Odin QIRC condenses long context streams into short active windows for model routing and candidate assembly. Hot Window Memory is runtime memory, not chat memory.

## Memory Classes

- Hot Window: current relevant events for a work cycle.
- Work Memory: prior route/slot/candidate outcomes for the same caller or intent family.
- Trace Memory: why a route was selected, blocked, held or escalated.
- Pattern Memory: seed/archetype/slot/route priors for intent families.

## Hot Window Construction

```text
raw digest → dedup → collapse → checkpoint → active window → context capsule
```

## Retention

Hot Window records should be short lived by default. Trace summaries may be retained longer. Raw payloads require explicit policy and redaction.

## Efficiency Rule

No model should receive full event history if a QIRC Hot Window can represent the active context with lower entropy.


## Required Runtime Behavior

The real implementation must keep this component deterministic where possible, typed at the boundary, local-only by default and candidate-only at output. Any future implementation must include positive and negative fixtures, registry entries, system map references and Codex task mapping.

## Failure Behavior

On malformed input, missing trace_id, missing privacy_class, authority escalation, direct apply request, raw secret payload or unbounded event fanout, this component must fail closed and emit a blocked QIRC event or an admissibility hold record.

## Codex Conversion Rule

Codex must build this as a small typed module with no hidden agent autonomy. If a model provider would be required, Codex must instead create a candidate ModelWorkPacket or a hold/split/ask_context route unless the provider stage has already been implemented under the correct PR bundle.
