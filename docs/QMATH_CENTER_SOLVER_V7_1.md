# QMath Center Solver v7.1

## Purpose

The QMath Center Solver provides deterministic scoring for center selection and route decisions. It is the numeric counterpart to narrative centerline selection.

## Core equation

```text
route_score = expected_quality_gain
            + stability_gain
            + boundary_fit
            + context_fit
            - token_cost
            - latency_cost
            - complexity_cost
            - privacy_risk
            - claim_risk
            - uncertainty_cost
```

## Center candidate scoring

Each center candidate receives:

- center_clarity
- artifact_fit
- output_contract_fit
- boundary_fit
- app_authority_fit
- seed_support
- archetype_role_support
- route_feasibility
- uncertainty

The chosen center is the smallest stable center with enough support.

## Route scoring

Routes:

- deterministic
- 1b_2b_micro
- 3b_micro
- 3b_multi
- 7b_8b_quality
- 3b_7b_8b_hybrid
- quality_13b_14b
- heavy_22b_32b_batch
- remote_optional_explicit
- cannot_safely_complete

Each route must declare:

- expected_gain
- cost
- risk
- latency class
- resource profile fit
- fallback
- reason

## Stop rule

If a smaller route clears threshold, larger routes are blocked unless the output contract explicitly requires quality escalation and route score justifies it.

## Why Trace integration

Every route score writes:

- selected route
- blocked routes
- score components
- thresholds
- reasons
- fallback path

## Codex Rule

Provider adapters may not select models directly. They execute a route plan produced by the QMath Center Solver / Model Router combination.
