# Q Metamodell / CUTK1 Intake for Odin v7.1

## Purpose

This document binds relevant Q Metamodell and CUTK1 patterns into Odin as neutral runtime concepts. The goal is not to import naming or public mythology. The goal is to extract operational mechanisms that improve local LLM quality, efficiency, safety and explainability.

## Core Source Findings

CUTK1 contains implementation-adjacent primitives for precompute-first and token-economy behavior: seed/archetype/composition budgeting, QMath center scoring, minimal change scope resolution, packet/export discipline and QIRC replay/projection snapshot compression. These are directly relevant to Odin because Odin's main purpose is to reduce expensive/chaotic model work by turning broad requests into compact, bounded, model-ready packets.

CUTK1 also identifies explicit runtime economy budgets, trigger hold/simulate gates, QMath center scoring, single-truth runtime packet building, minimal change scope resolution, seed activation/decay/conflict, QIRC replay snapshots, middle-out/radial states, resonance normalization and children/family invariant pruning.

For Odin this becomes a clear next optimization: add an Odin Core Centerline, QLI-like Master Interface, DFAS Stability Core, Seed/Archetype Economy, QMath Center Solver, Ring Radar/Resonance and Why Trace.

## Neutralized Operational Imports

### Runtime Economy

Odin should maintain budget profiles for:

- seed activation count
- archetype role activation count
- worklet fan-out
- candidate tournament branch count
- critic cascade depth
- context capsule token ceiling
- model route ceiling
- retry count
- trace retention depth

### Trigger Hold / Simulate Gate

Before invoking a model, Odin should decide:

- continue
- hold
- ask_context
- split_work
- deterministic_only
- 3b_micro
- 7b_8b_quality
- hybrid
- block

This replaces impulsive model dispatch with admissibility.

### QMath Center Scoring

Odin should score center candidates by stability gain minus cost terms. Costs include latency, token load, route complexity, privacy risk, claim risk, model uncertainty and context ambiguity. The best center is not the broadest answer; it is the smallest stable center that preserves boundaries.

### Minimal Change Scope

For code, document, workflow and app tasks, Odin should compute impact zone and narrow scope before model work. This is especially important for bounded code work and Codex handoff.

### Seed/Archetype Economy

Seed and archetype activation should happen before context distillation and slot forging. Activation is scored, capped, decayed, conflict-checked and recorded in Candidate DNA.

### QIRC Replay / Hot Window

The Internal Semantic Bus should not replay full history into models. It should produce active hot-window snapshots: recent events, warnings, route hints, active seeds and unresolved holes.

### Ring Radar / Resonance

Odin should maintain ring activation maps and deviation triggers. Only rings with meaningful pressure should activate more work. This prevents unnecessary subsystem fan-out.

## Odin-Specific Application

The following Odin components receive the intake:

- Universal Work Kernel gets centerline and admissibility before route.
- Small Model Power Layer gets seed/archetype budget and QMath route score.
- Internal Semantic Bus gets hot-window replay snapshot and seed prewarm packets.
- Shadow Runtime gets centerline, seed economy and why-trace modules.
- Runtime Pack Compiler gets generated gates for admissibility and route scoring.
- Candidate DNA gets active seeds, archetype roles, center score and blocked-route reasons.

## Safety Interpretation

The Q Core / Y Core analogy is valid only for Odin-internal LLM work. Odin Core does not own app state. Odin Core is a local boundary and admissibility center for model routing, candidate generation and LLM-side preparation.

## Codex Rule

Codex must implement the intake as typed data, algorithms, registries and tests. It must not implement it as free-form prose or unbounded agent behavior.
