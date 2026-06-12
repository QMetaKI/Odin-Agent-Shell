# PR-30 B4 Thor Compact Handoff Prompt

**claim_boundary:** thor_compact_handoff_is_external_candidate_guidance_not_runtime_proof
**thor_artifact_is_external_candidate_handoff_guidance_not_runtime_proof:** true

---

## Thor handoff-summary Output (from Odin root)

Task hash: `sha256:3064a29ffc05d3b199407473d7ecf38ff193f7a2534ce5c32101631a82da3307`
Task label: Odin B4
Agent: claude-code

### Thor Claim Boundary

This Thor handoff summary is candidate-only. It is not correctness proof, not runtime proof, not build proof, not platform proof, not model proof, not networking proof, not security certification, not deployment proof, not production readiness, and not maintainer acceptance.

---

## Compact B4 Handoff Prompt (Manually Distilled)

### Block 1 — Repo Cognition

**Task:** B4 Minicheck / Critics / Tournament / Candidate DNA / Response Packet / Final Gate Advisory for Odin v7.1.1

**Repo:** QMetaKI/Odin-Agent-Shell (branch: claude/pr-30-b4-minicheck-critics-final-gate-dq8dys)

**Base after:** PR #29 / B3 — ModelWorkPacket / Scale Ladder / Hybrid Director

**Key consumed artifacts:**
- `registries/v7_1_1_modelworkpacket_contract.json`
- `registries/v7_1_1_model_scale_ladder_registry.json`
- `schemas/v7_1_1_modelworkpacket.schema.json`
- `schemas/v7_1_1_model_scale_ladder.schema.json`

**Required outputs:**
- Minicheck schema/registry/example
- CriticWorkPacket schema/registry/example
- Critic Cascade schema/registry/example
- Tournament Selection schema/registry/example
- Candidate DNA schema/registry/example
- Candidate Artifact schema/registry/example
- Response Packet schema/registry/example
- Final Gate Advisory schema/registry/example
- Receipt Boundary schema/registry/example
- B4 static validator + report
- B4 tests (62 tests minimum)
- Audit + return report

### Block 2 — Architecture Review

**Core rule:** B4 evaluates candidates. B4 does not apply. B4 does not execute models. B4 does not execute providers. B4 does not mutate app state. B4 does not send externally. B4 does not certify correctness. B4 does not become app authority.

**Final Gate term:** Final Gate Advisory (never: Final Gate Authority, Apply Gate, Acceptance Gate, Execution Gate)

**Critic tiers (static contract roles in B4 only):**
- deterministic_schema_critic
- deterministic_contract_critic
- small_model_advisory_critic
- hybrid_advisory_critic
- human_review_required
- cannot_safely_complete

**Route-to-critic mapping (all 10 B3 route classes must be covered):**
- deterministic_no_model → deterministic_schema_critic / deterministic_contract_critic
- tiny_local_candidate → deterministic_contract_critic / small_model_advisory_critic
- small_model_candidate → small_model_advisory_critic
- small_model_multi_slot_candidate → small_model_advisory_critic
- local_7b_8b_candidate → hybrid_advisory_critic
- hybrid_3b_7b_candidate → hybrid_advisory_critic
- quality_hybrid_candidate → hybrid_advisory_critic
- heavy_local_candidate → human_review_required / hybrid_advisory_critic
- remote_explicit_only → human_review_required
- cannot_safely_complete → cannot_safely_complete

### Block 3 — Senior Code Review

**Mandatory checks:**
1. claim_boundary present in every schema, registry, example
2. candidate_only: true in every output
3. non_claims non-empty in every artifact
4. is_apply_gate: false (const) in final_gate_advisory schema
5. is_absolute_truth: false (const) in receipt_boundary schema
6. No forbidden provider SDK imports in B4 implementation files
7. No absolute local paths in report
8. FILE_MANIFEST free of ignored generated artifacts
9. All 62 tests must pass
10. validate-all must pass

**Forbidden imports:** openai, anthropic, requests, httpx, aiohttp, cohere, google.generativeai

### Block 4 — Return / Receipt

**Return artifacts:**
- `reports/v7_1_1_b4_minicheck_critics_final_gate_report.json` (zero hard_violations)
- `docs/codex/reports/PR_30_B4_MINICHECK_CRITICS_FINAL_GATE_RETURN_REPORT.md`
- `docs/codex/audits/PR_30_B4_THOR_ODIN_CLAUDE_CODE_AUDIT.md`
- `registries/v7_1_1_llm_work_audit_findings_registry.json` (B4 findings added)

**Non-claims:**
- not_runtime_completion
- not_production_readiness
- not_live_model_inference_proof
- not_model_quality_proof
- not_provider_execution_proof
- not_app_apply_authority
- not_final_gate_as_apply_gate
