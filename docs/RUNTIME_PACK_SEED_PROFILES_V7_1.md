# Runtime Pack Seed Profiles v7.1

Claim boundary: this document defines architecture, contracts, shadow behavior, and Codex build intent only. It does not claim host validation, model inference proof, network operation, deployment, security audit completion, app apply, or full implementation completeness.

## Purpose

Runtime Packs should not load the full seed universe. They should compile only the seed families, archetype roles, QIRC channels, and gates needed for their profile.

## Pack profiles

### Low Memory Strict

```text
hard seeds only
context seeds
economy seeds
small role set
semantic bus light
no heavy model seeds
```

### Standard Local

```text
hard seeds
context seeds
economy seeds
style seeds
3B/7B hybrid route seeds
normal role set
```

### Quality Local

```text
standard seeds
quality_synthesis seeds
style refinement seeds
candidate tournament seeds
```

### Heavy Local / Batch

```text
quality seeds
long synthesis seeds
batch trace seeds
explicit latency approval required
```

## Runtime Pack Manifest extension

```json
{
  "seed_profile": "standard_local_seed_profile",
  "included_seed_families": ["boundary", "context", "economy", "style"],
  "excluded_seed_families": ["heavy_batch", "remote_refiner"],
  "bug6_profile": "strict",
  "q7_profile": "standard"
}
```

## Codex rule

Runtime Pack Compiler must reject packs that omit hard seeds or include remote/heavy seed families without matching policy.
