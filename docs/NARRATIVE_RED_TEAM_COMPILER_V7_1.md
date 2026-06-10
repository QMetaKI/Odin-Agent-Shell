# Narrative Red-Team Compiler v7.1

## Purpose
The Narrative Red-Team Compiler turns Shadow Narrative anti-patterns into negative test cases and review prompts for Codex and Odin.

This document is part of Odin Agent Shell v7.1 / v0.7.0 Shadow Narrative Loki Anti-Pattern Lock. It is specification, shadow-runtime, validation and Codex-build guidance only. It does not claim runtime execution, model inference, host validation, network operation, deployment, security certification, app apply, external send, or full implementation completeness.

Core invariant: Odin remains candidate-only. App state, apply, external sends and domain reality remain app-owned. Loki/Shadow Narrative may reveal risk and propose gates; it may not decide authority or bypass Odin Final Gate.


## Generated Artifacts
- negative Universal Work fixture
- invalid handoff fixture
- seed pack abuse fixture
- QIRC fanout fixture
- runtime pack overclaim fixture
- agent adapter overreach fixture
- why-trace expectation

## Test Families
- no app mutation from model/agent
- no external send
- no direct apply
- no runtime pack overclaim
- no seed-pack execution
- no QIRC event without trace
- no agent consensus as receipt
- no Fairy prose execution
- no Loki authority

## Codex Rule
Red-team fixtures must be checked before feature expansion. If a new subsystem has no anti-pattern fixture, it is incomplete.

## Senior Reviewer Note
This compiler is the practical value of Shadow Narrative. It makes narrative=code visible as tests, not decoration.
