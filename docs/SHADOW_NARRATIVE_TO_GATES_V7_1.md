# Shadow Narrative to Gate Compiler v7.1

## Purpose
This compiler maps narrative anti-patterns into Odin gates. It is a compiler for safety logic, not a model, not a text generator, and not an executor.

This document is part of Odin Agent Shell v7.1 / v0.7.0 Shadow Narrative Loki Anti-Pattern Lock. It is specification, shadow-runtime, validation and Codex-build guidance only. It does not claim runtime execution, model inference, host validation, network operation, deployment, security certification, app apply, external send, or full implementation completeness.

Core invariant: Odin remains candidate-only. App state, apply, external sends and domain reality remain app-owned. Loki/Shadow Narrative may reveal risk and propose gates; it may not decide authority or bypass Odin Final Gate.


## Compiler Pipeline
```text
shadow narrative unit
→ parse anti-pattern fields
→ validate required signals
→ resolve gate family
→ bind repair route
→ emit negative fixture
→ bind to Runtime Pack / Capability Slice
→ expose Why Trace note
```

## Inputs
- odin_shadow_narrative
- odin_anti_fairy_unit
- odin_narrative_antipattern
- odin_loki_mediation_packet
- registries/narrative_antipattern_registry.json
- registries/shadow_to_gate_registry.json

## Outputs
- gate binding map
- negative test fixture
- runtime pack gate requirement
- candidate why-trace annotation
- unresolved holes report

## Hard Rule
If the compiler cannot map a story to a gate and fixture, the story cannot affect runtime behavior.

## Example
small_worker_overload maps to semantic_pressure_valve with repair split_work_or_escalate. The generated negative fixture asserts that a 3B route cannot be selected for long synthesis if slot pressure exceeds threshold.
