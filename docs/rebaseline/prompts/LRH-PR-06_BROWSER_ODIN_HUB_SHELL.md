# Codex Prompt — LRH-PR-06 Browser Odin Hub Shell

## Branch

Use `codex/lrh-pr-06-browser-odin-hub-shell`.

## PR title

LRH-PR-06: Browser Odin Hub Shell

## Objective

Create the local browser Hub shell and read-only navigation surface against the localhost API without adding app apply actions or remote networking defaults.

## Baseline

Master Architecture v7.1, Master Specs v7.1, the Local Runtime Hub target, the Road-to-100 ladder, candidate-only Odin and app-owned apply/state/external-send boundaries remain authoritative.

## Required intake

Read root canon, Master Architecture, Master Specs, LRH target, current-state audit, build ladder JSON, rebaseline manifest, coverage matrix, Road-to-100 acceptance harness, relevant subsystem docs, schemas, registries and tests.

## Target files
- `odin/hub/`
- `odin/hub/static/`
- `odin/hub/api_client.js`
- `docs/BROWSER_ODIN_HUB_SHELL_V1.md`
- `tests/test_lrh_pr_06_browser_hub_shell.py`

## Allowed new files
- `odin/hub/`
- `odin/hub/static/`
- `odin/hub/api_client.js`
- `docs/BROWSER_ODIN_HUB_SHELL_V1.md`
- `tests/test_lrh_pr_06_browser_hub_shell.py`

## Forbidden scope
- no hosted cloud UI
- no remote network default
- no app apply button
- no auth/security certification claim
- no provider execution

## Required behavior
- serve static/browser shell locally
- render API status
- show health panel and navigation shell
- avoid write/apply actions

## Required tests
- static shell served locally
- API status render test
- no write/apply control test
- no remote network default test

## Required commands
- `future target: python -m odin.cli prove-browser-hub --shell-only`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

## Acceptance gates
- static/browser shell served locally
- no auth claim
- no remote network default
- health panel
- navigation shell
- API status rendering
- no write/apply actions

## Proof boundaries
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof

## Final response format

Summary, Testing, Proof boundaries, Skipped implementation claims, Ready yes/no, Next recommended PR.
