# v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK

## Objective

This lock consolidates the full v0.8.1 through v0.8.6 runtime chain into a direct ChatGPT-built runtime release candidate. It materializes the v7.1 Master Architecture as far as possible inside the ZIP without claiming host, Windows service, tray, installer, provider or model-inference proof.

## Included runtime chain

1. v0.8.1 Runtime Core Completion
2. v0.8.2 App Bridge and Golden Apps
3. v0.8.3 Local API and Odin Hub Runtime
4. v0.8.4 Model Provider and Worker Boundary
5. v0.8.5 Windows Host Handoff
6. v0.8.6 Direct Runtime Release Candidate

## Built behaviors

- Universal Work execution
- caller manifest validation
- candidate-only final gate
- Seed Pack compile path
- Pattern Mine and Flow Pack compile path
- Work Atom planning and execution
- local QIRC event ledger
- persistent local candidate/session store
- Why Trace generation
- Provider boundary cards and stubs
- local HTTP API endpoints
- Odin Hub static UI generation
- support bundle emission
- safe mode plan generation
- Python app SDK
- golden app examples
- Windows handoff scripts

## Hard boundaries

- no app apply by Odin
- no external send by Odin
- no autonomous agent authority
- no hidden provider authority
- no executable Seed Pack or Pattern Mine payloads
- no Windows host proof
- no service/tray/installer proof
- no live model inference proof
- no security certification claim

## Acceptance commands

```bash
PYTHONDONTWRITEBYTECODE=1 python -m odin.cli validate-all
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 python -m odin.cli run-golden-flow
PYTHONDONTWRITEBYTECODE=1 python -m odin.cli build-hub --out .odin_runtime/hub/index.html
PYTHONDONTWRITEBYTECODE=1 python -m odin.cli emit-support-bundle --out .odin_runtime/support
PYTHONDONTWRITEBYTECODE=1 python -m odin.cli list-providers
```

## Codex handoff

Codex should now harden a running candidate rather than inventing the source body from specs. The next Codex tasks are type hardening, endpoint tests, Windows target-host proof, provider integration, UI polish, packaging and performance profiling.
