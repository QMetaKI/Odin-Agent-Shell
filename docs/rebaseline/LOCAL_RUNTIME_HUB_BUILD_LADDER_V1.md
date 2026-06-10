# Local Runtime Hub Build Ladder v1

Canonical ladder from the repo-real current state to a complete Odin Local Runtime Hub target. The detailed deterministic JSON is `registries/local_runtime_hub_build_ladder_v1.json`.

## LRH-PR-01 — Rebaseline, Legacy Quarantine, Local Runtime Hub Target

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Rebaseline, Legacy Quarantine, Local Runtime Hub Target.
- Depends on: none
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-02 — Portable Local Runtime Starter

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Portable Local Runtime Starter.
- Depends on: LRH-PR-01
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-03 — Runtime Doctor, First-Run Bootstrap and Self-Healing

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Runtime Doctor, First-Run Bootstrap and Self-Healing.
- Depends on: LRH-PR-01, LRH-PR-02
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-04 — Localhost API Contract Hardening and SDK Bridge v1

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Localhost API Contract Hardening and SDK Bridge v1.
- Depends on: LRH-PR-02, LRH-PR-03
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-05 — Browser Odin Hub Shell

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Browser Odin Hub Shell.
- Depends on: LRH-PR-03, LRH-PR-04
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-06 — Hub Runtime Dashboard and Health Surfaces

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Hub Runtime Dashboard and Health Surfaces.
- Depends on: LRH-PR-04, LRH-PR-05
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-07 — Sessions, Candidates, Store and Proof Gap Viewer

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Sessions, Candidates, Store and Proof Gap Viewer.
- Depends on: LRH-PR-05, LRH-PR-06
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-08 — Bus / Worklet / Atom Trace Viewer

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Bus / Worklet / Atom Trace Viewer.
- Depends on: LRH-PR-06, LRH-PR-07
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-09 — Provider / Worker / Pre-LLM Inspector

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Provider / Worker / Pre-LLM Inspector.
- Depends on: LRH-PR-07, LRH-PR-08
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-10 — Universal Work Playground

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Universal Work Playground.
- Depends on: LRH-PR-08, LRH-PR-09
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-11 — YNode Bridge Pack

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: YNode Bridge Pack.
- Depends on: LRH-PR-09, LRH-PR-10
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-12 — App Bridge Examples and Golden App Harness

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: App Bridge Examples and Golden App Harness.
- Depends on: LRH-PR-10, LRH-PR-11
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-13 — Local Config, Redaction and Safe Settings UI

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Local Config, Redaction and Safe Settings UI.
- Depends on: LRH-PR-11, LRH-PR-12
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-14 — Portable Packaging and Release ZIP

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Portable Packaging and Release ZIP.
- Depends on: LRH-PR-12, LRH-PR-13
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-15 — Windows Convenience Layer without Full Windows App

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Windows Convenience Layer without Full Windows App.
- Depends on: LRH-PR-13, LRH-PR-14
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-16 — Full Acceptance, E2E Golden Flows and User Start Proof

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Full Acceptance, E2E Golden Flows and User Start Proof.
- Depends on: LRH-PR-14, LRH-PR-15
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained


## Evidence and claim labels

This rebaseline uses these evidence labels only:

- **Verified now** = command run in this workspace.
- **Repo-grounded** = current file content inspected.
- **Diff-grounded** = current PR diff.
- **Prior-context** = handoff/source-chat memory, not reverified.
- **Inference** = architecture inference, not proof.

Proof boundaries: no production readiness proof, no Windows app proof, no Windows service/tray/installer proof, no live model inference proof, no model quality proof, no security certification proof, no external send proof, no app-state mutation proof.

