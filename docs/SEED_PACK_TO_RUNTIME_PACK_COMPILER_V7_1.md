# Seed Pack to Runtime Pack Compiler v7.1

```text
artifact_kind: odin_v7_1_document
lock: v0.6.9 APP_SEED_PACK_COMPILER_LOCK
claim_boundary: specification_only_not_runtime_or_implementation_claim
```

## Purpose

Seed Pack to Runtime Pack Compiler v7.1 defines a bounded, typed, app-provided Seed Pack system for Odin. Apps may ship seed packs that Odin can ingest, validate, compile, score, activate, and bind into QIRC, Odin Core, Y*, Fairy DSL, Shadow Runtime, Runtime Packs, Model Routing and Output Composition without granting the app or seed pack execution authority.

## Required anchors

- Runtime Pack capability slice
- Shadow Runtime seed weave
- compiled seed profile
- Generated gates

## Seed Pack System Position

The App Seed Pack Compiler is not a content loader. It is the ingestion and compilation layer for app-provided semantic operational material. A seed pack may include domain seeds, workflow seeds, style seeds, safety seeds, QIRC prewarm rules, artifact lens hints, archetype role preferences, slot forge hints, output composer patterns, model work avoidance preferences, and candidate experience defaults. These are declarative. Odin compiles them into internal profiles and runtime pack slices.

The functional equation is:

```text
App Seed Pack
→ validation
→ trust classification
→ seed graph normalization
→ operational seed function normalization
→ conflict/decay/budget policy
→ archetype role binding
→ QIRC prewarm plan
→ Shadow Runtime seed weave
→ Runtime Pack capability slice
→ Model Work Avoidance / Slot Forge / Output Composer
```

## Security Boundary

Seed packs are input artifacts, not plugins. They are never executed as code by default. Any functional element must be expressed as a typed operational seed function. Operational seed functions are declarative transforms or routing hints such as activate, decay, conflict_resolve, budget_cap, lens_hint, slot_hint, qirc_prewarm, output_pattern, why_trace_hint, and model_avoidance_hint. They compile to Odin-owned runtime tables and worklet hints, not to arbitrary user-provided code.

## Quality and Efficiency Thesis

The objective improvement is that apps can ship their own high-signal priors. Odin no longer starts cold for a domain. It receives structured semantic fuel: what matters, what must be avoided, which role patterns fit, which contexts are usually hot, which claims are forbidden, which output shapes users expect, which small model roles are useful, and which escalation routes are wasteful.

This helps all model sizes. 3B becomes better at domain-specific micro-work. 7B/8B receives cleaner context and style constraints. Larger models are called less often and for smaller premium fragments. Remote workers receive redacted, scoped, contract-bound tasks.

## Compiler Stages

Required compiler stages:

```text
SPC-01 Manifest validation
SPC-02 Trust and provenance classification
SPC-03 Seed unit normalization
SPC-04 Operational function validation
SPC-05 Seed graph construction
SPC-06 Conflict and decay analysis
SPC-07 Budget and fanout capping
SPC-08 Archetype role binding
SPC-09 QIRC prewarm plan build
SPC-10 Y*/Fairy binding build
SPC-11 Shadow Runtime seed weave
SPC-12 Runtime Pack capability slice compile
SPC-13 Generated gates and negative tests
SPC-14 Why Trace profile export
```

## App Integration Rule

Apps may include seed packs under their own repository or package. Odin discovers them through the app's Caller Manifest and App Seed Pack Manifest. The app remains authority over app state. Odin remains authority over LLM orchestration. The seed pack contributes bounded priors, never commands. If the seed pack conflicts with Odin Core, Bug6, Q7, GPL-2.0-only policy, Claim Boundary, App-owned Apply, or Remote Worker Boundary, Odin blocks or narrows the seed pack.

## Runtime Pack Output

Compiled output may include seed activation tables, role binding profiles, app-specific artifact lens overlays, QIRC prewarm channel lists, model work avoidance tables, output composer patterns, Why Trace templates, and negative gate fixtures. It may not include arbitrary executable code from the app seed pack.

## Red Lines

```text
No arbitrary seed-pack code execution.
No seed pack may mutate app state.
No seed pack may bypass Odin Final Gate.
No seed pack may expand model authority.
No seed pack may grant remote permission.
No seed pack may smuggle secrets or raw app state.
No seed pack may override Bug6, Q7, app-owned apply, GPL-2.0-only, or candidate-only law.
```

## Codex Rule

Codex must treat this document as build contract. Implement validator before compiler, compiler before loader, loader before runtime use, and negative tests before feature expansion. All later changes must update internal PR ladder, real bundle mapping, registries, schemas, shadow runtime, system map and file manifest.
