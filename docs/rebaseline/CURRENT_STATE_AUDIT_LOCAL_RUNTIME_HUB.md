# Current State Audit — Local Runtime Hub

## Current PR branch/head state

| Field | Value | Evidence label | Notes |
|---|---|---|---|
| PR | #5 — REBASELINE: Local Runtime Hub Target, Legacy Quarantine and 100% Build Ladder | Prior-context | PR metadata is supplied by the amend prompt. |
| Base | `main` | Prior-context | Remote PR metadata is not revalidated by this local control-plane pass. |
| Branch | `codex/rebaseline-local-runtime-hub` | Prior-context | This is the target PR branch name. The local checkout may have a different ephemeral name, but the public audit records the target branch. |
| Head | `b94f5deac07d1e09bb99968cde47766557b49c8f` | Verified now | Captured with `git rev-parse HEAD` in this workspace before this amend is committed. |
| State | open | Prior-context | Supplied by the amend prompt. |
| Control-plane PR | yes | Diff-grounded | Changes are limited to rebaseline docs, registries, manifest/system map and tests. |
| Runtime behavior changed | no | Diff-grounded | No runtime source module is modified by this amend. |

## Area audit

| Area | Current status | Evidence | Gap | Risk | Next action |
|---|---|---|---|---|---|
| Rebaseline governance | partial, this PR | Diff-grounded: `docs/rebaseline/` and rebaseline registries are changed | Final CI and reviewer approval pending | safe_current | Merge after validators/tests pass |
| Local Runtime Hub target | planning complete for this PR | Repo-grounded: target, 100 percent definition and build ladder exist | Implementation PRs pending | safe_current | LRH-PR-02 then LRH-PR-03 |
| Odin Agent Operator Mode | spec-only future slice | Repo-grounded: LRH-PR-02 ladder and prompt define future packet/command surface | No `odin agent-*` commands exist in this PR | review_required | Implement in LRH-PR-02 |
| Portable local runtime starter | partial/scaffold | Repo-grounded: runtime/local API files exist | Start/stop/check product flow pending | runtime_dependency | LRH-PR-03 |
| Runtime doctor/bootstrap | spec-only future slice | Repo-grounded: ladder defines doctor/bootstrap targets | Doctor, bootstrap and plan-only repair pending | review_required | LRH-PR-04 |
| Localhost API and SDK Bridge | partial/scaffold | Repo-grounded: `odin/daemon/local_api.py`, `odin_app_sdk/`, and `sdk/` exist | Hardened v1 API/SDK contract pending | runtime_dependency | LRH-PR-05 |
| Browser Hub | partial/scaffold | Repo-grounded: `odin/hub/` exists | Browser shell/dashboard/viewers pending | review_required | LRH-PR-06..09 |
| Provider/worker/pre-LLM visibility | partial | Repo-grounded: provider-worker validation exists | Inspector UI/API proof pending | review_required | LRH-PR-10 |
| Universal Work playground | pending | Repo-grounded: Universal Work flows exist elsewhere | Local playground pending | review_required | LRH-PR-11 |
| Neutral external app bridge | pending | Inference: SDK Bridge must support generic host apps | Neutral bridge pack and examples pending | review_required | LRH-PR-12..13 |
| Packaging and Windows convenience | pending | Repo-grounded: packaging/Windows paths exist | Portable ZIP and Windows convenience proof pending | review_required | LRH-PR-15..16 |
| Full acceptance harness | planning added | Diff-grounded: Road-to-100 harness docs/registry added | Future proof commands not implemented | review_required | LRH-PR-17 |

## Proof gaps retained

- No production readiness proof is claimed.
- No Windows service/tray/installer proof is claimed.
- No signed installer proof is claimed.
- No live model inference or model quality proof is claimed.
- No specific external app integration proof is claimed.
- No browser UI runtime proof is claimed.
- No public network API proof is claimed.
- No Thor full protocol support proof is claimed.
- No agent autonomy, hidden tool execution, app-state mutation or external send authority is claimed.

## Evidence labels

- **Verified now** = command run in this workspace.
- **Repo-grounded** = current file content inspected.
- **Diff-grounded** = current PR diff.
- **Prior-context** = handoff/source-chat/user-provided metadata, not reverified remotely.
- **Inference** = architecture inference, not proof.
