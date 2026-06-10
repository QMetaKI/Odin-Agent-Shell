# Narrative Anti-Pattern Mirror v7.1

## Purpose
The Narrative Anti-Pattern Mirror converts archetypic failure stories into concrete Odin gates, negative tests and repair routes.

This document is part of Odin Agent Shell v7.1 / v0.7.0 Shadow Narrative Loki Anti-Pattern Lock. It is specification, shadow-runtime, validation and Codex-build guidance only. It does not claim runtime execution, model inference, host validation, network operation, deployment, security certification, app apply, external send, or full implementation completeness.

Core invariant: Odin remains candidate-only. App state, apply, external sends and domain reality remain app-owned. Loki/Shadow Narrative may reveal risk and propose gates; it may not decide authority or bypass Odin Final Gate.


## Mirror Contract
```text
shadow narrative -> anti-pattern id -> signal set -> gate -> negative fixture -> repair route -> why trace
```

## Gate Families
- claim_evidence_gate
- app_apply_boundary_gate
- autonomy_escalation_gate
- seed_budget_noise_gate
- qirc_fanout_gate
- semantic_pressure_valve
- ring_authority_gate
- runtime_pack_capability_gate
- model_overconfidence_gate
- prompt_injection_gate

## Pattern Examples
### Helpful Tyrant
The system helps so strongly that it silently decides. Gate: app_apply_boundary_gate. Repair: return action candidate only.

### Golden Fog
The output is beautiful but evidence-light. Gate: claim_evidence_gate. Repair: downgrade language and attach evidence gaps.

### Seed Hydra
One seed activates many more until the route becomes noisy. Gate: seed_budget_noise_gate. Repair: top-k cap and conflict resolver.

### Mirror Trap
Critics keep reflecting without measurable gain. Gate: loop_gain_threshold. Repair: stop and produce review candidate.

### False Ring Promotion
Outer worker behaves like Odin Core. Gate: ring_authority_gate. Repair: demote to candidate_worker_only.

### Loki Gift Hidden Cost
An optimization hides a boundary cost. Gate: qmath_route_score_penalty. Repair: route only if total gain remains positive.

## Codex Implementation Rule
Every anti-pattern must be represented in registry form and at least one negative fixture. If no fixture exists, the pattern remains candidate doctrine and may not be used as a hard gate.
