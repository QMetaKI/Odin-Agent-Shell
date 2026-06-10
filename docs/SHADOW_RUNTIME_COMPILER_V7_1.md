# Odin Agent Shell — v7.1 Narrative Compiler Integration

This document is part of the v0.6.0 Narrative Aorta / Y* Compiler Lock. It preserves the Odin Agent Shell v7.1 functional canon and adds a typed, bounded, auditable meta-authoring and compile-prelude layer.

Hard boundary: Fairy prose never executes. Y* Native DSL validates and stages. Shadow Runtime remains code-near blueprint. Runtime packs load only after validation. Odin Host remains the stable local boundary.

## Purpose

Shadow Runtime Compiler converts validated Shadow Runtime IR into Runtime Packs. This is the anti-drift bridge between architecture and execution.

## Compiler Inputs

- Shadow Runtime IR modules
- Y* Mediation Directives
- schemas
- registries
- resource profile
- caller manifest type
- model scale ladder
- policy tables
- semantic bus channel registry

## Compiler Outputs

- Runtime Pack Manifest
- compiled validators
- compiled route tables
- compiled policy gates
- compiled semantic bus registry
- compiled slot tables
- compiled output contract maps
- generated golden tests
- generated negative tests
- traceability map

## Modes

### AOT Compile

Install/update stage. Produces frozen default runtime packs.

### Cached Capability Compile

App pairing/profile stage. Produces app-specific capability slices.

### Interpreted Shadow Fallback

Debug/recovery only. Reduced capability, no heavy routes.

## Hot Path Rule

No normal user request may trigger arbitrary runtime generation. The hot path executes validated packs.

## Determinism Rule

Same source hash + same compile profile must produce the same pack hash.

## Codex Rule

Implement pack manifest and validator before AOT compiler. Implement validator before loader. Implement generated negative gates before enabling new pack types.
