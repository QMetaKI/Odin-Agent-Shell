# REAL-PR-18 — Pre-LLM Intelligence and Perceived Intelligence Amplification

## Objective
Implement the v0.6.5 Pre-LLM Intelligence Amplification Lock as a real Codex PR bundle. This bundle ensures Odin does maximum safe structure, scoring, QIRC, seed, archetype, admissibility and output composition work before any model call.

## Internal Tasks Covered
- PR-61 — Pre-LLM Intelligence Layer
- PR-62 — Model Work Avoidance and Admissibility Expansion
- PR-63 — Output Intelligence Composer
- PR-64 — Perceived Intelligence Metrics
- PR-65 — Micro-to-Macro Candidate Synthesis

## Primary Files
- docs/PRE_LLM_INTELLIGENCE_LAYER_V7_1.md
- docs/MODEL_WORK_AVOIDANCE_V7_1.md
- docs/OUTPUT_INTELLIGENCE_COMPOSER_V7_1.md
- schemas/v7_1/odin_pre_llm_intelligence_packet.schema.json
- odin/shadow_runtime/pre_llm_intelligence_shadow.py
- registries/pre_llm_intelligence_registry.json
- tests/test_pre_llm_intelligence_amplification.py

## Required Behavior
- No model dispatch before admissibility and avoidance evaluation.
- Candidate-only visible results.
- Output Intelligence Composer produces app-native candidate bundles.
- Perceived intelligence is measured but never used to bypass boundaries.
- Direct apply is blocked.

## Forbidden Scope
- No actual app mutation.
- No external send.
- No model-generated executable code.
- No false verification claims.

## Definition of Done
- `python -m odin.cli validate-all` passes.
- `python -m pytest -q -p no:cacheprovider` passes.
- PR-61 through PR-65 are all represented in registries.
- All new schemas, docs, modules and tests are in FILE_MANIFEST.

## Codex PR Summary Template
Summary: Add Pre-LLM Intelligence and Perceived Intelligence Amplification bundle.
Tests: validate-all and pytest.
Boundary: candidate-only, app-owned apply, truthful perceived intelligence.


## Integration Sequence
1. Lock schemas and registries for pre-LLM packet families.
2. Wire shadow modules for pre-model cognition, avoidance, composition, metrics and micro-to-macro synthesis.
3. Add tests for allowed candidate-only path and blocked direct-apply path.
4. Update Master Architecture and Master Specs addenda.
5. Refresh SYSTEM_MAP and FILE_MANIFEST.
6. Preserve AI-Git safety consolidation and QIRC Gold Spine boundaries.

## Reviewer Risk Table
| Risk | Mitigation |
|---|---|
| Perceived-intelligence deception | Micro Model Illusion Boundary + Why Trace |
| Model called too early | Admissibility and Model Work Avoidance before dispatch |
| Large model overuse | Model Scale Ladder and route score justification |
| App authority drift | App-owned apply boundary and candidate-only output |
| QIRC overreach | local-only internal channels and digest-only app bridge |

## Bundle Acceptance Gate
The bundle is accepted only when all PR-61..PR-65 tasks are represented, validate-all is green, pytest is green, direct apply remains blocked, and model work avoidance has explicit reasons. No public text may claim runtime verification, security audit completion, test execution success, production readiness, deployment validation, or app mutation.
