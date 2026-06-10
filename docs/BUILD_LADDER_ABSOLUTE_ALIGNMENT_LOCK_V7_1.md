# Build Ladder Absolute Alignment Lock v7.1

## Purpose

This lock makes the Odin build ladder machine-clear and Master Architecture aligned.

The repository retains three planning layers:

1. `PR-00..PR-123` in `registries/codex_task_registry.json` — internal micro-task traceability.
2. `REAL-PR-01..REAL-PR-28` in `registries/codex_pr_bundle_registry.json` — internal legacy bundle traceability.
3. `REAL-GH-PR-01..REAL-GH-PR-08` in `registries/real_pr_execution_registry.json` — the only actual future GitHub PR execution sequence.

## Absolute Rule

Codex must build from `REAL-GH-PR-01..08`.

The internal ladders are not independent execution paths. They are absorbed by the actual PR sequence and exist to preserve detail, traceability, and review context.

## Alignment Requirements

Every actual PR must declare:

- absorbed internal tasks
- absorbed legacy bundles
- existing prep files and paths
- target implementation files and paths
- acceptance gates
- proof boundaries
- commands to run
- invariants to preserve
- Master Architecture sections it implements

## File Path Discipline

`existing_files` means the file or directory exists in this prep repository.

`target_files` / `expected_new_paths` means Codex is expected to create or materialize it during the implementation PR.

Do not mix these fields. A path that does not yet exist must not be treated as a present implementation proof.

## Master Architecture Binding

The actual sequence implements the v7.1 architecture in dependency order:

1. Foundation / Canon / Protocol / Universal Work.
2. Semantic Bus / Storage / API / Worklets / Work Atoms.
3. Model Runtime / Pre-LLM Intelligence / Universal Model-Agent Boundary.
4. Thor/Y/Mjolnir / AI-Git / Review.
5. Narrative Compiler / Shadow Runtime / Loki.
6. Odin Core / QIRC / Seeds / Pattern Mines / Flow Packs.
7. Windows Product Runtime / Odin Hub / IPC / Recovery.
8. App SDKs / Golden Flows / Public Build Gate.

## Non-Claims

This lock does not claim host proof, model inference proof, network proof, security certification, production status, or completed runtime behavior.

It claims only that the build ladder is aligned, traceable, and ready for actual implementation PRs.
