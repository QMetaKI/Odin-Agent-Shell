# QIRC Precompute Field v7.1

Status: Odin Agent Shell v7.1 integrated lock. This document is specification and shadow-runtime preparation only. It does not claim runtime proof, model proof, host validation, deployment, security audit completion, production readiness, app apply, or external send.

Core invariants preserved: app owns state, app owns apply, Odin returns candidate artifacts, models remain bounded projection workers, QIRC is local/internal, no hot-path runtime generation, no prose-only execution, no unvalidated runtime pack load, and all visible intelligence must remain traceable by Candidate DNA / Why Trace.


## Definition
The QIRC Precompute Field is the active internal event field that runs before model dispatch. It connects Odin Core, QLI Master Interface, DFAS Stability, Seed/Archetype Economy, QMath, Ring Radar, Runtime Pack Capability Slices, and Output Intelligence Composer.

## Core Channels
- `#context.hot_window`
- `#seed.prewarm`
- `#archetype.role`
- `#dfas.admissibility`
- `#qmath.route_score`
- `#ring.radar`
- `#model.avoidance`
- `#slot.forge`
- `#output.compose`
- `#why.trace`

## Field Logic
QIRC does not merely log. It routes typed precompute events. Each event must have work_id, trace_id, channel, source_module, authority_scope, privacy_class, payload summary, and redaction posture.

## Precompute Cycle
```text
ingress_event
→ hot_window_snapshot
→ seed_budget_check
→ archetype_roles_activated
→ centerline_scored
→ admissibility_decided
→ model_work_avoidance_decided
→ slot_or_no_model_output_planned
```

## Objective
The field creates the sense that Odin understands the task before any LLM begins. This is objective because the system has actually performed structure, filtering, scoring, and routing.

## Red Lines
No network expansion. No public IRC. No raw secret payloads. No full app-state mirror. No channel may mutate app state. No channel may directly dispatch a model unless admissibility has passed.
