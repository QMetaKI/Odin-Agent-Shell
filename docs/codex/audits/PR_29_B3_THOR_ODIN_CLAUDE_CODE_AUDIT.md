# PR-29 B3 Thor / Odin / Claude Code Audit

claim_boundary: b3_audit_is_static_review_not_runtime_proof

## 1. Thor-Agent-Kit Usage

- Thor-Agent-Kit cloned at: /tmp/odin_pr29_b3_external_refs/Thor-Agent-Kit
- Commit SHA: e9af7a333e4bcb11f2461696e4ebbcde994b98b1
- Install status: thor-agent-kit 4.1.1 installed successfully via pip install -e .
- Thor doctor: failed (must run from Thor-Agent-Kit root; Odin-Agent-Shell lacks Thor schemas/profiles)
- Thor validate: not run (doctor failed)
- Thor handoff-summary: run — exit_code=0, candidate-only output with task hash
- Thor pr-section: run — exit_code=0, candidate-only PR section output

## 2. Thor Repo Cognition Usage

Thor `repo` subcommands not available in thor-agent-kit 4.1.1.

Manual five-phase repo cognition applied:
1. Full directory scan of Odin-Agent-Shell
2. Reading all previous PR artifacts (B1, B2, foundation PRs)
3. Mapping B3-relevant prior artifacts (B2 Slot Forge route classes, Context Distillery, Worklet Graph)
4. Identifying target artifacts for B3 (ModelWorkPacket, Scale Ladder, Provider Seam, Small-Model Power, Hybrid Director)
5. Building risk map and review checklist

## 3. Thor/Y Composition Usage

Thor `y` subcommands not available in thor-agent-kit 4.1.1.

Y composition patterns applied manually:
- Candidate-only discipline: all B3 outputs carry candidate_only: true
- Authority split: app owns apply, Claude Code worker is external local worker only
- Slot-based dispatch: B3 Scale Ladder routes to slot-typed model classes
- Gaptext discipline: ModelWorkPacket references gaptext_ref for slot instructions
- B2 Slot Forge route_classes bound into B3 Scale Ladder (deterministic_no_model, small_model_candidate, hybrid_candidate, remote_explicit_only, cannot_safely_complete extended to full 10-class ladder)

## 4. Thor Protocol Shape Usage

Protocol mapping created in PR_29_B3_THOR_PROTOCOL_SHAPE_MAPPING.md:
- THOR_HANDOFF → B3 work packet / binding refs (kernel_binding shape)
- THOR_RETURN → PR return report requirements (files_changed, commands_run, evidence_refs)
- THOR_REVIEW → Senior Reviewer and Senior Code Reviewer simulations
- THOR_RECEIPT → final audit and non-claim receipt model

## 5. Odin Work-Kernel Usage

Applied transformation_verb: compile_static_model_routing_contracts
Output contract: candidate_only_static_contracts
candidate_only: true, app_owned_apply: true

B3 adds the model routing and dispatch contract layer between B2 semantic work outputs and future B4 critic/final-gate runtime. ModelWorkPacket assembles slot, capsule, gaptext into routable unit. Scale Ladder routes to smallest sufficient class. Provider Seam is transport contract only.

## 6. Claude-as-Worker Adapter Usage

B2 audit identified missing formal Claude-as-worker adapter contract.
B3 adds: schemas/v7_1_1_odin_claude_worker_adapter.schema.json
B3 adds: registries/v7_1_1_odin_claude_worker_adapter_registry.json
B3 adds: examples/v7_1_1/odin_claude_worker_adapter.example.json

Contract invariants:
- Claude Code may act as external local worker following Odin contracts
- Does not prove a local LLM runtime
- Does not grant app apply/state/external-send authority
- Returned work remains candidate until reviewed

## 7. Thor Handoff Intake Schema Usage

B2 audit identified missing native Thor bridge.
B3 adds static intake schema only (not runtime bridge):
- schemas/v7_1_1_thor_handoff_intake.schema.json
- registries/v7_1_1_thor_handoff_intake_registry.json
- examples/v7_1_1/thor_handoff_intake.example.json

## 8. ModelWorkPacket Design Impact

ModelWorkPacket is the central assembly unit connecting B2 semantic outputs to B3 routing:
- Carries slot_contract_ref (from B2 Slot Forge)
- Carries context_capsule_ref (from B2 Context Distillery)
- Carries gaptext_ref (from B2 Gaptext)
- Routes via model_route_ref to Scale Ladder class
- Points to provider_policy_ref for eventual execution
- Remains candidate_only until B4+ critic layer accepts

B4 must consume ModelWorkPacket outputs in Candidate/Critic/Final Gate layer.

## 9. Scale Ladder Design Impact

10-class ladder expands B2 Slot Forge route classes to full model routing spectrum:
- deterministic_no_model through heavy_local_candidate: local-first priority
- remote_explicit_only: gated behind explicit policy and receipt
- cannot_safely_complete: safe fallback

B5+ must add runtime execution layer consuming Scale Ladder routing decisions.

## 10. Provider Seam Boundary Impact

Provider seams are transport contracts only in B3. No execution, no API keys, no network.
Classes: mock_provider (test), local_ollama_candidate, local_llama_cpp_candidate, openai_compatible_remote_explicit, external_agent_worker, cannot_safely_complete.

B5 should add the first actual provider seam runtime integration (local Ollama candidate preferred).

## 11. Small-Model / Hybrid Director Impact

12-module Small-Model Power pipeline formalizes the candidate composition architecture.
9-role Hybrid Director formalizes routing decision logic.

Key architectural insight: small-model power does not require a large frontier model. The entire B3 pipeline (distill → worklet → slot → gaptext → packet → route → compose) can operate with deterministic logic or tiny local models for the majority of work.

## 12. What Was Not Used

- thor y analyze/compose/handoff/handoff-spine CLI: not available in thor-agent-kit 4.1.1
- thor repo cognition/intent/handoff-compile CLI: not available in thor-agent-kit 4.1.1
- thor pack --agent claude-code: requires initialized .thor/ session; not appropriate to commit generated artifacts
- YNode-prep: not a dependency per B3 spec section 0; Thor/Y surface used instead

## 13. Findings for B4/B5/B7+

**B4 findings:**
- B4 must consume ModelWorkPacket outputs in Candidate/Critic/Final Gate layer
- B4 critic should reference scale_ladder route_class to select appropriate critic tier
- B4 final gate advisor maps to Hybrid Director final_gate_advisor role (advisory only, not gate authority)

**B5 findings:**
- B5 should add first runtime provider seam integration (local Ollama preferred)
- B5 should add Storage/Trace/Receipt layer consuming ModelWorkPacket packet_id for audit trail
- B5 Thor-Odin bridge feasibility: Thor-Agent-Kit handoff packs can be generated targeting Odin B5+ work packets

**B7+ findings:**
- Evaluate actual Thor-Odin runtime bridge: Thor pack generation → Odin work packet intake
- Evaluate actual small-model execution: local_7b_8b_candidate via llama.cpp or Ollama for real workload routing
- Evaluate Hybrid Director runtime implementation consuming Scale Ladder decisions

## 14. Claim Boundary

b3_audit_is_static_review_not_runtime_proof
