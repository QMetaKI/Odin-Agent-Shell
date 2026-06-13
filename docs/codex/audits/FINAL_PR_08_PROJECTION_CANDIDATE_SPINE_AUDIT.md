# FINAL-PR-08 Projection Candidate Spine Audit

claim_boundary: projection_candidate_spine_prepares_candidates_not_runtime_execution
candidate_only: true

## What Was Implemented

| File | Key Functions |
|---|---|
| `materialization.py` | `MaterializationLevel` enum (M0–M9), `CandidateNode`, `build_candidate_node()` |
| `candidate_graph.py` | `CandidateGraph`, `build_candidate_graph()` — derived_from edges only |
| `projection_set.py` | `ProjectionSet` (candidate_only=True), `build_projection_set_from_field_selection()` |
| `expression_packet.py` | `ExpressionPacket` (near_code_execution=False), `build_expression_packet()` |
| `compare.py` | `CandidateComparison`, `compare_candidates()` — recommendation only |
| `receipt_link.py` | `ReceiptLink` (bound_at_utc, no QIRC emit), `build_receipt_link()` |
| `proof.py` | `build_proof_packet()`, `persist_proof_packet(repo_root)` |
| `__init__.py` | Public exports for all above |

## What Was NOT Implemented

- Runtime execution or model inference
- App apply or external send
- PR09 Release Closure (deferred)
- QIRC emit or runtime proof authority

## How PR08 Consumes PR07

`build_projection_set_from_field_selection(field_selection) -> ProjectionSet`
reads `dominant_field`, `coherence_score`, `why_trace` from PR07 FieldSelection without modifying PR07 modules.

## How PR08 Preserves PR06 Upstream

SeedRoute (selected_seed_id, selected_role_profile_id) is available via the full chain:
PR06 select_seed_route() → PR07 select_field_route() → PR08 build_projection_set_from_field_selection().
Chain test: `test_pr06_pr07_pr08_chain_works`.

## How PR08 Uses Y Materialization Ladder

ProjectionSet=M5_projection_set, CandidateArtifact=M6_candidate_artifact.
Validator checks all 10 levels M0–M9 are present and correctly ordered.

## Why ProjectionSets Are Candidate Organization Only

`ProjectionSet` has `candidate_only=True` hardcoded as dataclass default.
It organizes CandidateNodes on the ladder — it does not execute them, emit QIRC, or apply state.

## Why ExpressionPackets Are Near-Code Text Only

`near_code_execution=False` is carried in every ExpressionPacket and its proof dict.
No eval(), exec(), or subprocess calls exist anywhere in the module.

## Why CandidateGraphs Are Not Execution Graphs

Graph edges describe `derived_from` relations between materialization levels.
No execution semantics: candidate_only=True, no run/execute/invoke methods.

## Why ReceiptLinks Are Traceability Only

`link_id` is deterministic (sha256-based). `bound_at_utc` defaults to a hardcoded value
(not datetime.now()). No QIRC emit. No runtime proof authority claimed.

## Why Release Remains PR09

PR08 implements only M0–M9 candidate organization and ProjectionSet construction.
Release Closure (M9_release_evidence → actual release) requires PR09 authority, which is deferred.

## Not-Proven List

- production_readiness
- live_model_inference
- app_state_mutation
- external_send_authority
- generated_code_correctness_unless_tested
- hidden_runtime
