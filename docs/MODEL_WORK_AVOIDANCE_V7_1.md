# Model Work Avoidance v7.1

Status: Odin Agent Shell v7.1 integrated lock. This document is specification and shadow-runtime preparation only. It does not claim runtime proof, model proof, host validation, deployment, security audit completion, production readiness, app apply, or external send.

Core invariants preserved: app owns state, app owns apply, Odin returns candidate artifacts, models remain bounded projection workers, QIRC is local/internal, no hot-path runtime generation, no prose-only execution, no unvalidated runtime pack load, and all visible intelligence must remain traceable by Candidate DNA / Why Trace.


## Purpose
Model Work Avoidance is the explicit mechanism for not calling a model when deterministic, cached, templated, or precomputed work is enough.

## Decision Outputs
- `no_model_static_candidate`
- `no_model_template_candidate`
- `no_model_cached_candidate`
- `model_required_micro`
- `model_required_quality`
- `model_required_hybrid`
- `ask_context`
- `split_work`
- `hold`
- `block`

## Scoring
```text
avoidance_score = deterministic_fit + cache_fit + template_fit + risk_reduction
                  - user_quality_requirement - ambiguity_penalty
```
A model call is avoided when the score clears the resource-profile threshold and the output contract can be satisfied without hallucination or false claim.

## Examples
- Schema repair with known pattern: no-model or 3B micro.
- Button label suggestion: no-model template + optional 3B variant.
- Traureden final prose: model required.
- Unsupported claim verification: block or ask for evidence.

## Large Model Avoidance
Even when a model is needed, a large model is avoided when smaller route plus Output Intelligence Composer achieves the visible user goal. This is not quality reduction; it is route discipline.

## Required Trace
Every avoidance decision must record what work was avoided, why, what quality risk remains, and what fallback exists.
