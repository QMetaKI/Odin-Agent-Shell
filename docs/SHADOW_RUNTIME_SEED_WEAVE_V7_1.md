# Shadow Runtime Seed Weave v7.1

Claim boundary: this document defines architecture, contracts, shadow behavior, and Codex build intent only. It does not claim host validation, model inference proof, network operation, deployment, security audit completion, app apply, or full implementation completeness.

## Purpose

The Shadow Runtime Seed Weave makes seeds visible in every code-near shadow path. It is the bridge between operational seed substrate and almost-real code.

## Required shadow fields

Every major shadow result should include `active_seeds`, `suppressed_seeds`, `archetype_roles`, `bug6_status`, `q7_status`, `route_score`, and `why_trace_ref`.

## Affected modules

- `universal_work_shadow`
- `semantic_bus_shadow`
- `qirc_gold_spine_shadow`
- `fairy_to_shadow_ir_shadow`
- `ystar_mediation_shadow`
- `model_route_shadow`
- `candidate_shadow`
- `runtime_pack_shadow`

## Flow

```text
seed packet
→ archetype roles
→ shadow contract tags
→ slot profile
→ runtime pack profile
→ candidate DNA
```

## Candidate DNA enrichment

Candidate DNA should record seed activation packet id, archetype role packet id, Bug6 packet id, Q7 packet id, route score id, and why trace id.

## Codex rule

A shadow module without seed weave fields may be accepted only if it is explicitly marked `seed_irrelevant: true` with reason.
