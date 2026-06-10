# Odin Agent Shell — v7.1 Narrative Compiler Integration

This document is part of the v0.6.0 Narrative Aorta / Y* Compiler Lock. It preserves the Odin Agent Shell v7.1 functional canon and adds a typed, bounded, auditable meta-authoring and compile-prelude layer.

Hard boundary: Fairy prose never executes. Y* Native DSL validates and stages. Shadow Runtime remains code-near blueprint. Runtime packs load only after validation. Odin Host remains the stable local boundary.

## Purpose

Generated Runtime Gates are tests and validators derived from Shadow Runtime IR and runtime pack manifests.

## Generated Gate Families

- schema gates,
- registry parity gates,
- candidate-only gates,
- claim-boundary gates,
- semantic bus local-only gates,
- app authority gates,
- model route ladder gates,
- capability slice gates,
- pack loader gates,
- narrative boundary gates.

## Required Generated Tests

Every Runtime Pack must produce:

- at least one positive golden flow,
- at least one negative direct-apply flow,
- one semantic bus local-only check,
- one candidate-only check,
- one claim-boundary check,
- one rollback metadata check.

## Codex Rule

Do not expand compiler output classes without adding generated gates.
