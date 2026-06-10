# Schema Policy

Schemas under `schemas/v7_1/` are the contract surface. Implementations must validate all external and inter-layer packets against schemas where practical.

## Rules

- New packet type requires schema.
- Schema requires `artifact_kind` and `protocol_version` where applicable.
- Candidate-producing schemas must preserve candidate-only law.
- Schema changes require tests and registry updates.
