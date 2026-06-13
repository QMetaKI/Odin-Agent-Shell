# Claude Code Prompt — FINAL-PR-09++ — Functional Small-Model Operational Spine

Candidate-only: true  
Claim boundary: `final_pr_09_plusplus_prepares_and_implements_candidate_operational_spine_not_release_certification`  
Base assumption: PREP FINAL-PR-09++/10++ has landed. FINAL-PR-09++ runs before FINAL-PR-10++ and before FINAL-PR-11.

## Mission

Implement a functional operational spine that connects existing Odin components instead of creating a parallel fake runtime. This PR turns the audited Local Hub, CLI, provider readiness, execution gate, Universal Work, operational seed, field selection, projection candidate, QIRC, packets, proof chain, and final gate surfaces into a coherent local-first, candidate-only Universal Work Kernel path optimized for deterministic/no-model, 3B, 7B/8B, and 3B+7B/8B hybrid work.

## Required intake before editing

Read: README.md, START_HERE.md, CANON_ENTRY.md, AGENTS.md, SYSTEM_MAP.json, FILE_MANIFEST.json, docs/MASTER_ARCHITECTURE_V7_1.md, docs/MASTER_ARCHITECTURE_V7_1_1.md, docs/MASTER_SPECS_V7_1.md, docs/V7_1_1_OPERATIONAL_TARGET_SYNTHESIS.md, docs/V7_1_1_ROAD_TO_100_BUILD_LADDER.md, registries/v7_1_1_operational_target_registry.json, registries/v7_1_1_slice_absorption_map.json, every pre-release super audit document under docs/codex/audits/pre_release_super_audit/, the related reports/pre_release_super_audit_*.json files, and the existing modules named in the prep work packet.

## Non-negotiable boundaries

- candidate-only is mandatory.
- app-owned apply is mandatory; Odin must not apply changes.
- no app state mutation by Odin.
- no external send by Odin.
- local_first default remains mandatory.
- no hidden authority for model/provider/agent/tool/QIRC.
- model projection is not truth.
- receipt before claim.
- final gate required.
- no public QIRC by default.
- no live model inference claim unless this PR creates explicit local host receipts through an intentionally enabled local-only seam.
- local provider seam disabled by default.
- no model-quality benchmark claim.
- no security certification claim.
- no production-release claim.

## Functional path to implement

Raw input → Handoff Context → Universal Work Object → validation/binding → Context Capsule → Artifact Lens → Slot Contract → Gaptext → precompute/no-model analysis → ModelWorkPacket → small-model route plan → 3B / 7B / hybrid role assignment → operational seed route → field selection → projection candidate → deterministic/mock/local-provider-seam packet → Candidate Artifact → Final Gate → Response Packet → Trace/Receipt/Proof → Hub/CLI/API visibility.

## Build or strengthen these modules

- `odin/operational_spine/orchestrator.py`: owns the path above and calls existing subsystems where available.
- `odin/operational_spine/status.py`: exposes readiness, gaps, disabled provider seam status, and not_proven.
- `odin/operational_spine/model_roles.py`: declares no-model, 3B, 7B/8B, and hybrid role policies.
- `odin/operational_spine/modelworkpacket_builder.py`: builds and validates ModelWorkPacket envelopes.
- `odin/operational_spine/small_model_route_plan.py`: deterministic route planning, no benchmark claims.
- `odin/operational_spine/qshabang_runtime_map.py`: neutral Q-Shabang operational map.
- `odin/operational_spine/receipts.py`: trace/receipt/proof packet builders.
- `odin/operational_spine/reports.py`: writes reports listed below.

Do not duplicate the existing runtime engine, local hub, provider probe, execution gate, model router, precompute scorer, operational seed spine, field selection spine, projection candidate spine, QIRC, packets, final gate, proof chain, worklets, work atoms, seeds, patterns, or flow packs. Integrate them through narrow adapters.

## CLI commands to add

- `python -m odin.cli odin-status`
- `python -m odin.cli odin-doctor`
- `python -m odin.cli run-operational-spine --demo`
- `python -m odin.cli run-operational-spine --input "..."`
- `python -m odin.cli explain-operational-spine`
- `python -m odin.cli explain-small-model-route`
- `python -m odin.cli explain-qshabang-map`
- `python -m odin.cli validate-operational-spine`
- `python -m odin.cli validate-small-model-route-plan`
- `python -m odin.cli validate-modelworkpacket-enforcement`
- `python -m odin.cli validate-qshabang-operational-map`
- `python -m odin.cli validate-deferred-system-lift`

## Local Hub endpoints to add

- `GET /operational-spine/status.json`
- `GET /operational-spine/demo.json`
- `POST /operational-spine/run`
- `GET /operational-spine/evidence-index.json`
- `GET /operational-spine/provider-readiness.json`
- `GET /operational-spine/small-model-route.json`
- `GET /operational-spine/qshabang-map.json`
- `GET /operational-spine/modelworkpacket.example.json`

## Small-model roles

### 3B roles

scout, extractor, classifier, router, slot_filler, quick_critic, style_check, refusal_boundary_check.

### 7B/8B roles

writer, synthesizer, planner, repo_reasoner, candidate_composer, refiner, complex_critic.

### 3B+7B/8B hybrid roles

- 3B scout → 7B synthesize → 3B check.
- 3B extract → 7B compose → 3B boundary critic.
- 7B draft → 3B slot compliance check → 7B final refinement.
- no-model precompute → 3B route → 7B candidate → final gate.

### No-model roles

schema validation, manifest/binding validation, cache/fingerprint lookup, slot preparation, rule-based refusal, deterministic candidate shape, trace/receipt construction.

## ModelWorkPacket required fields

packet_id, work_id, caller_id, candidate_only, local_only, claim_boundary, input_refs, context_capsule, artifact_lens, transformation_verb, slot_contract, gaptext, model_role, route_policy, provider_policy, output_contract, forbidden_actions, privacy_boundary, cost_budget, latency_budget, critic_plan, final_gate_requirements, receipt_plan, not_proven.

Validation must reject missing fields, false candidate_only, false local_only default, missing forbidden_actions, missing final_gate_requirements, and any implied app apply or external send.

## Provider seam rules

Default remains deterministic/mock/no-model. Local provider execution remains disabled by default. If this PR adds a future execution seam, require explicit CLI/config/env permission, explicit provider_id, only local candidate providers (`ollama_candidate`, `llama_cpp_candidate`), no API key read, no remote call, no external network, timeout, max input length, output projection only, Candidate Artifact only after gates, `app_apply: false`, `external_send: false`, no model_quality claim, and host receipt. If unavailable, return a structured unavailable packet. Never fake live model inference.

## Q-Shabang operational map

Translate only into neutral Odin mechanics:

- KI ohne KI → deterministic precompute / no-model routes.
- Q gates → claim/evidence/reality gates.
- Mirror critics → Critic Cascade.
- Resonance/Fit → coherence and fit scoring.
- Seeds / Pattern Mines → seed continuity and flow packs.
- Narrative compiler → work-flow pack / shadow runtime preparation.
- QIRC → local semantic coordination and receipt bus.
- App sovereignty → app-owned apply/state/external-send.
- Candidate reality → Candidate Artifact / Response Packet.
- QoOO-style orchestration → route director / system profile compiler.
- Bug6/Q7 → authority drift and boundary scanners.

## Deferred system lift classification

Classify each as `minimal_runtime_hook_in_pr09`, `schema_and_packet_only_in_pr09`, `future_pr_required`, `external_receipt_required`, or `already_repo_real`: Context Distillery, Artifact Lenses, Slot Forge, Gaptext Compiler, Semantic Cache, Work Memory, Minicheck, Critic Cascade, Candidate Tournament, Style Stabilizer, Anti-Generic Engine, Taste Dials, Model Dojo, Scoreboard, SDK/App Bridge receipts.

## Reports to create

- reports/final_pr_09_operational_spine_report.json
- reports/final_pr_09_cli_surface_report.json
- reports/final_pr_09_hub_surface_report.json
- reports/final_pr_09_provider_readiness_report.json
- reports/final_pr_09_modelworkpacket_enforcement_report.json
- reports/final_pr_09_small_model_route_plan_report.json
- reports/final_pr_09_qshabang_operational_map_report.json
- reports/final_pr_09_deferred_system_lift_report.json

## Docs to create

- docs/release/FINAL_PR_09_OPERATIONAL_SPINE_EVIDENCE_INDEX.md
- docs/release/FINAL_PR_09_SMALL_MODEL_POWER_MAP.md
- docs/release/FINAL_PR_09_QSHABANG_OPERATIONAL_MAP.md
- docs/release/FINAL_PR_09_DEFERRED_SYSTEM_LIFT_PLAN.md

## Tests to create

- tests/test_final_pr_09_operational_spine.py
- tests/test_final_pr_09_cli_hub_convergence.py
- tests/test_final_pr_09_modelworkpacket_enforcement.py
- tests/test_final_pr_09_provider_seam.py
- tests/test_final_pr_09_small_model_route_plan.py
- tests/test_final_pr_09_qshabang_operational_map.py
- tests/test_final_pr_09_deferred_system_lift.py

## Acceptance gates

Run and record receipts for: `python -m odin.cli validate-operational-spine`, `python -m odin.cli run-operational-spine --demo`, `python -m odin.cli odin-status`, `python -m odin.cli odin-doctor`, `python -m odin.cli validate-small-model-route-plan`, `python -m odin.cli validate-modelworkpacket-enforcement`, `python -m odin.cli validate-qshabang-operational-map`, `python -m odin.cli validate-deferred-system-lift`, `python -m odin.cli validate-all`, and `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider --tb=no`.

## Output summary requirements

Explain what became operational, what remains scaffold, what is candidate-only, why the local provider seam is disabled by default, how 3B / 7B / hybrid routes are prepared, how Q-Shabang terms were neutralized, and what is not proven. State that release closure remains FINAL-PR-11.
