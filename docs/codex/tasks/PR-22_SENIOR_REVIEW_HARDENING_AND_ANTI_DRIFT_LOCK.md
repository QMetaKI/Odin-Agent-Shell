# PR-22 — Senior Review Hardening and Anti-Drift Lock

## Objective

Integrate senior reviewer findings into the repository canon, validation surface, internal PR ladder and real PR bundle plan before final release-prep work proceeds.

## Primary Files

```text
docs/reviews/SENIOR_REVIEW_SIMULATION_V0_4_2.md
docs/SENIOR_REVIEW_REMEDIATION_PLAN_V0_4_2.md
docs/CODEX_ANTI_DRIFT_POLICY.md
docs/TRACEABILITY_MATRIX_V7_1.md
docs/QUALITY_RISK_REGISTER_V7_1.md
docs/SEMANTIC_BUS_RED_LINES_V7_1.md
docs/PUBLIC_REPO_RELEASE_CHECKLIST_V7_1.md
registries/codex_task_registry.json
registries/codex_pr_bundle_registry.json
SYSTEM_MAP.json
FILE_MANIFEST.json
tests/test_senior_review_hardening.py
```

## Required Behavior

```text
Senior review findings are captured as persistent build obligations.
PR-22 appears in the internal ladder.
PR-22 is covered by REAL-PR-08.
Traceability matrix links architecture/spec areas to tasks and bundles.
Anti-drift policy defines Codex implementation boundaries.
Semantic Bus red-line policy exists.
Risk register captures critical/high/medium implementation risks.
Public release checklist avoids runtime overclaims.
Validation and tests pass.
```

## Forbidden Scope

```text
Do not implement runtime features in PR-22.
Do not add provider adapters.
Do not add UI/control-center behavior.
Do not enable remote routes.
Do not change the default model strategy away from 3B + 7B/8B hybrid.
Do not weaken candidate-only or app-owned apply rules.
```

## Definition of Done

```text
python -m odin.cli validate-all passes.
pytest passes.
PR-22 is present in codex_task_registry.
PR-22 is included in a real Codex PR bundle.
Senior review docs exist and contain required anchors.
Traceability matrix exists and includes PR-22.
Semantic Bus red-line policy exists.
Quality risk register exists.
FILE_MANIFEST.json is refreshed.
```

## Codex PR Summary Template

```text
PR: PR-22 Senior Review Hardening and Anti-Drift Lock
Architecture areas touched:
Specs touched:
Senior review findings addressed:
Registries updated:
Tests added:
Invariants preserved:
- no_llm_in_app:
- candidate_only:
- app_owns_state:
- semantic_bus_local_only:
- default_model_strategy_3b_7b_8b:
```

## Review Checklist

Codex must treat PR-22 as a governance and documentation hardening task. It is successful only when the repository can prove that the senior review findings are not loose prose but connected to validation and bundle coverage.

Checklist:

```text
Senior review simulation is present.
Senior remediation plan is present.
Traceability matrix includes PR-22 and REAL-PR-08.
Anti-drift policy names forbidden shortcuts.
Semantic Bus red lines name forbidden authority expansion.
Risk register includes critical implementation risks.
Public release checklist keeps runtime claims bounded.
validate-senior-review passes.
validate-all passes.
pytest passes.
```

## Expected Review Evidence

The real PR implementing this internal task should show the diff for docs, registries and tests, then include a short statement that no runtime behavior was implemented and no architecture law was weakened.
