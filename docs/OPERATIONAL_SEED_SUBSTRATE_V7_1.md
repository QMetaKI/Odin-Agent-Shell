# Operational Seed Substrate v7.1

Claim boundary: this document defines architecture, contracts, shadow behavior, and Codex build intent only. It does not claim host validation, model inference proof, network operation, deployment, security audit completion, app apply, or full implementation completeness.

## Purpose

The Operational Seed Substrate makes Odin's seed system real enough for routing, precompute, QIRC, Shadow Runtime, Y*, Fairy DSL, Runtime Packs, and model work. Seeds are not decoration. They are typed, scored, decayed, conflict-resolved, budgeted activation primitives.

## Seed lifecycle

```text
raw signal
→ seed candidates
→ activation score
→ decay pass
→ conflict resolver
→ top-k budget
→ archetype role activation
→ QMath route influence
→ why trace
```

## Seed packet

`odin_seed_activation_packet` contains `work_id`, `context_tags`, `active_seeds`, `suppressed_seeds`, `conflicts_removed`, `budget_profile`, `top_k_limit`, and `why_trace_ref`.

## Seed classes

```text
boundary
safety
context
economy
evidence
style
route
compiler
shadow
qirc
fairy
maria_michael
```

## Hard seeds

These may never be removed by normal decay: `children_family_first`, `candidate_only`, `claim_boundary`, `app_authority_preserve`, `no_hidden_apply`, and `local_first`.

## Seed conflict examples

`creative_expand` conflicts with `minimal_sufficient_route` when latency mode is interactive. `heavy_model_quality` conflicts with `low_memory_strict`. `external_refiner` conflicts with `remote_blocked`. `final_language` conflicts with `candidate_only`.

## Runtime Pack use

Runtime Pack Compiler may include only the seed families required by a capability slice. A low-memory pack may include hard seeds, context seeds, and economy seeds while excluding heavy creative expansion seeds.

## Codex rule

Every seed-producing module must output both activation reasons and suppression reasons. Hidden seed magic is forbidden.
