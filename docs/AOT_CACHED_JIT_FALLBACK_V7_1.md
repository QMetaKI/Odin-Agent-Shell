# Odin Agent Shell — v7.1 Narrative Compiler Integration

This document is part of the v0.6.0 Narrative Aorta / Y* Compiler Lock. It preserves the Odin Agent Shell v7.1 functional canon and adds a typed, bounded, auditable meta-authoring and compile-prelude layer.

Hard boundary: Fairy prose never executes. Y* Native DSL validates and stages. Shadow Runtime remains code-near blueprint. Runtime packs load only after validation. Odin Host remains the stable local boundary.

## Purpose

AOT / Cached-JIT / Fallback Modes define when compilation may occur.

## AOT Compile

Used during install/update. Produces default packs before normal use.

## Cached Capability Compile

Used during app pairing or resource profile changes. Produces a cached capability slice and reuses it until source hash or caller manifest changes.

## Interpreted Shadow Fallback

Used only for debug or recovery. It is reduced capability and may not use heavy routes or external network.

## Forbidden

- live compile during normal user request,
- arbitrary code generation on hot path,
- hidden pack invalidation,
- pack replacement without trace.

## Performance Rule

Compile before use. Execute fast during use.


## Pack Invalidation Policy

A cached capability compile is invalidated only when the caller manifest hash, resource profile, source Shadow Runtime hash, Y* source hash, schema set, registry set or policy table hash changes. Normal user requests may not invalidate packs directly.

## Recovery Behavior

If AOT compile fails, Odin remains in previous validated pack state or falls back to a reduced safe shadow interpreter mode. The fallback mode disables heavy routes, external network, runtime-pack expansion and app mutation. It exists only for recovery and diagnostics.

## Trace Requirements

Every compile mode must write source hash, compiler profile, pack id, validation result and rollback target. The trace is a diagnostic artifact and not a runtime proof claim.
