# Local Runtime Hub Build Ladder v1

Canonical ladder from the repo-real current state to a complete Odin Local Runtime Hub target. The detailed deterministic JSON is `registries/local_runtime_hub_build_ladder_v1.json`.

## Agent Operator Mode insertion

LRH-PR-02 is now Odin Agent Operator Mode. It defines the Codex-first / Claude-Code-equivalent repository workflow surface, Thor-compatible protocol surface and general agent boundary before portable runtime implementation begins. This is planning only: no `odin agent-*` commands, webapp, SDK bridge, provider integration or runtime behavior are implemented in this PR.

### Conceptual split

- Odin for Apps: Universal Work → Candidate Artifact.
- Odin for Coding Agents: Agent Task → Agent Work Packet → Guarded Patch/PR → Return Report.
- Odin for Agent Systems: Agent Packet → Permission Gate → Candidate Work → Proof / Return Packet.

## LRH-PR-01 — Rebaseline, Legacy Quarantine, Local Runtime Hub Target

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Rebaseline, Legacy Quarantine, Local Runtime Hub Target.
- Depends on: none
- Current coverage: Repo-grounded baseline from current v0.8.7 repo; no new runtime implemented by LRH-PR-01.
- Missing work: none for planning deliverable after audit artifacts exist
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Expected branch: `codex/rebaseline-local-runtime-hub-build-ladder`
- Expected PR title: REBASELINE: Local Runtime Hub Target, Legacy Quarantine and 100% Build Ladder
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-02 — Odin Agent Operator Mode

- Objective: Create the CLI/file-protocol planning surface that lets Codex, Claude Code and future coding agents use Odin as a repo-local handoff, plan, guard, proof and return-report layer, with Thor-compatible packet normalization where verified.
- Depends on: LRH-PR-01
- Current coverage: conceptual only; partially represented through Thor-style handoff practices, Codex prompts and existing return-report discipline
- Missing work: agent-handoff command, agent-plan command, agent-guard command, agent-check command, agent-proof command, agent-return command, agent work packet schema, agent return report schema...
- Acceptance gates: agent work packet schema validates positive and negative examples, Codex, Claude Code and generic CLI agent profiles exist, Thor-compatible mapping records verified mappings and gaps, agent commands are scaffolded or explicitly defined without hidden execution, candidate-only and no-app-apply boundaries are tested, validate-all and pytest pass
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: Agent Operator Mode is repository-local workflow protocol, not live LLM provider proof, Codex and Claude Code remain external workers, Odin validates and constrains but does not secretly execute app actions, Thor compatibility must be evidence-bound and gap-labeled
- Expected branch: `codex/lrh-pr-02-agent-operator-mode`
- Expected PR title: LRH-PR-02: Odin Agent Operator Mode
- Definition of done: agent work packet schema exists, Codex and Claude Code profiles exist, agent-handoff/plan/guard/proof/return commands exist or are clearly scaffolded, Thor-compatible packet mapping exists with explicit gaps, tests prove candidate-only and no hidden apply boundaries, validate-all and pytest pass

## LRH-PR-03 — Portable Local Runtime Starter

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Portable Local Runtime Starter.
- Depends on: LRH-PR-01
- Current coverage: partial/spec or pending implementation to be confirmed in that PR
- Missing work: implementation, tests, receipts, and documentation specific to this step
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Expected branch: `codex/lrh-pr-03-portable-local-runtime-starter`
- Expected PR title: LRH-PR-03: Portable Local Runtime Starter
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-04 — Runtime Doctor, First-Run Bootstrap and Self-Healing

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Runtime Doctor, First-Run Bootstrap and Self-Healing.
- Depends on: LRH-PR-01, LRH-PR-03
- Current coverage: partial/spec or pending implementation to be confirmed in that PR
- Missing work: implementation, tests, receipts, and documentation specific to this step
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Expected branch: `codex/lrh-pr-04-runtime-doctor-first-run-bootstrap-self-healing`
- Expected PR title: LRH-PR-04: Runtime Doctor, First-Run Bootstrap and Self-Healing
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-05 — Localhost API Contract Hardening and SDK Bridge v1

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Localhost API Contract Hardening and SDK Bridge v1.
- Depends on: LRH-PR-03, LRH-PR-04
- Current coverage: partial/spec or pending implementation to be confirmed in that PR
- Missing work: implementation, tests, receipts, and documentation specific to this step
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Expected branch: `codex/lrh-pr-05-localhost-api-contract-hardening-sdk-bridge-v1`
- Expected PR title: LRH-PR-05: Localhost API Contract Hardening and SDK Bridge v1
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-06 — Browser Odin Hub Shell

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Browser Odin Hub Shell.
- Depends on: LRH-PR-04, LRH-PR-05
- Current coverage: partial/spec or pending implementation to be confirmed in that PR
- Missing work: implementation, tests, receipts, and documentation specific to this step
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Expected branch: `codex/lrh-pr-06-browser-odin-hub-shell`
- Expected PR title: LRH-PR-06: Browser Odin Hub Shell
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-07 — Hub Runtime Dashboard and Health Surfaces

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Hub Runtime Dashboard and Health Surfaces.
- Depends on: LRH-PR-05, LRH-PR-06
- Current coverage: partial/spec or pending implementation to be confirmed in that PR
- Missing work: implementation, tests, receipts, and documentation specific to this step
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Expected branch: `codex/lrh-pr-07-hub-runtime-dashboard-health-surfaces`
- Expected PR title: LRH-PR-07: Hub Runtime Dashboard and Health Surfaces
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-08 — Sessions, Candidates, Store and Proof Gap Viewer

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Sessions, Candidates, Store and Proof Gap Viewer.
- Depends on: LRH-PR-06, LRH-PR-07
- Current coverage: partial/spec or pending implementation to be confirmed in that PR
- Missing work: implementation, tests, receipts, and documentation specific to this step
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Expected branch: `codex/lrh-pr-08-sessions-candidates-store-proof-gap-viewer`
- Expected PR title: LRH-PR-08: Sessions, Candidates, Store and Proof Gap Viewer
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-09 — Bus / Worklet / Atom Trace Viewer

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Bus / Worklet / Atom Trace Viewer.
- Depends on: LRH-PR-07, LRH-PR-08
- Current coverage: partial/spec or pending implementation to be confirmed in that PR
- Missing work: implementation, tests, receipts, and documentation specific to this step
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Expected branch: `codex/lrh-pr-09-bus--worklet--atom-trace-viewer`
- Expected PR title: LRH-PR-09: Bus / Worklet / Atom Trace Viewer
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-10 — Provider / Worker / Pre-LLM Inspector

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Provider / Worker / Pre-LLM Inspector.
- Depends on: LRH-PR-08, LRH-PR-09
- Current coverage: partial/spec or pending implementation to be confirmed in that PR
- Missing work: implementation, tests, receipts, and documentation specific to this step
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Expected branch: `codex/lrh-pr-10-provider--worker--pre-llm-inspector`
- Expected PR title: LRH-PR-10: Provider / Worker / Pre-LLM Inspector
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-11 — Universal Work Playground

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Universal Work Playground.
- Depends on: LRH-PR-09, LRH-PR-10
- Current coverage: partial/spec or pending implementation to be confirmed in that PR
- Missing work: implementation, tests, receipts, and documentation specific to this step
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Expected branch: `codex/lrh-pr-11-universal-work-playground`
- Expected PR title: LRH-PR-11: Universal Work Playground
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-12 — YNode Bridge Pack

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: YNode Bridge Pack.
- Depends on: LRH-PR-10, LRH-PR-11
- Current coverage: partial/spec or pending implementation to be confirmed in that PR
- Missing work: implementation, tests, receipts, and documentation specific to this step
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Expected branch: `codex/lrh-pr-12-ynode-bridge-pack`
- Expected PR title: LRH-PR-12: YNode Bridge Pack
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-13 — App Bridge Examples and Golden App Harness

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: App Bridge Examples and Golden App Harness.
- Depends on: LRH-PR-11, LRH-PR-12
- Current coverage: partial/spec or pending implementation to be confirmed in that PR
- Missing work: implementation, tests, receipts, and documentation specific to this step
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Expected branch: `codex/lrh-pr-13-app-bridge-examples-golden-app-harness`
- Expected PR title: LRH-PR-13: App Bridge Examples and Golden App Harness
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-14 — Local Config, Redaction and Safe Settings UI

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Local Config, Redaction and Safe Settings UI.
- Depends on: LRH-PR-12, LRH-PR-13
- Current coverage: partial/spec or pending implementation to be confirmed in that PR
- Missing work: implementation, tests, receipts, and documentation specific to this step
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Expected branch: `codex/lrh-pr-14-local-config-redaction-safe-settings-ui`
- Expected PR title: LRH-PR-14: Local Config, Redaction and Safe Settings UI
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-15 — Portable Packaging and Release ZIP

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Portable Packaging and Release ZIP.
- Depends on: LRH-PR-13, LRH-PR-14
- Current coverage: partial/spec or pending implementation to be confirmed in that PR
- Missing work: implementation, tests, receipts, and documentation specific to this step
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Expected branch: `codex/lrh-pr-15-portable-packaging-release-zip`
- Expected PR title: LRH-PR-15: Portable Packaging and Release ZIP
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-16 — Windows Convenience Layer without Full Windows App

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Windows Convenience Layer without Full Windows App.
- Depends on: LRH-PR-14, LRH-PR-15
- Current coverage: partial/spec or pending implementation to be confirmed in that PR
- Missing work: implementation, tests, receipts, and documentation specific to this step
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Expected branch: `codex/lrh-pr-16-windows-convenience-layer-without-full-windows-app`
- Expected PR title: LRH-PR-16: Windows Convenience Layer without Full Windows App
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained

## LRH-PR-17 — Full Acceptance, E2E Golden Flows and User Start Proof

- Objective: Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Full Acceptance, E2E Golden Flows and User Start Proof.
- Depends on: LRH-PR-15, LRH-PR-16
- Current coverage: partial/spec or pending implementation to be confirmed in that PR
- Missing work: implementation, tests, receipts, and documentation specific to this step
- Acceptance gates: validate-all OK, pytest OK, claim boundaries explicit, candidate-only/app-owned-apply preserved
- Required commands: `python -m pip install -e .`, `python -m odin.cli validate-current-public-canon`, `python -m odin.cli validate-all`, `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`, `python -m odin.cli run-golden-flow`
- Proof boundaries: no production readiness proof, no Windows app proof, no live model inference proof, no security certification proof, no external send proof, no app-state mutation proof
- Expected branch: `codex/lrh-pr-17-full-acceptance-e2e-golden-flows-user-start-proof`
- Expected PR title: LRH-PR-17: Full Acceptance, E2E Golden Flows and User Start Proof
- Definition of done: artifacts updated, required tests/checks recorded, proof boundaries retained
