# QIRC Channel Taxonomy v7.1

## Objective

Define the canonical channel families for Odin QIRC Gold Spine. Channels are semantic lanes, not user chat rooms. Every channel is local-only by default and bound to a module family, authority scope, payload policy, retention profile and trace requirement.

## Core Channels

- `#core.ingress` receives validated Universal Work ingress notices.
- `#core.centerline` carries Odin Core Centerline packet summaries.
- `#core.admissibility` carries hold/go/ask/split/block decisions.
- `#core.boundary` carries claim/app-authority boundary checks.
- `#core.final_gate` records final candidate gate decisions.
- `#core.hold` records fail-closed or ask-context outcomes.

## QLI / DFAS Channels

- `#qli.intent` normalizes intent family and ring path.
- `#qli.authority_posture` records app-owned/Odin-owned/model-owned boundary posture.
- `#qli.packet_compile` records packet compilation into compact work packets.
- `#dfas.stability` records stability score and center confidence.
- `#dfas.hold_simulate` records non-execution preview routes.
- `#dfas.stop_early` records stop-early decisions that prevent model calls.

## Seed / Archetype Channels

- `#seed.prewarm`, `#seed.activate`, `#seed.decay`, `#seed.conflict`, `#seed.noise_gate`.
- `#archetype.role`, `#archetype.composition`, `#archetype.budget`.

## QMath / Center Channels

- `#qmath.center_score`, `#qmath.route_score`, `#qmath.constraint_penalty`, `#qmath.admissibility`, `#qmath.threshold`.

## Ring / Resonance Channels

- `#ring.activation`, `#ring.radar`, `#ring.pressure`, `#resonance.normalize`, `#resonance.fit`, `#mirror.axis`, `#rad.balance`.

## Context / Memory Channels

- `#context.raw_digest`, `#context.hot_window`, `#context.snapshot`, `#context.dedup`, `#context.collapse`, `#context.checkpoint`.
- `#memory.work`, `#memory.trace`, `#memory.pattern`.

## Shadow / Compiler Channels

- `#shadow.ir`, `#shadow.flow`, `#shadow.holes`, `#fairy.mapping`, `#ystar.directive`.
- `#runtime_pack.compile`, `#runtime_pack.validate`, `#capability_slice.compile`.

## Model / Slot Channels

- `#worklet.graph`, `#slot.forge`, `#gaptext.build`, `#model.route`, `#model.3b`, `#model.7b`, `#model.hybrid`, `#model.heavy`, `#model.blocked`.

## Critic / Candidate Channels

- `#critic.claim`, `#critic.boundary`, `#critic.context`, `#critic.style`, `#critic.generic`, `#critic.schema`.
- `#candidate.ghost`, `#candidate.tournament`, `#candidate.compose`, `#candidate.dna`.

## Explainability Channels

- `#why.route`, `#why.hold`, `#why.seed`, `#why.model`, `#why.candidate`, `#receipt.candidate`, `#replay.work`.


## Required Runtime Behavior

The real implementation must keep this component deterministic where possible, typed at the boundary, local-only by default and candidate-only at output. Any future implementation must include positive and negative fixtures, registry entries, system map references and Codex task mapping.

## Failure Behavior

On malformed input, missing trace_id, missing privacy_class, authority escalation, direct apply request, raw secret payload or unbounded event fanout, this component must fail closed and emit a blocked QIRC event or an admissibility hold record.

## Codex Conversion Rule

Codex must build this as a small typed module with no hidden agent autonomy. If a model provider would be required, Codex must instead create a candidate ModelWorkPacket or a hold/split/ask_context route unless the provider stage has already been implemented under the correct PR bundle.
