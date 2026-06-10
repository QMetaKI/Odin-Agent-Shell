# Shadow Runtime Near-Final Lock v7.1

## Purpose

This document defines the v0.5.2 Shadow Runtime Near-Final Lock. The goal is to make the Shadow Runtime behave like a mechanical, code-near preview of the finished Odin Agent Shell system without making runtime claims.

The Shadow Runtime is not a mock demo. It is the conversion bridge from architecture and specs to real implementation.

It must show Codex exactly how the future system should be decomposed:

- binding gate
- policy engine
- resource posture
- universal work validation
- semantic bus batch
- context distillery
- artifact lens routing
- worklet graph
- slot forge
- gaptext
- model route plan
- provider adapter plan
- candidate tournament
- critic cascade
- candidate artifact
- candidate DNA
- response packet
- trace record
- support bundle plan
- Windows runtime plan
- app-QIRC digest bridge
- final gate

## Non-Authority Boundary

The Shadow Runtime may not:

- call live models
- open sockets
- start the API server
- mutate app state
- write app files
- apply patches
- send externally
- claim host validation
- claim model inference validation
- claim security validation

The Shadow Runtime may:

- create pure Python data structures
- validate boundaries
- plan routes
- build candidate-only artifacts
- build trace projections
- build provider plans
- build state-machine plans
- build failure-recovery plans
- provide fixtures and tests for Codex conversion

## Near-Final Spine

The canonical near-final entrypoint is:

```python
from odin.shadow_runtime import run_near_final_shadow_runtime
```

The function returns a full shadow result with policy, resource posture, state machine, context plan, worklet plan, route plan, provider plan, candidate artifact, response packet, trace, support bundle and boundary markers.

## Codex Rule

Codex must not invent a parallel implementation. Each real module should be built by converting a shadow object into a real implementation while preserving boundary semantics.

Required conversion pattern:

```text
shadow module
→ real target module
→ schema validation
→ registry parity
→ golden fixture
→ negative fixture
→ acceptance gate
```

## Near-Final Coverage

The v0.5.2 Shadow Runtime now covers:

- Universal Work Kernel
- Internal Semantic Bus
- Artifact Lens System
- Context Distillery
- Worklet Graph
- Slot Forge
- Gaptext
- Model Scale Ladder
- Provider Adapter Plan
- Small Model Power Layer
- Candidate Tournament
- Thor Bridge
- Bounded Code Work
- Storage / Trace / Receipt
- Local API Plan
- App-QIRC Digest Bridge
- Model Dojo and Scoreboard
- Security Redaction
- Support Bundle
- Windows Runtime Plan
- SDK and Template Validation
- Policy Engine
- Resource Scheduler
- State Machine
- Failure Recovery Matrix
- Registry Consistency Report
- End-to-End Orchestrator

## Required Invariants

1. Candidate-only output.
2. App-owned apply.
3. App-owned state.
4. Semantic bus local-only.
5. Model route by measured resources, not hardware names.
6. 3B + 7B/8B hybrid remains the default sweet spot.
7. Bigger models are escalation routes, not the architecture.
8. Remote is explicit opt-in only.
9. Shadow Runtime is code-near but not runtime proof.
10. Every future addition must update specs, internal PR ladder and REAL-PR bundles.

## Done Criteria

v0.5.2 is complete when:

- `run_near_final_shadow_runtime` exists.
- policy engine blocks forbidden outputs.
- resource scheduler emits route ceilings.
- state machine exposes success and failure states.
- failure recovery maps failure codes to safe actions.
- provider adapter shadow describes mock/Ollama/llama.cpp surfaces.
- registry consistency report can inspect required registries.
- fixtures cover valid near-final flow and invalid policy block.
- tests verify no hidden authority transfer.
- PR-25 and REAL-PR-11 are present and registered.
