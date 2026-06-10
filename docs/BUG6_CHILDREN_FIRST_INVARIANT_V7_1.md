# Bug6 / Children-First Invariant v7.1

Claim boundary: this document defines architecture, contracts, shadow behavior, and Codex build intent only. It does not claim host validation, model inference proof, network operation, deployment, security audit completion, app apply, or full implementation completeness.

## Purpose

Bug6 is the hard invariant that Odin must never optimize for model cleverness at the expense of protective structure, bounded authority, family-safe posture, or child-load discipline. In public Odin terms this is the **Children-First Safety Invariant**. It is not a UI persona, not moral theater, and not a permission to infantilize users. It is a runtime design invariant.

## Functional meaning in Odin

Bug6 means:

- do not overload weak workers with full-system context;
- do not let models carry authority they cannot safely carry;
- do not hide apply or external-send authority inside generated candidates;
- do not route to a larger model when a smaller bounded path is safer and sufficient;
- do not let narrative prose bypass typed DSL validation;
- do not let app-owned state become Odin-owned state;
- do not make unverifiable claims look real.

## Where Bug6 sits

```text
Universal Work ingress
→ Bug6 Pre-Selector Invariant Gate
→ Odin Core Centerline
→ QLI Master Interface
→ DFAS Stability Core
→ Seed / Archetype Economy
→ QMath Route Score
→ Model Route or Hold
→ Candidate Artifact
→ Bug6 Final Projection Gate
```

## Bug6 packet

The canonical packet is `odin_bug6_invariant_packet`.

Required fields:

- `work_id`
- `centerline_id`
- `children_first_preserved`
- `authority_separation_preserved`
- `worker_load_preserved`
- `candidate_only_preserved`
- `violations`
- `decision`

## Decisions

```text
allow
hold
split_work
ask_context
block
```

## Interaction with QIRC Gold Spine

QIRC emits Bug6 events on:

- `#bug6.precheck`
- `#bug6.worker_load`
- `#bug6.authority`
- `#bug6.final_projection`

No model dispatch can occur until the Bug6 precheck is green or explicitly resolved as `split_work` or `ask_context`.

## Interaction with Seeds

Bug6 is always represented as high-priority operational seeds:

- `children_family_first`
- `authority_separation`
- `candidate_only`
- `worker_load_limit`
- `no_hidden_apply`

These seeds may not be decayed below the hard floor defined in `bug6_invariant_registry.json`.

## Interaction with Fairy/Y*

Fairy prose may express Children-First meaning, but only Y* Native DSL may compile. The compiler must reject any Y* unit that lacks `candidate_only: true`, `app_authority: preserve`, `final_gate: odin`, and `children_first: preserve`.

## Interaction with Shadow Runtime

Every Shadow Runtime flow receives a Bug6 posture check before it can emit Worklet Graph, Slot Contract, ModelWorkPacket, Candidate Artifact, or Runtime Pack fragment.

## Codex rule

Codex must implement Bug6 as a gate and packet family, not as comments. Any implementation that merely documents Children-First without enforcing route, authority, or load constraints is incomplete.

## Red lines

- No direct app mutation.
- No external send.
- No hidden apply.
- No full-context dump into weak local models.
- No unbounded seed fanout.
- No narrative-only execution.
- No model route before admissibility.
- No output that presents a candidate as final app reality.
