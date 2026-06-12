# FINAL-PR-07: DFAS Field Selection + Coherence / Review Axes + Route Scoring

## Purpose / Objective

Implement neutral DFAS-derived field selection, dominance/suppression metadata, coherence scores, review axes, route scoring, hole density, and center-first routing. The implementation ranks and explains routes before model work using deterministic metadata.

## Base rule

Base: current main after FINAL-PR-06 merge. Do not base on open PR branches. Do not rewrite historical merged PRs.

## Allowed scope

Create the smallest deterministic, local-only field selection package. Add docs, neutral registries if needed, tests, validator, CLI hooks, proof packet, SYSTEM_MAP and FILE_MANIFEST updates. Preserve candidate-only outputs.

## Forbidden scope

No provider execution, model inference, API key reads, external network, public QIRC/network/federation, app apply, app state mutation, external send, production readiness claim, security certification claim, hidden authority, religious interpretation, persona injection, source-pattern runtime import, or Q-style new runtime artifact names.

## Files to create

- `odin/field_selection/__init__.py`
- `odin/field_selection/dfas.py`
- `odin/field_selection/coherence.py`
- `odin/field_selection/review_axes.py`
- `odin/field_selection/route_scoring.py`
- `odin/field_selection/proof.py`
- `tools/rebaseline/check_field_selection.py`
- `tests/test_final_pr_07_field_selection.py`
- `reports/final_pr_07_field_selection_proof_packet.json`

## Required objects

- `FieldSelection`
- `DominanceMap`
- `SuppressedField`
- `CoherenceScore`
- `ReviewAxis`
- `RouteScore`
- `HoleDensity`
- `CenterFirstRoute`

## Required review axes

- `evidence_vs_assumption`
- `scope_vs_sprawl`
- `care_vs_force`
- `center_vs_expansion`
- `novelty_vs_stability`
- `candidate_vs_claim`

## CLI commands

- `python -m odin.cli validate-field-selection`
- `python -m odin.cli explain-field-route --demo`
- `python -m odin.cli prove-field-selection`

## Validator requirement

Create `tools/rebaseline/check_field_selection.py`. It must verify files, neutral naming, required objects, review axes, deterministic scoring metadata, candidate-only/local-only/app-owned-apply flags, forbidden scope text, no provider/model execution, no app apply/state/external-send authority, no new forbidden Q-style runtime/schema/registry/CLI artifact names, and proof packet shape.

## Tests requirement

Create `tests/test_final_pr_07_field_selection.py` covering field selection, dominance/suppression metadata, coherence score ranges, review axes, route score ordering, hole-density behavior, center-first route explanation, negative boundaries, CLI validator, proof packet generation, and `validate-all` integration.

## Proof packet requirement

Create `reports/final_pr_07_field_selection_proof_packet.json` via `prove-field-selection`. It must state `candidate_only: true`, `local_only: true`, `app_owned_apply: true`, no provider/model execution, no network, no app apply/state/external-send, and no truth authority.

## Required invariant

DFAS/field selection ranks and explains routes. It does not authorize apply, model execution, external send, or truth.

## Senior review loop

Before finalizing, simulate a senior reviewer and a senior code reviewer. Confirm the implementation is bounded, neutral, deterministic, small, test-covered, and does not add hidden authority or runtime/model/app claims. Apply fixes before the final response.

## Final response format

Return summary, files changed, what remains scaffold, non-claims, and exact tests run. Each test/check command must be prefixed with pass/warn/fail status.
