# Odin Agent Shell — v7.1 Narrative Compiler Integration

This document is part of the v0.6.0 Narrative Aorta / Y* Compiler Lock. It preserves the Odin Agent Shell v7.1 functional canon and adds a typed, bounded, auditable meta-authoring and compile-prelude layer.

Hard boundary: Fairy prose never executes. Y* Native DSL validates and stages. Shadow Runtime remains code-near blueprint. Runtime packs load only after validation. Odin Host remains the stable local boundary.

## Purpose

Y* Native DSL is Odin's typed narrative IR. It is the machine-readable half of the dual-spine system. It mediates between human-readable Fairy stories and Shadow Runtime IR.

Y* does not own authority. It stages and enriches. Odin Final Gate remains the authority boundary.

## Canonical Unit Shape

```text
YSTAR story "odin.universal_work.rewrite"

center:
  app_authority: preserve
  candidate_only: true
  child_safety: preserve
  final_gate: odin

rings:
  R0: boundary
  R1: policy
  R2: universal_work
  R3: context
  R4: semantic_bus
  R5: slot_forge
  R6: model_route
  R7: critic
  R8: candidate

flow:
  receive UniversalWork
  validate Binding
  distill ContextCapsule
  forge SlotContract
  route smallest_sufficient
  build CandidateArtifact
  pass FinalGate

forbid:
  app_mutation
  external_send
  runtime_verified_claim
  test_success_claim

emit:
  shadow_runtime_flow
  worklet_graph
  slot_contracts
  candidate_dna
```

## Required Fields

- unit_id
- story_ref
- center
- rings
- flow
- forbidden
- emits
- holes
- confidence
- claim_boundary

## Ring Semantics

- R0 Boundary: app sovereignty, candidate-only, claim boundary.
- R1 Policy: local-first, remote explicit, resource profile.
- R2 Universal Work: artifact + verb + output contract.
- R3 Context: digest, capsule, privacy class.
- R4 Semantic Bus: local-only event batch.
- R5 Slot Forge: slot class, constraints, gaptext.
- R6 Model Route: smallest sufficient worker, model scale ladder.
- R7 Critic: claim/style/generic/schema/context checks.
- R8 Candidate: Candidate Artifact, DNA, Response Packet.

## Validation Rules

Invalid if:

- missing center,
- missing final_gate,
- missing candidate_only,
- missing app_authority preserve,
- unmapped Fairy node,
- untyped flow step,
- forbidden list absent,
- holes list absent,
- runtime mapping missing,
- authority escalation detected.

## Codex Rule

Codex must implement parser and validator before any compiler emitter. Y* output is compile input only after validation.
