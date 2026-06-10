# Slice / PR / Registry Coverage Matrix — Local Runtime Hub

This document summarizes the full machine-readable matrix in `registries/rebaseline_coverage_matrix_v1.json`. The JSON maps PR-00..PR-123, REAL-PR-01..28, REAL-GH-PR-01..08, Codex prompt/task/bundle files, and required registries with status, evidence, carry-forward action, legacy action, LRH mapping and risk.

## Summary

| Family | Count | Classification approach |
|---|---:|---|
| PR-00..PR-123 | 124 | Retained as internal traceability; validator dependencies are not moved. |
| REAL-PR-01..28 | 28 | Retained as bundle overlay traceability; reviewed before any quarantine. |
| REAL-GH-PR-01..08 | 8 | REAL-GH-PR-01..03 baseline in current git history; REAL-GH-PR-04..08 carried forward. |
| Codex prompts | 8 | Current REAL-GH prompt pack retained. |
| Codex tasks | 124 | Validator dependency; not moved. |
| Codex bundles | 28 | Validator dependency; not moved. |
| Codex reports | 3 | Current reports retained. |

## Required fields

Each JSON object includes: `id`, `title`, `source_path`, `mapped_current_implementation`, `status`, `evidence`, `reason`, `carry_forward_action`, `legacy_action`, `new_ladder_mapping`, and `risk`.

## Evidence and claim labels

This rebaseline uses these evidence labels only:

- **Verified now** = command run in this workspace.
- **Repo-grounded** = current file content inspected.
- **Diff-grounded** = current PR diff.
- **Prior-context** = handoff/source-chat memory, not reverified.
- **Inference** = architecture inference, not proof.

Proof boundaries: no production readiness proof, no Windows app proof, no Windows service/tray/installer proof, no live model inference proof, no model quality proof, no security certification proof, no external send proof, no app-state mutation proof.



## Agent Operator Mode coverage mappings

| Concept | New ladder mapping | Evidence | Status | Carry-forward action |
|---|---|---|---|---|
| Thor handoff / guard / plan / expected / return | LRH-PR-02 | Repo-grounded: Thor integration and bounded code work docs describe candidate-only Thor-inspired flows | partial conceptual | Add Thor-compatible normalization registry and gap-labeled return mapping |
| Codex PR prompt discipline | LRH-PR-02 | Repo-grounded: Codex prompts and task locks already structure branch, scope, commands and proof boundaries | partial conceptual | Add Codex agent profile and Agent Work Packet examples |
| Claude Code repo-worker discipline | LRH-PR-02 | Inference: profile target for Claude-Code-equivalent local repo work | spec-only | Add Claude Code profile without claiming provider integration |
| Future local model/agent worker boundary | LRH-PR-02 and LRH-PR-10 | Inference: agent protocol must remain distinct from provider/worker runtime | spec-only | Add permission cards, allowed-files packets and no-hidden-tool-use gates |
