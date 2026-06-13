# FINAL-PR-08 — Projection Candidate Spine

claim_boundary: projection_candidate_spine_prepares_candidates_not_runtime_execution
candidate_only: true

## What PR08 Implemented

Module: `odin/projection_candidate_spine/` — 8 files:

- `materialization.py` — MaterializationLevel enum M0_raw_input through M9_release_evidence
- `candidate_graph.py` — CandidateGraph, CandidateNode, CandidateEdge with explicit from/to/relation edges
- `projection_set.py` — ProjectionSet dataclass (candidate_only=True, app_owned_apply=True)
- `expression_packet.py` — ExpressionPacket (near_code_execution=False, text-only near-code)
- `compare.py` — CandidateComparison, compare_projection_candidates() recommendation only
- `receipt_link.py` — ReceiptLink traceability (bound_at_utc, no QIRC emit)
- `proof.py` — build_proof_packet(), persist_proof_packet(repo_root)
- `__init__.py` — public exports

## Materialization Levels

M0_raw_input → M1_normalized → M2_seed_route → M3_field_selection → M4_expression →
M5_projection_set → M6_candidate_artifact → M7_comparison → M8_receipt_link → M9_release_evidence

## PR07 FieldSelection Integration

`build_projection_set_from_field_selection(field_selection)` → ProjectionSet
Consumes PR07 `FieldSelection` (dominant_field, coherence_score, why_trace) without modification.

## PR06→PR07→PR08 Public Chain Test

`test_pr06_pr07_pr08_chain_works` — verifies select_seed_route() → select_field_route() →
build_projection_set_from_field_selection() end-to-end.

## Local Hub Endpoint

`GET /demo/projection-candidate.json` — returns status/candidate_only/claim_boundary/payload

## CLI Commands

- `validate-projection-candidate-spine` — returns 0 on success, list[str] errors on failure
- `explain-projection-candidate --demo` — returns valid JSON projection candidate explanation
- `prove-projection-candidate-spine` — returns proof packet with proven/not_proven/claim_boundary

## What PR08 Did NOT Implement

- Runtime execution or model inference
- App state apply or external send
- PR09 Release Closure (deferred)
- Any QIRC emission or live-clock outputs

## Not-Proven List

- production_readiness
- live_model_inference
- app_state_mutation
- external_send_authority
- hidden_runtime
- generated_code_correctness_unless_tested
- release_closure (deferred to PR09)
