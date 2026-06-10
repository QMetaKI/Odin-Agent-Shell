# QIRC Ring Radar Runtime v7.1

## Objective

Activate only the runtime rings required by the current work cycle. Ring Radar prevents full-system fanout and makes Odin more efficient.

## Rings

R0 Boundary, R1 Policy, R2 Universal Work, R3 Context, R4 Semantic Bus, R5 Slot Forge, R6 Model Route, R7 Critic, R8 Candidate, R9 Trace/Receipt.

## Outputs

Ring Activation Map contains pressure, status, route hints, deviation reasons and downstream channels. Ring pressure below threshold results in defer/watch, not active work.

## Resonance Relation

Resonance bands normalize fit, drift, privacy, claim and context pressure into routeable numeric signals.


## Required Runtime Behavior

The real implementation must keep this component deterministic where possible, typed at the boundary, local-only by default and candidate-only at output. Any future implementation must include positive and negative fixtures, registry entries, system map references and Codex task mapping.

## Failure Behavior

On malformed input, missing trace_id, missing privacy_class, authority escalation, direct apply request, raw secret payload or unbounded event fanout, this component must fail closed and emit a blocked QIRC event or an admissibility hold record.

## Codex Conversion Rule

Codex must build this as a small typed module with no hidden agent autonomy. If a model provider would be required, Codex must instead create a candidate ModelWorkPacket or a hold/split/ask_context route unless the provider stage has already been implemented under the correct PR bundle.
