# Thor Prompt Extraction and Handoff Pull

## Status

Artifact: `odin_handoff_prompt_pull`  
Architecture: Odin Agent Shell v7.1  
Lock: v0.6.7 Thor/Y/Mjölnir Handoff Compiler Lock  
Claim boundary: architecture/spec/shadow-prep only; no runtime proof, no model execution proof, no host validation, no auto-apply, no claim acceptance, no production readiness.

## Purpose

This document hardens Odin's original identity as a handoff compiler. Odin must be able to pull, normalize, compile, route, review, return and post-process Thor-compatible handoffs, Y-handoffs and Mjölnir-style focused-strike handoffs without turning into an agent swarm, chat server, code executor or autonomous apply system.

The goal is not to make handoffs longer. The goal is to make every handoff smaller, stricter, more reviewable, more evidence-bound and more useful for Codex and other bounded workers. Handoff work must preserve Odin's core laws: candidate-only, app-owned apply, no authority transfer, no hidden execution, no external send, local-first, claim-bound, Why Trace required, and smallest sufficient worker.

## Senior Review Decision

Approved with hard constraints. Handoff compilation is central because Thor, Y handoffs and Mjölnir-style focused strikes are the bridge between architecture, repo work, model work, Codex work and human review. However, handoff compilation is only valid if the compiler acts as a boundary-preserving reducer, not as an authority-inflating router.

The approved architecture is:

```text
Prompt / user intent / repo signal / app event
→ Handoff Pull
→ Handoff Intake Envelope
→ Source Type Detection
→ Kernel Binding
→ Claim Boundary Injection
→ Evidence Surface Mapping
→ Return Contract Selection
→ Universal Work Conversion
→ QIRC Gold Spine Precompute
→ Model/Agent Candidate Worker
→ Thor Return / Y Return / Mjölnir Strike Candidate
→ Review Gate
→ Candidate Artifact / Response Packet
```

Rejected architecture:

```text
Prompt → agent gets broad context → agent acts → Odin records afterwards
```

## Core Concepts

### Handoff Pull

Handoff Pull is the controlled extraction of enough intent, evidence, scope, constraints and return expectations from a prompt, chat, repo state, app event or external worker request to create a bounded handoff packet. It is not prompt stuffing. It must reduce the work surface.

### Handoff Compiler

The Handoff Compiler converts messy work signals into typed candidate-only artifacts:

- `odin_handoff_prompt_pull`
- `odin_handoff_compile_packet`
- `odin_thor_handoff_request`
- `odin_y_handoff_packet`
- `odin_mjolnir_strike_candidate`
- `odin_handoff_return_packet`
- `odin_handoff_review_gate`
- `odin_handoff_why_trace`

### Thor Alignment

Thor artifacts are kernel-bound, candidate-only coordination records. They do not transfer authority, accept claims, issue receipts, bypass review or execute returned code. Odin must preserve these Thor boundaries mechanically.

### Y Handoff Alignment

Y handoffs represent Y-Core-style handoff compilation: intent enters through centerline, ring posture, claim boundary, QIRC movement, seed/archetype prewarm, smallest sufficient worker and final gate. Odin uses the Y-handoff lane as an internal semantic handoff style, not as global app authority.

### Mjölnir Alignment

Mjölnir-style focused strike means a tightly scoped candidate patch/plan/action proposal, not a direct strike. In Odin, Mjölnir is a focused candidate compiler: one narrow target, one reason, one boundary, one return contract, one review path. It never means automatic application.

## Required Behavior

- Every handoff requires kernel binding or Odin-equivalent binding.
- Every handoff includes claim boundary and denied claims.
- Every handoff declares allowed scope and forbidden scope.
- Every handoff declares evidence surface or states evidence missing.
- Every handoff declares return contract.
- Every handoff compiles to Universal Work before model/agent dispatch unless it is blocked earlier.
- Every worker return normalizes to Candidate Artifact or conflict report.
- Every candidate return runs review gate and Why Trace.
- Every handoff route may be blocked, narrowed, split or converted to ask-context.
- Mjölnir-style outputs remain candidate-only focused-strike proposals.

## Forbidden Scope

- No autonomous delegation.
- No agent swarm.
- No hidden execution.
- No returned-code execution.
- No auto-apply.
- No auto-merge.
- No claim acceptance.
- No receipt issuance from handoff mediation alone.
- No broad repo scan claim without evidence.
- No production/security/deploy/runtime proof claim.

## Pipeline Detail

1. `detect_source_kind` classifies the incoming request as prompt, Thor handoff, Thor return, Y handoff, Mjölnir candidate, app event, repo issue, Codex task or ambiguous signal.
2. `pull_prompt_atoms` extracts goal, object, actor, target files/surfaces, constraints, forbidden scope, expected output and risk markers.
3. `bind_kernel` attaches Odin binding, Thor kernel binding or Y-Core centerline binding.
4. `inject_claim_boundary` adds non-claims and denied claims.
5. `resolve_evidence_surface` maps allowed evidence and missing evidence.
6. `select_return_contract` chooses review note, gap report, patchplan candidate, risk note, handoff return, candidate artifact bundle or conflict report.
7. `compile_universal_work` emits bounded Universal Work with model/agent route policy.
8. `precompute_qirc` runs QIRC hot window, seed/archetype prewarm, QMath center score and admissibility.
9. `dispatch_candidate_worker` uses smallest sufficient worker, including local model, hosted model, Codex, Thor-compatible worker, Y worker or Mjölnir-focused candidate worker.
10. `normalize_return` converts output into Candidate Artifact/Thor Return/Y Return/Mjölnir Candidate.
11. `review_gate` enforces boundaries.
12. `emit_response_packet` includes Semantic Diff, Why Trace and app-owned Apply boundary.

## Quality Benefits

This layer improves Odin because handoff generation is one of the highest-leverage places to reduce ambiguity. Bad handoffs create bad model work. Good handoffs make even small models and agents act more capable. The Handoff Compiler forces scope, evidence, return format and claim boundary before any worker sees the task.

## Codex Conversion Rule

Codex must treat this document as a build contract. Every implementation must add schema validation, fixtures, negative tests and registry coverage before any runtime adapter is expanded. Handoff compiler code must be deterministic where possible and must never call models merely to build the boundary that would control models.


## Precision Requirements

- Handoff Pull must prefer explicit user text and repo evidence over model interpretation.
- If source intent is ambiguous, emit `ask_context` or `split_work`; do not infer authority.
- Thor returns must remain candidate returns, not receipts.
- Y handoff packets must preserve centerline, ring posture, QIRC event trace and smallest-sufficient-worker routing.
- Mjölnir strike candidates must be narrow, file/surface-bound and review-first.
- Every compiled handoff must have a `why_trace` explaining why the route was selected and why other routes were rejected.
- Every prompt pattern must have a negative pattern that blocks direct apply, broad authority, hidden execution and fake verification.

## Review Checklist

- Is the kernel binding present?
- Is the app authority preserved?
- Is the model/agent worker candidate-only?
- Is evidence stated or explicitly missing?
- Is the return contract unambiguous?
- Are non-claims and denied claims included?
- Is the Universal Work conversion valid?
- Does QIRC precompute reduce the work rather than enlarge it?
- Is postprocessing app-native and candidate-only?
- Is a human/app review gate preserved?

## Integration with Existing v7.1 Layers

This layer binds directly to Universal Work, QIRC Gold Spine, Odin Core/QLI/DFAS, Seed/Archetype Economy, Model/Agent Parity, AI-Git Safety, Shadow Runtime, Runtime Pack Compiler and Thor Bridge. It does not replace those layers. It acts as the canonical ingress compiler for handoff-shaped work.
