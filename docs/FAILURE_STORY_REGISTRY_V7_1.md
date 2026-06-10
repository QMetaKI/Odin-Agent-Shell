# Failure Story Registry v7.1

## Purpose
The Failure Story Registry is a typed catalog of narrative anti-patterns. It is designed for Codex, validators and Odin Shadow Runtime, not for user-facing storytelling.

This document is part of Odin Agent Shell v7.1 / v0.7.0 Shadow Narrative Loki Anti-Pattern Lock. It is specification, shadow-runtime, validation and Codex-build guidance only. It does not claim runtime execution, model inference, host validation, network operation, deployment, security certification, app apply, external send, or full implementation completeness.

Core invariant: Odin remains candidate-only. App state, apply, external sends and domain reality remain app-owned. Loki/Shadow Narrative may reveal risk and propose gates; it may not decide authority or bypass Odin Final Gate.


## Entry Structure
Each failure story includes:
- id
- name
- short narrative form
- technical anti-pattern
- trigger signals
- affected subsystem
- violated invariant
- required gate
- repair route
- example negative fixture
- why-trace text
- severity band
- resource impact

## Required Families
1. Authority Drift
2. Apply Confusion
3. Claim Fog
4. Seed Hydra
5. QIRC Flood
6. Critic Loop
7. Worker Overload
8. Runtime Pack Overclaim
9. Seed Pack Injection
10. Remote Worker Overreach
11. Tool Permission Leak
12. Semantic Diff Masking
13. Candidate Merge Without Review
14. Missing Why Trace
15. Hidden Model Escalation

## Severity Bands
- watch: record and disclose.
- narrow: reduce scope or split work.
- hold: ask context or await review.
- block: forbidden until user/app provides valid boundary.

## Integration
The registry feeds Anti-Fairy DSL, Loki mediation, QIRC Why Trace, generated negative tests and runtime pack gates.


Machine field alias: required_gate. Every registry entry must expose required_gate as a JSON field or documented mapping.
