# FINAL-PR-09 Small Model Power Map

claim_boundary: final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply

## 3B Model Roles

| Role ID | Purpose | Authority Limit |
|---------|---------|----------------|
| 3b_scout | Fast context scan and relevance detection | candidate_hint_only |
| 3b_extractor | Extract structured fields from input | candidate_hint_only |
| 3b_classifier | Classify work type and route category | candidate_hint_only |
| 3b_router | Select route from precomputed options | candidate_hint_only |
| 3b_slot_filler | Fill slots in prepared slot contracts | candidate_hint_only |
| 3b_quick_critic | Fast boundary and quality check | candidate_hint_only |
| 3b_style_check | Check output style consistency | candidate_hint_only |
| 3b_refusal_boundary_check | Verify refusal boundaries are respected | candidate_hint_only |

## 7B/8B Model Roles

| Role ID | Purpose | Authority Limit |
|---------|---------|----------------|
| 7b_writer | Generate candidate text content | candidate_only |
| 7b_synthesizer | Synthesize multi-source candidate | candidate_only |
| 7b_planner | Plan candidate work structure | candidate_only |
| 7b_repo_reasoner | Reason about repo structure for candidates | candidate_only |
| 7b_candidate_composer | Compose final candidate artifact | candidate_only |
| 7b_refiner | Refine and improve candidate quality | candidate_only |
| 7b_complex_critic | Deep candidate quality evaluation | candidate_only |

## 3B+7B/8B Hybrid Routes

| Route ID | Pattern | Use Case |
|----------|---------|---------|
| hybrid_3b_scout_7b_synthesize_3b_check | 3B scout → 7B synthesize → 3B check | Standard high-quality candidate |
| hybrid_3b_extract_7b_compose_3b_boundary_critic | 3B extract → 7B compose → 3B boundary critic | Structured composition with safety |
| hybrid_7b_draft_3b_slot_check_7b_refine | 7B draft → 3B slot check → 7B refine | Quality-first with fast validation |
| hybrid_no_model_precompute_3b_route_7b_candidate_final_gate | No-model precompute → 3B route → 7B candidate → Final Gate | Full operational spine path |

## No-Model / Deterministic Roles

| Role ID | Purpose |
|---------|---------|
| schema_validation | Validate JSON/structure without model |
| manifest_binding_validation | Validate file manifest bindings |
| cache_fingerprint_lookup | Lookup semantic cache by fingerprint |
| slot_preparation | Prepare slot contracts deterministically |
| rule_based_refusal | Apply rule-based refusal without model |
| deterministic_candidate_shape | Build candidate structure deterministically |
| trace_receipt_construction | Build trace and receipt IDs deterministically |

## Route Selection Logic

1. If mode="deterministic": select deterministic_no_model route
2. If resource_profile="small" (3B available): select 3b_primary route
3. If resource_profile="medium" (7B/8B available): select 7b_primary route
4. If resource_profile="hybrid": select 3b_7b_hybrid route
5. Default: deterministic_no_model

All routes are plans, not execution. Roles are capability descriptions, not model calls.

## Non-Claims

- No live model inference
- No real model benchmark
- No provider execution
- Hybrid route is a plan, not empirical proof
- 3B/7B quality claims are not tested in this PR
