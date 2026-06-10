# Perceived Intelligence Metrics v7.1

Status: Odin Agent Shell v7.1 integrated lock. This document is specification and shadow-runtime preparation only. It does not claim runtime proof, model proof, host validation, deployment, security audit completion, production readiness, app apply, or external send.

Core invariants preserved: app owns state, app owns apply, Odin returns candidate artifacts, models remain bounded projection workers, QIRC is local/internal, no hot-path runtime generation, no prose-only execution, no unvalidated runtime pack load, and all visible intelligence must remain traceable by Candidate DNA / Why Trace.


## Purpose
Odin measures not only model accuracy but user-visible usefulness. The user experiences fit, speed, clarity, actionability, and trust — not raw parameter count.

## Metrics
- `perceived_task_understanding`
- `visible_usefulness`
- `first_response_fit`
- `correction_needed_rate`
- `user_actionability`
- `candidate_choice_quality`
- `why_trace_clarity`
- `model_work_avoided`
- `large_model_avoidance_rate`
- `unsupported_claim_rate`
- `app_apply_boundary_clarity`

## Scoring Rule
Metrics are advisory. They may inform Model Dojo and route selection, but may not override claim boundaries, safety gates, or app-owned apply.

## Anti-Deception Boundary
Perceived intelligence must come from actual structure: better context, better candidates, better explanation, better actions. It must not come from false claims, hidden verification, or pretending a smaller model performed analysis it did not perform.

## Use in Model Router
If a low-cost route produces high visible fit with low correction rate, Odin should prefer it. If user corrections spike, route profile must increase quality or ask context.
