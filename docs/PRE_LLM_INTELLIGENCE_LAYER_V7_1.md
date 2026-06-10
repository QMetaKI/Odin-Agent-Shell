# Pre-LLM Intelligence Layer v7.1

Status: Odin Agent Shell v7.1 integrated lock. This document is specification and shadow-runtime preparation only. It does not claim runtime proof, model proof, host validation, deployment, security audit completion, production readiness, app apply, or external send.

Core invariants preserved: app owns state, app owns apply, Odin returns candidate artifacts, models remain bounded projection workers, QIRC is local/internal, no hot-path runtime generation, no prose-only execution, no unvalidated runtime pack load, and all visible intelligence must remain traceable by Candidate DNA / Why Trace.


## Objective
The Pre-LLM Intelligence Layer makes Odin perform as much useful intelligence work as possible before any model call. This is not a trick layer. It is the formal system boundary where deterministic structure, QIRC events, seeds, archetype roles, QMath scoring, DFAS admissibility, output contracts, hot-window memory, and runtime pack capability slices reduce the task into the smallest safe work unit.

## Senior Reviewer Verdict
APPROVED WITH BOUNDARIES. The layer improves quality and efficiency if it stays pre-model, typed, auditable, and candidate-only. It must not claim that a model knows or verifies anything it did not actually process. It may improve perceived intelligence through genuine orchestration, not through false claims.

## Responsibilities
- Receive Universal Work only after Binding Gate.
- Create or request QIRC Hot Window.
- Trigger Seed/Archetype Prewarm.
- Ask QMath Center Solver for center and route scores.
- Ask DFAS Stability Core for GO/HOLD/ASK_CONTEXT/SPLIT_WORK/BLOCK.
- Build a Pre-Model Cognition Trace.
- Decide whether a model call is avoidable.
- Emit Slot Forge directives and Output Intelligence Composition hints.
- Preserve Bug6/Children-First and Q7/Bugfree Stability invariants.

## Non-Responsibilities
- It does not perform app apply.
- It does not send externally.
- It does not own app state.
- It does not decide final truth.
- It does not execute Fairy prose.
- It does not bypass Odin Final Gate.

## Pipeline
```text
Universal Work
→ Binding Gate
→ QIRC Hot Window
→ Seed/Archetype Prewarm
→ QMath Center Score
→ DFAS Admissibility
→ Model Work Avoidance Decision
→ Slot/Worklet Plan
→ Model Call only if still needed
→ Output Intelligence Composer
```

## Quality Mechanism
The user-visible quality improves because the model receives less entropy: fewer irrelevant facts, clearer center, active role constraints, output contract, forbidden claims, style/taste dials, and exact candidate type. Small models become more useful and large models become less wasteful.

## Efficiency Mechanism
Efficiency improves through model work avoidance, low-cost deterministic routing, cached runtime pack slices, precomputed seed profiles, hot-window snapshots, and early HOLD/SPLIT decisions. Larger models are reached only when expected gain exceeds latency, token, privacy, and complexity costs.

## Required Artifacts
- `odin_pre_llm_intelligence_packet`
- `odin_model_work_avoidance_decision`
- `odin_pre_model_cognition_trace`
- `odin_output_intelligence_composition`
- `odin_perceived_intelligence_score`
- `odin_micro_to_macro_synthesis_packet`

## Red Lines
No false verification. No hidden chain execution. No direct apply. No external send. No model dispatch before admissibility. No user-visible polish that hides uncertainty. No perceived-intelligence gain through deception.
