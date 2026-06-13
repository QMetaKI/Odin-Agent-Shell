# FINAL-PR-09 Thor-Style Operational Spine Handoff

claim_boundary: final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply

## Repo Evidence Compilation

**PR49 prep artifacts confirmed:** FINAL_PR_09_PLUSPLUS_SMALL_MODEL_OPERATIONAL_SPINE_CLAUDE_CODE_PROMPT.md exists. Prep registry and acceptance matrix exist. Prep validator passes.

**PR48 audit findings used:** Pre-release super audit identified deferred systems (Critic Cascade, Model Dojo, Context Distillery) and confirmed provider seam must be disabled by default. Audit confirmed PR08 Projection Candidate as the implementation ceiling before PR09.

**PR08 ProjectionCandidate public interface:** `build_projection_set_from_field_selection(field_selection) -> ProjectionSet`, `build_candidate_graph(nodes) -> CandidateGraph`. Materialization ladder M0-M9 established. Receipt links established.

**PR07 FieldSelection upstream evidence:** `select_field_route_from_seed_route(seed_route) -> FieldSelection`. Coherence scoring, review axes, why-trace. Candidate-only, field scores not truth.

**PR06 SeedRoute upstream evidence:** `select_seed_route(work_context) -> SeedRoute`. Deterministic 4-priority selection (trigger_shape → family/surface → work_type → fallback). Work capsule compilation.

**Runtime engine shape:** odin/runtime/engine.py runs universal work files. Candidate-only throughout.

**Provider/execution gate boundaries:** odin/providers/probe.py (readiness only), odin/execution_gate/gateway.py (mock execution only, remote disabled by default).

## Small-Model Role Target

3B roles handle: scouting, extraction, classification, routing, slot-filling, quick-critic, style-check, refusal-boundary-check. Fast, bounded, no complex synthesis.

7B/8B roles handle: writing, synthesis, planning, repo reasoning, candidate composition, refinement, complex criticism. Require more compute but produce higher-quality candidates.

Hybrid roles: 3B scout → 7B synthesize → 3B check. Combines speed and quality within bounded candidate workflow.

No-model roles: schema validation, manifest binding, cache lookup, slot preparation, rule-based refusal, deterministic candidate shape, trace/receipt construction.

## Q-Shabang Neutral Map Target

Q-Shabang concepts mapped to neutral Odin runtime mechanics:
- KI ohne KI → deterministic_precompute (odin/precompute/)
- Q gates → claim_evidence_reality_gates (odin/core/final_gate.py)
- Mirror critics → critic_cascade (roles defined, engine deferred)
- Resonance/Fit → coherence_and_fit_scoring (odin/field_selection_spine/coherence.py)
- QIRC → local_semantic_coordination (odin/qirc_core/)
- App sovereignty → app_owned_apply (odin/execution_gate/policy.py)

## Deferred System Lift Target

Context Distillery, Semantic Cache, Work Memory, Minicheck, Candidate Tournament, Style Stabilizer, Anti-Generic Engine, Taste Dials, Model Dojo, Scoreboard → all future_pr_required.
Critic Cascade → minimal_runtime_hook_in_pr09 (roles defined).
SDK/App Bridge receipts → already_repo_real.

## Scope

**In scope:**
- odin/operational_spine/ module (11 files)
- ModelWorkPacket builder + validator
- Small-model route plan (3B, 7B/8B, hybrid, no-model)
- Q-Shabang operational map (neutral terms)
- Deferred system lift classification
- Provider seam (disabled by default)
- CLI: odin-status, odin-doctor, run-operational-spine, explain-*, validate-*
- Local Hub: /operational-spine/* endpoints + UI section
- Registry, schema, examples, reports, proof packet
- Validator: tools/rebaseline/check_final_pr_09_operational_spine.py
- Tests: tests/test_final_pr_09_operational_spine.py
- Docs: handoffs, audits, reports

**Not in scope:**
- FINAL-PR-10++ Boundary-Gated Release Operationalization
- FINAL-PR-11 Release Closure
- Live model inference
- Real model benchmark
- Provider execution
- App apply / app state mutation
- External send / public network
- Production readiness
- Security certification

## Acceptance Gates

1. validate-operational-spine returns 0
2. run-operational-spine --demo returns valid JSON with candidate_only: true
3. ModelWorkPacket rejects app_apply, external_send, hidden_tool_authority
4. Small-model route plan includes 3B, 7B/8B, hybrid, no-model roles
5. Q-Shabang map includes all 11 neutral components
6. Deferred system lift classifies all 15 systems
7. Provider seam execution_allowed: false by default
8. REQUIRED_IDS contains "operational-spine-section"
9. validate-all includes PR09 validator
10. Full test suite passes

## Proof Boundary

Proven: module exists, demo returns candidate packet, ModelWorkPacket enforces boundaries, small-model roles defined, Q-Shabang map defined, deferred systems classified, provider seam disabled, CLI registered, Hub registered, trace/receipt surfaces present.

Not proven: live_model_inference, real_model_benchmark, provider_execution, app_apply, app_state_mutation, external_send, public_network, production_readiness, security_certification, release_certification.

## PR10++ Release-Boundary Handoff Implications

FINAL-PR-10++ must implement: local provider execution with explicit permission, boundary-gated release operationalization, full Critic Cascade, Context Distillery, Semantic Cache. FINAL-PR-09++ operational spine is the required input substrate.

## FINAL-PR-11 Closure Boundary

FINAL-PR-11 remains deferred. Release closure requires FINAL-PR-10++ boundary release gate and security certification, neither of which is implemented in FINAL-PR-09++.
