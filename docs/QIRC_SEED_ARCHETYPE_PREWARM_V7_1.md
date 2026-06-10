# QIRC Seed / Archetype Prewarm v7.1

## Objective

Run seed activation, decay, conflict resolution, noise gating and archetype role activation before model dispatch. This makes Odin cheaper and less noisy.

## Cycle

```text
context/event profile → seed candidates → activation score → decay stale seeds → resolve conflicts → top-k cap → archetype role selection → route hints
```

## Seed Budget

Profiles define `max_active_seeds`, `max_archetype_roles`, `max_compositions`, `decay_policy`, `conflict_policy` and `noise_gate`.

## Pattern Roles

BoundaryGuard, ContextWeaver, SlotSmith, CheapScout, QualityScribe, MirrorCritic, CandidateMessenger and TraceKeeper are neutral runtime archetypes. They are not agents and cannot own authority.

## Conflict Rules

Contradictory seed families must be resolved before model routing. If conflict cannot be resolved, the admissibility gate returns hold or ask_context.


## Required Runtime Behavior

The real implementation must keep this component deterministic where possible, typed at the boundary, local-only by default and candidate-only at output. Any future implementation must include positive and negative fixtures, registry entries, system map references and Codex task mapping.

## Failure Behavior

On malformed input, missing trace_id, missing privacy_class, authority escalation, direct apply request, raw secret payload or unbounded event fanout, this component must fail closed and emit a blocked QIRC event or an admissibility hold record.

## Codex Conversion Rule

Codex must build this as a small typed module with no hidden agent autonomy. If a model provider would be required, Codex must instead create a candidate ModelWorkPacket or a hold/split/ask_context route unless the provider stage has already been implemented under the correct PR bundle.
