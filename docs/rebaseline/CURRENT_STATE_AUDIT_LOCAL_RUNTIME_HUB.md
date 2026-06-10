# Current State Audit — Local Runtime Hub

## Current repo state

- Branch: `codex/rebaseline-local-runtime-hub-build-ladder`.
- Head: `75aa45b`.
- PR #4 / REAL-GH-PR-03 merge evidence: `merged in current git log`.
- Merged baseline used here: REAL-GH-PR-01, REAL-GH-PR-02, REAL-GH-PR-03.
- Open/pending baseline items: REAL-GH-PR-04, REAL-GH-PR-05, REAL-GH-PR-06, REAL-GH-PR-07, REAL-GH-PR-08.

## Runtime reality counts

{
  "docs/codex/prompts": 8,
  "docs/codex/tasks": 124,
  "docs/codex/bundles": 28,
  "docs/codex/reports": 3,
  "odin/runtime": 8,
  "odin/bus": 3,
  "odin/worklets": 3,
  "odin/work_atoms": 3,
  "odin/qirc": 2,
  "odin/models": 11,
  "odin/precompute": 4,
  "odin/output": 2,
  "odin/candidates": 3,
  "odin/why_trace": 2,
  "odin/hub": 2,
  "odin_app_sdk": 3,
  "sdk": 4,
  "examples": 75,
  "tests": 34,
  "schemas/v7_1": 132,
  "registries": 98,
  "windows": 9,
  "runtime": 6,
  "templates": 16
}

## Audit table

| Area | Current status | Evidence | Gap | Risk | Next action |
|---|---|---|---|---|---|
| Repo head / branch | codex/rebaseline-local-runtime-hub-build-ladder at 75aa45b | Verified now: git branch/git log run | Remote PR metadata not available in workspace | safe_current | Continue from current branch |
| Merged PRs | REAL-GH-PR-01..03 are in git history | Verified now: merge commits #2/#3/#4 inspected | Later PRs lack merge receipts here | safe_current | Treat PR-03 as baseline |
| Runtime | runtime modules exist with golden flow example | Repo-grounded: odin/runtime and examples inspected | Start/stop user flow not packaged | runtime_dependency | LRH-PR-02 |
| Local API | odin/daemon/local_api.py exists | Repo-grounded | Contract hardening and SDK bridge pending | runtime_dependency | LRH-PR-04 |
| Store/bus/worklets/atoms | odin/bus, odin/worklets, odin/work_atoms exist | Repo-grounded | Hub trace viewer pending | runtime_dependency | LRH-PR-08 |
| Provider/worker/pre-LLM | odin/models and odin/precompute exist; provider-worker validator available in CLI | Repo-grounded | Provider inspector UI pending | review_required | LRH-PR-09 |
| Hub/UI | odin/hub exists | Repo-grounded | Browser Hub product shell pending | safe_current | LRH-PR-05 |
| SDK/YNode bridge | odin_app_sdk and sdk exist | Repo-grounded | YNode bridge proof pending | review_required | LRH-PR-11 |
| Portable start | CLI doctor/run-golden-flow exist | Repo-grounded | One start command and release ZIP pending | safe_current | LRH-PR-02/LRH-PR-14 |
| Validation/test coverage | tests and validators exist | Repo-grounded | LRH-specific governance tests added by this PR | safe_current | Keep checks current |
| Legacy/superseded material | Older ladders retained | Repo-grounded | Review required before moves | review_required | No moves in LRH-PR-01 |

## Proof gaps and blockers

- No live model inference proof is claimed.
- No browser Hub product proof is claimed.
- No YNode integration proof is claimed.
- No Windows service/tray/installer proof is claimed.
- No WAN/LAN API proof is claimed.
- Blockers are planning/execution blockers, not evidence of runtime failure unless a command in this workspace fails.

## Evidence and claim labels

This rebaseline uses these evidence labels only:

- **Verified now** = command run in this workspace.
- **Repo-grounded** = current file content inspected.
- **Diff-grounded** = current PR diff.
- **Prior-context** = handoff/source-chat memory, not reverified.
- **Inference** = architecture inference, not proof.

Proof boundaries: no production readiness proof, no Windows app proof, no Windows service/tray/installer proof, no live model inference proof, no model quality proof, no security certification proof, no external send proof, no app-state mutation proof.

