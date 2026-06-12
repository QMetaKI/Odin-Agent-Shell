# FINAL-PR-05 Thor Effectiveness Audit

**claim_boundary:** `final_pr_05_thor_audit_candidate_only_not_runtime_proof`
**candidate_only:** true
**generated_at:** 2026-06-12T19:00:00Z

## Audit Structure: Observation → Cause → Thor Finding → Proposed Improvement → Priority → Evidence

---

### Finding 1: Execution Gate Policy Contract

**Observation:** Thor compiled a clear execution gate policy contract with all required fields: `execution_gate_enabled`, `mock_execution_allowed`, `local_candidate_execution_allowed`, `remote_execution_allowed`, `api_key_reads_allowed`, `external_network_allowed`, `app_apply_allowed`, `app_state_mutation_allowed`, `external_send_allowed`.

**Cause:** Prior PR-04 provider policy contract was a good template to inherit from.

**Thor Finding:** Policy contract is complete. Default values are all correctly set to blocked for real execution.

**Proposed Improvement:** Future gate opening could use a separate `LocalCandidateGateToken` to make the explicit future gate more traceable.

**Priority:** Low (deferred to FINAL-PR-06).

**Evidence:** `DEFAULT_EXECUTION_GATE_POLICY.as_dict()` returns full policy object with correct defaults.

---

### Finding 2: Mock Execution Contract Clarity

**Observation:** Thor derived a clear distinction between `mock_execution`, `real_provider_execution`, and `model_inference` terminology.

**Cause:** Ambiguous "mock_only" terminology in some prior drafts was replaced with explicit triads.

**Thor Finding:** Terminology is now unambiguous. Every mock response packet carries all three flags explicitly.

**Proposed Improvement:** Add `execution_kind: mock_deterministic` to all response packets for easier filtering in QIRC viewers.

**Priority:** Done — `execution_kind` field added to MockProvider response.

**Evidence:** `MockProvider.execute()` returns `execution_kind: "mock_deterministic"`.

---

### Finding 3: Local Candidate Blocked-By-Default Contract

**Observation:** Thor identified that both `ollama_candidate` and `llama_cpp_candidate` need explicit `requires_explicit_future_gate: true` and `ci_must_not_require_binary: true`.

**Cause:** CI environments may not have Ollama or llama.cpp installed; tests must not fail due to missing binaries.

**Thor Finding:** `LocalCandidatePolicy.ci_must_not_require_binary` flag added. Blocked attempt proof returns policy object with all constraints.

**Proposed Improvement:** Add a `ci_skip_reason` field to blocked attempt response to surface in CI logs.

**Priority:** Medium (nice to have for FINAL-PR-06).

**Evidence:** `LocalCandidatePolicy.as_dict()` includes `ci_must_not_require_binary: true`.

---

### Finding 4: Proof Chain Cross-Reference Gap

**Observation:** Prior PRs had independent proof packets but no unified chain. Thor identified this gap.

**Cause:** Each PR was a standalone deliverable; no aggregation existed.

**Thor Finding:** Proof chain registry maps all 5 FINAL-PRs to their report/proof paths. Builder checks if files exist without overclaiming.

**Proposed Improvement:** Add `proof_chain_version` field for future chain upgrades.

**Priority:** Low.

**Evidence:** `build_proof_chain()` returns 5 entries with `report_exists` flags.

---

### Finding 5: FINAL-PR Ladder Compiler Scaffold Scope

**Observation:** Thor correctly scoped the ladder compiler as a scaffold only, not a full prompt compiler.

**Cause:** Full Thor replacement requires significantly more capability than a 7-section template skeleton.

**Thor Finding:** Scaffold is claimed correctly as `final_pr_ladder_scaffold_not_full_prompt_compiler`. `thor_runtime_replacement` in `not_proven`.

**Proposed Improvement:** Thor vNext could generate full handoff prompts from return reports automatically.

**Priority:** deferred_to_thor_vnext.

**Evidence:** `compile_worker_packet_scaffold()` returns `claim_boundary: "final_pr_ladder_scaffold_not_full_prompt_compiler"`.

---

### Finding 6: Warning Block Generation

**Observation:** Thor generated clear warning blocks for all mandatory copy requirements in the prompt.

**Cause:** Prior PR audits showed that ambiguous boundaries lead to overclaims.

**Thor Finding:** UI warning copy is explicit and covers all 8 FINAL-PR-05 required copy items.

**Proposed Improvement:** None. Copy is sufficient.

**Priority:** Done.

**Evidence:** `REQUIRED_COPY` in `ui.py` includes all FINAL-PR-05 additions.

---

### Finding 7: Thor vNext Handoff Material

**Observation:** This PR accumulates enough proof chain + ladder scaffold material to inform a dedicated Thor vNext handoff.

**Cause:** PR-01 through PR-05 form a complete foundation. The ladder compiler scaffold is the seed for full prompt generation.

**Thor Finding:** Thor vNext should receive: (1) proof chain registry, (2) ladder scaffold 7-section template, (3) PR-01..05 return reports, (4) validator expectations from check_final_pr_05_execution_gate.py.

**Proposed Improvement:** Create `docs/codex/handoffs/THOR_VNEXT_HANDOFF_SEED.md` in FINAL-PR-06.

**Priority:** defer_to_final_pr_06.

**Evidence:** `PROOF_CHAIN_REGISTRY` has 5 entries; `WORKER_PACKET_SECTIONS` has 7 sections.

---

## Summary

| Finding | Priority | Status |
|---------|----------|--------|
| Execution gate policy contract | Critical | Done |
| Mock execution contract clarity | High | Done |
| Local candidate blocked-by-default | High | Done |
| Proof chain cross-reference gap | Medium | Done |
| Ladder compiler scaffold scope | Medium | Done |
| Warning block generation | Medium | Done |
| Thor vNext handoff material | Low | defer_to_final_pr_06 |
