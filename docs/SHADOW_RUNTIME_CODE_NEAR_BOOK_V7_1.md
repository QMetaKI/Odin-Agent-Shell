# Shadow Runtime Code-Near Book v7.1

## Purpose

This book explains how Codex should transform the Shadow Runtime into real Odin modules. It is modeled after the shadow-runtime discipline used in YNode-prep: the architecture becomes almost-code, and then Codex converts almost-code into real code under gates.

The Shadow Runtime is intentionally Python-shaped because Odin v7.1 currently uses a Python package skeleton. It does not prevent future Rust/Tauri/TypeScript shells. It gives the first deterministic implementation surface.

## Mechanical Conversion Pattern

Every subsystem should follow this mechanical build chain:

```text
Spec section
→ Data contract
→ Shadow type
→ Shadow function
→ Fixture
→ Unit test
→ Real module target
→ Integration test
→ Gate update
```

Codex should never implement a real subsystem directly from narrative prose when a shadow function exists.

## Required Module Mapping

| Shadow module | Real target | Purpose | First real tests |
|---|---|---|---|
| `shadow_runtime/types.py` | `odin/protocol/`, `odin/universal_work/`, `odin/packets/` | shared data shapes | protocol packet tests |
| `shadow_runtime/boundary.py` | `odin/core/final_gate.py`, `odin/core/claim_boundary.py` | candidate-only and authority checks | final gate negative tests |
| `shadow_runtime/semantic_bus_shadow.py` | `odin/semantic_bus/` | local-only bus event shape and batch | semantic bus lifecycle tests |
| `shadow_runtime/universal_work_shadow.py` | `odin/universal_work/` | work validation and compile skeleton | valid/invalid Universal Work tests |
| `shadow_runtime/model_route_shadow.py` | `odin/models/model_router.py` | resource/profile route plan | route ladder tests |
| `shadow_runtime/candidate_shadow.py` | `odin/packets/` | candidate artifact, response packet, DNA | candidate-only tests |
| `shadow_runtime/pipeline.py` | `odin/daemon.py` or orchestrator | end-to-end in-memory flow | E2E golden flow tests |

## Shadow Types Are Not Runtime Proof

A shadow dataclass that returns success means only:

```text
this candidate shape is internally consistent under the shadow rules
```

It does not mean:

```text
real model ran
real daemon ran
real app applied
real tests on host ran
security posture was externally assessed
```

## Conversion Rules

### Rule 1 — Preserve candidate-only status

Any real module derived from the Shadow Runtime must keep candidate outputs as candidates. App actions must remain app-owned.

### Rule 2 — Preserve model projection status

Model routes produce projected content. Even if the route uses a real model later, the result is not truth until Odin Final Gate and app decision.

### Rule 3 — Preserve local semantic bus boundary

`shadow_semantic_bus_batch` maps to a local-only bus. It cannot become public IRC, LAN mesh or external federation inside Odin Core.

### Rule 4 — Preserve route ladder discipline

Route selection must use deterministic and small-model-first paths before larger models. Bigger model routes are explicit escalation, not default architecture.

### Rule 5 — Preserve low-memory mode

Real implementations must keep a Low-Memory Strict path where deterministic, semantic bus light, 1B/2B/3B micro and ask-context routes can run without heavy UI, large traces or hybrid requirements.

## Recommended Codex Implementation Order

```text
1. Shadow type parity tests
2. Final Gate / Boundary functions
3. Universal Work validator
4. Semantic bus in-memory batch
5. Worklet graph and slot forge
6. Model route plan with mock provider only
7. Candidate artifact and response packet builders
8. End-to-end shadow flow as golden test
9. Real API wrapper
10. Provider adapters
```

## Done Criteria for Any Shadow-to-Real Slice

A slice is not done until:

- the shadow source is referenced in the PR summary;
- real target files match the build mapping;
- schema fixture exists;
- unit test exists;
- negative test exists;
- no forbidden authority escalation exists;
- `python -m odin.cli validate-all` remains green;
- `pytest` remains green;
- the real PR bundle registry remains accurate.

## Anti-Patterns

Codex must not:

```text
copy shadow docs without implementation tests
turn candidate actions into app apply
turn semantic bus events into external network messages
call real models before route/final-gate tests exist
store raw app state by default
skip Candidate DNA
skip trace IDs
skip failure state mapping
collapse all modules into one giant file
```

## Why this matters

The v7.1 architecture is designed to make small models perform well through structure. The Shadow Runtime makes that structure mechanically implementable. It is the bridge between “hammermässige Architektur” and “Codex can now build without guessing.”
