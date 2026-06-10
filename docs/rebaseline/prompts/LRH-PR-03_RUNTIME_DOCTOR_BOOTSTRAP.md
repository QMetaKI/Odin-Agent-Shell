# Codex Prompt — LRH-PR-03 Runtime Doctor, First-Run Bootstrap and Self-Healing

## Branch

Use `codex/lrh_pr_03_runtime-doctor,-first-run-bootstrap-and-self-healing`.

## PR title

LRH-PR-03: Runtime Doctor, First-Run Bootstrap and Self-Healing

## Objective

Advance Odin Local Runtime Hub toward the 100 percent local runtime target: Runtime Doctor, First-Run Bootstrap and Self-Healing.

## Baseline

Master Architecture v7.1, current v0.8.7 handoff, runtime base v0.8.6, and LRH build ladder v1.

## Required intake

Read root canon, Master Architecture, Master Specs, current REAL-GH plan/index, LRH target, LRH audit, LRH build ladder JSON, rebaseline manifest, relevant subsystem docs, schemas, registries and tests.

## Target files

['odin/', 'odin_app_sdk/', 'sdk/', 'docs/', 'tests/']

## Forbidden scope

['do not make Odin apply app state', 'do not enable WAN/LAN API by default', 'do not claim live model proof without receipt', 'do not replace Master Architecture v7.1']

## Required behavior

Preserve candidate-only Odin, app-owned apply/state/external send, localhost-only default API, and explicit proof gaps. Do not implement outside this prompt's bounded scope.

## Required tests

Add or update local deterministic tests. No network and no generated runtime artifacts.

## Required commands

- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `python -m odin.cli run-golden-flow`

## Acceptance gates

['validate-all OK', 'pytest OK', 'claim boundaries explicit', 'candidate-only/app-owned-apply preserved']

## Proof boundaries

['no production readiness proof', 'no Windows app proof', 'no live model inference proof', 'no security certification proof', 'no external send proof', 'no app-state mutation proof']

## Final response format

Summary, Testing, Legacy moved/skipped, Proof boundaries, Ready yes/no, Next recommended PR.
