# Odin Y-Core Posture v7.1

Claim boundary: this document defines architecture, contracts, shadow behavior, and Codex build intent only. It does not claim host validation, model inference proof, network operation, deployment, security audit completion, app apply, or full implementation completeness.

## Purpose

Odin can be viewed as a Y-Core-like system only inside its bounded domain: local LLM orchestration, precompute, routing, model work packets, candidates, and explainable traces. Odin is not the app's sovereign core. Odin is the **LLM Work Core**.

## Authority split

```text
App Core:
- app state
- domain truth
- apply
- external sends
- user accounts
- product workflow

Odin Y-Core:
- LLM work admissibility
- candidate boundaries
- model route authority
- internal semantic bus
- seed/archetype activation
- QMath score
- why trace
```

## Odin Ring 0

Odin Ring 0 is not app Ring 0. Odin Ring 0 is only the internal boundary and final gate for LLM work. It guards model dispatch, candidate status, claim boundaries, app authority preservation, and traceability.

## Ring posture

```text
R0 Boundary / Final Gate
R1 Policy / Bug6 / Q7
R2 Universal Work
R3 Context / Hot Window
R4 QIRC Gold Spine
R5 Seeds / Archetypes
R6 QMath / DFAS
R7 Worklets / Slots
R8 Model Route
R9 Candidate / Trace
```

## Y-Core output

Odin Y-Core never outputs app reality. It outputs admissibility decisions, route plans, seed activation packets, archetype role packets, route scores, candidate artifacts, and why traces.

## Y-Core and Maria/Michael

Default posture is 80 Maria / 20 Michael for holding order, context coherence, family-first, and human-readable synthesis. High-risk or code/compiler contexts may shift to Michael-heavy profiles, but the profile must be explicit and traceable.

## Codex rule

Any real implementation must preserve the app/Odin authority split. A module called `core` may not become an app authority bridge.
