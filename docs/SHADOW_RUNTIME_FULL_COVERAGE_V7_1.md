# Shadow Runtime Full Coverage v7.1

## Purpose

This document locks v0.5.1 FULL_SHADOW_RUNTIME_COVERAGE. The previous Shadow Runtime covered the central Odin spine. This lock extends the code-near blueprint to every major subsystem that Codex must implement later.

## Coverage Principle

Every covered subsystem must have:

```text
shadow module
shadow function
valid or invalid fixture
contract registry entry
test
real target module
internal PR task
REAL-PR bundle
boundary statement
```

## Covered Subsystems

- Binding Gate and Final Gate
- Universal Work Compile
- Semantic Bus Batch
- Model Route Plan
- Candidate Response Packet and Candidate DNA
- Artifact Lens and Context Distillery
- Worklet Graph, Slot Forge and Gaptext
- Candidate Tournament
- Low-Memory Strict Mode
- Thor Bridge
- Bounded Code Work
- Storage, Trace and Receipt Candidate
- Local API Endpoint Plan
- App-QIRC Digest Bridge
- Model Dojo and Scoreboard
- Security Redaction
- Support Bundle
- Windows Runtime Plan
- SDK and App Template Validation

## Non-Authority Boundary

Shadow Runtime remains non-executing and non-authoritative. It never calls real models, never starts sockets, never mutates app state, never applies patches, never sends externally and never claims runtime proof.

## Codex Rule

Codex must implement real modules by preserving the shadow contract shape. If future implementation deviates from a shadow contract, the PR must update the shadow module, fixture, registry entry, tests, PR ladder and REAL-PR bundle in the same commit.

## Acceptance

Required commands:

```text
python -m odin.cli validate-shadow-runtime
python -m odin.cli validate-all
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
```

## Full Shadow Runtime Acceptance Anchor

The phrase **Full Shadow Runtime** is intentional. It marks that v0.5.1 covers the entire major-subsystem map, not only the initial spine. The coverage is still a shadow contract and not runtime proof.

## v0.5.2 Near-Final Extension

Full coverage is extended with a near-final orchestrator, policy engine, resource posture planner, state machine, failure recovery map, provider adapter plan and registry consistency report. These are the highest-priority conversion references for Codex after the core architecture and specs.
