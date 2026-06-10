# Task DoD Matrix v0.4.0

Each task has a local Definition of Done and a global Definition of Done.

## Global DoD

```text
schema/registry parity OK
SYSTEM_MAP updated when canonical paths change
FILE_MANIFEST regenerated
validation CLI clean
pytest exits 0
no app LLM runtime introduced
no Odin state mutation of app domain
no direct external send by Odin
no unsupported claim promotion
```

## Matrix

| PR | Task | Contract Updates | Test Expectation | Required Commands | Boundary |
|---|---|---|---|---|---|
| PR-00 | Canon Gates and Repo Hygiene | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-01 | Schema Strictening and Registry Parity | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-02 | Protocol Packets and Binding Gate | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-03 | Universal Work Kernel | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-04 | Candidate Artifacts Response Packets and Candidate DNA | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-05 | Internal Semantic Bus MVP | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-06 | Artifact Lenses and Context Distillery | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-07 | Worklet Graph Slot Forge and Gaptext | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-08 | Model Scale Ladder Router and Mock Provider | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-09 | Small Model Power Core | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-10 | Thor Bridge and Bounded Code Work | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-11 | Storage Trace Receipt Layer | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-12 | Local API Server | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-13 | SDKs and App Templates | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-14 | Ollama and llama.cpp Provider Adapters | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-15 | Low-Memory Strict Mode | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-16 | App QIRC Bridge Digest | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-17 | Model Dojo and Scoreboard | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-18 | Control Center Skeleton | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-19 | Windows Runtime Tray and Installer Prep | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-20 | End-to-End Golden Flows | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |
| PR-21 | Release Prep Hygiene and Support Bundle | docs+schemas as needed | unit + negative where relevant | validate-all + pytest | no boundary regression |

# v0.4.2 DoD Addendum

| Task | Additional DoD |
|---|---|
| PR-22 | senior review docs present, traceability matrix present, anti-drift policy present, semantic bus red lines present, risk register present, PR-22 bundled into REAL-PR-08 |


## v0.5.1 Full Shadow Runtime Coverage Update

- Added PR-24 — Full Shadow Runtime Coverage.
- Added REAL-PR-10 — Full Shadow Runtime Coverage.
- Rule: all future changes must update architecture/specs, internal PR ladder, REAL-PR bundle registry, shadow contract registry, System Map, tests and FILE_MANIFEST.
