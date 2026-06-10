# Anti-Fairy DSL v7.1

## Definition
Anti-Fairy DSL is the structured negative counterpart to Fairy DSL. It encodes archetypic anti-patterns as compact, readable, testable, machine-mapped failure stories.

This document is part of Odin Agent Shell v7.1 / v0.7.0 Shadow Narrative Loki Anti-Pattern Lock. It is specification, shadow-runtime, validation and Codex-build guidance only. It does not claim runtime execution, model inference, host validation, network operation, deployment, security certification, app apply, external send, or full implementation completeness.

Core invariant: Odin remains candidate-only. App state, apply, external sends and domain reality remain app-owned. Loki/Shadow Narrative may reveal risk and propose gates; it may not decide authority or bypass Odin Final Gate.


## Why It Exists
Fairy DSL can bias the system toward ideal flow. Anti-Fairy DSL prevents narrative optimism from hiding bad paths. It gives Odin a formal way to ask: what failure story resembles this work request, model route, seed pack, runtime pack or agent handoff?

## Syntax Sketch
```text
ANTI_FAIRY story "small_worker_overload"

mirror_of: "small_helper_carries_safe_basket"
violates:
  - smallest_sufficient_worker
  - semantic_pressure_valve
signals:
  - slot_context_too_large
  - requested_output_requires_long_synthesis
  - model_route_underpowered
required_gate:
  - semantic_pressure_valve
repair:
  - split_work
  - escalate_7b_if_gain_positive
why_trace:
  user_safe: "This task was split because the requested context exceeded the safe micro-worker budget."
```

## Required Anchors
Anti-Fairy DSL must include: mirror_of, violated invariants, signals, required gate, repair route, why-trace note and test fixture reference.

## Anti-Pattern Families
- helpful_tyrant: helpfulness becomes unauthorized action.
- golden_fog: eloquent output hides unsupported claims.
- seed_hydra: seed activation fans out without budget.
- mirror_trap: critics loop without gain.
- false_ring_promotion: outer worker acts like core.
- loki_gift_hidden_cost: optimization creates boundary cost.
- qirc_flood: too many semantic events inflate work.
- app_shadow_takeover: Odin mirrors app state instead of digesting it.
- runtime_pack_mask: generated pack claims broader capabilities than allowed.

## Anti-Deception Boundary
Anti-Fairy does not make Odin suspicious for drama. It only surfaces typed risk. Each risk must be actionable, bounded and test-linked. If the signal is weak, the output is a watch note rather than a block.

## Integration Points
- Seed Pack Compiler uses Anti-Fairy to detect prompt-injection-shaped seeds.
- QIRC Gold Spine uses Anti-Fairy to prevent event fanout and trace fog.
- Model Route Ladder uses Anti-Fairy to detect hidden large-model temptation.
- Thor/Y Handoff Compiler uses Anti-Fairy to detect authority-transfer phrasing.
- Runtime Pack Compiler uses Anti-Fairy to detect overbroad capabilities.
