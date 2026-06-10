# Odin Agent Shell — v7.1 Narrative Compiler Integration

This document is part of the v0.6.0 Narrative Aorta / Y* Compiler Lock. It preserves the Odin Agent Shell v7.1 functional canon and adds a typed, bounded, auditable meta-authoring and compile-prelude layer.

Hard boundary: Fairy prose never executes. Y* Native DSL validates and stages. Shadow Runtime remains code-near blueprint. Runtime packs load only after validation. Odin Host remains the stable local boundary.

## Purpose

Capability Slice Compiler creates minimal app-specific runtime packs based on Caller Manifest, resource profile and allowed tasks.

## Inputs

- Caller Manifest
- resource profile
- allowed verbs
- allowed artifact types
- allowed output contracts
- privacy policy
- model policy
- semantic bus policy

## Output

- app capability runtime pack
- app-specific validator
- app-specific route map
- blocked capability list
- generated negative tests

## Example

Wedding Studio App needs document lens, wedding speech lens, context distillery, 3B+7B/8B route and candidate renderer contracts. It does not need bounded code work, game state lens or patchplan route.

## Efficiency Rule

A capability slice should not load features unrelated to the caller manifest.

## Safety Rule

Capability slice may only remove or narrow capabilities. It may not expand beyond caller manifest.
