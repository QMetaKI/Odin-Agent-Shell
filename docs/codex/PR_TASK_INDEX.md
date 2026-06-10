# PR Task Index

This index is generated for Codex navigation. The authoritative structured version is `registries/codex_task_registry.json`.

| PR | Title | Depends On | Primary Goal |
|---|---|---|---|
| PR-00 | Canon Gates and Repo Hygiene | none | Lock the repository as a deterministic build surface before feature work starts. |
| PR-01 | Schema Strictening and Registry Parity | PR-00 | Make JSON schemas and registries strict enough that protocol drift is caught early. |
| PR-02 | Protocol Packets and Binding Gate | PR-01 | Implement local mediation packets, binding validation and caller policy enforcement. |
| PR-03 | Universal Work Kernel | PR-02 | Implement Universal Work validation, compilation entrypoint and failure reasons. |
| PR-04 | Candidate Artifacts Response Packets and Candidate DNA | PR-03 | Implement candidate-only output objects, response bundles and traceable Candidate DNA. |
| PR-05 | Internal Semantic Bus MVP | PR-02 | Build the local-only semantic event bus, event envelope validation and replay skeleton. |
| PR-06 | Artifact Lenses and Context Distillery | PR-03, PR-05 | Create artifact lens routing and compact context capsules bound to Universal Work. |
| PR-07 | Worklet Graph Slot Forge and Gaptext | PR-06 | Split work into worklets, forge slot contracts and produce bounded gaptext. |
| PR-08 | Model Scale Ladder Router and Mock Provider | PR-07 | Implement hardware-agnostic route selection with mock provider execution. |
| PR-09 | Small Model Power Core | PR-08 | Add critic cascade, candidate tournament, style stabilizer and anti-generic engine. |
| PR-10 | Thor Bridge and Bounded Code Work | PR-04, PR-09 | Map Thor-style handoff discipline into Odin candidate-only code and review flows. |
| PR-11 | Storage Trace Receipt Layer | PR-04, PR-05 | Add SQLite/object-store abstractions, trace entries, receipt candidates and retention hooks. |
| PR-12 | Local API Server | PR-03, PR-04, PR-05, PR-11 | Expose local-only HTTP endpoints for status, apps, work, bus, traces and scoreboard. |
| PR-13 | SDKs and App Templates | PR-12 | Create TypeScript/Python SDK surfaces and no-LLM-in-app connector templates. |
| PR-14 | Ollama and llama.cpp Provider Adapters | PR-08, PR-12 | Implement provider adapters behind ModelWorkPacket boundaries. |
| PR-15 | Low-Memory Strict Mode | PR-08, PR-09 | Implement low-resource route limits, semantic bus light mode and small-slot preference. |
| PR-16 | App QIRC Bridge Digest | PR-05, PR-13 | Prepare digest-only bridge between app-owned event systems and Odin internal bus. |
| PR-17 | Model Dojo and Scoreboard | PR-08, PR-09, PR-11 | Add model capability profiling and route quality metrics without model training. |
| PR-18 | Control Center Skeleton | PR-12, PR-17 | Prepare local control-center surfaces for apps, models, work lab, bus and traces. |
| PR-19 | Windows Runtime Tray and Installer Prep | PR-12, PR-18 | Define and scaffold Windows daemon lifecycle, tray integration and package boundaries. |
| PR-20 | End-to-End Golden Flows | PR-13, PR-14, PR-16, PR-18 | Add representative local golden flows and negative paths across the full stack. |
| PR-21 | Release Prep Hygiene and Support Bundle | PR-20 | Add support bundle export, manifest refresh, docs parity and final pre-release gates. |

# v0.4.2 Index Addendum

```text
PR-22 — Senior Review Hardening and Anti-Drift Lock
Doc: docs/codex/tasks/PR-22_SENIOR_REVIEW_HARDENING_AND_ANTI_DRIFT_LOCK.md
Bundle: REAL-PR-08
```


## v0.5.1 Full Shadow Runtime Coverage Update

- Added PR-24 — Full Shadow Runtime Coverage.
- Added REAL-PR-10 — Full Shadow Runtime Coverage.
- Rule: all future changes must update architecture/specs, internal PR ladder, REAL-PR bundle registry, shadow contract registry, System Map, tests and FILE_MANIFEST.


## v0.7.0 Shadow Narrative / Loki / Anti-Pattern Lock

Adds PR-93 through PR-97 and REAL-PR-23 for typed narrative anti-patterns, Loki mediation, gate mapping and narrative red-team fixtures. Candidate-only and no-Loki-authority boundaries are mandatory.
