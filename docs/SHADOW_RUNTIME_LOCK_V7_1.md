# Shadow Runtime Lock v7.1 / v0.5.0

## Status

This document defines the Odin Agent Shell **Shadow Runtime**. It is a code-near, non-production, non-authoritative runtime shape for Codex. It is deliberately close to real Python module boundaries, data shapes, call order, failure states and tests. It exists to make future Codex implementation mechanical instead of interpretive.

The Shadow Runtime is inspired by the YNode-prep pattern: long architecture prose is converted into executable-shape artifacts, state machines, fixtures and module contracts, while preserving the claim boundary. Odin adapts that pattern neutrally. Odin does not import YNode identity, public QIRC networking or mesh features. Odin imports the method: central authority first, models as bounded workers, event-bus coordination, receipt-before-claim discipline, and code-near build maps.

## Non-Authority Boundary

The Shadow Runtime:

- does not prove Odin runtime behavior;
- does not call real local models;
- does not open sockets;
- does not mutate app state;
- does not send external messages;
- does not apply code or patches;
- does not claim host validation;
- does not create public IRC, LAN mesh or federation;
- does not bypass the Odin Final Gate;
- does not replace Master Architecture v7.1 or Master Specs v7.1.

The Shadow Runtime produces **candidate-shaped objects** only. If a shadow function returns a candidate, it remains `model_projection` or `shadow_projection` until a future real implementation gates it.

## Why this exists

The v7.1 architecture is large. Codex can read it, but real code work improves when the architecture is represented as:

```text
contract → type → function → flow → fixture → test → real target module
```

The Shadow Runtime fills exactly that gap. It turns the following into code-near shape:

- Universal Work validation;
- Binding Gate;
- Artifact Lens route;
- Internal Semantic Bus event sequence;
- Context Capsule;
- Worklet Graph;
- Slot Forge;
- Model Route Plan;
- Candidate Artifact;
- Candidate DNA;
- Response Packet;
- Final Gate decision;
- failure states;
- trace reasons.

## Authority Order

When Codex builds real modules from this Shadow Runtime, conflicts must be resolved in this order:

```text
1. Claim Boundary / Final Gate laws
2. Master Architecture v7.1
3. Master Specs v7.1
4. Data Contracts v7.1
5. This Shadow Runtime Lock
6. Shadow code-near modules
7. Examples / fixtures
8. prose comments
```

## Codex Rule

Codex must not copy the Shadow Runtime as if it were finished production code. Codex should use it as the exact real-code-shape north star.

Codex may convert shadow modules into real modules only when:

- a schema exists or is created;
- a fixture exists;
- a negative fixture exists for unsafe behavior;
- unit tests exist;
- claim boundary is preserved;
- app-owned apply is preserved;
- semantic bus remains local-only;
- model output remains a projection;
- no direct app mutation is introduced.

## Required Reading Order for Codex

```text
1. START_HERE.md
2. CANON_ENTRY.md
3. AGENTS.md
4. docs/MASTER_ARCHITECTURE_V7_1.md
5. docs/MASTER_SPECS_V7_1.md
6. docs/SHADOW_RUNTIME_LOCK_V7_1.md
7. docs/SHADOW_RUNTIME_CODE_NEAR_BOOK_V7_1.md
8. docs/SHADOW_RUNTIME_TO_REAL_BUILD_MAPPING_V7_1.md
9. docs/CONTRACT_TO_SHADOW_CODE_MAP_V7_1.md
10. odin/shadow_runtime/*.py
11. examples/shadow_runtime/*.json
12. docs/codex/tasks/PR-23_SHADOW_RUNTIME_CODE_NEAR_LOCK.md
13. docs/codex/bundles/REAL-PR-09_SHADOW_RUNTIME_MECHANICAL_BUILD_BRIDGE.md
```

## Shadow Runtime Modules

```text
odin/shadow_runtime/constants.py
odin/shadow_runtime/types.py
odin/shadow_runtime/boundary.py
odin/shadow_runtime/semantic_bus_shadow.py
odin/shadow_runtime/universal_work_shadow.py
odin/shadow_runtime/model_route_shadow.py
odin/shadow_runtime/candidate_shadow.py
odin/shadow_runtime/pipeline.py
```

## Shadow Flow

```text
ShadowUniversalWork input
→ shadow binding check
→ candidate-only output check
→ artifact lens hint
→ semantic bus batch
→ context capsule candidate
→ worklet graph candidate
→ slot contract candidate
→ model route plan candidate
→ candidate artifact candidate
→ candidate DNA candidate
→ response packet candidate
→ shadow final gate
```

## Hard Red Lines

The Shadow Runtime may never introduce:

- app mutation;
- external send;
- public network;
- model truth promotion;
- direct provider call;
- direct patch application;
- semantic bus authority escalation;
- real storage side effects beyond test-only in-memory objects;
- hidden background model execution;
- automatic remote fallback.

## Implementation Target

The Shadow Runtime is the closest current non-authoritative representation of future Odin code. The next implementation stage must build from this shape, not from a blank interpretation of prose.


---

## v0.5.1 FULL_SHADOW_RUNTIME_COVERAGE

This release extends the Shadow Runtime from central spine coverage to full major-subsystem coverage. Every future addition must update the architecture/specs, internal PR ladder, REAL-PR bundles, registries, System Map, tests and FILE_MANIFEST. The Shadow Runtime remains candidate-only, local-only, non-authoritative and non-executing.

New coverage includes Artifact Lenses, Context Distillery, Worklet/Slot/Gaptext, Candidate Tournament, Low-Memory Strict Mode, Thor Bridge, Bounded Code Work, Storage/Trace/Receipt, Local API, App-QIRC Digest Bridge, Model Dojo, Security Redaction, Support Bundle, Windows Runtime and SDK/App Template validation.
