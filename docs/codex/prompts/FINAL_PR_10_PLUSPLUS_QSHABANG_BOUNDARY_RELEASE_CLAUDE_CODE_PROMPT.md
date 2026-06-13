# Claude Code Prompt — FINAL-PR-10++ — Boundary-Gated Q-Shabang Release Operationalization

Candidate-only: true  
Claim boundary: `final_pr_10_plusplus_release_gates_record_boundaries_not_release_certification`  
Dependency: FINAL-PR-09++ merged and validated. Release closure remains FINAL-PR-11.

## Mission

Turn all boundaries, Q-Shabang operationalization, model role authority constraints, artifact currency classes, and release evidence into validator-backed release gates. This PR does not certify production, security, model quality, host deployment, live local model inference, or external runtime behavior. It makes release claims explicit and blocks claims without receipts.

## Required intake

Read the PREP work packet, FINAL-PR-09++ outputs, all pre-release super audit docs and reports, docs/MASTER_ARCHITECTURE_V7_1_1.md, docs/V7_1_1_OPERATIONAL_TARGET_SYNTHESIS.md, docs/V7_1_1_ROAD_TO_100_BUILD_LADDER.md, SYSTEM_MAP.json, FILE_MANIFEST.json, and the FINAL-PR-09++ operational spine docs/reports.

## Non-negotiable boundaries

candidate-only, app-owned apply, no app state mutation, no external send, local-only default, remote explicit only, no hidden authority, qirc not app authority, model projection not truth, provider not authority, receipt before claim, final gate required, no public QIRC by default, no model benchmark without receipt, no security certification without receipt, no production-release claim without receipt, local provider seam disabled by default, historical artifact not current claim, Q-Shabang neutral terms only, small-model route not quality benchmark, model role not authority.

## Build or strengthen these files

- docs/release/FINAL_PR_10_BOUNDARY_MATRIX.md
- docs/release/FINAL_PR_10_RING_AUTHORITY_MAP.md
- docs/release/FINAL_PR_10_BUG6_Q7_OPERATIONAL_MAP.md
- docs/release/FINAL_PR_10_QSHABANG_RELEASE_GATE_MAP.md
- docs/release/FINAL_PR_10_MODEL_ROLE_AUTHORITY_MATRIX.md
- docs/release/FINAL_PR_10_RELEASE_EVIDENCE_CLOSURE_INDEX.md
- registries/final_pr_10_boundary_matrix_registry.json
- registries/final_pr_10_artifact_currency_registry.json
- registries/final_pr_10_model_role_authority_registry.json
- registries/final_pr_10_qshabang_release_gate_registry.json
- reports/final_pr_10_boundary_matrix_report.json
- reports/final_pr_10_ring_authority_map.json
- reports/final_pr_10_bug6_q7_operational_map.json
- reports/final_pr_10_qshabang_release_gate_report.json
- reports/final_pr_10_model_role_authority_report.json
- reports/final_pr_10_release_evidence_closure_index.json
- reports/final_pr_10_artifact_currency_report.json
- reports/final_pr_10_release_preflight_report.json

## Boundary matrix rows

candidate_only, app_owned_apply, no_app_state_mutation, no_external_send, local_only_default, remote_explicit_only, no_hidden_authority, qirc_not_app_authority, model_projection_not_truth, provider_not_authority, receipt_before_claim, final_gate_required, no_public_qirc_by_default, no_model_benchmark_without_receipt, no_security_certification_without_receipt, no_production_ready_claim_without_receipt, local_provider_execution_disabled_by_default, historical_artifact_not_current_claim, qshabang_neutral_terms_only, small_model_route_not_quality_benchmark, model_role_not_authority.

## Ring / authority layers

- Ring 0: Host App / User Apply Authority.
- Ring 1: Odin Candidate Kernel.
- Ring 2: Universal Work / ModelWorkPacket Layer.
- Ring 3: QIRC / Semantic Bus Coordination.
- Ring 4: Provider / Worker Projection.
- Ring 5: Critic / Final Gate / Candidate Selection.
- Ring 6: Proof / Trace / Receipt.
- Ring 7: Release / Claim Governance.
- Ring X: External / Remote / Host-specific Proof Required.

## Model role authority matrix

For each role define allowed_inputs, allowed_outputs, forbidden_actions, authority_limit, candidate_only requirement, final_gate requirement, receipt requirement, and claim boundary: 3B scout, 3B extractor, 3B router, 3B slot_filler, 3B quick_critic, 7B writer, 7B synthesizer, 7B planner, 7B candidate_composer, 7B complex_critic, hybrid_scout_write_check, deterministic_no_model_worker, mock_provider, local_provider_candidate.

## Q-Shabang release gates

For each neutralized component define runtime evidence, validator evidence, release claim allowed, release claim forbidden, and future proof required: deterministic precompute, claim/evidence/reality gates, critic cascade, coherence/fit scoring, seed continuity, flow packs, QIRC coordination, app-owned apply, candidate artifact, response packet, route director, authority drift scanners.

## Artifact currency classes

current_runtime, current_release_evidence, current_supporting, historical_supporting, superseded, target_only, external_receipt_required.

## CLI validators and explainers to add

validate-boundary-matrix, validate-ring-authority-map, validate-bug6-q7-operational-map, validate-qshabang-release-gate-map, validate-model-role-authority, validate-release-evidence-closure, validate-artifact-currency, validate-final-release-preflight, release-preflight, explain-boundaries, explain-release-claims, explain-model-role-authority, explain-qshabang-release-gates.

## Local Hub endpoints

- `GET /release/boundary-matrix.json`
- `GET /release/ring-authority-map.json`
- `GET /release/model-role-authority.json`
- `GET /release/qshabang-gates.json`
- `GET /release/evidence-closure.json`
- `GET /release/preflight.json`
- `GET /release/artifact-currency.json`

## Tests to create

- tests/test_final_pr_10_boundary_matrix.py
- tests/test_final_pr_10_ring_authority_map.py
- tests/test_final_pr_10_bug6_q7_operational_map.py
- tests/test_final_pr_10_qshabang_release_gate.py
- tests/test_final_pr_10_model_role_authority.py
- tests/test_final_pr_10_release_evidence_closure.py
- tests/test_final_pr_10_artifact_currency.py
- tests/test_final_pr_10_release_preflight.py

## Acceptance gates

Run and record receipts for: `python -m odin.cli validate-boundary-matrix`, `python -m odin.cli validate-ring-authority-map`, `python -m odin.cli validate-bug6-q7-operational-map`, `python -m odin.cli validate-qshabang-release-gate-map`, `python -m odin.cli validate-model-role-authority`, `python -m odin.cli validate-release-evidence-closure`, `python -m odin.cli validate-artifact-currency`, `python -m odin.cli validate-final-release-preflight`, `python -m odin.cli release-preflight`, `python -m odin.cli validate-all`, and `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider --tb=no`.

## Output summary requirements

Explain how the boundary matrix, ring authority map, Bug6/Q7 map, Q-Shabang release gates, model role authority, artifact currency, and release preflight work. State what remains not proven and that FINAL-PR-11 is the release closure step.
