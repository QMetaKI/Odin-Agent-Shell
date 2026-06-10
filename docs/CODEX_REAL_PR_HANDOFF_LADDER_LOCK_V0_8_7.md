# v0.8.7 — Codex Real PR Handoff Ladder Lock

## Purpose

This lock reframes the actual eight GitHub/Codex PRs after the direct ChatGPT runtime build.
The base is no longer architecture-only. The base is:

```text
v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK
```

Codex therefore receives a running source candidate and must complete, harden, type, host-test, and polish it through eight focused PRs.

## Ladder rule

```text
REAL-GH-PR-01..08 is the only actual execution ladder.
PR-00..PR-123 remains internal micro-task traceability.
REAL-PR-01..28 remains internal legacy bundle traceability.
```

## Current runtime candidate already contains

```text
Runtime Core
Universal Work flow
QIRC local ledger
Seed Pack compiler
Pattern Mine / Flow Pack compiler
Work Atom runtime
Candidate Artifact / Why Trace
Mock and stub provider boundary
Local API smoke path
Static Odin Hub
App SDK and Golden Apps
Windows handoff scripts
Direct runtime RC validator
```

## Reoptimized PR overview

| PR | Title | ChatGPT materialization status |
|---|---|---|
| REAL-GH-PR-01 | Foundation, Canon, Protocol and Universal Work Core — Codex Hardening | mostly materialized; Codex mainly hardens and normalizes |
| REAL-GH-PR-02 | Runtime Bus, Persistence, Local API, Worklets and Work Atoms — Completion | partially materialized; Codex completes bus/worklet/store/API depth |
| REAL-GH-PR-03 | Model Provider Runtime, Pre-LLM Intelligence and Universal Worker Boundary — Provider-Ready | strong boundary scaffold; real providers remain Codex/host work |
| REAL-GH-PR-04 | Thor/Y/Mjölnir Handoff, AI-Git Safety and Review Pipeline — Real Modules | mostly spec-level plus candidate/trace primitives; Codex builds real pipeline modules |
| REAL-GH-PR-05 | Narrative Compiler, Shadow Runtime, Runtime Packs and Loki Anti-Pattern Layer — Executable Contracts | good shadow layer scaffold; Codex deepens actual compiler integration |
| REAL-GH-PR-06 | Odin Core, QIRC Gold Spine, Seeds, Pattern Mines and Flow Packs — Runtime Hardening | one of the strongest materialized areas; Codex hardens security/performance/edge cases |
| REAL-GH-PR-07 | Windows Product Runtime, Odin Hub, Installer, IPC and Recovery — Host-Real Track | prepared but not host-proven; Codex/Windows host work is substantial |
| REAL-GH-PR-08 | App SDKs, Golden Apps, Release Gates and Public Build Handoff — Final Codex RC | good RC layer; Codex turns it into final handoff quality |

## Codex execution stance

Codex must not restart from blank architecture.
It must start from the runtime candidate, inspect current code, run gates, and then complete each domain.

## Non-claims

This lock does not claim real Windows host proof, real service proof, real tray proof, installer proof, code-signing proof, real local model inference proof, or production deployment proof.
