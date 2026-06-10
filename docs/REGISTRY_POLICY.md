# Registry Policy

Registries define canonical names for artifact types, verbs, output contracts, slot classes, model ladder, semantic bus channels, failure states and acceptance gates.

## Rules

- Do not hardcode canonical lists in implementation without registry source.
- Registry additions require validation and tests.
- Semantic bus channels must be local-only by default.
- Model scale ladder default must remain `3b_7b_8b_hybrid`.
